from function import get_ticker

event = {"node": {'inputs': [{"name": "Name", "value": "삼성전자"}]}}

answer = get_ticker.lambda_handler(event, None)

print(answer)