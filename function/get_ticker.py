import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('KoreanStocks')


def get_params_by_name(data, name):
    node = data.get('node')
    if node:
        inputs = node.get('inputs')
        if inputs:
            for input_dict in inputs:
                if input_dict.get('name') == name:
                    return input_dict.get('value')
    return None


def lambda_handler(event, context):
    # 회사명 파라미터 받기
    company_name = get_params_by_name(event, "Name")

    # DynamoDB에서 회사 검색
    response = table.query(
        KeyConditionExpression=Key('Name').eq(company_name)
    )

    items = response['Items']

    # 결과 반환
    if items:
        return {
            'ticker': items[0]['Yahoo_Ticker']
        }
    else:
        return {
            'ticker': ''
        }
