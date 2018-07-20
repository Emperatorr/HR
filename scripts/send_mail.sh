#!/bin/bash

THISHOST=$(hostname)
if [ $THISHOST = "ebiassy" ]; then
    echo "ebiassy send_mail"_$(date +'%Y_%m_%dT%H_%M_%S')
    export USER=smsi
    export MAIL=/var/mail/smsi
    export OLDPWD=/home/smsi/Biyassi
    export PWD=/home/smsi/Biyassi/script
    export HOME=/home/smsi
    export LOGNAME=smsi
    export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin
else
    echo "localhost"
fi

mailto=''
python3 manage.py send_mail

#*/03 * * * * cd /home/smsi/Biyassi/script && ./send_mail.sh
