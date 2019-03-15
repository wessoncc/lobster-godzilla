from __future__ import absolute_import, division, print_function

from matplotlib import pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
# import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from keras import layers
from sql_conn import password
import pymysql

pymysql.install_as_MySQLdb()
Base = declarative_base()
host = "secondawsdb.caa0qcwnjnci.us-east-2.rds.amazonaws.com"
port = 3307
dbname = "stock_data"
user = "root"
password = f"{password}"

# host = "localhost"
# port = 3306
# dbname = "stock_data"
# user = "root"
# password = f"{password}"

# noinspection PyCompatibility
engine = create_engine(f"mysql://root:{password}@{host}:{port}/stock_data")
Base.metadata.create_all(engine)
session = Session(engine)

ticker = "MCD"

DJIA = {'MSFT': 'Microsoft',
        'WMT': 'Walmart',
        'V': 'Visa',
        'AXP': 'American Express',
        'PG': 'Proctor and Gamble',
        'CVX': 'Chevron',
        'JNJ': 'Johnson & Johnson',
        'HD': 'Home Depot',
        'KO': 'Coca-Cola',
        'NKE': 'Nike',
        'JPM': 'JP Morgan Chase',
        'MCD': 'McDonalds',
        'UTX': 'United Technologies',
        'MMM': '3M',
        'AAPL': 'Apple',
        'GS': 'Goldman Sachs',
        'IBM': 'IBM',
        'TRV': 'The Travelers Company',
        'VZ': 'Verizon',
        'CSCO': 'Cisco',
        'DIS': 'Disney',
        'UNH': 'United Health',
        'XOM': 'Exxon Mobil',
        'MRK': 'Merck & Co.',
        'BA': 'Bank of America',
        'INTC': 'Intel',
        'DWDP': 'DowDuPont',
        'CAT': 'Caterpillar',
        'PFE': 'Pfizer',
        'WBA': 'Walgreens Boots Alliance'}

stoch_sql = f'SELECT * FROM stock_data.STOCH_{ticker}'
stoch = pd.read_sql(stoch_sql, engine)
stoch = stoch.drop(['level_0'], axis=1)

adx_sql = f'SELECT * FROM stock_data.ADX_{ticker}'
adx = pd.read_sql(adx_sql, engine)
adx = adx.drop(['level_0', 'Symbol'], axis=1)

macd_sql = f'SELECT * FROM stock_data.MACD_{ticker}'
macd = pd.read_sql(macd_sql, engine)
macd = macd.drop(['level_0', 'Symbol'], axis=1)

ema_sql = f'SELECT * FROM stock_data.EMA_{ticker}'
ema = pd.read_sql(ema_sql, engine)
ema = ema.drop(['level_0', 'Symbol'], axis=1)

bbands_sql = f'SELECT * FROM stock_data.BBANDS_{ticker}'
bbands = pd.read_sql(bbands_sql, engine)
bbands = bbands.drop(['level_0', 'Symbol'], axis=1)

rsi_sql = f'SELECT * FROM stock_data.RSI_{ticker}'
rsi = pd.read_sql(rsi_sql, engine)
rsi = rsi.drop(['level_0', 'Symbol'], axis=1)

hist_sql = f'SELECT * FROM stock_data.historical_data_{ticker}'
hist = pd.read_sql(hist_sql, engine)
hist = hist.drop(['ticker'], axis=1)

join1 = stoch.join(adx.set_index('index'), on='index')

join2 = join1.join(bbands.set_index('index'), on='index')

join3 = join2.join(ema.set_index('index'), on='index')

join4 = join3.join(macd.set_index('index'), on='index')

join5 = join4.join(rsi.set_index('index'), on='index')
stock_df = join5
join1.describe()
join1.head(1)
join1.tail(1)
hist.head(1)
hist.tail(1)
stock_df = stock_df.dropna()
stock_df = stock_df.rename(columns={'index': 'Date'})
stock_combo = stock_df.set_index('Date').join(hist.set_index('Date'))
stock_combo.head(1)
stock_combo['SlowK'] = stock_combo['SlowK'].astype(float)
stock_combo['SlowD'] = stock_combo['SlowD'].astype(float)
stock_combo['ADX'] = stock_combo['ADX'].astype(float)
stock_combo['Real Upper Band'] = stock_combo['Real Upper Band'].astype(float)
stock_combo['Real Middle Band'] = stock_combo['Real Middle Band'].astype(float)
stock_combo['Real Lower Band'] = stock_combo['Real Lower Band'].astype(float)
stock_combo['EMA'] = stock_combo['EMA'].astype(float)
stock_combo['MACD_Signal'] = stock_combo['MACD_Signal'].astype(float)
stock_combo['MACD_Hist'] = stock_combo['MACD_Hist'].astype(float)
stock_combo['MACD'] = stock_combo['MACD'].astype(float)
stock_combo['RSI'] = stock_combo['RSI'].astype(float)
stock_combo = stock_combo.drop(columns=["Symbol"])
stock_combo.insert(0, "date", stock_combo.index)
stock_combo.head(1)
# stock_combo.reset_index(drop='False')
plt.figure(figsize=(20, 5))
plt.subplot(1, 2, 1)
plt.plot(stock_combo['Close'])
# plt.xticks(stock_combo['date'])
plt.title(f'{ticker}', fontsize=18)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Closing Price', fontsize=18)


