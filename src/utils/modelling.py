import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error as mae

plt.style.use('ggplot')


def get_features_labels(data):
    features = data.drop('amount', axis=1)
    labels = data['amount']

    return features, labels


def split_data(features, labels, test_size=0.3):
    features_train, features_test, labels_train, labels_test = train_test_split(
        features, labels,
        test_size=test_size,
        random_state=69
    )

    return features_train, features_test, labels_train, labels_test


def get_lgb_data(features_train, features_test, labels_train, labels_test):
    lgb_train = lgb.Dataset(features_train, labels_train)
    lgb_test = lgb.Dataset(features_test, labels_test, reference=lgb_train)

    return lgb_train, lgb_test


def evaluate_set(reg, features, labels):
    pred = reg.predict(features)

    error = mae(labels, pred)

    return error


def prepare_data(data):
    # Get features and labels
    features, labels = get_features_labels(data)

    # Split data
    features_train, features_test, labels_train, labels_test = split_data(features, labels)

    return features_train, features_test, labels_train, labels_test


def plot_importance(reg):
    for importance_type in ('gain', 'split'):
        fig, ax = plt.subplots(figsize=(15,7))
        lgb.plot_importance(reg, importance_type='gain', ax=ax)
        plt.tight_layout()
        plt.show()

def plot_coefficient(lr, feature_list):
    coef = pd.Series(lr.coef_)
    coef.index = feature_list

    plt.figure(figsize=(15,7))
    coef.plot(kind='bar')
    plt.show()
