FROM python:3.10-slim-bullseye

ENTRYPOINT ["/bin/pex_binary"]

COPY helloworld/pex_binary.pex /bin/pex_binary