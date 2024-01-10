import streamlit as st
import pandas as pd
import numpy as np
from main import calculate_rebalancing
from test import output_sanity_check

def app():
    st.title("Excel File Viewer")

    # File upload widget
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Read the Excel file into a DataFrame
        excel_data = pd.read_excel(uploaded_file ,usecols=['stock_symbol','number_of_shares','target_percentage'])

        # Display a info message
        with st.expander("ℹ️ How to use rebalancer"):
            st.write("""
            This page allows you to upload an Excel file of your portfolio and view the rebalancing instructions. \n
            Excel file should have 3 columns: 'stock_symbol', 'number_of_shares', 'target_percentage' \n
            **stock_symbol** : the stock symbol of the stock \n
            **number_of_shares** : the number of shares of the stock you currently own \n
            **target_percentage** : the percentage of the stock you want to own \n
            """)
        st.expander(label="i:", expanded=False)

        # Display the DataFrame
        st.write("### Excel Data")
        st.dataframe(excel_data)

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

if __name__ == "__main__":
    app()
