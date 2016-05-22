import os
import boto3
import botocore
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--region', default='us-east-1',
    help='AWS Region to spawn up cluster in'
)
parser.add_argument(
    'cluster',
    help='Name of the kubernetes cluster being spun up'
)

args = parser.parse_args()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
KUBE_AWS = os.path.join(BASE_PATH, 'kube-aws')
boto3.setup_default_session(region_name=args.region)

os.makedirs(os.path.join(BASE_PATH, args.cluster))
os.chdir(os.path.join(BASE_PATH, args.cluster))

ec2 = boto3.resource('ec2')

try:
    ssh_key = ec2.create_key_pair(KeyName=args.cluster)

    with open('cluster_key', 'w') as w:
        os.chmod('cluster_key', 0o600)
        w.write(ssh_key.key_material)
except botocore.exceptions.ClientError as e:
    if 'Error' in e.response and \
       e.response['Error']['Code'] == 'InvalidKeyPair.Duplicate':
        print('key already exists')
    else:
        raise

kms = boto3.client('kms')
kms_entry = kms.create_key(Description=args.cluster)

kms_arn = kms_entry['KeyMetadata']['Arn']

subprocess.check_call([
    KUBE_AWS,
    'init',
    '--external-dns-name', args.cluster + '.omgwtf.in',
    '--cluster-name', args.cluster,
    '--region', args.region,
    '--availability-zone', args.region + 'c',
    '--key-name', args.cluster,
    '--kms-key-arn', kms_arn
])

subprocess.check_call([
    KUBE_AWS,
    'render'
])

subprocess.check_call([
    KUBE_AWS,
    'up'
])

subprocess.check_call([
    KUBE_AWS,
    'status'
])
