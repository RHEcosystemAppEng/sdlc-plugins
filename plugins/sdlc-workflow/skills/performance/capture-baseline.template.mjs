#!/usr/bin/env node

/**
 * Performance Baseline Capture Script
 *
 * Collects frontend performance metrics via Playwright browser automation.
 *
 * MODES:
 *   Localhost: node capture-baseline.mjs --config <path> --port 3000
 *   Hosted:   node capture-baseline.mjs --config <path> --base-url https://host [auth] [--insecure]
 *
 * AUTH OPTIONS (hosted mode only, mutually exclusive):
 *   --storage-state auth.json   Playwright saved session (primary — works with SSO/Keycloak/OIDC)
 *   --user admin --pass secret  Form-login (Cognito, Keycloak, and standard HTML forms)
 *
 *   Form-login tries visible username/password fields first, then falls back to
 *   auth-type-specific selectors (Cognito signInForm*, Keycloak #username/#password).
 *   For multi-step or non-standard flows, use --storage-state instead:
 *     npx playwright codegen --save-storage=auth.json https://your-host
 *
 * VERIFICATION:
 *   Before measurement, one verification iteration per scenario checks HTTP status,
 *   final URL (SPA auth redirect detection), navigation timing, FCP, LCP (with element
 *   attribution), and JS errors. Halts immediately with actionable diagnostics on failure.
 *
 * OUTPUT:
 *   JSON to stdout with per-scenario metrics. All timing values in milliseconds.
 *   No cross-scenario aggregate — consumers compute summaries from per-scenario data.
 *   Percentile method: linear interpolation (output config.percentile_method).
 *
 * LIMITATIONS:
 *   LCP is collected via a PerformanceObserver injected before navigation
 *   (addInitScript). After load, waits for LCP to stabilize (no new candidates
 *   for 2s, up to 10s) before reading the final entry. LCP may still be null
 *   on pages without a qualifying largest-contentful-paint element (e.g.,
 *   canvas-only rendering) or when content appears after the stabilization window.
 *   No network throttling — uses Playwright defaults (no preset).
 *   Viewport is fixed at 1280×720 for reproducible baselines.
 *   FCP/LCP may be null for pages without qualifying paint events.
 *   Dynamic route segments (:id) must be substituted with real values before config entry.
 *
 * SECURITY:
 *   - Localhost mode: only navigates to 127.0.0.0/8, ::1
 *   - Hosted mode: navigates to the user-provided --base-url only
 *   - TLS errors rejected by default; --insecure opts in to accepting invalid certs
 *   - Absolute config paths always accepted; relative paths enforce CWD containment
 *   - Iterations bounded (max 50); warmup bounded (max 10)
 *   - Query strings stripped from resource URLs before output (prevents token leakage)
 *   - WARNING: --pass is visible in process listings and shell history.
 *     Use --storage-state or BASELINE_PASS env var for sensitive environments.
 */

import { chromium } from '@playwright/test';
import { readFile, realpath, access } from 'fs/promises';
import { URL } from 'url';
import { resolve, relative, isAbsolute } from 'path';

// Module-level variables (set in validateAndRun)
let configPath;
let portOverride;
let baseUrl;
const captureMode = 'cold-start'; // fresh browser context per iteration, same browser process
let storageStatePath;
let authUser;
let authPass;
let insecureFlag;

const AUTH_PATH_PATTERNS = ['/login', '/auth', '/signin', '/oauth', '/sso'];

// ── Config ──────────────────────────────────────────────────────────────

async function parseConfig(path) {
  const raw = JSON.parse(await readFile(path, 'utf-8'));
  const scenarios = (raw.scenarios || [])
    .filter(s => (s.type || 'frontend') !== 'backend')
    .map(s => ({
      name: s.name, path: s.url, description: s.description || ''
    }));
  if (!scenarios.length) throw new Error('No frontend scenarios in config. Check scenario types or run /sdlc-workflow:performance-baseline first.');
  const iterations = Math.min(Math.max(raw.baseline_settings?.iterations ?? 20, 1), 50);
  const warmupRuns = Math.min(Math.max(raw.baseline_settings?.warmup_runs ?? 2, 0), 10);
  return { scenarios, iterations, warmupRuns };
}

