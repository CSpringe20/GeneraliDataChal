import pandas as pd
import numpy as np
import ast
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
from collections import Counter
import matplotlib.pyplot as plt

num_data = 10000  # select only the first num_data rows
k = 10            # num of dimensions to keep in svd
num_nn = 150      # num of nearest neighbours to consider
num_cov_ret = 4   # num of coverages to propose

# -------------------
# Load and preprocess
# -------------------
df = pd.read_csv("../data/merged_table.csv")
df = df.head(num_data)

drop_cols = ["id_cliente", "id_polizza", "numero_preventivo_generante",
             "id_preventivo", "numero_preventivo"]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])
df = df.dropna()

# parse cod_garanzia if it's stringified list
if isinstance(df["cod_garanzia"].iloc[0], str):
    df["cod_garanzia"] = df["cod_garanzia"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

# encode categorical features
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
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

svd = TruncatedSVD(n_components=k, random_state=42)
X_train_emb = svd.fit_transform(X_train_scaled)

nn_model = NearestNeighbors(metric="cosine")
nn_model.fit(X_train_emb)

# -------------------
# Recommendation function
# -------------------
def recommend_coverages(new_customer_df, nn_neighbors=5, num_cov_ret=5):
    """
    Given a new customer (1-row DataFrame),
    return the top cod_garanzia recommendations 
    based on the first nn_neighbors nearest neighbors.
    """
    new_scaled = scaler.transform(new_customer_df)
    new_emb = svd.transform(new_scaled)

    _, indices = nn_model.kneighbors(new_emb, n_neighbors=nn_neighbors)

    coverages = []
    for idx in indices[0]:
        coverages.extend(y_train.iloc[idx])

    counter = Counter(coverages)  # count frequency
    recommended = [cov for cov, _ in counter.most_common(num_cov_ret)]

    return recommended

# -------------------------------
# Test model with Jaccard's coeff
# -------------------------------
def jaccard_similarity(list1, list2):
    set1, set2 = set(list1), set(list2)
    if not set1 and not set2:
        return 1.0
    return len(set1 & set2) / len(set1 | set2)


def evaluate_recommender(X_test, y_test, num_nn=5, num_cov_ret=5):
    scores = []
    for i in range(len(X_test)):
        x = X_test.iloc[[i]]  # keep DataFrame format
        y_true = y_test.iloc[i]
        y_pred = recommend_coverages(x, nn_neighbors=num_nn, num_cov_ret=num_cov_ret)
        scores.append(jaccard_similarity(y_true, y_pred))
    return np.mean(scores)

import matplotlib.pyplot as plt

def plot_svd_components(X_emb, y=None, title="SVD 2D Projection"):
    """
    Plot the first two components of the SVD embedding.

    Parameters:
        X_emb : ndarray, shape (n_samples, n_components)
            The SVD-transformed features.
        y : list/Series/ndarray (optional)
            Labels to color points.
        title : str
            Title of the plot.
    """
    plt.figure(figsize=(8,6))
    if y is not None:
        plt.scatter(X_emb[:,0], X_emb[:,1], c=y, cmap="viridis", s=10, alpha=0.7)
    else:
        plt.scatter(X_emb[:,0], X_emb[:,1], s=10, alpha=0.7)
    
    plt.xlabel("SVD Component 1")
    plt.ylabel("SVD Component 2")
    plt.title(title)
    plt.savefig("svd_plot.png", dpi=300, bbox_inches="tight")
    plt.show()



if __name__=="__main__":
    mean_jaccard = evaluate_recommender(X_test, y_test, num_nn=num_nn, num_cov_ret=num_cov_ret)
    print(f"Mean Jaccard similarity on test set: {mean_jaccard:.4f}")
    plot_svd_components(X_train_emb, title="Train set SVD projection")
