import pandas as pd
from sklearn.model_selection import train_test_split
import os

# 1. Setup paths
INPUT_FILE = 'data/dd_masterfile.csv'
TRAIN_OUTPUT = 'data/train_dataset.csv'
BLIND_OUTPUT = 'data/blind_test.csv'

# 2. Load the Masterfile
df = pd.read_csv(INPUT_FILE)
print(f"🧬 Loaded {len(df)} compounds from {INPUT_FILE}")

# 3. The Split
train_df, blind_df = train_test_split(df, test_size=0.10, random_state=42)

# 4. Save
train_df.to_csv(TRAIN_OUTPUT, index=False)
blind_df.to_csv(BLIND_OUTPUT, index=False)

print(f"Splitting Complete:")
print(f"Training/Validation Pool: {len(train_df)} rows (Saved to {TRAIN_OUTPUT})")
print(f"Blind Test Vault:         {len(blind_df)} rows (Saved to {BLIND_OUTPUT})")
