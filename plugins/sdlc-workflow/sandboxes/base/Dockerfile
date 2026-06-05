FROM registry.access.redhat.com/hi/core-runtime:latest-builder

ARG GH_CLI_VERSION=2.74.1

USER root

COPY plugins/sdlc-workflow/sandboxes/base/claude-code.repo /etc/yum.repos.d/claude-code.repo

RUN dnf install -y \
      claude-code \
      git \
      openssh-clients \
      python3 \
      jq \
      tar \
      gzip \
    && dnf clean all

RUN ARCH=$(uname -m) \
    && if [ "$ARCH" = "x86_64" ]; then GH_ARCH="linux_amd64"; \
       elif [ "$ARCH" = "aarch64" ]; then GH_ARCH="linux_arm64"; \
       else echo "Unsupported architecture: $ARCH" && exit 1; fi \
    && curl -fsSL "https://github.com/cli/cli/releases/download/v${GH_CLI_VERSION}/gh_${GH_CLI_VERSION}_${GH_ARCH}.tar.gz" \
       | tar -xz --strip-components=1 -C /usr/local

RUN groupadd -r sandbox \
    && useradd -r -g sandbox -m -d /home/sandbox -s /bin/bash sandbox

COPY plugins/sdlc-workflow/ /home/sandbox/.claude/plugins/sdlc-workflow/

RUN chown -R sandbox:sandbox /home/sandbox

USER sandbox
WORKDIR /home/sandbox

CMD ["/bin/bash"]
