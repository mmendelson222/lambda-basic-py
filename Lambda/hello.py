from __future__ import print_function

import json
import boto3

print('Loading function')

def handler(event, context):
    session = boto3.Session()
    ec2 = session.resource('ec2')

    print('List all EC2 instances in default region.:')
    for instance in ec2.instances.all():
        print ("InstanceID: %s" % instance.id)
    return "ok, we done."

    #raise Exception('Something went wrong')


if __name__ == "__main__":
    handler({'Organization': 'NPO1'}, "Dummy Data")