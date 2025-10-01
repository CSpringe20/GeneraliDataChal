import time

import pandas as pd
import streamlit as st
from engine import engine
import random

st.set_page_config(page_title="Generali Data Challenge", layout="wide")

# ---- HEADER ----

# center the title
st.markdown("<h1 style='text-align: center;'>🦁 Generali Data Challenge 🦁</h1>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("## New Insurance Application")
st.markdown("Please fill in the form below with your personal information, or insert a CSV file.")

result = ""

# ---- FORM ----
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

            valore_personale_veicolo = st.number_input("Valore Personale Veicolo", min_value=1, max_value=3, placeholder=1)
            num_utilizzatori = st.number_input("Numero Utilizzatori", min_value=1, max_value=10, placeholder=1)
            classe_assegnazione_stessa_scala = st.number_input("Classe Assegnazione Stessa Scala", min_value=1, max_value=18, placeholder=1)
            flag_autonomia = st.selectbox("Sei il proprietario dell'auto?", options=['Si', 'No'], index=1)
            flag_motomia = st.selectbox("Sei un motociclista?", options=['Si', 'No'], index=1)
            flag_bicimia = st.selectbox("Sei un ciclista?", options=['Si', 'No'], index=1)
            flag_autosharing = st.selectbox("Usi servizi di car sharing?", options=['Si', 'No'], index=1)
            flag_motosharing = st.selectbox("Usi servizi di moto sharing?", options=['Si', 'No'], index=1)
            flag_bikesharing = st.selectbox("Usi servizi di bike sharing?", options=['Si', 'No'], index=1)
            flag_mezzipubblici = st.selectbox("Usi mezzi pubblici?", options=['Si', 'No'], index=1)
            flag_piedi = st.selectbox("Ti sposti a piedi?", options=['Si', 'No'], index=1)
            flag_partner = st.selectbox("Hai un partner?", options=['Si', 'No'], index=1)
            flag_figli = st.selectbox("Hai figli?", options=['Si', 'No'], index=1)
            flag_cane = st.selectbox("Hai un cane?", options=['Si', 'No'], index=1)
            flag_solo = st.selectbox("Vivi da solo?", options=['Si', 'No'], index=1)
            flag_altre_situazioni = st.selectbox("Hai altre situazioni abitative?", options=['Si', 'No'], index=1)

            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                if not name or not surname or not anno_nascita or not email or not phone or not address:
                    st.warning("Please fill in the form or upload a CSV file.")
                else:
                    st.success("Form submitted successfully!")
                    df = pd.DataFrame([anno_nascita, cod_sesso, valore_personale_veicolo, num_utilizzatori,classe_assegnazione_stessa_scala, flag_autonomia, flag_motomia, flag_bicimia, flag_autosharing, flag_motosharing, flag_bikesharing, flag_mezzipubblici, flag_piedi, flag_partner, flag_figli, flag_cane, flag_solo, flag_altre_situazioni])
                    result = engine(df)

# --- RESULTS ----
if result is not "":
    batch_result = ['001','171','G07', 'G09', '172', '057', '065', '067']
    result = random.sample(batch_result, 3)

    st.markdown("## Results")
    st.markdown("Based on the information provided, here are your insurance quotes:")

    # introduce some sleep time to simulate processing
    time.sleep(1)

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
