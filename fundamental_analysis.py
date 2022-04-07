# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 08:05:34 2022

@author: alber
"""

import pandas as pd
import requests

api_key = 'x'
stock = input('Enter Ticker Symbol (uppercase): ')
# rf_rate = input('Enter Risk-Free Rate (in Decimals): ')
# date = input('Enter date for risk-free rate(YYY-MM-DD): ')

#%%
#FunctionS that returns financial data
def get_income_statement(stock):
    income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=annual&limit=400&apikey={api_key}")
    income_statement = income_statement.json()
    
    return income_statement

def get_balance_sheet(stock):
    balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=annual&limit=400&apikey={api_key}")
    balance_sheet = balance_sheet.json()
    
    return balance_sheet

def get_cash_flow(stock):
    cash_flow = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?period=annual&limit=400&apikey={api_key}")
    cash_flow = cash_flow.json()
    
    return cash_flow

def get_dcf(stock):
    dcf = requests.get(f"https://financialmodelingprep.com/api/v3/historical-discounted-cash-flow-statement/{stock}?period=annual&limit=400&apikey={api_key}")
    dcf = dcf.json()
    
    return dcf

def get_financial_growth(stock):
    financial_growth = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{stock}?period=annual&limit=400&apikey={api_key}")
    financial_growth = financial_growth.json()
    
    return financial_growth

# def get_market_risk_premium(stock):
#     market_risk_premium = requests.get(f"https://financialmodelingprep.com/api/v4/market_risk_premium?apikey={api_key}")
#     market_risk_premium = market_risk_premium.json()
    
#     return market_risk_premium

# def get_risk_free_rate(stock):
#     risk_free_rate = requests.get(f"https://financialmodelingprep.com/api/v4/treasury?from=2022-01-01&to={date}&apikey={api_key}")
#     risk_free_rate = risk_free_rate.json()
    
#     return risk_free_rate


#%% Get Financials


income_statement = get_income_statement(stock)
income_statement = pd.DataFrame.from_dict(income_statement).set_index('date').T

balance_sheet = get_balance_sheet(stock)
balance_sheet = pd.DataFrame.from_dict(balance_sheet).set_index('date').T

cash_flow = get_cash_flow(stock)
cash_flow = pd.DataFrame.from_dict(cash_flow).set_index('date').T

financial_growth = get_financial_growth(stock)
financial_growth = pd.DataFrame.from_dict(financial_growth).set_index('date').T

dcf = get_dcf(stock)
dcf = pd.DataFrame.from_dict(dcf).set_index('date').T

# # type(get_income_statement(stock))


#%% Some Quick Metrics

#roce = EBIT/Capital Employed
#EBIT = Gross Profit - Operating Expensis
#Capital Employed = Total Assets - Current Liabilities

ebit = income_statement.loc['grossProfit'] - income_statement.loc['operatingExpenses']
cap_employed = balance_sheet.loc['totalAssets'] - balance_sheet.loc['totalCurrentLiabilities']
roce = ebit/cap_employed

# print(roce)