// ── URL Resolution ──────────────────────────────────────────────────────

function validateLocalhostUrl(urlPath, defaultPort) {
  let fullUrl;
  const pathPattern = /^[a-zA-Z0-9\/_\-.:?&=%]+$/;
  if (!urlPath.startsWith('http://') && !urlPath.startsWith('https://') && !pathPattern.test(urlPath)) {
    throw new Error(`Invalid characters in URL path: ${urlPath}`);
  }
  if (urlPath.startsWith('http://') || urlPath.startsWith('https://')) {
    fullUrl = urlPath;
  } else {
    if (!defaultPort) throw new Error(`URL "${urlPath}" needs a port. Use --port.`);
    fullUrl = `http://localhost:${defaultPort}${urlPath.startsWith('/') ? '' : '/'}${urlPath}`;
  }
  const parsed = new URL(fullUrl);
  const hostname = parsed.hostname.toLowerCase();
  const isLocalhost = hostname === 'localhost';
  const isIPv4Loopback = /^127\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/.test(hostname) &&
    hostname.split('.').slice(1).every(o => { const n = parseInt(o, 10); return n >= 0 && n <= 255; });
  const isIPv6Loopback = hostname === '[::1]' || hostname === '::1';
  if (hostname === '0.0.0.0') throw new Error('0.0.0.0 not allowed. Use localhost or 127.0.0.1.');
  if (hostname.includes('::ffff:')) throw new Error('IPv6-mapped addresses not allowed.');
  if (!isLocalhost && !isIPv4Loopback && !isIPv6Loopback) {
    throw new Error(`Only localhost URLs allowed. Got: ${hostname}`);
  }
  if (!parsed.port) throw new Error(`Port required in URL: ${fullUrl}. Use --port.`);
  return fullUrl;
}

function resolveUrl(scenarioPath) {
  if (scenarioPath.startsWith('http://') || scenarioPath.startsWith('https://')) return scenarioPath;
  if (baseUrl) {
    const base = baseUrl.replace(/\/+$/, '');
    return `${base}${scenarioPath.startsWith('/') ? '' : '/'}${scenarioPath}`;
  }
  return validateLocalhostUrl(scenarioPath, portOverride);
}

function stripQueryString(url) {
  try { const u = new URL(url); return `${u.origin}${u.pathname}`; } catch { return url; }
}

function isAuthRedirect(url) {
  try {
    const path = new URL(url).pathname.toLowerCase();
    return AUTH_PATH_PATTERNS.some(p => path.includes(p));
  } catch { return false; }
}

// ── Auth ─────────────────────────────────────────────────────────────────

