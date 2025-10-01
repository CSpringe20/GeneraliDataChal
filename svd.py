from sklearn.decomposition import TruncatedSVD
import numpy as np

def perform_svd(matrix, n_components=100):
    """
    Applies Truncated SVD to reduce dimensionality of a term-document matrix.

    Parameters:
    - matrix : The term-document matrix (most likely scipy sparse)
    - n_components (int) : Number of latent semantic dimensions

    Returns:
    - reduced_matrix (np.ndarray): Matrix in reduced latent semantic space
    - svd_model (TruncatedSVD): Fitted SVD model
    """
    svd = TruncatedSVD(n_components=n_components, random_state=24)
    reduced_matrix = svd.fit_transform(matrix)
    return reduced_matrix, svd
