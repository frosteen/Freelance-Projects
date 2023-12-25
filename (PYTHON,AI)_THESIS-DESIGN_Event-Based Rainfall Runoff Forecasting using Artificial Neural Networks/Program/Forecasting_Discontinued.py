import pandas as pd
from keras.layers import LSTM, Dense
from keras.models import Sequential
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

df = pd.read_csv("Data/Marcos Highway.csv")
df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
df = df[["Datetime", "Data"]]
df = df.set_index("Datetime")
df["Data"] = df["Data"].str.replace("-", "0", regex=False)
df["Data"] = df["Data"].str.replace("*", "", regex=False)
df["Data"] = df["Data"].astype(float)
df.asfreq("H")

train_set = df.iloc[: int(len(df) * 0.70)]
validation_set = df.iloc[: int(len(df) * 0.10)]
test_set = df.iloc[: int(len(df) * 0.20)]

scaler.fit(train_set)
scaled_train_set = scaler.transform(train_set)
scaled_validation_set = scaler.transform(validation_set)
scaled_test_set = scaler.transform(test_set)

# define generator
n_input = 24
n_features = 1
generator_train_set = TimeseriesGenerator(
    scaled_train_set, scaled_train_set, length=n_input, batch_size=1
)
generator_validation_set = TimeseriesGenerator(
    scaled_validation_set, scaled_validation_set, length=n_input, batch_size=1
)

# define model
model = Sequential()
model.add(LSTM(100, activation="relu", input_shape=(n_input, n_features)))
model.add(Dense(1))
model.compile(optimizer="adam", loss="mse")
model.fit(
    generator_train_set, validation_data=generator_validation_set, epochs=100, verbose=2
)