async function attemptFormLogin(page) {
  await page.goto(baseUrl, { waitUntil: 'networkidle', timeout: 30000 });

  if (!isAuthRedirect(page.url())) {
    await page.waitForURL(url => isAuthRedirect(url.toString()), { timeout: 5000 }).catch(() => {});
  }

  // Primary: visible username/password fields + Enter — covers most standard forms
  let primaryFilled = false;
  try {
    await page.fill('input[name="username"]:visible', authUser);
    await page.fill('input[name="password"]:visible', authPass);
    primaryFilled = true;
    await page.keyboard.press('Enter');
    // Wait for the full redirect chain (e.g. Cognito → callback → app) to settle
    await page.waitForURL(
      url => url.toString().startsWith(baseUrl) && !isAuthRedirect(url.toString()),
      { timeout: 30000 }
    ).catch(() => {});
    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});

    if (!isAuthRedirect(page.url())) {
      return { success: true };
    }
    // Enter didn't submit or redirect chain didn't complete — fall through
  } catch {
    // Primary selectors failed — fall through to auth-type-specific selectors
  }

  // Fallback: detect auth type from URL and use specific selectors + submit button
  const currentUrl = page.url().toLowerCase();

  if (currentUrl.includes('cognito')) {
    if (!primaryFilled) {
      const userField = await page.$('input[name="signInFormUsername"]:visible');
      const passField = await page.$('input[name="signInFormPassword"]:visible, input[type="password"]:visible');
      if (!userField || !passField) return { success: false, reason: 'no-form' };
      await userField.fill(authUser);
      await passField.fill(authPass);
    }
    const submitBtn = await page.$('input[name="signInSubmitButton"]:visible, button[type="submit"]:visible');
    if (submitBtn) {
      await submitBtn.click();
    } else {
      return { success: false, reason: 'no-form' };
    }
  } else if (currentUrl.includes('keycloak') || currentUrl.includes('/auth/realms')) {
    if (!primaryFilled) {
      const userField = await page.$('input[id="username"]:visible');
      const passField = await page.$('input[id="password"]:visible');
      if (!userField || !passField) return { success: false, reason: 'no-form' };
      await userField.fill(authUser);
      await passField.fill(authPass);
    }
    const submitBtn = await page.$('input[id="kc-login"]:visible, button[type="submit"]:visible');
    if (submitBtn) {
      await submitBtn.click();
    } else {
      return { success: false, reason: 'no-form' };
    }
  } else {
    if (!primaryFilled) {
      const userField = await page.$('input[id="username"], input[name="user"]');
      const passField = await page.$('input[id="password"], input[type="password"]');
      if (!userField || !passField) return { success: false, reason: 'no-form' };
      await userField.fill(authUser);
      await passField.fill(authPass);
    }
    const submitBtn = await page.$('button[type="submit"], input[type="submit"]');
    if (submitBtn) {
      await submitBtn.click();
    } else {
      return { success: false, reason: 'no-form' };
    }
  }

  await page.waitForLoadState('networkidle', { timeout: 30000 });

  if (isAuthRedirect(page.url())) {
    return { success: false, reason: 'login-failed' };
  }
  return { success: true };
}

async function setupAuth(browser, firstScenarioUrl) {
  if (!baseUrl) return null;

  if (storageStatePath) {
    const stored = JSON.parse(await readFile(storageStatePath, 'utf-8'));
    const context = await browser.newContext(contextOptions(stored));
    const page = await context.newPage();
    await page.goto(firstScenarioUrl, { waitUntil: 'load', timeout: 30000 });
    if (isAuthRedirect(page.url())) {
      await context.close();
      console.error(`\n✗ Session expired in ${storageStatePath}`);
      console.error(`  Re-run: npx playwright codegen --save-storage=${storageStatePath} ${baseUrl}`);
      process.exit(1);
    }
    console.error('  ✓ Storage state loaded and validated');
    const state = await context.storageState();
    await context.close();
    return state;
  }

  if (authUser && authPass) {
    const context = await browser.newContext(contextOptions(null));
    const page = await context.newPage();
    const result = await attemptFormLogin(page);
    if (!result.success) {
      await context.close();
      if (result.reason === 'no-form') {
        console.error('\n✗ No login form found at ' + baseUrl);
        console.error('  For SSO/Keycloak/OIDC, use --storage-state instead of --user/--pass');
        console.error('  Generate with: npx playwright codegen --save-storage=auth.json ' + baseUrl);
      } else {
        console.error('\n✗ Login failed — still on login page after submit');
        console.error('  Check credentials or use --storage-state for complex login flows');
      }
      process.exit(1);
    }
    console.error('  ✓ Form login succeeded');
    const state = await context.storageState();
    await context.close();
    return state;
  }

  // No auth args — check if public
  const context = await browser.newContext(contextOptions(null));
  const page = await context.newPage();
  await page.goto(firstScenarioUrl, { waitUntil: 'load', timeout: 30000 });
  if (isAuthRedirect(page.url())) {
    await context.close();
    console.error('\n✗ Redirected to login page: ' + page.url());
    console.error('  Provide --storage-state or --user/--pass for authenticated environments');
    console.error('  Generate storage state: npx playwright codegen --save-storage=auth.json ' + baseUrl);
    process.exit(1);
  }
  console.error('  ✓ No auth required (public)');
  const state = await context.storageState();
  await context.close();
  return state;
}

