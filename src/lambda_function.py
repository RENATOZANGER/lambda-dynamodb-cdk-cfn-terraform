import json
from uuid import uuid4
from decimal import Decimal
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def lambda_handler(event, context):
    http_method = event.get('requestContext', {}).get('http', {}).get('method')

    if http_method == 'POST':
        return handle_post(event)
    elif http_method == 'GET':
        return handle_get()
    else:
        return response(400, {'message': 'Método não suportado'})
    
def handle_post(event):
    body = get_request_body(event)
    if body is None:
        return response(400, {'message': 'Corpo da requisição vazio'})
    
    item = {
        'id': str(uuid4()),       
        'name': body.get('name'),
        'price': Decimal(str(body.get('price')))
    }
    table.put_item(Item=item)
    
    return response(200, {
        'message': 'Item inserido com sucesso!',
        'item': decimal_to_float(item)
    })

def handle_get():
    items = table.scan().get('Items', [])
    return response(200, decimal_to_float(items))

def get_request_body(event):
    if 'body' in event and event['body']:
        return json.loads(event['body'])
    return None

def response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body, indent=2)
    }

def decimal_to_float(data):
    if isinstance(data, list):
        return [decimal_to_float(item) for item in data]
    elif isinstance(data, dict):
        return {k: decimal_to_float(v) for k, v in data.items()}
    elif isinstance(data, Decimal):
        return float(data)
    return data
