#!/bin/sh
# Compile Api.java en api.jar SANS installer de JDK sur votre machine :
# on utilise un conteneur jetable (Podman) qui contient deja le JDK.
# Compiles Api.java into api.jar WITHOUT installing a JDK: a disposable Podman container does it.
set -e
podman run --rm -v "$PWD":/src -w /src docker.io/library/eclipse-temurin:21-jdk sh -c '
  mkdir -p build &&
  javac -d build Api.java &&
  jar --create --file api.jar --main-class Api -C build .'
echo "api.jar construit / built:"
ls -lh api.jar
