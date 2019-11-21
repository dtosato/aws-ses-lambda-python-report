"""SES report sending test"""
try:
  import unzip_requirements
except ImportError:
  pass

import io
import os
import base64
import boto3
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from botocore.exceptions import ClientError
from template import TEMPLATE
sns.set(style="whitegrid")

SENDER = os.environ['SENDER']
RECIPIENT = os.environ['RECIPIENT']
AWS_REGION = os.environ['AWS_REGION']
SUBJECT = os.environ['SUBJECT']          
CHARSET = os.environ['CHARSET']

def send_mail(graph):
    """Send mail."""
    client = boto3.client('ses',region_name=AWS_REGION)
    body_html = TEMPLATE.format(graph=graph)     
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def analysis1():
    """Analyse data."""
    graph = io.BytesIO()
    f, _ = plt.subplots(figsize=(10, 5))
    sns.set_color_codes("pastel")
    sns.scatterplot(range(0, 100), np.random.random_sample(100) + 100)
    f.savefig(graph, format='png')
    return base64.b64encode(graph.getvalue()).decode(CHARSET)

def lambda_handler(event, context):
    """AWS lambda handler."""
    graph = analysis1()
    send_mail(graph)
    result = {
        'statusCode': 200,
        'body': json.dumps({'isBase64Encoded': False})
    }
    return result    


if __name__ == '__main__':
    lambda_handler(None, None)