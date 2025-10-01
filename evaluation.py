import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score

def evaluate_irs(proposal : np.array, gt : np.array):
    """
        Params 
        Proposal (np.array) : one hot encode of predicted garancies
        Ground truth (np.array) : one hot encode of ground truth garancies
        
        Return the jacczrd similarity between proposal and gt
    """
    return jaccard_score(proposal, gt)

def retrieve_ground_truth(user_information : dict, df : pd.DataFrame, garancies_df : pd.DataFrame):
    """
        Retrieve gt from an user information.
        User information are stored as dict with the following format:
            id, anno_nascita, cod_sesso, cod_provincia_residenza, valore_personale_veicolo, num_utilizzatori, classe_assegnazione_stessa_scala, flag_automia, flag_motomia, flag_bicimia, flag_autosharing, flag_motosharing, flag_bicisharing, flag_mezzipubblici, flag_piedi, flag_partent, flag_figli, flag_cane, flag_solo, flag_altre_situazioni 
        The df contaians user informations plus the accepted preventiv id.
        The preventiv df link the preventiv to what garancies are included in that preventiv.
        It returns the vector representation of the ground truth in term of garancies offered in a preventiv.
    """

    # -- Preventiv retrieval --
    id_preventivo = df.loc[
    (df["anno_nascita"] == user_information["anno_nascita"]) &
    (df["cod_sesso"] == user_information["cod_sesso"]) &
    (df["cod_provincia_residenza"] == user_information["cod_provincia_residenza"]) &
    (df["valore_personale_veicolo"] == user_information["valore_personale_veicolo"]) &
    (df["num_utilizzatori"] == user_information["num_utilizzatori"]) &
    (df["classe_assegnazione_stessa_scala"] == user_information["classe_assegnazione_stessa_scala"]) &
    (df["flag_automia"] == user_information["flag_automia"]) &
    (df["flag_motomia"] == user_information["flag_motomia"]) &
    (df["flag_bicimia"] == user_information["flag_bicimia"]) &
    (df["flag_autosharing"] == user_information["flag_autosharing"]) &
    (df["flag_motosharing"] == user_information["flag_motosharing"]) &
    (df["flag_bicisharing"] == user_information["flag_bicisharing"]) &
    (df["flag_mezzipubblici"] == user_information["flag_mezzipubblici"]) &
    (df["flag_piedi"] == user_information["flag_piedi"]) &
    (df["flag_partner"] == user_information["flag_partner"]) &
    (df["flag_figli"] == user_information["flag_figli"]) &
    (df["flag_cane"] == user_information["flag_cane"]) &
    (df["flag_solo"] == user_information["flag_solo"]) &
    (df["flag_altre_siztuazioni"] == user_information["flag_altre_siztuazioni"]), 
    ["prev"]].values[0]
    print(id_preventivo)
    # -- Garancies retrieval --
    garancies = garancies_df.loc[
        garancies_df["id_preventivo"] == id_preventivo[0], 
        ["cod_garanzia"]
    ]
    return garancies

def one_hot_encode_garancies(garancies_df : pd.DataFrame, garancies_list : list ):
    """
        Return the one hot encode of the garancies given a garancies list
    """
   # All possible garancies
    all_garancies = sorted(garancies_df["cod_garanzia"].unique())
    
    # Initialize with zeros
    one_hot = pd.Series(0, index=all_garancies, dtype=int)
    
    # Mark the selected garancies
    for g in garancies_list:
        if g in one_hot.index:
            one_hot[g] = 1
    
    return one_hot.to_numpy()

if __name__ == "__main__":

    # --- Mock Data ---
    # Main dataframe (user info + which preventivo was accepted)
    df = pd.DataFrame({
        "id": [1, 2],
        "anno_nascita": [1990, 1985],
        "cod_sesso": ["M", "F"],
        "cod_provincia_residenza": ["MI", "RM"],
        "valore_personale_veicolo": [10000, 20000],
        "num_utilizzatori": [1, 2],
        "classe_assegnazione_stessa_scala": [3, 2],
        "flag_automia": [1, 0],
        "flag_motomia": [0, 1],
        "flag_bicimia": [0, 0],
        "flag_autosharing": [1, 0],
        "flag_motosharing": [0, 0],
        "flag_bicisharing": [0, 0],
        "flag_mezzipubblici": [1, 1],
        "flag_piedi": [0, 1],
        "flag_partner": [1, 0],
        "flag_figli": [0, 1],
        "flag_cane": [0, 0],
        "flag_solo": [1, 0],
        "flag_altre_siztuazioni": [0, 1],
        "prev": [101, 102]  # link to preventivo
    })

    # Garancies dataframe (which garancies each preventivo offers)
    garancies_df = pd.DataFrame({
        "id_preventivo": [101, 101, 102, 102],
        "cod_garanzia": ["A", "B", "B", "C"]
    })

    # --- Test Run ---
    # User input (simulate a query)
    user_info = {
        "id": 1,
        "anno_nascita": 1990,
        "cod_sesso": "M",
        "cod_provincia_residenza": "MI",
        "valore_personale_veicolo": 10000,
        "num_utilizzatori": 1,
        "classe_assegnazione_stessa_scala": 3,
        "flag_automia": 1,
        "flag_motomia": 0,
        "flag_bicimia": 0,
        "flag_autosharing": 1,
        "flag_motosharing": 0,
        "flag_bicisharing": 0,
        "flag_mezzipubblici": 1,
        "flag_piedi": 0,
        "flag_partner": 1,
        "flag_figli": 0,
        "flag_cane": 0,
        "flag_solo": 1,
        "flag_altre_siztuazioni": 0, 
    }

    # Retrieve ground truth garancies
    gt_list = retrieve_ground_truth(user_info, df, garancies_df)
    print("GT List:", gt_list["cod_garanzia"].to_numpy())

    # One-hot encode ground truth
    gt_vector = one_hot_encode_garancies(garancies_df, gt_list["cod_garanzia"].to_numpy())
    print("GT Vector:", gt_vector)

    # Create a random proposal vector
    proposal = np.array([1, 1, 0])
    print("Proposal Vector:", proposal)

    # Evaluate Jaccard similarity
    score = evaluate_irs(proposal, gt_vector)
    print("Jaccard Score:", score)