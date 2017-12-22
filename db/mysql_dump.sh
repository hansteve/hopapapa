#!/usr/bin/env bash

DATE=`date +%Y-%m-%d_%H:%M:%S`
DATA_DIR=$1




main(){
    mysqldump --default-character-set=utf8mb4 --routines --single-transaction --force -v --add-drop-table --create-options --quick --extended-insert --compress -u root -p -h localhost hopapapa | gzip > ${DATA_DIR}/hopapapa_${DATE}.sql.gz

}
if [ ! ${DATA_DIR} ]
then
    echo 'UAGE: ./mysql_dump.sh <string:DATA_DIR>'
else
    main
fi