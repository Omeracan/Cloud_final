import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import json

SENDER = "Amazon Gae <Chananvich.p@gmail.com>"
AWS_REGION = "ap-southeast-1"

SUBJECT = "Amazon SES Classic Test (SDK for Python)"
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)
with open('map_eng_th.json') as f:
  map_eng_2_th = json.load(f)

def sendEmail(RECIPIENT,cart,total):
    SENDER = "Amazon Gae <Chananvich.p@gmail.com>"
    AWS_REGION = "ap-southeast-1"
    SUBJECT = "Amazon Gae Transaction Description"
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
    items_html = ""

    for item,(quantity, price) in cart.items():
        print(item, quantity, price)
        item_html = """<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}บาท</td>
            <td>{}บาท</td>
        </tr>""".format(map_eng_2_th[item], quantity, price, quantity*price)
        items_html+="\n"
        items_html += item_html
    total_html = """<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>""".format("", "", "Total", "{} บาท".format(total))
    items_html += total_html
    BODY_HTML = """<html>
        <head>
            <style>
                table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 30%;
                }

                td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
                }

                tr:nth-child(even) {
                background-color: #dddddd;
                }
            </style>
        </head>
        <body>
        <table>
            <tr>
                <th>Name</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Amount</th>
            </tr>"""+ items_html +"""</table>
        </body>
        </html>"""
    # BODY_HTML = BODY_HTML.format(items_html)
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
