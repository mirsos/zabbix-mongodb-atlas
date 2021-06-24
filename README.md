# zabbix-mongodb-atlas
Script to downloading statistics from API MongoDB Atlat Database and place it on Zabbix Server

Requirements
1. Python3
2. Zabbix Server 4.4

Installation:
1. Create API Key - https://docs.atlas.mongodb.com/configure-api-access/
2. Add template into your Zabbix Server
3. Add atlasApiToZabbix.py mongodbAtlasStats.sh into /etc/zabbix/scripts on your Zabbix Server
4. Add cron file into /etc/cron.d/

How this works!

This script connect to API MongoDB Atlas downloading all metrick from ReplikaSet and sending it to Zabbix Serwer through zabbix_sender.
Script on output gives server names, and you have to add that names to Zabbix Server. 
I useed CRON because trigger dowloading metrics for all nodes in ReplikaSet, otherwise in one minutes you got N-triggers where N is number of nodes in your ReplikaSet
