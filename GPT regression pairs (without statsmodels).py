import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch data

year_start = input('Start Year: ')
month_start = input('Start Month: ')
day_start = input('Start Day: ')

if len(month_start) == 0:
    month_start = '01'
if len(day_start) == 0:
    day_start = '01'

start_date = year_start + '-' + month_start + '-' + day_start

print(start_date)

year_end = input('End Year: ')
month_end = input('End Month: ')
day_end = input('End Day: ')


if len(month_end) == 0:
    month_end = '01'
if len(day_end) == 0:
    day_end = '01'

    
end_date = year_end + '-' + month_end + '-' + day_end
print(end_date)


tick1=input('Ticker 1: ')
tick2=input('Ticker 2: ')

tick1_data = yf.download(tick1, start=start_date, end=end_date)
tick2_data = yf.download(tick2, start=start_date, end=end_date)

# Use only closing price for each day
tick1_data = tick1_data['Close']
tick2_data = tick2_data['Close']

# Estimate the hedge ratio using linear regression
hedge_ratio = np.polyfit(tick2_data, tick1_data, 1)[0]

# Compute the spread
spread = tick1_data - hedge_ratio * tick2_data

# Compute the z-score of the spread
z_score = (spread - spread.mean()) / spread.std()

# Create signals based on the z-score
threshold = 0.25
tick1_data = pd.DataFrame(tick1_data)
tick1_data['Long'] = z_score < -threshold
tick1_data['Short'] = z_score > threshold
tick1_data['Exit'] = abs(z_score) < 0.05

tick1_data['Positions'] = tick1_data['Long'].astype(int) - tick1_data['Short'].astype(int)

tick1_data['Returns'] = tick1_data['Positions'].shift() * tick1_data['Close'].pct_change()

# Calculate cumulative returns
tick1_data['Cumulative Return'] = (1 + tick1_data['Returns']).cumprod()

# Print the dataframe
print(tick1_data)

# Plot cumulative returns
plt.figure(figsize=(12,5))
plt.title('Cumulative Returns of the ' + tick1 + ' ' + tick2 + ' Pair Trading Strategy')
plt.plot(tick1_data['Cumulative Return'])
plt.show()
