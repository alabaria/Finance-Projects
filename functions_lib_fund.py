# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 01:07:42 2022

@author: alber
"""
import requests

api_key = 'x'
stock = input('Enter Ticker Symbol: ').upper()
#FunctionS that returns financial data
def get_income_statement(stock):
    income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=annual&limit=400&apikey={api_key}")
    income_statement = income_statement.json()
    
    return income_statement

def get_income_statement_q(stock):
    income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit=400&apikey={api_key}")
    income_statement = income_statement.json()
    
    return income_statement

def get_balance_sheet(stock):
    balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=annual&limit=400&apikey={api_key}")
    balance_sheet = balance_sheet.json()
    
    return balance_sheet

def get_balance_sheet_q(stock):
    balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=quarter&limit=400&apikey={api_key}")
    balance_sheet = balance_sheet.json()
    
    return balance_sheet

def get_cash_flow(stock):
    cash_flow = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?period=annual&limit=400&apikey={api_key}")
    cash_flow = cash_flow.json()
    
    return cash_flow

def get_cash_flow_q(stock):
    cash_flow_q = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?period=quarter&limit=400&apikey={api_key}")
    cash_flow_q = cash_flow_q.json()
    
    return cash_flow_q


def get_dcf(stock):
    dcf = requests.get(f"https://financialmodelingprep.com/api/v3/historical-discounted-cash-flow-statement/{stock}?period=annual&limit=400&apikey={api_key}")
    dcf = dcf.json()
    
    return dcf

def get_financial_growth(stock):
    financial_growth = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{stock}?period=annual&limit=400&apikey={api_key}")
    financial_growth = financial_growth.json()
    
    return financial_growth


def get_ev(stock):
    ev = requests.get(f"https://financialmodelingprep.com/api/v3/enterprise-values/{stock}?limit=40&apikey={api_key}")
    ev = ev.json()
    
    return ev


def get_ev_q(stock):
    ev_q = requests.get(f"https://financialmodelingprep.com/api/v3/enterprise-values/{stock}?period=quarter&limit=40&apikey={api_key}")
    ev_q = ev_q.json()
    
    return ev_q


def get_metrics(stock):
    metrics = requests.get(f"https://financialmodelingprep.com/api/v3/key-metrics/{stock}?limit=40&apikey={api_key}")
    metrics = metrics.json()
    
    return metrics


def get_metrics_ttm(stock):
    metrics_ttm = requests.get(f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{stock}?limit=40&apikey={api_key}")
    metrics_ttm = metrics_ttm.json()
    
    return metrics_ttm

#get_cagr
def cagr(start_value,end_value, num_periods):
    return (end_value/start_value) ** (1/(num_periods-1))-1