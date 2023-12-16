import ais.stream
from numpy import *
import numpy as np
from sklearn.neural_network import MLPRegressor

counter = 1
aisData = {}
with open("AIVDM-7-15-19.txt") as f:
    for msg in ais.stream.decode(f):
        if "timestamp" in msg:
            aisData[counter] = (msg)
        counter = counter + 1
sortedAisData = sorted(aisData.items(), key = 
             lambda kv:(kv[1]["timestamp"], kv[1]["timestamp"]))
timestamps = 1
_5TimestampsAisData = []
for msg in sortedAisData:
    msg = msg[1]
    if msg["mmsi"] == 548456200:
        if timestamps > 1:
##            print("-----------------------------------------------------")
##            print("id:",msg["id"])
##            print("mmsi:",msg["mmsi"])
##            print("rot:",msg["rot"])
##            print("sog:",msg["sog"])
##            print("x:",msg["x"])
##            print("y:",msg["y"])
##            print("cog:",msg["cog"])
##            print("true_heading:",msg["true_heading"])
##            print("timestamp:",msg["timestamp"])
##            print("-----------------------------------------------------")
            _5TimestampsAisData.append(msg)
            timestamps = 1
        timestamps = timestamps + 1

##MLP

#Training Set
inputs = []
outputs = []
for x in _5TimestampsAisData:
    if "x" in x and "y" in x and "sog" in x and "rot" in x:
        inputs.append([x["timestamp"]])
        outputs.append([x["x"],x["y"],x["rot"],x["sog"],x["cog"],x["true_heading"]])
#MLPRegression
mlp = MLPRegressor(solver='lbfgs', alpha=1e-10,
                   hidden_layer_sizes=200, random_state=1)
print(inputs[0])
print(outputs[0])

#Training
mlp.fit(inputs,outputs)

#Prediction
print(mlp.predict([[1]]))

#Score closer to 0 means best
print(mlp.score(inputs, outputs))
