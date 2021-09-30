import boto3
import socket
import os


def lambda_handler(event, context):
    record_name = os.environ['record_name']
    hosted_zone_id = os.environ['hosted_zone_id']
    # check the existing value for the DNS query
    existing_value = socket.gethostbyname('google.com')

    client = boto3.client('route53')
    response = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        StartRecordName='a',
        StartRecordType='A'
    )
    # pprint.pprint(response)

    # current value in r53
    for i in range(int(len(response['ResourceRecordSets']))):
        if response['ResourceRecordSets'][i]['Name'] == record_name:
            resource_value = response['ResourceRecordSets'][i]['ResourceRecords'][0]['Value']

    # print(f'value of resource record {record_name} is {resource_value}')

    if resource_value == existing_value:
        print(f'Resource Record for {record_name} does not need any update')
    else:
        print(f'Modifying the RR for{record_name} to {existing_value}...')
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                "Comment": "Automatic DNS update",
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": record_name,
                            "Type": "A",
                            "TTL": 180,
                            "ResourceRecords": [
                                {
                                    "Value": existing_value
                                },
                            ],
                        }
                    },
                ]
            }
        )
        response = client.list_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            StartRecordName='a',
            StartRecordType='A'
        )
        for i in range(int(len(response['ResourceRecordSets']))):
            if response['ResourceRecordSets'][i]['Name'] == record_name:
                new_resource_value = response['ResourceRecordSets'][i]['ResourceRecords'][0]['Value']
        print(f' RR for {record_name} is set to {existing_value}')
