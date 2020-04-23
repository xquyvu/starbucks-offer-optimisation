# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Parsing transcript data
# 
# This notebook matches the transactions with the offers if there were any when the transaction was made.

# %%
import pandas as pd
import numpy as np
from src.utils.parse_transcript import parse_transcript, get_transaction_dataframe


# %%
# Load data
portfolio = pd.read_csv('./data/final/portfolio.csv')
transcript = pd.read_csv('./data/final/transcript.csv')

# %% [markdown]
# ## Portfolio data

# %%
# Create a dictionary to store portfolio validity
portfolio_validity = {
    offer: duration
    for offer, duration
    in portfolio[['offer', 'duration']].values
}

portfolio_validity

# %% [markdown]
# ## Transcript data

# %%
transcript.head(10)


# %%
# Match offers and transactions
transaction_list = parse_transcript(transcript, portfolio_validity)
transaction_df = get_transaction_dataframe(transaction_list)

transaction_df.head(10)


# %%
transaction_df.to_csv('./data/final/transaction_frame.csv', index=False)

