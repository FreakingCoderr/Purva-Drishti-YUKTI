import joblib
import pandas as pd

with open('annapurna_model (1).pkl', 'rb') as file:
    model=joblib.load(file)

if hasattr(model, 'n_features_in_'):
    print(f"ERROR CAUSE: Model expects {model.n_features_in_} inputs, but you gave only 1.")

if hasattr(model, 'feature_names_in_'):
    print(f"REQUIRED FEATURES: {list(model.feature_names_in_)}")

else:
    print("NO NAMES FOUND: It needs raw numbers in a specific order.")
