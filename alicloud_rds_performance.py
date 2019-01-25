import json,datetime,time,os
import requests
import logging


from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def getRdsPerformance(instanceId, key, startTime, endTime):
    client = AcsClient(access_id, access_secret, 'default')

    request = CommonRequest()
    
    request.set_accept_format('json')
    request.set_domain('rds.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-08-15')
    request.set_action_name('DescribeDBInstancePerformance')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('DBInstanceId', instanceId)
    request.add_query_param('Key', key)
    #example of time 2019-01-15T15:00Z
    request.add_query_param('StartTime', startTime)
    #example of time 2019-01-15T15:03Z
    request.add_query_param('EndTime', endTime)

    response = client.do_action_with_exception(request)
    # python2:  print(response) 
    return str(response, encoding = 'utf-8')

#get all mysql DBInstanceId
def getRdsMysqlList(pageNum=1, pageSize=100):

    client = AcsClient(access_id, access_secret, 'default')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('rds.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-08-15')
    request.set_action_name('DescribeDBInstances')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('Engine', 'MySQL')

    request.add_query_param('PageSize', pageSize)
    request.add_query_param('PageNumber', pageNum)

    response = client.do_action_with_exception(request)
    # python2:  print(response) 
    return str(response, encoding = 'utf-8')

def getAllRdsMysqlList():
    rds_list = []
    page_num = 0
    while True:
        page_num += 1
        single_page_resp = json.loads(getRdsMysqlList(page_num))
        page_rds = single_page_resp["Items"]["DBInstance"]
        if len(page_rds) == 0:
            break
        for rds in page_rds:
            rds_list.append(rds)
    return rds_list



#format aliyun rds performance datapoints to influxdb line protocol
def FormatAliyunDatapoints(aliyunDatapoints):
    """
    Example1:
    "PerformanceKeys": {
		"PerformanceKey": [
			{
				"Values": {
					"PerformanceValue": [
						{
							"Value": "1384.88&0.82&0.0&1.62&2.7",
							"Date": "2019-01-15T08:00:53Z"
						},
						{
							"Value": "936.83&0.77&0.0&1.33&2.6",
							"Date": "2019-01-15T08:01:53Z"
						},
						{
							"Value": "651.08&0.77&0.0&2.25&2.98",
							"Date": "2019-01-15T08:02:53Z"
						}
					]
				},
				"Key": "MySQL_RowDML",
				"Unit": "int",
				"ValueFormat": "inno_row_readed&inno_row_update&inno_row_delete&inno_row_insert&Inno_log_writes"
            }
        ]
    },
    convert to
    MySQL_InnoDBBufferRatio Engine=MySQL,ibufType=ibuf_read_hit value=100.0 2019-01-14T06:59:16Z
    """

    datapoints = json.loads(aliyunDatapoints)
    engine = datapoints["Engine"]
    instance_id = datapoints['DBInstanceId']
    tag_info = "engine=%s,instanceId=%s" % (engine, instance_id)

    data = []
    key_values = datapoints["PerformanceKeys"]["PerformanceKey"]
    if len(key_values) == 0:
        logging.info("no data")

    for key in key_values:
        pfmkey = key['Key']
        #pfmUnit = key['Unit']
        pfmValueFormat = key['ValueFormat']
        key_fields = pfmValueFormat.split('&')
        pfmValues = key['Values']['PerformanceValue']
        
        for point in pfmValues:
            value_list = point["Value"].split('&')
            date = point["Date"]
            timestamp = int(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()) * (10 ** 9)
            logging.info("timestamp of %s is %s " % (date, timestamp))

            field_kv = []

            for i in range(len(key_fields)):
                field_kv.append(key_fields[i] + "=" + value_list[i])

            field_info = ','.join(field_kv)
            data.append(pfmkey + "," + tag_info + " " + field_info + " " + str(timestamp))
    return data

        
#add instanceId and instanceName, or maybe tags

#check influxdb connection

#write data in batch mode
def influxdbWrite(url, data):
    r = requests.post(url, data=data)
    if str(r.status_code) == "204":
        logging.info("write to %s succcess, get response code %s " %(url, r.status_code))
    else:
        logging.error("write to %s failed, get response code %s " %(url, r.status_code))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO
    )
    loglevel = "info"
    access_id = os.environ.get("ACCESS_ID")
    access_secret = os.environ.get("ACCESS_SECRET")
    influxdb_url = os.environ.get("INFLUXDB_URL")
    #get all mysql performance key
    performancekeys = [
        'MySQL_NetworkTraffic',
        'MySQL_QPSTPS',
        'MySQL_Sessions',
        'MySQL_InnoDBBufferRatio',
        'MySQL_InnoDBDataReadWriten',
        'MySQL_InnoDBLogRequests',
        'MySQL_InnoDBLogWrites',
        'MySQL_TempDiskTableCreates',
        'MySQL_MyISAMKeyBufferRatio',
        'MySQL_MyISAMKeyReadWrites',
        'MySQL_COMDML',
        'MySQL_RowDML',
        'MySQL_MemCpuUsage',
        'MySQL_IOPS',
        'MySQL_DetailedSpaceUsage',
        'MySQL_CPS',
        'slavestat',
    ]
    performanceKey = ','.join(performancekeys)

    #get all datapoints with specified key in timerange
    UTC_End = datetime.datetime.today() - datetime.timedelta(hours=8)
    offset_m = 12 * 60
    UTC_Start = UTC_End - datetime.timedelta(minutes=offset_m)
    StartTime = datetime.datetime.strftime(UTC_Start, '%Y-%m-%dT%H:%MZ')
    EndTime = datetime.datetime.strftime(UTC_End, '%Y-%m-%dT%H:%MZ')

    rdsItems = getAllRdsMysqlList()
    for rds in rdsItems:
        rdsId = rds['DBInstanceId']
        logging.info(rdsId)
        raw_datapoints = getRdsPerformance(rdsId, performanceKey, StartTime, EndTime)
        data = FormatAliyunDatapoints(raw_datapoints)
        line_protocol_data = '\n'.join(data)

        influxdbWrite(influxdb_url, line_protocol_data)