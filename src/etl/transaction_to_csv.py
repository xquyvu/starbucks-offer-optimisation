import json
import pandas as pd


# Transcript
with open('./data/raw/transcript.json') as f:
    transaction_list = f.read().splitlines()

def transaction_line_to_dict(line):
    # Try to parse line to json
    try:
        transaction = json.loads(line)
        return transaction
    except json.JSONDecodeError:
        pass


def get_transaction_details(transaction):
    # Initialise placeholder for transaction details
    transaction_details = {key: None for key in ('amount', 'offer id', 'offer_id', 'reward')}

    # Get details
    transaction_details.update(transaction)
    transaction_details.update(transaction['value'])

    # Remove value key as details are already parsed
    del transaction_details['value']

    return transaction_details

transaction_list = [transaction for transaction in transaction_list if transaction]
transaction_dicts = [transaction_line_to_dict(line) for line in transaction_list]

all_keys = [list(transaction['value']) for transaction in transaction_dicts]
all_keys = set([item for sublist in all_keys for item in sublist])

all_transactions = [
    get_transaction_details(transaction)
    for transaction
    in transaction_dicts
]

transaction_frame = pd.DataFrame(all_transactions)
transaction_frame['offer_id'] = transaction_frame['offer_id'].where(
    transaction_frame['offer id'].isnull(),
    transaction_frame['offer id']
)

transaction_frame.drop(['offer id'], axis=1, inplace=True)

transaction_frame.to_csv('./data/processed/transcript.csv', index=False)
