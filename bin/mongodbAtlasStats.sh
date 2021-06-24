#!/bin/bash

getMongoStats(){
python3.8 /etc/zabbix/scripts/atlasApiToZabbix.py
}

getMongoStats | zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i -