// ── LCP Observer ────────────────────────────────────────────────────────

const CAPTURE_VIEWPORT = { width: 1280, height: 720 };
const LCP_SETTLE_MS = 2000;
const LCP_MAX_WAIT_MS = 10000;

const LCP_INIT_SCRIPT = `
  window.__lcpEntries = [];
  window.__lcpElements = [];
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      window.__lcpEntries.push(entry.startTime);
      const el = entry.element;
      window.__lcpElements.push({
        tag: el?.tagName || null,
        url: entry.url || null,
        size: entry.size ?? null
      });
    }
  }).observe({ type: 'largest-contentful-paint', buffered: true });
`;

function contextOptions(storageState) {
  return {
    viewport: CAPTURE_VIEWPORT,
    ...(insecureFlag ? { ignoreHTTPSErrors: true } : {}),
    ...(storageState ? { storageState } : {})
  };
}

async function waitForLcpStable(page) {
  await page.evaluate(async ({ settleMs, maxWaitMs }) => {
    const start = performance.now();
    let lastLen = window.__lcpEntries?.length ?? 0;
    let lastChange = performance.now();
    while (performance.now() - start < maxWaitMs) {
      const len = window.__lcpEntries?.length ?? 0;
      if (len !== lastLen) {
        lastLen = len;
        lastChange = performance.now();
      }
      if (len > 0 && performance.now() - lastChange >= settleMs) break;
      await new Promise(r => setTimeout(r, 100));
    }
  }, { settleMs: LCP_SETTLE_MS, maxWaitMs: LCP_MAX_WAIT_MS });
}

// ── Metrics Collection ──────────────────────────────────────────────────

async function collectMetrics(page) {
  return page.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0];
    const paints = performance.getEntriesByType('paint');
    const lcpEntries = window.__lcpEntries || [];
    const lcpElements = window.__lcpElements || [];
    const lcp = lcpEntries.length ? lcpEntries[lcpEntries.length - 1] : null;
    const lcpElement = lcpEntries.length ? lcpElements[lcpEntries.length - 1] : null;
    const resources = performance.getEntriesByType('resource');
    return {
      navigationTiming: nav ? {
        dns: nav.domainLookupEnd - nav.domainLookupStart,
        tcp: nav.connectEnd - nav.connectStart,
        request: nav.responseStart - nav.requestStart,
        response: nav.responseEnd - nav.responseStart,
        domProcessing: nav.domComplete - nav.domInteractive,
        loadComplete: nav.loadEventEnd - nav.loadEventStart,
        totalTime: nav.loadEventEnd - nav.fetchStart
      } : null,
      fcp: paints.find(e => e.name === 'first-contentful-paint')?.startTime || null,
      lcp,
      lcpElement,
      domInteractive: nav ? nav.domInteractive : null,
      resources: resources.map(r => ({
        name: r.name, type: r.initiatorType,
        duration: r.duration, size: r.transferSize || 0, startTime: r.startTime
      })),
      resourceSummary: {
        scripts: resources.filter(r => r.initiatorType === 'script').length,
        stylesheets: resources.filter(r => r.initiatorType === 'link' || r.initiatorType === 'css').length,
        images: resources.filter(r => r.initiatorType === 'img').length,
        fetch: resources.filter(r => r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest').length,
        total: resources.length
      }
    };
  });
}

// ── Navigation Stabilization ────────────────────────────────────────────

async function waitForNavigationSettle(page, timeoutMs = 8000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      await page.waitForURL(/.*/, { timeout: 3000, waitUntil: 'load' });
    } catch {
      break;
    }
  }
  await page.waitForLoadState('load').catch(() => {});
}

// ── Verification Pass ───────────────────────────────────────────────────

