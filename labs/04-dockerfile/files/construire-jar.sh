#!/bin/sh
# Compile Api.java en api.jar SANS installer de JDK sur votre machine :
# on utilise un conteneur jetable qui contient deja le JDK.
set -e
docker run --rm -v "$PWD":/src -w /src eclipse-temurin:21-jdk sh -c '
  mkdir -p build &&
  javac -d build Api.java &&
  jar --create --file api.jar --main-class Api -C build .'
echo "api.jar construit :"
ls -lh api.jar
