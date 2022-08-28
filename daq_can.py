import csv
import cantools
from pprint import pprint
import pandas as pd
import json
import sys

CAN_database_file="./Megasquirt_CAN-2014-10-27.dbc"
input_log_file=""
output_file=""


while len(sys.argv) > 0:
    arg=sys.argv.pop(0)
    if arg=="-i":
        if len(sys.argv)==0:
            print("\033[31mError: no argument passed to '-i'\033[m")
            exit(1)
        input_log_file=sys.argv.pop(0)
    elif arg=="-o":
        if len(sys.argv)==0:
            print("\033[31mError: no argument passed to '-o'\033[m")
            exit(1)
        output_file=sys.argv.pop(0)
    elif arg=="-d":
        if len(sys.argv)==0:
            print("\033[31mError: no argument passed to '-d'\033[m")
            exit(1)
        CAN_database_file=sys.argv.pop(0)
    elif arg=="-h":
        print("Usage: daq_can.py -i IN_FILE -o OUT_FILE [-d DBC_FILE] [-h]")
        print(" -i FILE set input log file (required)")
        print(" -o FILE set output csv file (required)")
        print(" -d FILE set input dbc file (optional, defaults to '"+CAN_database_file+"' if unspecified)")
        print(" -h display this help")
        exit(0)

if len(input_log_file)==0:
    print("\033[31mError: no input file supplied\033[m")
    exit(1)
if len(output_file)==0:
    print("\033[31mError: no output file supplied\033[m")
    exit(1)
#TODO:check input file and database file are real and readable

#Import CAN database
db = cantools.database.load_file(CAN_database_file)
signal_names=[]
for m in db.messages:
    for s in m.signals:
        signal_names.append(s.name)
#print(signal_names)

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
    return CAN_signals

#Import weird format gollum outputs (time,module,{body})
f=open(input_log_file)
lines=f.readlines()
raw_data=[]
for line in lines:
    raw_datum={}
    time,module,body=line.split(',',2)
    raw_datum["time"]=time
    raw_datum["module"]=module
    raw_datum["body"]=json.loads(body.strip())
    if "can0" in module:
        #can specific stuff
        signals=decode_can(raw_datum["body"])
        for key,value in signals.items():
            raw_datum[key]=value
    else:
        #non-can stuff
        for key,value in raw_datum["body"].items():
            raw_datum[key]=value
    raw_data.append(raw_datum)

#read data into pandas
df = pd.DataFrame(raw_data)
print(df)

#write pandas table to csv
df.to_csv(output_file, index = False)