async function runVerificationPass(browser, scenarios, storageState) {
  console.error('\n── Verification pass ──');
  for (const scenario of scenarios) {
    const url = resolveUrl(scenario.path);
    const context = await browser.newContext(contextOptions(storageState));
    const page = await context.newPage();
    await page.addInitScript(LCP_INIT_SCRIPT);
    const jsErrors = [];
    page.on('pageerror', e => jsErrors.push(e.message));

    try {
      const response = await page.goto(url, { waitUntil: 'load', timeout: 30000 });
      await waitForNavigationSettle(page);
      await waitForLcpStable(page);
      const status = response?.status() ?? 0;
      const finalUrl = page.url();
      const errors = [];

      if (status >= 400) errors.push(`HTTP ${status}`);
      if (isAuthRedirect(finalUrl)) errors.push(`Redirected to auth page: ${finalUrl}`);

      const metrics = await collectMetrics(page);
      if (!metrics.navigationTiming) errors.push('No navigation timing data');
      if (jsErrors.length) errors.push(`${jsErrors.length} JS error(s): ${jsErrors[0]}`);
      if (!metrics.lcp) console.error(`  ⚠ ${scenario.name}: LCP not available (no candidates during ${LCP_MAX_WAIT_MS/1000}s window)`);

      if (errors.length) {
        console.error(`\n✗ Verification FAILED: ${scenario.name}`);
        errors.forEach(e => console.error(`  - ${e}`));
        if (isAuthRedirect(finalUrl)) {
          console.error('  → Provide --storage-state or --user/--pass');
        }
        process.exit(1);
      }

      const resourceCount = metrics.resources?.length ?? 0;
      const lcpStr = metrics.lcp ? Math.round(metrics.lcp) + 'ms' : 'n/a';
      const lcpUrl = metrics.lcpElement?.url ? stripQueryString(metrics.lcpElement.url) : null;
      const lcpEl = metrics.lcpElement?.tag
        ? ` (${metrics.lcpElement.tag}${lcpUrl ? ', ' + lcpUrl : ''})`
        : '';
      console.error(`  ✓ ${scenario.name}: HTTP ${status}, FCP ${metrics.fcp ? Math.round(metrics.fcp) + 'ms' : 'n/a'}, LCP ${lcpStr}${lcpEl}, ${resourceCount} resources`);
    } catch (err) {
      console.error(`\n✗ Verification FAILED: ${scenario.name}`);
      console.error(`  ${err.message}`);
      if (baseUrl) {
        console.error('  → Check network connectivity and VPN');
        if (!insecureFlag) console.error('  → For self-signed certs, add --insecure');
      } else {
        console.error(`  → Is the app running on localhost:${portOverride}?`);
      }
      process.exit(1);
    } finally {
      await context.close();
    }
  }
  console.error('── All scenarios verified ✓ ──\n');
}

// ── Measurement ─────────────────────────────────────────────────────────

async function measureScenario(browser, scenario, iterations, warmupRuns, storageState) {
  const url = resolveUrl(scenario.path);
  const allMetrics = [];
  let failCount = 0;
  const maxFailures = Math.ceil((iterations + warmupRuns) * 0.2);

  for (let i = 0; i < iterations + warmupRuns; i++) {
    const context = await browser.newContext(contextOptions(storageState));
    const page = await context.newPage();
    await page.addInitScript(LCP_INIT_SCRIPT);
    const jsErrors = [];
    page.on('pageerror', e => jsErrors.push(e.message));

    try {
      await page.goto(url, { waitUntil: 'load', timeout: 30000 });
      await waitForNavigationSettle(page);
      await waitForLcpStable(page);
      const metrics = await collectMetrics(page);
      if (metrics.resources) {
        metrics.resources = metrics.resources.map(r => ({ ...r, name: stripQueryString(r.name) }));
      }
      if (i >= warmupRuns) allMetrics.push(metrics);
      if (i === warmupRuns - 1 && warmupRuns > 0) console.error('    Warmup done');
      if (jsErrors.length && i >= warmupRuns) {
        console.error(`    Iteration ${i - warmupRuns + 1}: ${jsErrors.length} JS error(s)`);
      }
      if (i >= warmupRuns && (i - warmupRuns + 1) % 5 === 0) {
        console.error(`    ${i - warmupRuns + 1}/${iterations}`);
      }
    } catch (error) {
      failCount++;
      console.error(`    Iteration ${i + 1} failed: ${error.message}`);
      if (failCount > maxFailures) {
        await context.close();
        throw new Error(`Too many failures (${failCount}/${iterations + warmupRuns}). Halting "${scenario.name}".`);
      }
    } finally {
      await context.close();
    }
  }

  const aggregated = aggregateMetrics(allMetrics);
  if (aggregated && aggregated.lcpSamples < aggregated.iterations) {
    console.error(`    ⚠ LCP available in ${aggregated.lcpSamples}/${aggregated.iterations} iterations`);
  }
  return aggregated;
}

