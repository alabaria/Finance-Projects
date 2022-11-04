# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:21:24 2022

@author: alber
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 08:05:34 2022

@author: alber
"""

import pandas as pd
import os
from functions_lib_fund import *

# import income_analysis
# path = r'C:\Users\labar\Desktop'
# os.chdir(path)




#%% Get Financials


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

metrics_ttm = get_metrics_ttm(stock)
metrics_ttm = pd.DataFrame.from_dict(metrics_ttm)
metrics_ttm = metrics_ttm.set_axis(['ttm'], axis='index')


#%%% Important Metrics

ebit = income_statement['ebitda'] - cash_flow['depreciationAndAmortization']
ebit_ttm = income_statement_q['ebitda'].iloc[:4].sum() - cash_flow['depreciationAndAmortization'].iloc[:4].sum()

cap_employed = balance_sheet['totalAssets'] - balance_sheet['totalCurrentLiabilities']
cap_employed_q = balance_sheet_q['totalAssets'].iloc[0] - balance_sheet_q['totalCurrentLiabilities'].iloc[0]

roce = ebit/cap_employed


roce_ttm = ebit_ttm/cap_employed_q
roce_ttm = pd.DataFrame(pd.Series(data=roce_ttm))
roce_ttm = roce_ttm.rename(columns={0:'roce'})
roce_ttm = roce_ttm.set_axis(['ttm'], axis='index')


#combine dataframes
roce = pd.DataFrame(roce,columns=['roce']).sort_index(ascending=False)
roce = pd.concat([roce_ttm, roce])*100


metrics_df = roce


### FCF Yield
## FMP already has this calculated

fcf = cash_flow['operatingCashFlow'] + cash_flow['capitalExpenditure']
fcf_q = cash_flow_q['operatingCashFlow'].iloc[:4].sum() + cash_flow_q['capitalExpenditure'].iloc[:4].sum()

fcf_df = pd.DataFrame(data=fcf)
fcf_df = fcf_df.rename(columns={0:'fcf'})

fcf_q_df = pd.Series(fcf_q)

fcf_q_df = pd.DataFrame(data=fcf_q_df)
fcf_q_df = fcf_q_df.rename(columns={0:'fcf'})
fcf_q_df = fcf_q_df.set_axis(['ttm'], axis='index')

fcf_df = pd.concat([fcf_q_df,fcf_df])

metrics_df = metrics_df.join(fcf_df)

enterprise_value = ev['enterpriseValue']
enterprise_value_q = ev_q['enterpriseValue'].iloc[0]


fcf_yield = fcf/enterprise_value
fcf_yield = pd.DataFrame(data=fcf_yield)
fcf_yield = fcf_yield.rename(columns={0:'fcf_yield'})

fcf_yield_ttm = pd.Series(fcf_q/enterprise_value_q)

fcf_yield_ttm = pd.DataFrame(data=fcf_yield_ttm)
fcf_yield_ttm = fcf_yield_ttm.rename(columns={0:'fcf_yield'})
fcf_yield_ttm = fcf_yield_ttm.set_axis(['ttm'], axis='index')
fcf_yield = pd.concat([fcf_yield_ttm,fcf_yield])*100

metrics_df = metrics_df.join(fcf_yield)


### Cash Conversion
cash_conversion = pd.DataFrame(cash_flow['freeCashFlow']/income_statement['netIncome'], columns=['cash_conversion']).sort_index(ascending=False)

cash_conversion_ttm =  pd.Series(data=(cash_flow_q['freeCashFlow'].iloc[:4].sum()/income_statement_q['netIncome'].iloc[:4].sum()))
cash_conversion_ttm = cash_conversion_ttm.rename('cash_conversion')
cash_conversion_ttm = pd.DataFrame(cash_conversion_ttm)
cash_conversion_ttm = cash_conversion_ttm.set_axis(['ttm'], axis='index')


cash_conversion = pd.concat([cash_conversion_ttm, cash_conversion])*100

metrics_df = metrics_df.join(cash_conversion)



### cash return on cash invested (CROCI) 
# ebitda / Capital Invested
# CI = Total Equity + Short-term Debt + Leases + Long-term Debt
total_equity = balance_sheet['totalEquity']

capital_invested = balance_sheet['longTermDebt'] + balance_sheet['shortTermDebt'] + balance_sheet['totalEquity'] + balance_sheet['capitalLeaseObligations']


capital_invested_q =  balance_sheet_q['longTermDebt'].iloc[0] + balance_sheet_q['shortTermDebt'].iloc[0] + balance_sheet_q['totalEquity'].iloc[0] + balance_sheet_q['capitalLeaseObligations'].iloc[0]

ebitda=income_statement['ebitda']

ebitda_ttm = income_statement_q['ebitda'].iloc[:4].sum()



croci = pd.DataFrame(ebitda/capital_invested,columns=['croci']).sort_index(ascending=False)

croci_q =  pd.Series(data=(ebitda_ttm/capital_invested_q))
croci_q = croci_q.rename('croci')
croci_q = pd.DataFrame(croci_q)
croci_q = croci_q.set_axis(['ttm'], axis='index')

croci = pd.concat([croci_q, croci])*100

metrics_df = metrics_df.join(croci)



### Calculating tax rate

tax_rate = income_statement['incomeTaxExpense']/income_statement['incomeBeforeTax']
tax_rate_ttm = income_statement_q['incomeTaxExpense'].iloc[0]/income_statement_q['incomeBeforeTax'].iloc[0]


###ROIC Calculations recheck later


# nopat

nopat = ebit*(1 - tax_rate)
nopat_ttm = ebit_ttm*(1 - tax_rate_ttm)

total_debt_and_leases = balance_sheet['shortTermDebt'] + balance_sheet['longTermDebt'] + balance_sheet['capitalLeaseObligations']
total_debt_and_leases_ttm = pd.Series(data=(balance_sheet_q['shortTermDebt'].iloc[0] + balance_sheet_q['longTermDebt'].iloc[0] + balance_sheet_q['capitalLeaseObligations'].iloc[0]))
 

total_equity_and_equivalents = balance_sheet['commonStock'] + balance_sheet['retainedEarnings']
total_equity_and_equivalents_ttm = pd.Series(data=(balance_sheet['commonStock'].iloc[0] + balance_sheet['retainedEarnings'].iloc[0]))


non_operated_cash_and_investments = cash_flow['netCashUsedForInvestingActivites'] + cash_flow['netCashUsedProvidedByFinancingActivities']
non_operated_cash_and_investments_ttm = pd.Series(data=cash_flow_q['netCashUsedForInvestingActivites'].iloc[:4].sum() + cash_flow_q['netCashUsedProvidedByFinancingActivities'].iloc[:4].sum())


invested_cap = total_debt_and_leases + total_equity_and_equivalents + non_operated_cash_and_investments
invested_cap_ttm = total_debt_and_leases_ttm + total_equity_and_equivalents_ttm + non_operated_cash_and_investments_ttm

# nopat_ttm = nopat_ttm.reset_index(drop=True)
roic_ttm = nopat_ttm/invested_cap_ttm
roic_ttm = pd.DataFrame(roic_ttm)
roic_ttm = roic_ttm.rename(columns={0:'roic'})
roic_ttm = roic_ttm.set_axis(['ttm'], axis='index')



roic = nopat/invested_cap 
roic = pd.DataFrame(roic)
roic = roic.rename(columns={0:'roic'})



roic = pd.concat([roic_ttm,roic])*100

metrics_df = metrics_df.join(roic)


### D/E

debt = balance_sheet['totalDebt']
debt_ttm = balance_sheet_q['totalDebt'].iloc[0]

equity = balance_sheet['totalEquity']
equity_ttm = balance_sheet['totalEquity'].iloc[0]


de = debt/equity
de = pd.DataFrame(de)
de = de.rename(columns={0:'debt/equity'})

de_ttm = pd.DataFrame(pd.Series(debt_ttm/equity_ttm))
de_ttm = de_ttm.rename(columns={0:'debt/equity'})
de_ttm = de_ttm.set_axis(['ttm'],axis='index')

de = pd.concat([de_ttm,de])

metrics_df = metrics_df.join(de)



### Interest Coverage ebitda/incomeTaxExpense

ebitda = income_statement['ebitda']
ebitda_ttm = income_statement_q['ebitda'].iloc[:4].sum()

tax_expense = income_statement['interestExpense']
tax_expense_ttm = income_statement_q['interestExpense'].iloc[:4].sum()


ic = pd.DataFrame(ebitda/tax_expense)
ic = ic.rename(columns={0:'interest_coverage'})

ic_ttm = pd.DataFrame(pd.Series(ebitda_ttm/tax_expense_ttm))
ic_ttm = ic_ttm.rename(columns={0:'interest_coverage'})
ic_ttm = ic_ttm.set_axis(['ttm'],axis='index')


ic = pd.concat([ic_ttm,ic])
metrics_df = metrics_df.join(ic)




### PE Ratio 

pe = pd.DataFrame(metrics['peRatio'])
pe = pe.rename(columns={'peRatio':'pe'})

pe_ttm = pd.DataFrame(metrics_ttm['peRatioTTM'])
pe_ttm = pe_ttm.rename(columns={'peRatioTTM':'pe'})


pe = pd.concat([pe_ttm,pe])


metrics_df = metrics_df.join(pe)


### Gross Profit Margin
pm = pd.DataFrame(income_statement['grossProfitRatio'])
pm = pm.rename(columns={'grossProfitRatio':'gross_profit_margin'})


pm_ttm = pd.DataFrame(income_statement_q['grossProfitRatio'][:1])
pm_ttm = pm_ttm.rename(columns={'grossProfitRatio':'gross_profit_margin'})
pm_ttm = pm_ttm.set_axis(['ttm'], axis='index')

pm = pd.concat([pm_ttm,pm])*100


metrics_df = metrics_df.join(pm)


### Profit Margin

net_income = income_statement['netIncome']
net_income_ttm = income_statement_q['netIncome'].iloc[:4].sum()

revenue = income_statement['revenue']
revenue_ttm = income_statement_q['revenue'].iloc[:4].sum()

pm2 = pd.DataFrame(net_income/revenue)
pm2 = pm2.rename(columns={0:'profit_margin'})
pm2_ttm = pd.DataFrame(pd.Series(net_income_ttm/revenue_ttm))
pm2_ttm = pm2_ttm.rename(columns={0:'profit_margin'})
pm2_ttm = pm2_ttm.set_axis(['ttm'],axis='index')


pm2 = pd.concat([pm2_ttm,pm2])*100
metrics_df = metrics_df.join(pm2)


### Operating Margin
oi = pd.DataFrame(income_statement['operatingIncomeRatio'])
oi = oi.rename(columns={'operatingIncomeRatio':'operating_margin'})

oi_ttm = pd.DataFrame(income_statement_q['operatingIncomeRatio'][:1])
oi_ttm = oi_ttm.rename(columns={'operatingIncomeRatio':'operating_margin'})
oi_ttm = oi_ttm.set_axis(['ttm'], axis='index')

oi = pd.concat([oi_ttm,oi])*100


metrics_df = metrics_df.join(oi)


### Dividend Coverage fcf/dividendspaid
dc = pd.DataFrame(fcf/(cash_flow['dividendsPaid']*-1),columns=['dividend_coverage'])

dc_ttm = pd.Series(fcf_q/(cash_flow_q['dividendsPaid'][:4].sum()*-1))
dc_ttm = dc_ttm.rename('dividend_coverage')
dc_ttm = pd.DataFrame(dc_ttm)
dc_ttm = dc_ttm.set_axis(['ttm'], axis='index')

dc = pd.concat([dc_ttm,dc])


metrics_df = metrics_df.join(dc)


### Shares Outstanding 
shares_outstanding = pd.DataFrame(ev.numberOfShares)
shares_outstanding_q = pd.DataFrame(pd.Series(ev_q.numberOfShares.iloc[0]),columns=['numberOfShares'])
shares_outstanding_q = shares_outstanding_q.set_axis(['ttm'], axis='index')
             
shares_outstanding = pd.concat([shares_outstanding_q,shares_outstanding])                                   


metrics_df['fcf_growth'] =  metrics_df['fcf'].pct_change(-1)*100
metrics_df['fcf_growth_5_yr'] =  metrics_df['fcf'].pct_change(-5)*100
metrics_df['fcf_growth_3_yr'] =  metrics_df['fcf'].pct_change(-3)*100
metrics_df['fcf_per_share'] = metrics_df['fcf']/shares_outstanding.numberOfShares
metrics_df['fcf_per_share_growth'] = metrics_df['fcf_per_share'].pct_change(-1)*100

fcf_growth_df = metrics_df[['fcf','fcf_per_share','fcf_per_share_growth','fcf_growth','fcf_growth_3_yr','fcf_growth_5_yr']]

#historic averages

cols = ['roce', 'fcf_yield', 'cash_conversion', 'dividend_coverage', 'croci', 'roic' ,\
        'interest_coverage' , 'pe' , 'gross_profit_margin' , 'profit_margin','operating_margin']


avg_metrics_df_10 = pd.DataFrame(metrics_df[cols].mean(), columns =['10yr_mean'])
med_metrics_df_10 = pd.DataFrame(metrics_df[cols].median(), columns =['10yr_median'])
ttm_df = pd.DataFrame(metrics_df[cols].loc['ttm'])

avg_metrics_df_5 = pd.DataFrame(metrics_df[cols][:5].mean(), columns =['5yr_mean'])
med_metrics_df_5 = pd.DataFrame(metrics_df[cols][:5].median(), columns =['5yr_median'])

recent_year_metrics = pd.DataFrame(metrics_df[cols].iloc[1])

avg_metrics_df = ttm_df.join(recent_year_metrics)
avg_metrics_df = avg_metrics_df.join(avg_metrics_df_5)
avg_metrics_df = avg_metrics_df.join(med_metrics_df_5)
avg_metrics_df = avg_metrics_df.join(avg_metrics_df_10)
avg_metrics_df = avg_metrics_df.join(med_metrics_df_10)



# Print Output

metrics_df = metrics_df.round(2)
avg_metrics_df = avg_metrics_df.round(2)

cols = ['fcf_growth', 'fcf_growth_3_yr', 'fcf_growth_5_yr']
fcf_growth_df[cols] = fcf_growth_df[cols].round(2)
fcf_growth_df['fcf'] = (fcf_growth_df['fcf']/1000000000).apply(lambda x: '${:,.2f}B'.format(x))

# income_fcf_metrics = income_analysis.join(fcf_growth_df)

print(avg_metrics_df)
print(fcf_growth_df)
# print(income_analysis)

