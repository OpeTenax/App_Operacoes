import streamlit as st
import streamlit as st
from streamlit_msal import Msal

# Acessando os segredos do Streamlit
client_id = st.secrets['azure']["client_id"]
authority = st.secrets['azure']["authority"]

with st.sidebar:
    auth_data = Msal.initialize_ui(
        client_id=client_id,
        authority=authority,
        scopes=["User.Read"],  # Adicione escopos se necessário
        # Customize (Default values):
        connecting_label="Connecting",
        disconnected_label="Disconnected",
        sign_in_label="Sign in",
        sign_out_label="Sign out"
    )

if auth_data != None:
    st.sidebar.write("Você está conectado")
else:
    st.sidebar.write("Você não está conectado")
