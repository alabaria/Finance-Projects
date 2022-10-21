# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 19:34:23 2022

@author: alber
"""

import pandas as pd
import os
from functions_lib_fund import *
from fundamental_analysis import metrics_df
from income_analysis import *

income_statement = get_income_statement(stock)
income_statement = pd.DataFrame.from_dict(income_statement).set_index('date').head(10)#.T

income_statement_q = get_income_statement_q(stock)
income_statement_q = pd.DataFrame.from_dict(income_statement_q).set_index('date').head(10)#.T

balance_sheet = get_balance_sheet(stock)
balance_sheet = pd.DataFrame.from_dict(balance_sheet).set_index('date').head(10)#.T

balance_sheet_q = get_balance_sheet_q(stock)
balance_sheet_q = pd.DataFrame.from_dict(balance_sheet_q).set_index('date').head(10)#.T

cash_flow = get_cash_flow(stock)
cash_flow = pd.DataFrame.from_dict(cash_flow).set_index('date').head(10)#.T

cash_flow_q = get_cash_flow_q(stock)
cash_flow_q = pd.DataFrame.from_dict(cash_flow_q).set_index('date').head(10)#.T

financial_growth = get_financial_growth(stock)
financial_growth = pd.DataFrame.from_dict(financial_growth).set_index('date').head(10)#.T

dcf = get_dcf(stock)
dcf = pd.DataFrame.from_dict(dcf).set_index('date').head(10)#.T

ev = get_ev(stock)
ev = pd.DataFrame.from_dict(ev).set_index('date').head(10)#.T

ev_q = get_ev_q(stock)
ev_q = pd.DataFrame.from_dict(ev_q).set_index('date').head(10)#.T

metrics = get_metrics(stock)
metrics = pd.DataFrame.from_dict(metrics).set_index('date').head(10)


#%% Assumptions

required_rate = 0.125
perpetual_growth_rate = 0.02

#calculating average free cash flow growth over 10 years to get fcf_growth_rate

fcf_growth_rate = .04
# fcf_growth_rate = metrics_df['fcf_growth'][:5].mean()

years =[1,2,3,4,5]

#%% Calculations

fcf_list = metrics_df['fcf'][:5].tolist()

future_fcf =[]
discount_factor= []
discounted_future_fcf = []

terminal_value = fcf_list[0] * (1+perpetual_growth_rate)/(required_rate-perpetual_growth_rate)


for year in years:
    cash_flow = fcf_list[0] * (1+fcf_growth_rate)**year
    future_fcf.insert(0,cash_flow)
    discount_factor.insert(0,(1+required_rate)**year)



for i in range (0, len(years)) :
    discounted_future_fcf.insert(0,future_fcf[i]/discount_factor[i])


discounted_terminal_value = terminal_value/(1+required_rate)**4
discounted_future_fcf.insert(0,discounted_terminal_value)

todays_value = sum(discounted_future_fcf)

fair_value = todays_value/ev.numberOfShares[0]


print("The fair value of {} is {}".format(stock,round(fair_value,2)))
