# Starbucks offer optimisation

Optimise target customers for offers based on transaction, demographic and offer data

## 1. Background

Starbucks is a coffee company and coffeehouse chain that serves hot and cold drinks, various kinds of coffee and tea. Once every few days, Starbucks sends out an offer to users of their mobile app as a way to stimulate customer spending. Starbucks is looking to optimise their offering strategy so that the right offer is sent to the right customer.

## 2. Problem statement

With millions of customers and various types of offers, it is impossible to allocate personel to manually decide the offering for each customer. Each person in the simulation has some hidden traits that influence their purchasing patterns and are associated with their observable traits. People produce various events, including receiving offers, opening offers, and making purchases. Therefore, it is necessary to build an automated decision process that allocate the right offer to the right customer.

"The right offer" must satisfies the following criteria:

- **Influence**: The offer needs to actually influence customer behavior. For example, if the buy 1 get 1 offer was sent to someone who would buy 2 drinks anyway, then that offer is not "the right offer". This also means the offer needs to stimulate customer spending, i.e increase their spending.
- **Efficiency**: The offer needs to be used and completed by the user. If not, sending out the offer would be meaningless.

Therefore, it is also important to assess what a certain demographic group will buy when not receiving any offers.

The above will serve as the objectives for this project.

## 3. Dataset

Starbucks has provided a dataset that contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be an advertisement for a drink or an actual offer. Some users might not receive any offer during certain weeks.

The data is contained in three files:

- `portfolio.json` - containing offer ids and meta data about 10 available offers (duration, type, etc.) sent during 30-day test period
  - id (string) - offer id
  - offer_type (string) - type of offer ie BOGO, discount, informational. In details:
    - Buy-one-get-one (BOGO): A user needs to spend a certain amount to get a reward equal to that threshold amount.
    - Discount: A user gains a reward equal to a fraction of the amount spent
    - Informational: There is no reward, but neither is there a requisite amount that the user is expected to spend.
  - difficulty (int) - minimum required spend to complete an offer
  - reward (int) - reward (in USD) given for completing an offer
  - duration (int) - time for offer to be open, in days
  - channels (list of strings) web, email, mobile, social

- `profile.json` - demographic data for each customer, aging from 18 to 118, with approximately 15,000 customers, in which 6000 females, 8000 males, and 200 other, income ranging from 30,000 USD per annum to 120,000 USD per annum.
  - age (int) - age of the customer, missing value encoded as 118
  - became_member_on (int) - date when customer created an app account, format YYYYMMDD
  - gender (str) - gender of the customer (M, F, O, or null)
  - id (str) - customer id
  - income (float) - customer's income

- `transcript.json` - records for approximately 300,000 events such as offers received, offers viewed, and offers completed. This shows user purchases made on the app including the timestamp of purchase and the amount of money spent on a purchase. This transactional data also has a record for each offer that a user receives as well as a record for when a user actually views the offer. There are also records for when a user completes an offer. It's also important to know that a user can receive an offer, never actually view the offer, and still complete the offer. For example, a user might receive the "buy 10 dollars get 2 dollars off offer", but the user never opens the offer during the 10 day validity period. The customer spends 15 dollars during those ten days. There will be an offer completion record in the data set; however, the customer was not influenced by the offer because the customer never viewed the offer.
  - event (str) - record description (ie transaction, offer received, offer viewed, etc.)
  - person (str) - customer id
  - time (int) - time in hours since start of test. The data begins at time t=0
  - value - (dict of strings) - either an offer id or transaction amount depending on the record

## 4. Solution statement

The proposed solution has 2 parts, outlined as follows:

This is the section that needs to be elaborated way more: please be specific about the tools you would like to use to solve this problem: algorithms, models, deployment, etc.

### 4.1. Predict customer spending

This part aims to predict how customer would spend with and without the influence of offer, based on their profiles (age, gender, income, time, etc.)

In this part, information on offer, customer profile and historical spending are combined into 1 data table with the following information:

| Source          | Information | Note                                                                                  |
| --------------- | ----------- | ------------------------------------------------------------------------------------- |
| portfolio.json  | Offer type  | Label encoded or one-hot encoded                                                      |
| portfolio.json  | channels    | Label encoded or one-hot encoded                                                      |
| profile.json    | age         | Might need to be binned depending on model type                                       |
| profile.json    | income      | Might need to be binned depending on model type                                       |
| profile.json    | id          | Might be included/removed depending on data availability                              |
| transcript.json | Spending    | Spending during the period when the offer is valid, which is also the target variable |

Then, relevant features will be engineered, depending on the findings from the exploratory data analysis part.

Data is then split into training and validation set, with 80% of customers in the training set and 20% in the validation set. This is to mimic the situation where we need to predict on new customers.

A machine learning algorithm is then chosen to learn to predict customer spending given an offer.

### 4.2. Create offer policy to maximise customer spending

Since the above step generate a simulation of customer spending if given each offer, the decision rule will simply choose the offer that maximise the increased spending.

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

- **Spending increased** by allocating an offer to customer (in USD).

```python
spending_increased = spending_with_offer - spending_without_offer
```

- **Income efficiency** which is the increased income in relative to the difficulty of the offer.

```python
income_efficiency = spending_increased/difficulty
```

In which:

- `spending_with_offer`, `spending_without_offer` is the amount that a customer would spend if they receive or did not receive an offer. This is provided in the `transcript.json`.
- `difficulty`: An attribute of the offer, provided in the `portfolio.json`.

## 7. Project design

The workflow is as follow:

- Data transformation: Transform data from json to table format to facilitate later analysis
  - `portfolio` and `profile` datasets: [Script](src/etl/portfolio_and_profile_to_csv.py)
  - `transaction` dataset: [Notebook](src/etl/transaction_to_csv.ipynb)
- Exploratory data analysis ("EDA"): Apply statistical/visualisation method to obtain further understanding of customer profiles and transactions
  - `profile` dataset: [Notebook](src/eda/analyse_profiles.ipynb)
  - `portfolio` dataset: [Notebook](src/eda/analyse_portfolio.ipynb)
  - Customer spending: [Notebook](src/eda/analyse_spendings.ipynb)
- Perform data ETL and data cleaning as informed by the EDA step:
  - Parsing transcript data: [Notebook](src/etl/parse_transcript.ipynb)
  - Numerically encoded portfolio data: [Notebook](src/etl/process_portfolio.ipynb)
- Feature engineering, informed by the EDA step: [Notebook](src/features/feature_engineering.ipynb)
- Setup benchmark model
- Create machine learning model to predict customer spending. The choice of algorithm will be informed by the exploratory analysis phase. Tentative candidates are `LightGBM` and `LinearRegressor`.
- Use the above trained model to simulate how customer would react to each type of offer
- Create a decision rule to allocate offers to customers that maximise increased spending. Since the above step generate a simulation of customer spending if given each offer, the decision rule will choose the offer that maximise the increased spending.
- Evaluate and compare results obtained from benchmark models and machine learning model according to the metrics defined in [Section 6](#6-evaluation-metrics).
- Critical reflection and assessment of the solution's business impact
