#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/biyassi.log
LOGDIR=$(dirname $LOGFILE)
LOGLEVEL=debug   # info ou warning une fois l'installation OK
NUM_WORKERS=3    # Règle : (2 x $num_cores) + 
IP=127.0.0.1
PORT=8000
APP_PATH=/home/smsi/Biyassi/

# user/group to run as
USER=smsi
GROUP=root

#we stop the services wich are runing on port 80
#kill $(sudo lsof -t -i:80)

#go to the app folder
cd /home/smsi/Biyassi/
# source ../bin/activate  # activate virtualenv
test -d $LOGDIR || sudo mkdir -p $LOGDIR
cd $APP_PATH && sudo gunicorn config.wsgi -w $NUM_WORKERS  --user=$USER --group=$GROUP -b $IP:$PORT  
# --log-level=$LOGLEVEL  --log-file=$LOGFILE 2>>$LOGFILE \
# -b $IP:$PORT
