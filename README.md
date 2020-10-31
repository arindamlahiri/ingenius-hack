# ServerPolice - A Discord Bot
## Team 41: Serial Hackers

###  BiLSTM Model :

> 

 - BiLSTM is a type of RNN architecture used to analyze sequential data.
 - RNNs use their internal state to process sequences of inputs as they are all related to each other.  They provide the same weights  and biases to all the layers, hence making the activations dependent on the previous ones.

   > 
 - Long Short-Term Memory (LSTM) networks make it easier to remember past data in memory by making use of back-propagation.

   > 

 - Bi-directional LSTM (BiLSTM) is a structure of two RNNs put together, hence allowing both forward and backward propagation. The    data is run in both ways, thereby learning relationships between    words of a sentence in both the directions.

   > 

 - The neural network for this discord bot makes use of an Embedding layer, three BiLSTM layers along with the suitable Dropout layers and two Dense layers with rectifier and sigmoidal activations respectively. This model makes use of the Adam optimizer and its performance is measured based on its accuracy, loss and F1 score
    - > Accuracy = 86.67%
    - > Loss = 0.5
    - > F1 score = 0.74
    
### Node.js

In node, we have used the npm module **discord.js** which is an *object oriented library* for interacting with the **Discord API** from a javascript application. Here we have spawned a child process inside node
to run the *python script* which imports and makes use of the model. The python script accepts a string input and gives an output which tells us if the input string is appropriate or not. 

We have passed the incoming message content from discord into the python script as input. 

We have used a *mongodb* database to keep track of how many offences does a particular user make. They get **2** warnings and are then kicked out of the server if they repeat their offence **thrice**.

### How to use

+ Our bot is deployed on heroku. Click on this [link](https://tinyurl.com/serialhackers) to add our bot to your own server.
+ Alternatively, you can join this [test server](https://discord.gg/e5HZGvdGDg) where the bot is already added. 
+ Start messaging on the general text channel to test it out.
