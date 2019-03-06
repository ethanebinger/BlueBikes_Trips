# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:38:02 2019

@author: eebinger
"""

import csv
import datetime as datetime

working_dir = r'C:/Documents/'
data_files = [
    '201501-hubway-tripdata.csv',
    '201502-hubway-tripdata.csv',
    '201503-hubway-tripdata.csv',
    '201504-hubway-tripdata.csv',
    '201505-hubway-tripdata.csv',
    '201506-hubway-tripdata.csv',
    '201507-hubway-tripdata.csv',
    '201508-hubway-tripdata.csv',
    '201509-hubway-tripdata.csv',
    '201510-hubway-tripdata.csv',
    '201511-hubway-tripdata.csv',
    '201512-hubway-tripdata.csv',
    '201601-hubway-tripdata.csv',
    '201602-hubway-tripdata.csv',
    '201603-hubway-tripdata.csv',
    '201604-hubway-tripdata.csv',
    '201605-hubway-tripdata.csv',
    '201606-hubway-tripdata.csv',
    '201607-hubway-tripdata.csv',
    '201608-hubway-tripdata.csv',
    '201609-hubway-tripdata.csv',
    '201610-hubway-tripdata.csv',
    '201611-hubway-tripdata.csv',
    '201612-hubway-tripdata.csv',
    '201701-hubway-tripdata.csv',
    '201702-hubway-tripdata.csv',
    '201703-hubway-tripdata.csv',
    '201704-hubway-tripdata.csv',
    '201705-hubway-tripdata.csv',
    '201706-hubway-tripdata.csv',
    '201707-hubway-tripdata.csv',
    '201708-hubway-tripdata.csv',
    '201709-hubway-tripdata.csv',
    '201710-hubway-tripdata.csv',
    '201711-hubway-tripdata.csv',
    '201712-hubway-tripdata.csv',
    '201801_hubway_tripdata.csv',
    '201802_hubway_tripdata.csv',
    '201803_hubway_tripdata.csv',
    '201804-hubway-tripdata.csv',
    '201805-bluebikes-tripdata.csv',
    '201806-bluebikes-tripdata.csv',
    '201807-bluebikes-tripdata.csv',
    '201808-bluebikes-tripdata.csv',
    '201809-bluebikes-tripdata.csv',
    '201810-bluebikes-tripdata.csv',
    '201811-bluebikes-tripdata.csv',
    '201812-bluebikes-tripdata.csv',
    '201901-bluebikes-tripdata.csv',
    '201902-bluebikes-tripdata.csv'
]

for f in data_files:
    # collect stations
    stations = []
    with open(working_dir + "/csv_data/" + f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("reading csv: " + f)
        for trip in reader:
            stations.append(int(trip['start station id']))
        #end for
    #end with
    csvfile.close()
    stations = list(set(stations))
    
    # create dict to store records per station (+1 for total column)
    heatmap_dict = {}
    for d in range(0,7):
        for h in range(0,24):
            heatmap_dict[(d,h)] = [x*0 for x in range(len(stations)+1)]
        #end for
    #end for
    
    # fill dict with data
    with open(working_dir + "/csv_data/" + f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for trip in reader:
            start_time = str(trip['starttime'])
            station_id = int(trip['start station id'])
            try:
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
                start_dow = start_time.weekday()
                start_hour = start_time.hour
                heatmap_dict[(start_dow, start_hour)][-1] += 1
                heatmap_dict[(start_dow, start_hour)][stations.index(station_id)] += 1
            except ValueError:
                try:
                    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                    start_dow = start_time.weekday()
                    start_hour = start_time.hour
                    heatmap_dict[(start_dow, start_hour)][-1] += 1
                    heatmap_dict[(start_dow, start_hour)][stations.index(station_id)] += 1
                except ValueError:
                    pass
                #end try
            #end try
        #end for
    #end with
    csvfile.close()
    
    # write to CSV
    with open(working_dir+ "/heatmap_data/heatmap_data_"+f[:6]+".csv", "wb") as csv_file:
        writer = csv.writer(csv_file)
        #data_files_trunc = [x[:6] for x in data_files]
        writer.writerow(["day"] + ["hour"] + stations + ["total"])
        for d in range(0,7):
            for h in range(0,24):
                writer.writerow([d] + [h] + heatmap_dict[(d,h)])
            #end for
        #end for
    #end with
#end for