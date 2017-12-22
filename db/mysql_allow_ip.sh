#!/usr/bin/env bash

HOSTNAME=$1
IP=$2

main(){
    ssh $HOSTNAME
    mysql -uroot -p
    GRANT ALL PRIVILEGES ON *.* TO 'root'@${IP} IDENTIFIED BY 'Mianmian2017' WITH GRANT OPTION;

}
if [ ! ${HOSTNAME} ]
then
    echo 'UAGE: ./mysql_allow.sh <string:HOSTNAME>'
else
    main
fi
