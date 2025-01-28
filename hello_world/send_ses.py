import os
import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

recv_email = os.getenv('STOCK_WATCHER_RECV').split(',')
sender_email = os.getenv('STOCK_WATCHER_SENDER')


def send_email(subject, body):
    if not recv_email:
        logger.error("recv email list is empty")
        return "recv email list is empty"
    client = boto3.client('ses', region_name='us-east-1')
    response = client.send_email(
    Destination={
        'ToAddresses': recv_email
    },
    Message={
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': body,
            }
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': subject,
        },
    },
    Source=sender_email
    )
    
    #print(response)
    return response