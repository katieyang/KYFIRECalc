# KYFIRECalc
A FIRE (financial independence retire early) calculator application built using Pandas, Plotly, and Streamlit
 
# Description
Using different simulation settings (e.g., number of years in retirement, stock/bond weighting etc.), this app simulates portfolio returns using US stock and bond real returns data since 1872 from Robert Shiller which can be found [here](http://www.econ.yale.edu/~shiller/data.htm). The portfolio grows and is withdrawn from monthly. It is also assumed to be rebalanced monthly. The methodology was inspired by [Early Retirement Now's Safe Withdrawal Rate series](https://earlyretirementnow.com/safe-withdrawal-rate-series/). The app allows for setting two different withdrawal rates over the simulation period. If there are any questions about the app, you can reach me at 13hy22@queensu.ca.

# Hosted On Streamlit
You can see the project live here: [https://kyfirecalc.streamlit.app/](https://kyfirecalc.streamlit.app/)


# Install and Run The Project
After cloning the repository, go to the folder and use `pip install -r requirements.txt` to install requirements. 
Then use `streamlit run KYFireCALC.py` to run the app locally.


# Other Notes
I am open to updating this project if anyone has any issues/desired functionality not already in it. Please feel free to fork and build your own calculator as well.
