# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 01:05:58 2022

@author: alber
"""

import pandas as pd
from functions_lib_fund import *
from fundamental_analysis_2 import *



### Revenue

revenue = pd.DataFrame(income_statement.revenue)
revenue_ttm = pd.DataFrame(pd.Series(income_statement_q.revenue.iloc[:4].sum()))
revenue_ttm = revenue_ttm.rename(columns={0:'revenue'})
revenue_ttm = revenue_ttm.set_axis(['ttm'],axis='index')


revenue = pd.concat([revenue_ttm,revenue])

revenue_cagr = pd.DataFrame(cagr(revenue.iloc[10],revenue.iloc[0],len(revenue))*100)
revenue_cagr = revenue_cagr.rename(columns={0:'revenue'})


### EBITDA

ebitda = pd.DataFrame(income_statement.ebitda)

ebitda_ttm = pd.DataFrame(pd.Series(income_statement_q['ebitda'].iloc[:4].sum()))
ebitda_ttm = ebitda_ttm.rename(columns={0:'ebitda'})
ebitda_ttm = ebitda_ttm.set_axis(['ttm'],axis='index')

ebitda = pd.concat([ebitda_ttm,ebitda])
ebitda['ebitda_growth'] =  ebitda['ebitda'].pct_change(-1)*100


ebitda_cagr = pd.DataFrame(pd.Series(cagr(ebitda.ebitda.iloc[10],ebitda.ebitda.iloc[0],len(ebitda.ebitda))*100))
ebitda_cagr = ebitda_cagr.rename(columns={0:'ebitda'})



### Market Cap

market_cap = pd.DataFrame(ev.marketCapitalization)
market_cap_q = pd.DataFrame(pd.Series(ev_q.marketCapitalization.iloc[0]))
market_cap_q = market_cap_q.rename(columns={0:'marketCapitalization'})
market_cap_q = market_cap_q.set_axis(['ttm'],axis='index')

market_cap = pd.concat([market_cap_q,market_cap])
market_cap['market_cap_growth'] =  market_cap['marketCapitalization'].pct_change(-1)*100

market_cap_cagr = pd.DataFrame(pd.Series(cagr(market_cap.marketCapitalization.iloc[10],market_cap.marketCapitalization.iloc[0],len(market_cap.marketCapitalization))*100))
market_cap_cagr = market_cap_cagr.rename(columns={0:'market_cap_cagr'})



### Enterprise Value

enterprise_value = pd.DataFrame(ev.enterpriseValue)
enterprise_value_q = pd.DataFrame(pd.Series(ev_q.enterpriseValue.iloc[0]))
enterprise_value_q = enterprise_value_q.rename(columns={0:'enterpriseValue'})
enterprise_value_q = enterprise_value_q.set_axis(['ttm'],axis='index')

enterprise_value = pd.concat([enterprise_value_q,enterprise_value])
enterprise_value['ev_growth'] =  enterprise_value['enterpriseValue'].pct_change(-1)*100

ev_cagr = pd.DataFrame(pd.Series(cagr(enterprise_value.enterpriseValue.iloc[10],enterprise_value.enterpriseValue.iloc[0],len(enterprise_value.enterpriseValue))*100))
ev_cagr = ev_cagr.rename(columns={0:'ev_cagr'})




### EV/EBITDA

ev_ebitda = pd.DataFrame(enterprise_value.enterpriseValue/ebitda.ebitda)
ev_ebitda = ev_ebitda.rename(columns={0:'ev/ebitda'})
ev_ebitda_avg = pd.DataFrame(pd.Series(ev_ebitda.mean()))
ev_ebitda_avg = ev_ebitda_avg.rename(columns={0:'ev_ebitda_avg'})


income_analysis = revenue.join([ebitda,market_cap,enterprise_value,ev_ebitda])

print(income_analysis)