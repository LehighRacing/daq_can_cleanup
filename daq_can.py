import csv
import cantools
from pprint import pprint
import pandas as pd
import json

#Import CAN database
db = cantools.database.load_file('./Megasquirt_CAN-2014-10-27.dbc')
signal_names=[]
for m in db.messages:
    for s in m.signals:
        signal_names.append(s.name)
#print(signal_names)

#Import daq data from text file and convert to csv
txt_file = r"daqdata.log"
csv_file = r"daqdata.csv"

#Import shitty format
f=open(txt_file)
lines=f.readlines()
raw_data=[]
for line in lines:
    raw_datum={}
    time,module,body=line.split(',',2)
    raw_datum["time"]=time
    raw_datum["module"]=module
    raw_datum["body"]=json.loads(body.strip())
    #if "can0" in module:
        #can specific stuff
        #print(raw_datum["body"]["id"])
    raw_data.append(raw_datum)

#takes in string of hex bytes and makes it raw hex
#this function is just a pointless redirect, but I like the name, so it stays
def dispell_hex(hex_string):
    bytes = bytearray.fromhex(hex_string)
    return bytes

#decode can data, from body of message, return all signals in message as dictionary
def decode_can(body):
    CAN_id=int(body["id"],0)
    CAN_data=dispell_hex(body["data"])
    CAN_signals=db.decode_message(CAN_id,CAN_data)
    return [list(CAN_signals.keys()),list(CAN_signals.values())]

#read data
df = pd.DataFrame(raw_data)
df["can"]=df.loc[df.module.str.contains("can0")].apply(lambda x: decode_can(x["body"]),axis=1)
#split
#pivot
#expand
print(df)

exit()

df = df.loc[~df.M.str.contains("real_sec")] #Delete the real_sec lines
df.drop(df.columns[[0, 1,2,3,4]], axis=1, inplace=True) #Delete first five columns
df = df.iloc[3:] #Delete first three rows

#Delete text in each row
df['ept'] = df['ept'].map(lambda x: x.lstrip('ept:'))
df['lat'] = df['lat'].map(lambda x: x.lstrip('lat:'))
df['lon'] = df['lon'].map(lambda x: x.lstrip('lon:'))
df['track'] = df['track'].map(lambda x: x.lstrip('track:'))
df['speed'] = df['speed'].map(lambda x: x.lstrip('speed:').rstrip('}'))
df['time'] = df['time'].map(lambda x: x.lstrip('time:"2019-05-').rstrip('Z"'))

#Export csv
#df.to_csv(r'daqdata_cleaned.csv', index = False)
