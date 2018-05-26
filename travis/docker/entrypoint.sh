#!/bin/bash

APPS_DIR=/apps
TYGER_ROOT=$APPS_DIR/TygerCaddy
TYGER_DIR=$TYGER_ROOT/TygerCaddy
TYGER_DATA=$TYGER_DIR/data
TYGER_LOGS=$TYGER_DATA/logs

if [ -e $TYGER_ROOT ]
then
  exec /sbin/init --log-target=journal 3>&1
else
  exec /baremetal.sh
fi