// ── Statistics ───────────────────────────────────────────────────────────

function percentile(sorted, p) {
  if (!sorted.length) return null;
  const idx = (sorted.length - 1) * p;
  const lo = Math.floor(idx), hi = Math.ceil(idx);
  if (lo === hi) return sorted[lo];
  return Math.round((sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo)) * 100) / 100;
}

function calculateStats(values) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  const sum = values.reduce((a, b) => a + b, 0);
  return {
    mean: Math.round(sum / values.length * 100) / 100,
    p50: percentile(sorted, 0.5),
    p95: percentile(sorted, 0.95),
    p99: percentile(sorted, 0.99)
  };
}

function aggregateMetrics(arr) {
  if (!arr.length) return null;
  const lcpValues = arr.map(m => m.lcp).filter(v => v !== null);
  return {
    iterations: arr.length,
    lcpSamples: lcpValues.length,
    fcp: calculateStats(arr.map(m => m.fcp).filter(v => v !== null)),
    lcp: calculateStats(lcpValues),
    domInteractive: calculateStats(arr.map(m => m.domInteractive).filter(v => v !== null)),
    totalTime: calculateStats(arr.map(m => m.navigationTiming?.totalTime).filter(v => v != null)),
    resources: categorizeResources(arr)
  };
}

function categorizeResources(metricsArray) {
  const all = metricsArray.flatMap(m => m.resources || []);
  const byType = (type) => all.filter(r =>
    type === 'stylesheets' ? (r.type === 'link' || r.type === 'css') :
    type === 'fetch' ? (r.type === 'fetch' || r.type === 'xmlhttprequest') :
    r.type === type
  );
  const avgResources = (resources) => {
    const grouped = {};
    resources.forEach(r => {
      if (!grouped[r.name]) grouped[r.name] = { durations: [], sizes: [], startTimes: [] };
      grouped[r.name].durations.push(r.duration);
      grouped[r.name].sizes.push(r.size);
      grouped[r.name].startTimes.push(r.startTime);
    });
    return Object.entries(grouped).map(([name, d]) => ({
      name,
      duration: Math.round(d.durations.reduce((a, b) => a + b, 0) / d.durations.length),
      size: Math.round(d.sizes.reduce((a, b) => a + b, 0) / d.sizes.length),
      startTime: Math.round(d.startTimes.reduce((a, b) => a + b, 0) / d.startTimes.length)
    }));
  };
  const n = metricsArray.length;
  const make = (items) => ({ count: Math.round(items.length / n), items: avgResources(items) });
  return {
    scripts: make(byType('script')),
    stylesheets: make(byType('stylesheets')),
    images: make(byType('img')),
    fetch: make(byType('fetch'))
  };
}

// ── Main ─────────────────────────────────────────────────────────────────