plt.subplot(1, 2, 2)
plt.plot(stock_combo['Adj. Close'], color='orange')
# plt.xticks(stock_combo['date'])
plt.title(f'{ticker}', fontsize=18)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Adjusted Closing Price', fontsize=18)
plt.figure(figsize=(18, 9))
plt.plot(stock_combo['Adj. Close'], color='orange')
plt.plot(stock_combo['Real Upper Band'], color='red')
plt.plot(stock_combo['Real Lower Band'], color='red')
plt.plot(stock_combo['EMA'], color='green')
plt.plot(stock_combo['MACD'], color='black')
# plt.plot(stock_combo['Real Middle Band'], color='red')
# plt.xticks(stock_combo['date'])
plt.title(f'{ticker}', fontsize=18)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Adjusted Closing Price', fontsize=18)
plt.grid(b=None, which='major', axis='both')
plt.show()

stock_combo = stock_combo.reset_index(drop=True)
stock_train = stock_combo.drop(stock_combo.index[2601:])
stock_test = stock_combo.drop(stock_train.index)
stock_train = stock_train.sample(frac=0.9, random_state=2)
train_stats = stock_train.describe()
print(train_stats)
train_stats.pop("Close")
train_stats = train_stats.transpose()
print(train_stats)
train_labels = stock_train.pop('Close')
test_labels = stock_test.pop('Close')
stock_train = stock_train.set_index('date')
stock_test = stock_test.set_index('date')


def norm(x):

        return (x - train_stats['mean']) / train_stats['std']


normed_train_data = norm(stock_train)
normed_test_data = norm(stock_test)


def build_model() -> object:
        model = keras.Sequential({
                layers.Dense(64, activation=tf.nn.relu, input_shape=[len(stock_train.keys())]),
                layers.Dense(64, activation=tf.nn.relu),
                layers.Dense(1)
        })

        optimizer = tf.keras.optimizers.RMSprop(0.001)

        model.compile(loss='mean_squared_error',
                      optimizer=optimizer,
                      metrics=['mean_absolute_error', 'mean_squared_error'])
        return model


model = build_model()

model.summary()
example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
print(example_result)


class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print('.', end='')


EPOCHS = 1000

history = model.fit(
    normed_train_data, train_labels,
    epochs=EPOCHS, validation_split=0.2, verbose=0,
    callbacks=[PrintDot()])

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print(hist.tail())


def plot_history(history):
        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch

        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Mean Abs Error [Close]')
        plt.plot(hist['epoch'], hist['mean_absolute_error'], label='Train Error'),
        plt.title(f'{ticker} Training Data'),
        plt.plot(hist['epoch'], hist['val_mean_absolute_error'], label='Val Error'),
        plt.title(f'{ticker} Training Data'),
        plt.ylim([0, 5])
        plt.legend()

        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Mean Square Error [$Close^2$]')
        plt.plot(hist['epoch'], hist['mean_squared_error'], label='Train Error'),
        plt.title(f'{ticker} Training Data'),
        plt.plot(hist['epoch'], hist['val_mean_squared_error'], label='Val Error'),
        plt.title(f'{ticker} Training Data'),
        plt.ylim([0, 20])
        plt.legend()
        plt.show()


plot_history(history)

model = build_model()

early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
                    validation_split=0.2, verbose=0, callbacks=[early_stop, PrintDot()])

plot_history(history)

loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)

print("Testing set Mean Abs Error: {:5.2f} Close".format(mae))

test_predictions = model.predict(normed_test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [Close]')
plt.ylabel('Predictions [Close]')
plt.title(f'{ticker} Test Data Predictions')
plt.axis('equal')
plt.axis('square')
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
_ = (plt.plot([-100, 100], [-100, 100]))

error = test_predictions - test_labels
plt.hist(error, bins=25)
plt.title(f'{ticker} Prediction Error Distribution')
plt.xlabel("Prediction Error [Close]")
_ = plt.ylabel("Count")