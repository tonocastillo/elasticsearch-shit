#!/usr/bin/env python

import pytz
import datetime
from elasticsearch import Elasticsearch
import time


def delete_index(index):
    response = None
    try:
	print "Deleteting index: %s" % index
	#uncomment below to delete indices or else is sort of a dry run mode.
        #response = es.indices.delete(index=index)
    except:
        print "Error!"
    return response


if __name__ == '__main__':

    es = Elasticsearch()

    #just for fun, not doint anything, for future reference.
    #today_date = pytz.utc.localize(datetime.datetime.utcnow())
    

    # use 8 for a 7 days retention:
    retention_days = 5
    retention = pytz.utc.localize(datetime.datetime.utcnow()) - datetime.timedelta(days=retention_days)
    
     
    syslog_indices = es.indices.get(index='syslog-*')
    netlow_indices = es.indices.get(index='netflow-*')

    for k,v in syslog_indices.iteritems():

        #get creation time of index, this comes in epoch time
        epoch_time_creation = str(v['settings']['index']['creation_date'])
	#removing the last 3 digits from epoch string then convert to datetime
        creation_time_fixed = epoch_time_creation[:-3]
        #convert epoch to datetime 
        index_creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(creation_time_fixed)))
        index_time_to_datetime = datetime.datetime.strptime(index_creation_time, "%Y-%m-%d %H:%M:%S")
        #convert from time naive to time aware to be able to perform a time comparation
        aware_time_conversion = index_time_to_datetime.replace(tzinfo=pytz.UTC)

        if aware_time_conversion < retention:
#            print k
            delete_index(k)

    for k,v in netlow_indices.iteritems():

        #get creation time of index, this comes in epoch time
        epoch_time_creation = str(v['settings']['index']['creation_date'])
        #removing the last 3 digits from epoch string then convert to datetime
        creation_time_fixed = epoch_time_creation[:-3]
        #convert epoch to datetime
        index_creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(creation_time_fixed)))
        index_time_to_datetime = datetime.datetime.strptime(index_creation_time, "%Y-%m-%d %H:%M:%S")
        #convert from time naive to time aware to be able to perform a time comparation
        aware_time_conversion = index_time_to_datetime.replace(tzinfo=pytz.UTC)

        if aware_time_conversion < retention:
#            print k
            delete_index(k)

