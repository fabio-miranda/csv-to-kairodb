import requests
import json
import gzip
import argparse
import csv
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return int((dt - epoch).total_seconds() * 1000)

def loadCsv(inputfilename, server, metric, tcolumn, tformat, tags, usegzip, delimiter, batchsize):

    # open csv
    datapoints = []
    inputfile = open(inputfilename, 'r')
    count = 0
    with open(inputfilename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            point = [unix_time_millis(datetime.datetime.strptime(row[tcolumn],tformat)), float(row[metric])]
            datapoints.append(point)

            if count % 100000 == 0:
                print 'Read %d lines'%count
            count+=1

    # format tags
    tks = tags.split(',')
    tags = {}
    for t in tks:
        tks2 = t.split(':')
        tags[tks2[0]] = tks2[1]

    start = 0
    end = min(count, batchsize)
    while start < count:

        data = [
            {
                "name": metric,
                "tags": tags,
                "datapoints": datapoints[start:end]
            }
        ]

        # insert
        print 'Inserting datapoints...'
        if usegzip:
            headers = {'content-type': 'application/gzip'}
            gzipped = gzip.compress(bytes(json.dumps(data), 'UTF-8'))
            response = requests.post(server + "/api/v1/datapoints", gzipped, headers=headers)
        else:
            response = requests.post(server + "/api/v1/datapoints", json.dumps(data))
            print server + "/api/v1/datapoints"

        print "Wrote %d, response: %d (status code)" % (end-start, response.status_code)
        print start, end

        start += batchsize
        end = min(count, end+batchsize)


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Csv to kairodb.')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input csv file.')

    parser.add_argument('-d', '--delimiter', nargs='?', required=False, default=',',
                        help='Csv delimiter. Default: \',\'.')

    parser.add_argument('-s', '--server', nargs='?', default='http://localhost:8080',
                        help='Server address. Default: http://localhost:8080')

    parser.add_argument('-m', '--mname', nargs='?', default='value',
                        help='Metric column name. Default: value')

    parser.add_argument('-tc', '--tcolumn', nargs='?', default='timestamp',
                        help='Timestamp column name. Default: timestamp.')

    parser.add_argument('-tf', '--tformat', nargs='?', default='%Y-%m-%d %H:%M:%S',
                        help='Timestamp format. Default: \'%%Y-%%m-%%d %%H:%%M:%%S\' e.g.: 1970-01-01 00:00:00')

    parser.add_argument('-t', '--tags', nargs='?', default='host:server',
                        help='Tag names separated by comma, e.g.: host:server1,data_center:dc1. Default: host:server')

    parser.add_argument('-g', '--gzip', action='store_true', default=False,
                        help='Compress before sending to kairodb.')

    parser.add_argument('-b', '--batchsize', type=int, default=5000,
                        help='Batch size. Default: 5000.')

    args = parser.parse_args()
    loadCsv(args.input, args.server, args.mname, args.tcolumn, args.tformat, args.tags, args.gzip, args.delimiter, args.batchsize)