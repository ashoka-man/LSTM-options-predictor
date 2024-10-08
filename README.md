# LSTM-options-predictor
Goal: We will build a neural network which can process a time series of relevant market data to predict the immediate future price and direction of SPY options within a $2.00 range of strike prices. We will use its percent accuracy to determine its percent contribution to an assisted Black-Scholes pricing prediction.
Accuracy Grading: The model will be compared against other traditional prediction methods and the Black-Scholes model. We will see how far the model deviates from true prices and compare this deviation to the Black-Scholes deviation to determine the percentage contribution of both methods to a final predicted price.
Why are we doing this: We are building this model in order to see if a seemingly chaotic system based on consumer sentiment can be predicted through patterns that the human eye can’t see. Seemingly chaotic systems are a major problem in physics, so if predicting options’ prices is possible maybe a similar method can be applied to noisy data from physics experiments to extract meaningful trends.
What we’ll need: The first set of inputs we need are the parameters of the Black-Scholes model. These will serve as the main block of features required to train our neural network. We will need the following:
1.	Pre-recorded data of options prices for at least five different stocks within a certain industry
a.	We will use a multitude of different strike prices and separate the datasets by their classification as either a call or a put.
b.	The data will record the price of the instruments over their entire lifetime. Thus, we would be best served by finding data recording options with long lifetimes until expiry. This may cause a problem in the future, but this is the strategy we will go with for now.
2.	Pre-recorded data of the prices of the underlying stocks themselves
3.	The risk-free interest rate across the duration of the options’ lifetimes
4.	Volatility: We will have to determine how to calculate this at a given moment
Because we are attempting to beat the Black-Scholes model and other predictors, we will attempt to gauge market sentiment in our model. We will require the following information to do this:
1.	Market capitalization of each stock: We will use this to determine the “ranking” of a company in the scope of the entire industry
2.	Earnings call schedule of each stock and the corresponding results: We will use this to determine when major events have occurred to the stock and allow the model to factor in any unexpected volatility.
3.	Federal interest rate and corresponding results: These rates and their corresponding shifts can cause market sentiments to shift greatly. We will also need the dates of major federal rate cut announcements.
Data Processing: 
1.	We will convert each price datapoint for both stocks and options into deltas (change in the stock price over a unit of time).
2.	We will interpolate the risk-free interest rate such that we have a value for each input vector.
3.	We will use the earnings call schedule to produce four features: days since last earnings call, predicted number of days until the next earnings call, was the current day an earnings call day, and what was the result of the earnings call. We will simplify the “result” feature to either positive, neutral, or negative.
4.	We will interpolate the federal interest rate to create a datapoint for each input vector.
5.	Similar to #3, we will use the Fed’s meetings schedule to produce four features: days since last meeting, predicted number of days until the next meeting, was there a meeting on the current day, and what was the result of the meeting.
6.	We will break up time into a number of features:
a.	Day of the week
b.	Relative seconds before the present
c.	During market/aftermarket
Choosing a model: In order to choose a model, we need to review the nature of our data. We need a model that can read through sequential, time-step data in order to predict a value in a number of timesteps after the present. This necessitates the use of a recurrent neural network (RNN). To avoid the vanishing/exploding gradient problem and to have a mechanism by which the model can remember long term changes in the SPY ETF and options markets, we will use a specific kind of RNN: the LSTM.

