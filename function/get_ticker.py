import json
import boto3
from boto3.dynamodb.conditions import Key


session = boto3.Session()
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('KoreanStocks')


def lambda_handler(event, context):
    # 회사명 파라미터 받기
    company_name = event['queryStringParameters']['company']

    # DynamoDB에서 회사 검색
    response = table.query(
        KeyConditionExpression=Key('CompanyName').eq(company_name)
    )

    items = response['Items']

    # 결과 반환
    if items:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'company': company_name,
                'ticker': items[0]['YahooTicker']
            })
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Company not found'})
        }
