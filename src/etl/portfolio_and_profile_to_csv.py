import pandas as pd


# Portfolio and profile
def json_to_csv(from_path, to_path):
    pd.read_json(from_path, orient='records', lines=True).to_csv(to_path, index=False)

ARGS = zip(
    (
        './data/raw/portfolio.json',
        './data/raw/profile.json'
    ),
    (
        './data/processed/portfolio.csv',
        './data/processed/profile.csv'
    )
)

for from_path, to_path in ARGS:
    json_to_csv(from_path, to_path)

print('Done')
