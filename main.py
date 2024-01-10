import pandas as pd
import yfinance as yf
import os
import test

def get_stock_price(stock_symbol):
    """
    Note: Not all stock symbols have stock_data.info['currentPrice'] e.g. QQQ
    """
    # Get the current stock price of the stock with the given stock_symbol
    # Fetch the stock data
    stock_data = yf.Ticker(stock_symbol)
    # print(stock_data.info)
    # print('stock_symbol', stock_symbol)
    # print(stock_data.history(period='1d')['Close'][0])
    # print('currentPrice', stock_data.info['currentPrice'])

    # Get the latest stock price
    if 'currentPrice' not in stock_data.info:
      latest_price = stock_data.history(period='1d')['Close'][0]
    else:
      latest_price = stock_data.info['currentPrice']
    return latest_price


def calculate_rebalancing(excel_data):
    # excel data has 3 columns: 'stock_symbol', 'number_of_shares', 'target_percentage'
    # principle is the total amount of money

    # Calculate the current value of the stocks and the current percentage of holdings
    # get new stock price
    excel_data['current_stock_price'] = excel_data['stock_symbol'].apply(get_stock_price)
    excel_data['current_stock_price'] = excel_data['current_stock_price'].round(2)
    
    # calculate current investment
    excel_data['current_total_value'] = excel_data['current_stock_price'] * excel_data['number_of_shares']
    excel_data['current_total_value'] = excel_data['current_total_value'].round(2)
    
    # calculate current percentage
    excel_data['current_percentage'] = excel_data['current_total_value'] / excel_data['current_total_value'].sum()
    excel_data['current_percentage'] = excel_data['current_percentage'].round(3)

    # Determine whether to buy or sell shares based on the difference
    excel_data['difference'] = excel_data['target_percentage'] - excel_data['current_percentage'] 
    excel_data['buy_sell'] = excel_data.apply(lambda x: (x['difference'] * excel_data['current_total_value'].sum() / x['current_stock_price']), axis=1)
    excel_data['buy_sell'] = excel_data['buy_sell'].round(0).astype(int)

    return excel_data



if __name__ == '__main__':
  # get current folder path
  current_path = os.path.dirname(os.path.realpath(__file__)) + '/'
  # read excel data into a pd dataframe
  excel_data = pd.read_excel(current_path+'sample.xlsx',usecols=['stock_symbol','number_of_shares','target_percentage'])  # Replace 'average_travel_time.xlsx' with your file path


  # Example usage

  shares_to_rebalance = calculate_rebalancing(excel_data)
  print(shares_to_rebalance)
  print(shares_to_rebalance.apply(lambda x: (("Buy" if x['buy_sell']>0 else "Sell" ) +f" {x['buy_sell']} shares of {x['stock_symbol']} at ${x['current_stock_price']}"), axis=1))
  #[current_stock_price] * shares_to_rebalance['buy_sell']
  # sanity check
  test.output_sanity_check(shares_to_rebalance)
  print(shares_to_rebalance)