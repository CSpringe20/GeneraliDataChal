import pandas as pd
import numpy as np
import ast
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors

# -------------------
# Load and preprocess
# -------------------
df = pd.read_csv("merged_table.csv")

drop_cols = ["id_cliente", "id_polizza", "numero_preventivo_generante",
             "id_preventivo", "numero_preventivo"]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])
df = df.dropna()
df = df.head(10000)

if isinstance(df["cod_garanzia"].iloc[0], str):
    df["cod_garanzia"] = df["cod_garanzia"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

if "cod_sesso" in df.columns:
    df["cod_sesso"] = df["cod_sesso"].astype("category").cat.codes

if "cod_provincia_residenza" in df.columns:
    df["cod_provincia_residenza"] = df["cod_provincia_residenza"].astype("category").cat.codes

# -------------------
# Train / test split
# -------------------
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

X_train = train_df.drop(columns=["cod_garanzia"])
y_train = train_df["cod_garanzia"]

X_test = test_df.drop(columns=["cod_garanzia"])
y_test = test_df["cod_garanzia"]

# -------------------
# Train once
# -------------------
k = 10
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

svd = TruncatedSVD(n_components=k, random_state=42)
X_train_emb = svd.fit_transform(X_train_scaled)

nn = NearestNeighbors(n_neighbors=1, metric="cosine")
nn.fit(X_train_emb)

# -------------------
# Recommendation function
# -------------------
def recommend_coverages(new_customer_df):
    """
    Given a new customer (1-row DataFrame),
    return the cod_garanzia list of nearest neighbor.
    Uses pre-trained scaler, svd, nn, and y_train.
    """
    new_scaled = scaler.transform(new_customer_df)
    new_emb = svd.transform(new_scaled)
    _, indices = nn.kneighbors(new_emb)
    nearest_idx = indices[0][0]
    return y_train.iloc[nearest_idx]