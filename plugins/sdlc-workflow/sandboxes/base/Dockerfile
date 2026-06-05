FROM registry.access.redhat.com/hi/core-runtime:latest-builder

USER root
WORKDIR /sandbox

COPY plugins/sdlc-workflow/sandboxes/base/claude-code.repo /etc/yum.repos.d/claude-code.repo

RUN dnf install -y dnf5-plugins \
    && dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo \
    && dnf install -y \
      claude-code \
      gh \
      git \
      openssh-clients \
      openssh-server \
      python3 \
      jq \
      iproute \
      procps-ng \
    && dnf clean all

RUN groupadd -r supervisor && useradd -r -g supervisor -s /usr/sbin/nologin supervisor \
    && groupadd -r sandbox && useradd -r -g sandbox -d /sandbox -s /bin/bash sandbox

COPY plugins/sdlc-workflow/ /sandbox/.claude/plugins/sdlc-workflow/

RUN chown -R sandbox:sandbox /sandbox

USER sandbox
ENTRYPOINT ["/bin/bash"]
