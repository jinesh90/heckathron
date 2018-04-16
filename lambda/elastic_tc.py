import boto3



def lambda_handler(event, context):

    client = boto3.client('elastictranscoder', 'us-east-1')
    print("Welcome")
    sourcekey = event.get('Records')[0].get('s3').get('object').get('key')

    print("Input Key:{}".format(sourcekey))

    output_key = sourcekey.split('.')[0]
    pipeline_id = "1517711532722-afzjr6"
    input = {
        'Key' : sourcekey
    }
    hls_2000k = {
        'Key': 'hls2000k/' + output_key,
        'ThumbnailPattern': 'hls2000k/thumbnail/' + output_key + '-{resolution}-{count}',
        'PresetId': '1351620000001-200010',
        'SegmentDuration': '4'
    }

    outputs = [hls_2000k]

    job_result = client.create_job(PipelineId=pipeline_id,
                                        Input=input,
                                        Outputs=outputs)

"""

{u'Records': 
[{u'eventVersion': u'2.0', u'eventTime': u'2018-04-16T01:12:16.411Z', u'requestParameters': {u'sourceIPAddress': u'73.92.64.228'}, u's3': {u'configurationId': u'a068a465-e79e-4ac1-932f-2fe671ec801d', u'object': {u'versionId': u'oosA.ipb49tOWXkWfFuSQ9XgirSRxsdD', u'eTag': u'd9061d3da8601932e98f79ec8ba1c877', u'sequencer': u'005AD3F8704B11A86B', u'key': u'earth.mp4', u'size': 1570024}, u'bucket': {u'arn': u'arn:aws:s3:::ebooks-jinesh', u'name': u'ebooks-jinesh', u'ownerIdentity': {u'principalId': u'A2M93P9NTLTVKS'}}, u's3SchemaVersion': u'1.0'}, u'responseElements': {u'x-amz-id-2': u'wKqFVpiu6+pRLEHMxgNhfCQ7mgADHrYnpoTpWgeYyqKrpf6Ec9y9EGQRlegpQzN2wgXX+IN0yCc=', u'x-amz-request-id': u'13F5D0C3F76C57CA'}, u'awsRegion': u'us-east-1', u'eventName': u'ObjectCreated:Put', u'userIdentity': {u'principalId': u'A2M93P9NTLTVKS'}, u'eventSource': u'aws:s3'}]}

"""