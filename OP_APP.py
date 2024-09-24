import streamlit as st
import streamlit as st
from streamlit_msal import Msal

client_id = "bfd3bcad-c28b-43bd-a835-02bc69cdaf5c"
authority = "https://login.microsoftonline.com/cc2d437c-9657-43ce-b9b9-a84614e5f413"

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




# file = pd.read_csv('T:\OPERACOES\ARQUIVOS LOTE45\Daily Benchmark\Ajustados\RepInternoFIC_20240321.csv')
# if performanceatt:
#     with st.spinner('Rodando o Performance Atribution'):
#         perfatrib.build_pnl_books_V2()
#         file = pd.read_csv('T:\OPERACOES\ARQUIVOS LOTE45\Daily Benchmark\Ajustados\RepInternoFIC_20240321.csv')
#         st.write('Pert Att gerado!')
     
# consolidado_Classificacao = base_filtrada.pivot_table(values = 'Valor Investido',index = 'Classificação CVM1',columns = 'Data',aggfunc = 'sum')
# perfatrib.build_pnl_books_V2()

# file = pd.read_csv('T:\OPERACOES\ARQUIVOS LOTE45\Daily Benchmark\Ajustados\RepInternoFIC_20240321.csv')

# resumo = file.pivot_table(index = 'TradingDesk',values =['PL_D1_PCT','PL_MTD_PCT','PL_YTD_PCT','PL_INCEPT_PCT'],aggfunc='sum')
# resumo = resumo*100
# st.table(resumo)
# st.expander('Resumo')



# # client_id = "a8273d6e-50bf-4760-8899-a516ac2887a8"
# authority = "https://login.microsoftonline.com/cc2d437c-9657-43ce-b9b9-a84614e5f413"

# import streamlit as st
# from streamlit_msal import Msal

# with st.sidebar:
#     auth_data = Msal.initialize_ui(
#         client_id=client_id,
#         authority=authority,
#         scopes=[], # Optional
#         # Customize (Default values):
#         connecting_label="Connecting",
#         disconnected_label="Disconnected",
#         sign_in_label="Sign in",
#         sign_out_label="Sign out"
#     )

# if not auth_data:
#     st.write("Authenticate to access protected content")
#     st.stop()

# st.write("Protected content available")


# from streamlit_msal import Msal

# auth_data = Msal.initialize(
#     client_id=client_id,
#     authority=authority,
#     scopes=[],
# )

# if st.button("Sign in"):
#     Msal.sign_in() # Show popup to select account

# if st.button("Sign out"):
#     Msal.sign_out() # Clears auth_data

# if st.button("Revalidate"):
#     Msal.revalidate() # Usefull to refresh "accessToken"

# # Getting usefull information
# access_token = auth_data["accessToken"]

# account = auth_data["account"]
# name = account["name"]
# username = account["username"]
# account_id = account["localAccountId"]


# # Display information
# st.write(f"Hello {name}!")
# st.write(f"Your username is: {username}")
# st.write(f"Your account id is: {account_id}")
# st.write("Your access token is:")
# st.code(access_token)

# st.write("Auth data:")
# st.json(auth_data)