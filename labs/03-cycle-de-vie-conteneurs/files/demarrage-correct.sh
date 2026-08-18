#!/bin/sh
# CORRECTION : le service tourne au premier plan, et 'exec' remplace le shell
# par le service, qui devient donc PID 1 et recevra les signaux.
echo "API demarree"
exec sleep 300
