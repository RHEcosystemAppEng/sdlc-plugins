FROM registry.access.redhat.com/hi/core-runtime:latest-builder

USER root

COPY plugins/sdlc-workflow/sandboxes/base/claude-code.repo /etc/yum.repos.d/claude-code.repo

RUN dnf install -y dnf5-plugins \
    && dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo \
    && dnf install -y \
      claude-code \
      gh \
      git \
      openssh-clients \
      python3 \
      jq \
    && dnf clean all

RUN groupadd -r sandbox \
    && useradd -r -g sandbox -m -d /home/sandbox -s /bin/bash sandbox

COPY plugins/sdlc-workflow/ /home/sandbox/.claude/plugins/sdlc-workflow/

RUN chown -R sandbox:sandbox /home/sandbox

USER sandbox
WORKDIR /home/sandbox

CMD ["/bin/bash"]
