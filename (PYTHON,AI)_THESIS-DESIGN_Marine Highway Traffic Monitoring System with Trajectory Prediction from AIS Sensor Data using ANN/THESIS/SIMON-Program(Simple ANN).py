import ais.stream
from numpy import *
from scipy.special import expit

counter = 1
aisData = {}
class NeuralNet(object): 
    def __init__(self): 
        # Generate random numbers 
        random.seed(1) 
  
        # Assign random weights to a 3 x 1 matrix, 
        self.synaptic_weights = 2 * random.random((3, 1)) - 1
  
    # The Sigmoid function 
    def __sigmoid(self, x):
        return 1 / (1 + expit(-x))
  
    # The derivative of the Sigmoid function. 
    # This is the gradient of the Sigmoid curve. 
    def __sigmoid_derivative(self, x): 
        return x * (1 - x) 
  
    # Train the neural network and adjust the weights each time. 
    def train(self, inputs, outputs, training_iterations): 
        for iteration in range(training_iterations): 
  
            # Pass the training set through the network. 
            output = self.learn(inputs) 
  
            # Calculate the error 
            error = outputs - output 
  
            # Adjust the weights by a factor 
            factor = dot(inputs.T, error * self.__sigmoid_derivative(output)) 
            self.synaptic_weights += factor 
  
    # The neural network thinks. 
    def learn(self, inputs): 
        return self.__sigmoid(dot(inputs, self.synaptic_weights))

with open("AIVDM-7-15-19.txt") as f:
    for msg in ais.stream.decode(f):
        if "timestamp" in msg:
            aisData[counter] = (msg)
        counter = counter + 1
sortedAisData = sorted(aisData.items(), key = 
             lambda kv:(kv[1]["timestamp"], kv[1]["timestamp"]))
timestamps = 1
counter = 1
_5TimestampsAisData = []
for msg in sortedAisData:
    msg = msg[1]
    if timestamps == 5:
##        print("-----------------------------------------------------")
##        print("id:",msg["id"])
##        print("mmsi:",msg["mmsi"])
##        print("rot:",msg["rot"])
##        print("sog:",msg["sog"])
##        print("x:",msg["x"])
##        print("y:",msg["y"])
##        print("cog:",msg["cog"])
##        print("true_heading:",msg["true_heading"])
##        print("timestamp:",msg["timestamp"])
##        print("-----------------------------------------------------")
        _5TimestampsAisData.append(msg)
        timestamps = 1
        counter = counter + 1
    timestamps = timestamps + 1

#The training set.
inputs = []
outputs = []
for x in _5TimestampsAisData:
    if "x" in x and "y" in x and "sog" in x and "rot" in x:
        inputs.append([x["x"],x["y"],x["sog"]])
        outputs.append(x["rot"])
inputs = array(inputs)
outputs = array([outputs]).T
print(inputs,outputs)

#Initialize 
neural_network = NeuralNet()


#Train the neural network 
neural_network.train(inputs, outputs, 10**3) 
#Test the neural network with a test example. 
print(neural_network.learn(array([120.9571, 14.5752, 1.7999999523162842])))