async function main() {
  let browser;
  try {
    const config = await parseConfig(configPath);

    console.error('Launching Chromium (headless)...');
    browser = await chromium.launch({ headless: true });

    // Auth setup (once for the entire run)
    const firstUrl = resolveUrl(config.scenarios[0].path);
    console.error('Setting up authentication...');
    const storageState = await setupAuth(browser, firstUrl);

    // Verification pass
    await runVerificationPass(browser, config.scenarios, storageState);

    // Pre-compute sanitized names
    const safeNames = new Map();
    for (const scenario of config.scenarios) {
      const safeName = String(scenario.name).replace(/[^a-zA-Z0-9_\- ]/g, '_');
      if (safeName !== scenario.name) console.error(`  Name sanitized: "${scenario.name}" → "${safeName}"`);
      safeNames.set(scenario.name, safeName);
    }

    // Measurement loop
    const results = Object.create(null);
    for (const scenario of config.scenarios) {
      const safeName = safeNames.get(scenario.name);
      console.error(`  Measuring: ${safeName} (${config.warmupRuns} warmup + ${config.iterations} measured)`);
      results[safeName] = await measureScenario(browser, scenario, config.iterations, config.warmupRuns, storageState);
    }

    const scenarios = config.scenarios.map(s => {
      const safeName = safeNames.get(s.name);
      const r = results[safeName];
      return r ? {
        name: safeName, url: stripQueryString(resolveUrl(s.path)),
        metrics: {
          lcp: r.lcp, lcpSamples: r.lcpSamples, fcp: r.fcp,
          domInteractive: r.domInteractive, totalLoadTime: r.totalTime
        },
        resources: r.resources
      } : null;
    }).filter(Boolean);

    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      mode: captureMode,
      unit: 'ms',
      config: {
        iterations: config.iterations,
        warmupRuns: config.warmupRuns,
        port: portOverride,
        baseUrl: baseUrl || null,
        captureTarget: baseUrl ? 'hosted' : 'localhost',
        viewport: CAPTURE_VIEWPORT,
        lcp_settle_ms: LCP_SETTLE_MS,
        lcp_max_wait_ms: LCP_MAX_WAIT_MS,
        headless: true,
        percentile_method: 'linear'
      },
      scenarios
    }, null, 2));

  } catch (error) {
    console.error(`\nFatal: ${error.message}`);
    console.error('\nChecklist:');
    if (baseUrl) {
      console.error(`  1. Is ${baseUrl} reachable?`);
      console.error('  2. Are credentials / storage-state valid?');
      if (!insecureFlag) console.error('  3. For self-signed certs, add --insecure');
    } else {
      console.error(`  1. Is the app running on localhost:${portOverride}?`);
      console.error('  2. Is @playwright/test installed?');
      console.error('  3. Are Playwright browsers installed? (npx playwright install chromium)');
    }
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
}

// ── Arg Parsing ──────────────────────────────────────────────────────────

function getArg(args, flag) {
  const i = args.indexOf(flag);
  return i !== -1 && args[i + 1] ? args[i + 1] : null;
}

function hasFlag(args, flag) {
  return args.includes(flag);
}

