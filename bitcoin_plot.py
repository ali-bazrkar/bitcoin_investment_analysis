import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from million_converter import million_converter

# receive data
btc = yf.download('BTC-USD', period='max', start='2019-01-01')

# dataframe
df = pd.DataFrame(btc)
df.reset_index(inplace=True)
df.drop(columns=['Volume', 'Adj Close', 'Low'], inplace=True)

# creating weekdays
df['Weekdays'] = df['Date'].dt.dayofweek

# filtering datas over wednesday and saturday
df = df[df['Weekdays'].isin([5, 2])]
df.reset_index(drop=True, inplace=True)

# shifting for ratio calculation
df['Next_Close'] = df['Close'].shift(-1)
df['Next_High'] = df['High'].shift(-1)

# dropping wednesdays
df = df[df['Weekdays'].isin([5])]
df.dropna(subset=['Next_Close', 'Next_High'], inplace=True)
df.reset_index(inplace=True)

# calculating the ratio
df['Ratio_Close'] = df['Next_Close'] / df['Open']
df['Ratio_High'] = df['Next_High'] / df['Open']

# dropping unworthy columns
df.drop(columns=['Open', 'High', 'Close', 'Weekdays', 'Next_High', 'Next_Close'], inplace=True)

# calculating invested amount in Close and High
df['Invest_Close'] = (1000 * df['Ratio_Close'].cumprod()).round(2)
df['Invest_High'] = (1000 * df['Ratio_High'].cumprod()).round(2)

# checking the left fund
print(f"Final USD on-Close : {df['Invest_Close'].iloc[-1]} $")
print(f"Final USD on-High : {df['Invest_High'].iloc[-1]} $")

# figure setting
plt.figure(figsize=(9, 7))

# close plot
plt.subplot(2, 1, 1)
plt.plot(df['Date'], df['Invest_Close'], color='blue')
plt.xlim(df['Date'].min(), df['Date'].max())
plt.title('Sold-on-Close')
plt.ylabel('USD')
plt.grid(True)

# high plot
plt.subplot(2, 1, 2)
plt.plot(df['Date'], df['Invest_High'], color='#fb780e')
plt.xlim(df['Date'].min(), df['Date'].max())

# convert scientific notation -> million
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(million_converter))

plt.title('Sold-on-High')
plt.ylabel('USD')
plt.grid(True)

# adjusting space between plots
plt.subplots_adjust(hspace=0.4)
plt.show()

