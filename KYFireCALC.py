"""
# KY FIRECalc App
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="KY FireCalc App",
    initial_sidebar_state="expanded"
)

st.markdown("""
  <style>
    .css-hxt7ib.e1fqkh3o2 {
      margin-top: -75px;
    }
  </style>
""", unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Set variables for simulation on sidebar
st.sidebar.header("Simulation Settings")
num_years = st.sidebar.slider("Number of Years In Retirement",1,100,30)
multiple_period = st.sidebar.checkbox('Check if you want two different withdrawal periods / rates')
if not multiple_period:
    withdrawal_rate_whole = st.sidebar.slider("Withdrawal Rate",0.0,20.0,4.0,0.5,format="%f%%")
    withdrawal_rate = withdrawal_rate_whole/100
else:
    withdrawal_rate_1_whole = st.sidebar.slider("Withdrawal Rate 1",0.0,20.0,3.5,0.5,format="%f%%")
    withdrawal_rate_1 = withdrawal_rate_1_whole/100
    time_period_1 = st.sidebar.slider("Years of Withdrawing at Withdrawal Rate 1:",0,num_years,5)
    withdrawal_rate_2_whole = st.sidebar.slider("Withdrawal Rate 2",0.0,20.0,4.0,0.5,format="%f%%")
    withdrawal_rate_2 = withdrawal_rate_2_whole/100
annual_fees_equities_whole = st.sidebar.slider("Annual Management Fees (Equities)",0.0,1.5,0.1,0.05,format="%f%%")
annual_fees_equities = annual_fees_equities_whole/100
annual_fees_bonds_whole = st.sidebar.slider("Annual Management Fees (Bonds)",0.0,1.5,0.1,0.05,format="%f%%")
annual_fees_bonds = annual_fees_bonds_whole/100
starting_portfolio = 100
equity_weight_whole = st.sidebar.slider("Equity Weight (Remainder is bonds)",0,100,60,format="%f%%")
equity_weight = equity_weight_whole/100
bond_weight = 1-equity_weight
amount_for_success_whole = st.sidebar.slider("% of portfolio spending power that needs to be left at the end of simulation to be considered successful",0,100,0,format="%f%%")
amount_for_success = amount_for_success_whole/100

#title
st.title("KY FIRECalc App")

st.write("""Using the simulation settings in the left sidebar, this app simulates portfolio returns using US stock and bond real returns data since 1872 from Robert Shiller which can be found [here](http://www.econ.yale.edu/~shiller/data.htm). 
The portfolio grows and is withdrawn from monthly. It is also assumed to be rebalanced monthly. The methodlogy was inspired by [Early Retirement Now's Safe Withdrawal Rate series](https://earlyretirementnow.com/safe-withdrawal-rate-series/). 
The code is up on GitHub here. If there are any questions about the app, you can reach me at 13hy22@queensu.ca.""")

# progress bar
latest_iteration = st.empty()
bar = st.progress(0)

df = pd.read_csv('./Data/returns_data.csv')

# At the start of simulation, determine amount to withdraw. 
# During each month, the portfolio grows according to nominal market returns and you rebalance. Fees are deducted.
# Withdrawals are made each month.

results_df = []
num_sims = 0
if not multiple_period:
    monthly_withdrawal_amt = starting_portfolio * withdrawal_rate / 12

# Increasing in one year increments each simulation
for index in range(0, len(df) - (num_years+1) * 12, 12): #for each simulation of num_years years
    num_sims += 1
    portfolio = starting_portfolio
    simulation_start = index + 12
 
    latest_iteration.text(f'Running simulations...')
    bar.progress(num_sims/np.ceil((len(df) - (num_years+1)*12)/12))
    
    for year in range(num_years): # for each year
    
        if multiple_period:
            if year < time_period_1:
                monthly_withdrawal_amt = starting_portfolio * withdrawal_rate_1 / 12
            else:
                monthly_withdrawal_amt = starting_portfolio * withdrawal_rate_2 / 12
        start_index = index + 12 * (year+1)
        #dollar amount lost every month
        monthly_equity_fees = equity_weight * portfolio * annual_fees_equities / 12
        #dollar amount lost every month
        monthly_bond_fees = bond_weight * portfolio * annual_fees_bonds / 12
        
        # During each month, (1) grow the portfolio, (2) take out the fees, (3) withdraw
        for month in range(12):
            equity_returns = df.loc[start_index + month]['Real Total Stock Return']
            bond_returns = df.loc[start_index + month]['Real Total Bonds Return']
            portfolio = portfolio*(1+(equity_weight * equity_returns + bond_weight * bond_returns)) - monthly_equity_fees - monthly_bond_fees

            #withdrawal
            portfolio -= monthly_withdrawal_amt

        #append to results_df
        results_df.append([df.loc[simulation_start,'Date'],year+1,portfolio])
        
# using results_df, calculate the success rate

results_df = pd.DataFrame(results_df, columns = ['Simulation Start', 'Year', 'End Portfolio Value'])

success_rate_df = results_df[results_df['Year']==num_years]

success_rate = len(success_rate_df[success_rate_df['End Portfolio Value'] >= starting_portfolio * amount_for_success])/len(success_rate_df)

latest_iteration.text(f'Simulations complete')
st.write('The calculator ran through ', num_sims, ' ', num_years, '-year simulations. The success rate was: ',success_rate,'.')

results_df = results_df.pivot(index='Year', columns='Simulation Start', values='End Portfolio Value')

data = []

for col in results_df.columns[:]:
    trace0 = go.Scatter(
    x = results_df.index,
    y = results_df[col],
    name = str(col)[:4]
    )
    data.append(trace0)

figure = go.Figure(data = data)

figure.update_layout(
    xaxis_title="Year in Simulation",
    yaxis_title="Portfolio End Value (Starting is 100)",
    legend_title="Starting Year of Simulation",
    font=dict(
        family="Courier New, monospace",
        size=10,
        color="RebeccaPurple"
    )
)

st.plotly_chart(figure)

st.write("Double click on a year in the legend to see just that year. Double click again to bring back all the years.")