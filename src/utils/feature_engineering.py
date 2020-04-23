import pandas as pd
from sklearn.preprocessing import LabelEncoder


def label_encode_feature(dataframe, feature, encoder=None):
    if encoder is None:
        encoder = LabelEncoder()

    # encode
    dataframe[feature] = encoder.fit_transform(dataframe[feature])

    return dataframe, encoder


def onehot_encode_feature(dataframe, feature):
    # Merge one-hot encoded feature
    dataframe_feature_encoded = pd.concat(
        [dataframe, pd.get_dummies(dataframe[feature], drop_first=True)],
        axis=1
    )

    # Clean up
    dataframe_feature_encoded.drop(feature, axis=1, inplace=True)

    return dataframe_feature_encoded


def remove_outlier_customer(transaction_frame):
    with open('./data/customer_to_be_removed.txt') as f:
        to_remove = [customer.strip() for customer in f.readlines()]

    transaction_frame = transaction_frame[~transaction_frame['person'].isin(to_remove)]

    return transaction_frame


def merge_all_data(transaction_frame, portfolio, profile_gender_encoded):
    features = transaction_frame\
        .merge(portfolio, on='offer', how='left')\
        .merge(profile_gender_encoded, on='person', how='inner')

    # Clean up
    features.drop('offer', axis=1, inplace=True)

    return features


def add_median_spending(features):
    # Compute median spending
    median_spending = features.groupby('person', as_index=False)['amount'].median()
    median_spending.rename(columns={'amount': 'median_spending'}, inplace=True)

    # Merge to feature set
    features = features.merge(median_spending, on='person')

    return features
