# Starbucks offer optimisation

Optimise target customers for offers based on transaction, demographic and offer data

## 1. Background

Starbucks is a coffee company and coffeehouse chain that serves hot and cold drinks, various kinds of coffee and tea. Once every few days, Starbucks sends out an offer to users of their mobile app as a way to stimulate customer spending. Starbucks is looking to optimise their offering strategy so that the right offer is sent to the right customer.

## 2. Problem statement

With millions of customers and various types of offers, it is impossible to allocate personel to manually decide the offering for each customer. Therefore, it is necessary to build an automated decision process that allocate the right offer to the right customer.

"The right offer" must satisfies the following criteria:

- **Influence**: The offer needs to actually influence customer behavior. For example, if the buy 1 get 1 offer was sent to someone who would buy 2 drinks anyway, then that offer is not "the right offer".
- **Efficiency**: The offer needs to be used and completed by the user. If not, sending out the offer would be meaningless.

Therefore, it is also important to assess what a certain demographic group will buy when not receiving any offers.

The above will serve as the objectives for this project.

## 3. Dataset

Starbucks has provided a dataset that contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be an advertisement for a drink or an actual offer. Some users might not receive any offer during certain weeks.

The data is contained in three files:

- `portfolio.json` - containing offer ids and meta data about each offer (duration, type, etc.)
  - id (string) - offer id
  - offer_type (string) - type of offer ie BOGO, discount, informational
  - difficulty (int) - minimum required spend to complete an offer
  - reward (int) - reward given for completing an offer
  - duration (int) - time for offer to be open, in days
  - channels (list of strings)

- `profile.json` - demographic data for each customer
  - age (int) - age of the customer
  - became_member_on (int) - date when customer created an app account
  - gender (str) - gender of the customer (note some entries contain 'O' for other rather than M or F)
  - id (str) - customer id
  - income (float) - customer's income

- `transcript.json` - records for transactions, offers received, offers viewed, and offers completed. This shows user purchases made on the app including the timestamp of purchase and the amount of money spent on a purchase. This transactional data also has a record for each offer that a user receives as well as a record for when a user actually views the offer. There are also records for when a user completes an offer.
  - event (str) - record description (ie transaction, offer received, offer viewed, etc.)
  - person (str) - customer id
  - time (int) - time in hours since start of test. The data begins at time t=0
  - value - (dict of strings) - either an offer id or transaction amount depending on the record

## 4. Solution statement

The proposed solution has 3 parts:

- Predict how customer would spend without the influence of offer, based on their profiles (age, gender, income, time, etc.)
- Predict how customer would spend with the influence of offer, based on their profiles (age, gender, income, time, etc.)
- Create a policty to choose the offer that maximises customer spending

## 5. Benchmark model

### 5.1. For predicting spending

- Linear regression: Predict spending from customer and offer data without feature engineering
- Simple average model: Takes the average customer spending as the prediction for each group (with offer / without offer)

### 5.2. For optimising offer sending

- Random offer choice: Assign offers randomly to customer, or
- Sending out no offer at all.

## 6. Evaluation metrics

### 6.1. For predicting spending

For this task, RMSE was selected, which is a standard metric for regression tasks. However, this is not the direct metric we would like to optimise because the goal is to maximise spending increased by offer. Therefore, this will only be used to assess goodness of fit for spending prediction models.

### 6.2. For optimising offer sending

Businesses may seek to optimise for maximum income (i.e. customer spending) or profit. Therefore, the 2 following metrics were selected:

- **Spending increased** by allocating an offer to customer (in USD)
- **Profit** which is defined as:

$$profit = spending\_increased - cost\_of\_offer$$

where

$$cost\_of\_offer \approx difficulty * factor$$

## 7. Project design

The initial proposed workflow is as follow:

- Data transformation: Transform data from json to table format to facilitate later analysis
- Exploratory data analysis: Apply statistical/visualisation method to obtain further understanding of customer profiles and transactions. This section will seek to answer the following questions:
  - How can we describe the offers?
  - What is the distribution of customer characteristics and transactions? (e.g. most of the customers are from 20-30 year-old)
  - How are customers reacting to the offers?
  - What features can we engineer to predict customer spending?
  - What data cleaning steps would be necessary?
- Perform data cleaning as informed by the exploratory data analysis step
- Feature engineering
- Setup benchmark model
- Create machine learning model to predict customer spending
- Used the above model to predict how customer would react to each type of offer
- Create a decision rule to allocate offers to customers that maximise increased spending
- Evaluate and compare results obtained from benchmark models and machine learning model
- Critical reflection and assessment of the solution's impact
