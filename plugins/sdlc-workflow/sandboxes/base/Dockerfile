FROM ghcr.io/fullsend-ai/fullsend-code:latest

USER root

COPY plugins/sdlc-workflow/ /tmp/claude-config/plugins/sdlc-workflow/
COPY plugins/sdlc-workflow/sandboxes/base/bootstrap-plugin-cache.sh /tmp/bootstrap-plugin-cache.sh
RUN /tmp/bootstrap-plugin-cache.sh /tmp/claude-config/plugins/sdlc-workflow /tmp/claude-config \
    && rm /tmp/bootstrap-plugin-cache.sh

RUN chown -R sandbox:sandbox /tmp/claude-config

USER sandbox