async function validateAndRun() {
  const args = process.argv.slice(2);

  // Config path
  const configRaw = getArg(args, '--config');
  if (!configRaw) {
    console.error('Usage:');
    console.error('  Localhost: node capture-baseline.mjs --config <path> --port <port>');
    console.error('  Hosted:   node capture-baseline.mjs --config <path> --base-url <url> [--storage-state <path>] [--user <u> --pass <p>] [--insecure]');
    process.exit(1);
  }

  const configPathResolved = resolve(configRaw);

  if (isAbsolute(configRaw)) {
    try { configPath = await realpath(configPathResolved); }
    catch (e) { if (e.code !== 'ENOENT') { console.error(`Config path error: ${e.message}`); process.exit(1); } configPath = configPathResolved; }
  } else {
    const relPath = relative(process.cwd(), configPathResolved);
    if (relPath.startsWith('..') || isAbsolute(relPath)) {
      console.error('Config path must be within CWD for relative paths. Use an absolute path instead.');
      process.exit(1);
    }
    try {
      const real = await realpath(configPathResolved);
      const realRel = relative(process.cwd(), real);
      if (realRel.startsWith('..') || isAbsolute(realRel)) {
        console.error('Config symlink points outside CWD. Use an absolute path instead.');
        process.exit(1);
      }
      configPath = real;
    } catch (e) {
      if (e.code !== 'ENOENT') { console.error(`Config path error: ${e.message}`); process.exit(1); }
      configPath = configPathResolved;
    }
  }

  // Port
  const portRaw = getArg(args, '--port');
  portOverride = portRaw ? parseInt(portRaw, 10) : null;
  if (portRaw && (isNaN(portOverride) || portOverride < 1 || portOverride > 65535)) {
    console.error(`Invalid port: ${portRaw}`); process.exit(1);
  }

  // Base URL
  baseUrl = getArg(args, '--base-url');
  if (baseUrl) {
    try {
      const parsed = new URL(baseUrl);
      if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') {
        console.error(`Invalid protocol: ${parsed.protocol}. Use http: or https:.`); process.exit(1);
      }
      baseUrl = baseUrl.replace(/\/+$/, '');
    } catch (e) {
      console.error(`Invalid --base-url: ${e.message}`); process.exit(1);
    }
    if (portOverride) {
      console.error('Warning: --port ignored when --base-url is provided.');
      portOverride = null;
    }
  }

  // Insecure
  insecureFlag = hasFlag(args, '--insecure');
  if (insecureFlag && !baseUrl) {
    console.error('--insecure requires --base-url.'); process.exit(1);
  }
  if (insecureFlag) {
    console.error('Warning: --insecure bypasses TLS certificate validation. Use only for self-signed certs in dev/test.\n');
  }

  // Storage state
  storageStatePath = getArg(args, '--storage-state');
  if (storageStatePath) {
    if (!baseUrl) { console.error('--storage-state requires --base-url.'); process.exit(1); }
    const storageResolved = resolve(storageStatePath);
    if (!isAbsolute(storageStatePath)) {
      const storageRel = relative(process.cwd(), storageResolved);
      if (storageRel.startsWith('..') || isAbsolute(storageRel)) {
        console.error('--storage-state path must be within CWD for relative paths. Use an absolute path instead.');
        process.exit(1);
      }
    }
    // Resolve symlinks and re-check containment (matches --config behavior)
    if (!isAbsolute(storageStatePath)) {
      try {
        const real = await realpath(storageResolved);
        const realRel = relative(process.cwd(), real);
        if (realRel.startsWith('..') || isAbsolute(realRel)) {
          console.error('--storage-state symlink points outside CWD. Use an absolute path instead.');
          process.exit(1);
        }
        storageStatePath = real;
      } catch (e) {
        if (e.code !== 'ENOENT') { console.error(`--storage-state path error: ${e.message}`); process.exit(1); }
        storageStatePath = storageResolved;
      }
    } else {
      storageStatePath = storageResolved;
    }
    try {
      await access(storageStatePath);
      JSON.parse(await readFile(storageStatePath, 'utf-8'));
    } catch (e) {
      console.error(`Invalid --storage-state: ${e.message}`);
      console.error(`Generate with: npx playwright codegen --save-storage=${storageStatePath} ${baseUrl}`);
      process.exit(1);
    }
  }

  // User/pass
  authUser = getArg(args, '--user');
  authPass = getArg(args, '--pass') || process.env.BASELINE_PASS || null;
  if (authUser && !baseUrl) { console.error('--user requires --base-url.'); process.exit(1); }
  if (authPass && !authUser) { console.error('--pass requires --user.'); process.exit(1); }
  if (storageStatePath && (authUser || authPass)) {
    console.error('--storage-state and --user/--pass are mutually exclusive.'); process.exit(1);
  }
  if (getArg(args, '--pass')) {
    console.error('Warning: --pass is visible in process listings and shell history.');
    console.error('  Prefer --storage-state or BASELINE_PASS env var.\n');
  }

  await main();
}

validateAndRun();
