import numpy as np
def output_sanity_check(excel_data, tolerance = 0.015):
    # check 1
    # new_percentage should be equal to percentage
    print('check 1')
    # calculate percentage after rebalancing
    excel_data['new_percentage'] = (excel_data['number_of_shares'] + excel_data['buy_sell'])*excel_data['current_stock_price'] / excel_data['current_total_value'].sum()
    # check if new_percentage is equal to percentage
    if len(excel_data) == sum(np.abs(excel_data['new_percentage'] - excel_data['target_percentage']) < tolerance):
      print('Test 1 Pass')
    else:
      print('Test 1 Fail')