#!/usr/bin/python3.8

# author: Mirek Sosna
# contact: mirek.sosna@gmail.com


import requests
from requests.auth import HTTPDigestAuth
from requests import Request, Session
import json
from collections import namedtuple
import time
from datetime import datetime


# varaibles
projectid='your projectID'
keypub='genereted public key'
keypriv='generated private key'

s = requests.Session()

# cluster information
def clusterInfo():
    url = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + projectid + '/clusters?pretty=true'
    response = s.get(url, auth=HTTPDigestAuth(keypub, keypriv))

    cluster = json.dumps(response.json())
    x = json.loads(cluster, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    for i in x.results:
        for db in dblist():
            print(db.replace(":27017", ""), "DISK_TOTAL_IOPS", i.providerSettings.diskIOPS)


# server replikaset information
def replikaSetInfo():
    url = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + projectid + '/processes'
    response = s.get(url, auth=HTTPDigestAuth(keypub, keypriv))

    dbs = json.dumps(response.json())
    x = json.loads(dbs, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    for i in x.results:
        if i.typeName == 'REPLICA_PRIMARY':
            primary = 1
        else:
            primary = 0
        print(i.hostname, "REPLIKASET_PRIMERY_STATE", primary)
        print(i.hostname, "REPLIKASET_LAST_PING", round((datetime.utcnow()-datetime.strptime(i.lastPing,'%Y-%m-%dT%H:%M:%SZ')).total_seconds()))


# lists ip:port replikasetu
def dblist():
    url = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + projectid + '/processes?pretty=true'
    response = s.get(url, auth=HTTPDigestAuth(keypub, keypriv))

    lists = []
    dbs = json.dumps(response.json())
    x = json.loads(dbs, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    for i in x.results:
        lists.append(i.id)
    return lists;


# Get measurements for the specified host.
def serverStats():
    for db in dblist():
        url = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + projectid + '/processes/' + db + '/measurements?granularity=PT5M&period=PT5M'
        response = s.get(url, auth=HTTPDigestAuth(keypub, keypriv))

        data = json.dumps(response.json())
        x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        for i in x.measurements:
            for a in i.dataPoints:
                if a.value is not None:
                    value = round(a.value)
                    print(db.replace(":27017", ""), i.name, value)

# Get the list of disks or partitions for the specified host
def diskList():
    for db in dblist():
        url = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + projectid + '/processes/' + db + '/disks'
        response = s.get(url, auth=HTTPDigestAuth(keypub, keypriv))

        dLists = []
        disk = json.dumps(response.json())
        x = json.loads(disk, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        for i in x.results:
            dLists.append(i.partitionName)
        return dLists;

# Get measurements of specified disk for the specified host
def diskStatus():
    for db in dblist():
        for disk in diskList():
            url = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + projectid + '/processes/' + db + '/disks/' + disk + '/measurements?granularity=PT5M&period=PT5M'
            response = s.get(url, auth=HTTPDigestAuth(keypub, keypriv))

            data = json.dumps(response.json())
            x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            for i in x.measurements:
                for a in i.dataPoints:
                    if a.value is not None:
                        value = round(a.value)
                        print(db.replace(":27017", ""), i.name, value)


# print metric
clusterInfo()
replikaSetInfo()
serverStats()
diskStatus()
