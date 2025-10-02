import pandas as pd

clienti     = pd.read_csv("~/Desktop/data challenge/data challenge/cliente.csv")
preventivi_  = pd.read_csv("~/Desktop/data challenge/data challenge/preventivi.csv")
garanzie    = pd.read_csv("~/Desktop/data challenge/data challenge/garanzie.csv")
polizze     = pd.read_csv("~/Desktop/data challenge/data challenge/polizze.csv")

polizze = polizze.drop("data_decorrenza", axis=1)

clienti_to_drop = [
    "cap_residenza", "comune_residenza", "flg_persona_giuridica", "flg_figli_conviv"
]

clienti = clienti.drop(columns=clienti_to_drop)

preventivi = preventivi_[preventivi_["flag_convertito_contratto"]==1] # select only bought policies

preventivi_to_drop = [
    "flag_convertito_contratto", "num_versione", "canale", "premio_anno_precedente",
    "potenza_kw", "cod_tipo_alimentazione", "importo_valore_commerciale",
    "classe_provenienza_stessa_scala", "premio", "num_sinistri_ultimi_2_anni",
    "num_sinistri_primi_3_anni", "numero_pdp", "percorrenza_annua", "data_acquisto",
    "cod_marca", "desc_marca", "cod_modello", "desc_modello", "cod_provincia_circolazione"
]

preventivi = preventivi.drop(columns=preventivi_to_drop)

df = polizze.merge(clienti, how="left", left_on="id_cliente", right_on="id_cliente")
df = df.merge(preventivi, how="left", left_on="numero_preventivo_generante", right_on="numero_preventivo")


garanzie_list = (
    garanzie.groupby("id_preventivo")["cod_garanzia"]
    .apply(list)        # turn into Python list
    .reset_index()
)

# Step 2: merge back to df
df = df.merge(garanzie_list, how="left", on="id_preventivo")

df.to_csv("merged_table.csv", index=False)
