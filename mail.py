import boto3
from botocore.exceptions import ClientError
from datetime import datetime

SENDER = "Amazon Gae <Chananvich.p@gmail.com>"
AWS_REGION = "ap-southeast-1"

SUBJECT = "Amazon SES Classic Test (SDK for Python)"
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)


def sendEmail(RECIPIENT,cart,total):
    SENDER = "Amazon Gae <Chananvich.p@gmail.com>"
    AWS_REGION = "ap-southeast-1"
    SUBJECT = "Amazon SES Classic Test (SDK for Python)"
    CHARSET = "UTF-8"

    list_item = [f"{name}\t\t{amount}\t{price}\t{amount*price} \n" for name,(amount,price) in cart.items()]
    list_item = "".join(list_item)
    BODY_TEXT = ("Amazon Gae Transaction Description\r\n"
            f"USER: {RECIPIENT} \n"
            f"time: {datetime.now()}\n"
            f"-------------------------------------------\n"
            f"Items\t\t Qty.\t Price\t amount\n"
            f"{list_item}\n"
            f"{total}"
            
    )
    BODY_HTML = """<html>
        <head></head>
        <body>
        <h1>Amazon SES Classic Test (SDK for Python)</h1>
        <p>This email was sent with
            <a href='https://aws.amazon.com/ses/'>Amazon SES Classic</a> using the
            <a href='https://aws.amazon.com/sdk-for-python/'>
            AWS SDK for Python (Boto)</a>.</p>
        </body>
        </html>
                """     
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
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )