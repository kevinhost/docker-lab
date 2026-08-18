#!/bin/sh
# ERREUR CLASSIQUE : le service est lance en arriere-plan avec &.
# Le script se termine, donc le PID 1 se termine, donc le conteneur meurt.
# (sleep 300 tient ici le role de "java -jar api.jar")
sleep 300 &
echo "API demarree (mais le conteneur va mourir tout de suite)"
