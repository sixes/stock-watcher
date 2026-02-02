import os
import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

recv_email = os.getenv('STOCK_WATCHER_RECV').split(',')
sender_email = os.getenv('STOCK_WATCHER_SENDER')


def send_email(subject, body, html_body=None):
    """
    Send an email using AWS SES with support for both plain text and HTML content
    
    Parameters:
    - subject: Email subject
    - body: Plain text email body
    - html_body: Optional HTML email body. If provided, the email will be sent as multipart
                with both HTML and plain text versions.
    """
    if not recv_email:
        logger.error("recv email list is empty")
        return "recv email list is empty"
    
    client = boto3.client('ses', region_name='us-east-1')
    
    # If HTML body is provided, send a multipart email
    if html_body:
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': recv_email
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': 'UTF-8',
                            'Data': html_body,
                        },
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
            logger.info(f"Sent multipart email with subject: {subject}")
            return response
        except Exception as e:
            logger.error(f"Failed to send multipart email: {str(e)}")
            raise e
    else:
        # Original plain text email if no HTML is provided
        try:
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
            logger.info(f"Sent plain text email with subject: {subject}")
            return response
        except Exception as e:
            logger.error(f"Failed to send plain text email: {str(e)}")
            raise e
