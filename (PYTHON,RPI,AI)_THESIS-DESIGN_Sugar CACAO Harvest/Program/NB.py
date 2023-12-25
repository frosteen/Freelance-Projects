import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import time
import joblib

# The filepath is dependent on the data_path set in the previous cell
df = pd.read_csv("Sample_Input.csv")
df = df.drop(columns=["REFRAC AVE"], axis=1)
print(df)
le = LabelEncoder()

for col in ["Classification"]:
    df[col] = le.fit_transform(df[col])

X = df.drop("Classification", axis=1)
y = df["Classification"]

print(df)

# PREDICTION

model = joblib.load("naive_bayes_model.joblib")
start_time = time.time()
y_pred = model.predict(X)
elapsed_time = time.time() - start_time

# Evaluate the performance of the model
accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred, average="weighted")
recall = recall_score(y, y_pred, average="weighted")
f1 = f1_score(y, y_pred, average="weighted")


print("Elapsed time:", elapsed_time, "seconds")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 score:", f1)
