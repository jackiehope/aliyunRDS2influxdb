import unittest
import json

#from alicloud_rds_performance import getRdsMysqlList, getAllRdsMysqlList

class TestAliyunApi(unittest.TestCase):

    # def test_getRdsMysqlList_return_type(self):
    #     resp = getRdsMysqlList()
    #     self.assertIsInstance(resp, str)
    #     #self.assertEqual(resp_type, 'str')

    def test_getRdsMysqlList_response(self):
        resp = """
            {
                "Items": {
                    "DBInstance": [
                        {
                            "LockMode": "Unlock",
                            "DBInstanceNetType": "Intranet",
                            "DBInstanceClass": "rds.mysql.c1.large",
                            "ResourceGroupId": "rg-acfm37cyf7cstaq",
                            "DBInstanceId": "rm-bp1nbwu82369l8g96",
                            "VpcCloudInstanceId": "rm-bp1nbwu82369l8g96",
                            "ZoneId": "cn-hangzhou-h",
                            "ReadOnlyDBInstanceIds": {
                                "ReadOnlyDBInstanceId": []
                            },
                            "InstanceNetworkType": "VPC",
                            "DBInstanceDescription": "new-rdsdb12001-market_report",
                            "ConnectionMode": "Standard",
                            "VSwitchId": "vsw-bp1ygvfm0fmrxnhp4pka8",
                            "VpcId": "vpc-qckfke9qw",
                            "Engine": "MySQL",
                            "MutriORsignle": false,
                            "InsId": 1,
                            "ExpireTime": "2019-02-11T16:00:00Z",
                            "CreateTime": "2019-01-11T11:08Z",
                            "DBInstanceType": "Primary",
                            "RegionId": "cn-hangzhou",
                            "EngineVersion": "5.7",
                            "LockReason": "",
                            "DBInstanceStatus": "Running",
                            "PayType": "Prepaid"
                        },
                        {
                            "LockMode": "Unlock",
                            "DBInstanceNetType": "Intranet",
                            "DBInstanceClass": "rds.mysql.c1.large",
                            "ResourceGroupId": "rg-acfm37cyf7cstaq",
                            "DBInstanceId": "rm-bp1g8b35nr61wn8rw",
                            "VpcCloudInstanceId": "rm-bp1g8b35nr61wn8rw",
                            "ZoneId": "cn-hangzhou-h",
                            "ReadOnlyDBInstanceIds": {
                                "ReadOnlyDBInstanceId": []
                            },
                            "InstanceNetworkType": "VPC",
                            "DBInstanceDescription": "new-rdsdb1202-market_report",
                            "ConnectionMode": "Standard",
                            "VSwitchId": "vsw-bp1ygvfm0fmrxnhp4pka8",
                            "VpcId": "vpc-qckfke9qw",
                            "Engine": "MySQL",
                            "MutriORsignle": false,
                            "InsId": 1,
                            "ExpireTime": "2019-02-11T16:00:00Z",
                            "CreateTime": "2019-01-11T11:06Z",
                            "DBInstanceType": "Primary",
                            "RegionId": "cn-hangzhou",
                            "EngineVersion": "5.7",
                            "LockReason": "",
                            "DBInstanceStatus": "Running",
                            "PayType": "Prepaid"
                        },
                        {
                            "LockMode": "Unlock",
                            "DBInstanceNetType": "Intranet",
                            "DBInstanceClass": "rds.mysql.c1.large",
                            "ResourceGroupId": "rg-acfm37cyf7cstaq",
                            "DBInstanceId": "rm-bp1kfqfh9e754hedi",
                            "VpcCloudInstanceId": "rm-bp1kfqfh9e754hedi",
                            "ZoneId": "cn-hangzhou-h",
                            "ReadOnlyDBInstanceIds": {
                                "ReadOnlyDBInstanceId": []
                            },
                            "InstanceNetworkType": "VPC",
                            "DBInstanceDescription": "new-rdsdb12003-market_report",
                            "ConnectionMode": "Standard",
                            "VSwitchId": "vsw-bp1ygvfm0fmrxnhp4pka8",
                            "VpcId": "vpc-qckfke9qw",
                            "Engine": "MySQL",
                            "MutriORsignle": false,
                            "InsId": 1,
                            "ExpireTime": "2019-02-11T16:00:00Z",
                            "CreateTime": "2019-01-11T11:06Z",
                            "DBInstanceType": "Primary",
                            "RegionId": "cn-hangzhou",
                            "EngineVersion": "5.7",
                            "LockReason": "",
                            "DBInstanceStatus": "Running",
                            "PayType": "Prepaid"
                        }
                    ]
                },
                "TotalRecordCount": 113,
                "PageNumber": 1,
                "RequestId": "4FC97520-E196-482C-8677-FC86B9B686D8",
                "PageRecordCount": 3
            }
        """
        
        resp_dict = json.loads(resp, encoding="utf-8")
        self.assertIsInstance(resp_dict['TotalRecordCount'], int)
        self.assertIsInstance(resp_dict["Items"]["DBInstance"], list)
    
    # def test_getAllRdsMysqlList(self):
    #     resp = getAllRdsMysqlList()
    #     print(resp[0])
    #     self.assertGreater(len(resp), 0)


# class TestFormatDatapoint(unittest.TestCase):
#     performance_test_data = """
#     {
# 	"DBInstanceId": "rm-bp1nbwu82369l8g96",
# 	"RequestId": "1750BE86-75EC-4F87-8820-7E462FB8C4C0",
# 	"PerformanceKeys": {
# 		"PerformanceKey": [
# 			{
# 				"Values": {
# 					"PerformanceValue": [
# 						{
# 							"Value": "1384.88&0.82&0.0&1.62&2.7",
# 							"Date": "2019-01-15T08:00:53Z"
# 						},
# 						{
# 							"Value": "936.83&0.77&0.0&1.33&2.6",
# 							"Date": "2019-01-15T08:01:53Z"
# 						},
# 						{
# 							"Value": "651.08&0.77&0.0&2.25&2.98",
# 							"Date": "2019-01-15T08:02:53Z"
# 						}
# 					]
# 				},
# 				"Key": "MySQL_RowDML",
# 				"Unit": "int",
# 				"ValueFormat": "inno_row_readed&inno_row_update&inno_row_delete&inno_row_insert&Inno_log_writes"
# 			}
# 		]
# 	},
# 	"EndTime": "2019-01-15T08:03Z",
# 	"StartTime": "2019-01-15T08:00Z",
# 	"Engine": "MySQL"
#     }
#     """

if __name__ == '__main__':
    unittest.main()