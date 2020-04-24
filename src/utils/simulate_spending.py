import pandas as pd


def subset_features(features, feature_type):
    if feature_type == 'customer':
        selected_cols = ['person', 'age', 'income', 'M', 'O', 'median_spending']
    elif feature_type == 'offer':
        selected_cols = ['reward', 'difficulty', 'duration', 'mobile', 'social', 'web', 'discount', 'informational']
    else:
        raise ValueError('feature_type must be either customer or offer')

    # Get only the sepcified attributes
    feature_subset = features[selected_cols]

    # Drop duplicates
    feature_subset.drop_duplicates(inplace=True)

    # Reset index
    feature_subset.reset_index(drop=True, inplace=True)

    return feature_subset


def simulate_offers(profile_features, offer_features):
    # Create a dummy key to perform many-to-many join
    profile_features['m'] = 1
    offer_features['m'] = 1

    # Merge
    simulated_transactions = profile_features.merge(offer_features, on='m', how='left')

    # clean up
    simulated_transactions.drop('m', axis=1, inplace=True)

    return simulated_transactions


def rearrange_columns(simulated_transactions):
    column_order = [
        'person',
        'reward', 'difficulty', 'duration', 'mobile', 'social', 'web', 'discount', 'informational',
        'age', 'income', 'M', 'O', 'median_spending'
    ]

    simulated_transactions = simulated_transactions[column_order]

    return simulated_transactions


def get_offer_labels(offer_features, portfolio):
    offer_labels = offer_features.merge(portfolio, how='left', on=['reward', 'difficulty', 'duration'])['offer']
    offer_labels[offer_labels.isnull()] = 'no_offer'

    return offer_labels


def simulate_transactions(profile_features, offer_features):
    simulated_transactions = simulate_offers(profile_features, offer_features)
    simulated_transactions = rearrange_columns(simulated_transactions)

    return simulated_transactions


def get_spending_without_offer(simulated_transactions):
    no_offer_spending = simulated_transactions[simulated_transactions['difficulty'].isnull()][['person', 'predicted_spending']]

    return no_offer_spending


def get_max_spending(simulated_transactions):
    max_spending = simulated_transactions.groupby('person', as_index=False)['predicted_spending'].max()

    return max_spending


def compare_spendings(no_offers, max_spending):
    spending_comparison = pd.merge(
        no_offers.rename(columns={'predicted_spending': 'no_offer_spending'}),
        max_spending.rename(columns={'predicted_spending': 'optimum_offer_spending'}),
        on='person'
    )

    spending_comparison['spending_increased'] = spending_comparison['optimum_offer_spending'] - spending_comparison['no_offer_spending']

    spending_comparison['pct_change'] = (
        spending_comparison['optimum_offer_spending'] / spending_comparison['no_offer_spending'] - 1
    ) * 100


    return spending_comparison
