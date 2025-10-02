import pandas as pd
import streamlit as st
from engine import recommend_coverages as engine


st.set_page_config(page_title="Generali Data Challenge", layout="wide")

# ---- HEADER ----
st.markdown("<h1 style='text-align: center;'>🦁 Generali Data Challenge 🦁</h1>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("## New Insurance Application")
st.markdown("Please fill in the form below with your personal information, or insert a CSV file.")


# ---- FORM ----
result = ""

with st.expander("➕ Insert your data", expanded=False):
    with st.form("my_form"):

        data_file = st.file_uploader("Upload a CSV with required data", type=["csv"])

        st.markdown('---')

        if data_file:
            submit_button_via_file = st.form_submit_button(label="Submit via CSV")

            if submit_button_via_file:
                try:
                    df = pd.read_csv(data_file)
                    result = engine(df)
                except Exception as e:
                    st.error(f"Error reading CSV file: {e}")

        else:
            st.markdown("#### Personal Info")
            name = st.text_input("Name", max_chars=50, placeholder="Mario")
            surname = st.text_input("Surname", max_chars=50, placeholder="Rossi")
            anno_nascita = st.number_input("Year of Birth", min_value=1900, max_value=2024, placeholder=1990)
            email = st.text_input("Email", max_chars=100, placeholder="example@example.com")
            phone = st.text_input("Phone Number", max_chars=15, placeholder="+39 1234567890")
            address = st.text_input("Address", max_chars=100, placeholder="Via Roma 1")
            cod_provincia_residenza = st.text_input("Provincia di Residenza", max_chars=50, placeholder="RM")
            cod_sesso = st.selectbox("Codice Sesso", options=['Maschio', 'Femmina'], index=0)
            anni_assicurati = st.number_input("Anni Assicurati", min_value=0, max_value=30, placeholder=0)
            anni_assicurati_continuativi = st.number_input("Anni Assicurati Continuativi", min_value=0, max_value=30, placeholder=anni_assicurati)

            valore_personale_veicolo = st.number_input("Valore Personale Veicolo", min_value=1, max_value=3, placeholder=1)
            num_utilizzatori = st.number_input("Numero Utilizzatori", min_value=1, max_value=10, placeholder=1)
            classe_assegnazione_stessa_scala = st.number_input("Classe Assegnazione Stessa Scala", min_value=1, max_value=18, placeholder=1)
            flag_automia = st.selectbox("Sei il proprietario dell'auto?", options=['Si', 'No'], index=1)
            flag_motomia = st.selectbox("Sei un motociclista?", options=['Si', 'No'], index=1)
            flag_bicimia = st.selectbox("Sei un ciclista?", options=['Si', 'No'], index=1)
            flag_autosharing = st.selectbox("Usi servizi di car sharing?", options=['Si', 'No'], index=1)
            flag_motosharing = st.selectbox("Usi servizi di moto sharing?", options=['Si', 'No'], index=1)
            flag_bicisharing = st.selectbox("Usi servizi di bike sharing?", options=['Si', 'No'], index=1)
            flag_mezzipubblici = st.selectbox("Usi mezzi pubblici?", options=['Si', 'No'], index=1)
            flag_piedi = st.selectbox("Ti sposti a piedi?", options=['Si', 'No'], index=1)
            flag_partner = st.selectbox("Hai un partner?", options=['Si', 'No'], index=1)
            flag_figli = st.selectbox("Hai figli?", options=['Si', 'No'], index=1)
            flag_cane = st.selectbox("Hai un cane?", options=['Si', 'No'], index=1)
            flag_solo = st.selectbox("Vivi da solo?", options=['Si', 'No'], index=1)
            flag_altre_situazioni = st.selectbox("Hai altre situazioni abitative?", options=['Si', 'No'], index=1)

            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                # Validazione minima
                if not name or not surname:
                    st.warning("Please fill in at least name and surname.")
                else:
                    # Normalizza cod_sesso da UI (Maschio / Femmina → lowercase)
                    cod_sesso_raw = cod_sesso  # ad esempio proviene da selectbox ["Maschio","Femmina"]
                    cod_sesso_norm = cod_sesso_raw.strip().lower()  # “Maschio” -> “maschio”, “Femmina” -> “femmina”

                    # Costruisci la riga con tutte le colonne attese
                    new_row = {
                        "anno_nascita": int(anno_nascita),
                        "cod_sesso": cod_sesso_norm,
                        "cod_provincia_residenza": cod_provincia_residenza.strip(),  # potrebbe voler normalizzare anche gli spazi
                        "num_utilizzatori": int(num_utilizzatori),
                        "classe_assegnazione_stessa_scala": int(classe_assegnazione_stessa_scala),
                        "valore_personale_veicolo": int(valore_personale_veicolo),
                        "anni_assicurati": int(anni_assicurati),
                        "anni_assicurati_continuativi": int(anni_assicurati_continuativi),


                        # Tutte le flag come “Si” / “No” normali
                        # convert yes/no into 1/0
                        "flag_automia": flag_automia.strip().lower(),
                        "flag_automia": flag_automia.strip().lower(),
                        "flag_motomia": flag_motomia.strip().lower(),
                        "flag_bicimia": flag_bicimia.strip().lower(),
                        "flag_autosharing": flag_autosharing.strip().lower(),
                        "flag_motosharing": flag_motosharing.strip().lower(),
                        "flag_bicisharing": flag_bicisharing.strip().lower(),
                        "flag_mezzipubblici": flag_mezzipubblici.strip().lower(),
                        "flag_piedi": flag_piedi.strip().lower(),
                        "flag_partner": flag_partner.strip().lower(),
                        "flag_figli": flag_figli.strip().lower(),
                        "flag_cane": flag_cane.strip().lower(),
                        "flag_solo": flag_solo.strip().lower(),
                        "flag_altre_situazioni": flag_altre_situazioni.strip().lower()
                    }

                    # Crea un DataFrame con una sola riga
                    df_new = pd.DataFrame([new_row])

                    # Chiama la tua funzione engine / recommend_coverages
                    try:
                        result = engine(df_new)
                    except Exception as e:
                        st.error(f"Error in engine: {e}")

# --- RESULTS ----
if result != "":
    st.markdown("## Results")
    st.markdown("Based on the information provided, here are your insurance quotes:")

    for i in range(len(result)):
        # empty space
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='
            padding: 20px;
            width: 250px;
            height: 80px;
            border-radius: 15px;
            background: linear-gradient(135deg, #ffffff, #e6e6e6);
            border: 1.5px solid #cccccc;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: "Arial", sans-serif;
            font-size: 18px;
            font-weight: 600;
            color: #000000;
            text-align: center;
            margin-top: 10px;
        '>
            {result[i]}
        </div>
        """, unsafe_allow_html=True)
