#!/usr/bin/env python

import pytz
import datetime
import re
from elasticsearch import Elasticsearch
import time

es = Elasticsearch()

#just for fun, not doint anything
today_date = pytz.utc.localize(datetime.datetime.utcnow())
# seven days retention:
retention = pytz.utc.localize(datetime.datetime.utcnow()) - datetime.timedelta(days=8)

syslog_indices = es.indices.get(index='syslog-*')


for k,v in syslog_indices.iteritems():
    epoch_time_creation = str(v['settings']['index']['creation_date'])
    creation_time_fixed = epoch_time_creation[:-3]
    index_creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(creation_time_fixed)))
    index_time_to_datetime = datetime.datetime.strptime(index_creation_time, "%Y-%m-%d %H:%M:%S")
    aware_time_conversion = index_time_to_datetime.replace(tzinfo=pytz.UTC)
    if aware_time_conversion < retention:
        print k