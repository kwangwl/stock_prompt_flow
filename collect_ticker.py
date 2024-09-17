import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr


# KRX 상장기업 목록 가져오기
def get_krx_stocks():
    df = fdr.StockListing('KRX')
    return df[['Code', 'Name', 'Market']]


# 야후 파이낸스 ticker 형식으로 변환
def convert_to_yahoo_ticker(row):
    if row['Market'] == 'KOSPI':
        return f"{row['Code']}.KS"
    elif row['Market'] == 'KOSDAQ':
        return f"{row['Code']}.KQ"
    return None


# ticker 유효성 검증
def validate_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock.info
        return True
    except:
        return False


# 메인 실행 코드
krx_stocks = get_krx_stocks()
krx_stocks['Yahoo_Ticker'] = krx_stocks.apply(convert_to_yahoo_ticker, axis=1)

# None 값을 가진 행 제거
krx_stocks = krx_stocks.dropna(subset=['Yahoo_Ticker'])

# 유효성 검증 및 최종 데이터프레임 생성
valid_stocks = []
total_stocks = len(krx_stocks)

for index, row in krx_stocks.iterrows():
    if validate_ticker(row['Yahoo_Ticker']):
        valid_stocks.append({'Name': row['Name'], 'Yahoo_Ticker': row['Yahoo_Ticker']})

    # 진행 상황 출력 (선택사항)
    if (index + 1) % 100 == 0:
        print(f"Progress: {index + 1}/{total_stocks}")

    # if index > 20:
    #     break

valid_stocks_df = pd.DataFrame(valid_stocks)

# 결과 저장
valid_stocks_df.to_csv('korean_stocks_yahoo_tickers.csv', index=False)
