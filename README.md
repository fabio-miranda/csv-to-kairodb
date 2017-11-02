# csv-to-kairodb
Simple python script that inserts data points read from a csv file into a running kairodb instance.

## Usage

```
usage: csv-to-kairodb.py [-h] -i [INPUT] [-d [DELIMITER]] [-s [SERVER]]
                         [-m [METRICNAME]] [-tc [TIMECOLUMN]]
                         [-tf [TIMEFORMAT]] [-t [TAGCOLUMNS]] [-g]
                         [-b BATCHSIZE]

Csv to kairodb.

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT], --input [INPUT]
                        Input csv file.
  -d [DELIMITER], --delimiter [DELIMITER]
                        Csv delimiter. Default: ','.
  -s [SERVER], --server [SERVER]
                        Server address. Default: http://localhost:8080
  -m [METRICNAME], --metricname [METRICNAME]
                        Metric column name. Default: value
  -tc [TIMECOLUMN], --timecolumn [TIMECOLUMN]
                        Timestamp column name. Default: timestamp.
  -tf [TIMEFORMAT], --timeformat [TIMEFORMAT]
                        Timestamp format. Default: '%Y-%m-%d %H:%M:%S' e.g.:
                        1970-01-01 00:00:00
  -t [TAGCOLUMNS], --tagcolumns [TAGCOLUMNS]
                        List of csv columns to use as tags, separated by
                        comma, e.g.: host,data_center. Default: host
  -g, --gzip            Compress before sending to kairodb.
  -b BATCHSIZE, --batchsize BATCHSIZE
                        Batch size. Default: 5000.

```

## Example

Considering the csv file:
```
timestamp,value,computer
1970-01-01 00:00:00,51.374894,0
1970-01-01 00:00:01,74.562764,1
1970-01-01 00:00:02,17.833757,2
1970-01-01 00:00:03,40.125102,0
1970-01-01 00:00:04,88.160817,1
1970-01-01 00:00:05,28.401695,2
1970-01-01 00:00:06,98.670792,3
1970-01-01 00:00:07,69.532011,0
1970-01-01 00:00:08,39.198964,0
```

The following command will insert the file into a running kairodb instance:

```python csv-to-kairodb.py --input data.csv --tagcolumns computer```