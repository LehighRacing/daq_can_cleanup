# Software for converting DAQ logs generated by gollum to csv

## Usage
- `python3 daq_can_cleanup.py -i IN_FILE -o OUT_FILE [-d DBC_FILE]`
- Note: untrimmed logs can take quite a long time to process, and use a lot of memory, so consider trimming it down first
	- for example, a log of ~30 minutes of data takes ~4 mins and >10 GiB of memory to convery
- Note: make sure your csv editor won't try to merge empty delimiters

## Installation
- good practice in python is to use a virtual environment such as `venv`
- install python packages from `requirements.txt`
	- `pip install -r requirements.txt`
