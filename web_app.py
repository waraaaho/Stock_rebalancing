import streamlit as st
import pandas as pd
import numpy as np
import os
from main import calculate_rebalancing
from test import output_sanity_check

def rebalance_st(excel_data):
    # Display the DataFrame
    st.write("### Excel Data")
    st.dataframe(excel_data[['stock_symbol','number_of_shares','target_percentage']])

    # Calculate the rebalancing
    shares_to_rebalance = calculate_rebalancing(excel_data)

    # Regulate decimal places
    # print(shares_to_rebalance.columns) 
    st.write("### Rebalancing Summary")
    with st.expander("Brief View"):
        st.dataframe(shares_to_rebalance.drop(columns=['target_percentage','current_stock_price','number_of_shares','difference']).style.format(subset=['current_total_value',], formatter="{:.2f}"))
    with st.expander("Detailed View"):
        st.dataframe(shares_to_rebalance.style.format(subset=['target_percentage','current_stock_price', 'current_total_value', 'current_percentage', 'difference',], formatter="{:.2f}"))

    # Display the rebalancing instructions
    st.write("### Rebalancing Instructions")
    for instruction in shares_to_rebalance.apply(lambda x: (("Buy" if x['buy_sell']>0 else "Sell" ) +f" {np.abs(x['buy_sell'])} shares of {x['stock_symbol']} at ${round(x['current_stock_price'],2)}"), axis=1):
        st.write(instruction)
        
    output_sanity_check(shares_to_rebalance)
    return shares_to_rebalance

def app():
    st.title("Stock Rebalancer")

    # Display a info message
    with st.expander("ℹ️ How to use rebalancer"):
        st.write("""
        This page allows you to upload an Excel file of your portfolio and view the rebalancing instructions. \n
        Excel file should have 3 columns: 'stock_symbol', 'number_of_shares', 'target_percentage' \n
        **stock_symbol** : the stock symbol of the stock \n
        **number_of_shares** : the number of shares of the stock you currently own \n
        **target_percentage** : the percentage of the stock you want to own \n
        """)
        st.write(os.getcwd())
        st.image("sample_img.png", caption="Sample Excel File", use_column_width=True)
    data_type = st.radio(
        "Would you like to upload an Excel file or fill a form?",
        ["Upload Excel File", "Fill a Form"],
        horizontal=True,
        )

    if data_type == "Upload Excel File":
        # File upload widget
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

        if uploaded_file is not None:
            # Read the Excel file into a DataFrame
            excel_data = pd.read_excel(uploaded_file ,usecols=['stock_symbol','number_of_shares','target_percentage'])
            # Rebalance the portfolio
            rebalance_st(excel_data)

    elif data_type == "Fill a Form":
        if 'data' not in st.session_state:
            st.session_state['data'] = pd.DataFrame(columns=['stock_symbol','number_of_shares','target_percentage'])

        # Create a form
        with st.form(key='my_form',clear_on_submit=False):
            # Add a text input for stock symbol
            stock_symbol = st.text_input('Stock Symbol')
            # Add a text input for number of shares
            number_of_shares = st.number_input('Number of Shares', min_value=0, max_value=100000, value=0, step=1)
            # Add a text input for target percentage
            target_percentage = st.number_input('Target Percentage', min_value=0.0, max_value=1.0, value=0.0, step=0.01)
            # Create a submit button and add a label
            add = st.form_submit_button(label='Add',)

        if add:
            # find stock symbol in the dataframe
            if stock_symbol in st.session_state['data']['stock_symbol'].values:
                # update the number of shares and target percentage
                st.session_state['data'].loc[st.session_state['data']['stock_symbol'] == stock_symbol, ['number_of_shares','target_percentage']] = [number_of_shares,target_percentage]
            else:
                # Append from the input form data 
                st.session_state['data'] = st.session_state['data'].append({'stock_symbol':stock_symbol,'number_of_shares':number_of_shares,'target_percentage':target_percentage}, ignore_index=True)
        
        # Create a button to remove last row
        remove = st.button('Remove Last Row')
        if remove:
            # Remove last row
            st.session_state['data'] = st.session_state['data'].iloc[:-1]

        # Conduct rebalancing if there is data
        if not st.session_state['data'].empty:
            # Rebalance the portfolio
            rebalance_st(st.session_state['data'])
        

if __name__ == "__main__":
    app()
