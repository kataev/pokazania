#!/bin/bash

# Replace these three settings.
PROJDIR="/home/django/pokazania/"
PIDFILE="$PROJDIR/pokazania.pid"
SOCKET="$PROJDIR/pokazania.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi


exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi host=127.0.0.1 port=12702 pidfile=$PIDFILE
