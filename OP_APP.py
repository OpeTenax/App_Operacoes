import streamlit as st
from streamlit_msal import Msal
from azure.storage.blob import BlobServiceClient
import pandas as pd
import numpy as np
import datetime as datetime
from io import StringIO

# Acessando os segredos do Streamlit
client_id = st.secrets['azure']["client_id"]
authority = st.secrets['azure']["authority"]
connection_string = st.secrets['azure']["connection_string"]
container_name = st.secrets['azure']['container_name']


acoes = ['Tenax Acoes A FIC FIA','Tenax Acoes Alocadores FIC FIA','Tenax Acoes FIC FIA','Tenax Acoes Institucional A FIC FIA','Tenax Acoes Master FIA','Tenax Acoes Master Institucional FIA','TX A Acoes FIA','Tenax Equity Hedge FIM']
macro = ['Tenax Macro A FIC FIM','Tenax Macro Alocadores FIC FIM','Tenax Macro FIC FIM','Tenax Macro Master FIM']
total_return = ['Tenax Total Return A FIC FIM','Tenax Total Return Alocadores FIC FIM','Tenax Total Return FIC FIM','Tenax Total Return Master FIM','Tenax Total Return Prev FIE','Tenax Total Return Prev Master FIFE','Tenax TR FIC FIA','Tenax TR Master FIA']
renda_fixa = ['Geri Tenax FI RF','Synta Tenax FI RF','Tenax Renda Fixa LP']
credito_privado = ['Tenax RFA Incentivado FIF CIC','Tenax RFA Incentivado Master FIF','Tenax RFA Prev Master FIFE']

de_para_corretoras = {85:'BTG',
                        3:'XP',
                        114:'ITAU',
                        39:'BRADESCO',
                        107:'TERRA',
                        127:'TULLET',
                        122:'LIQUIDEZ',
                        1982:'MODAL',
                        23:'NECTON',
                        8:'UBS',
                        92:'RENASCENCA',
                        45:'CREDIT SUISSE',
                        16:'JP MORGAN',
                        6003:'C6',
                        120:'GENIAL',
                        27:'SANTANDER',
                        77:'CITIBANK',
                        13:'BOFA',
                        238:'GOLDMAN',
                        1099:'INTER',
                        1130:'STONEX',
                        40:'MORGAN STANLEY',
                        59:'SAFRA'}

CLASSE_PRODUTOS_BOVESPA = ['BDR Options','BDR Unsponsored','Equity','Equity Options','Equity Receipts','Equity Subscription','ETF BR','ETF BR ISHARES OFF','ETF BR Receipts','ETF Options','IBOV Options']
CLASSE_PRODUTOS_BMF = ['AUDUSD Futures - BMF','CPM Options - BMF','DAP Future','DI1Future','DIF','DII','DR1','EURUSD Futures - BMF','GBPUSD Futures - BMF','IBOVSPFuture','IDIOptionCall','IDIOptionPut','IR1','S&P500 Future Options - BMF','S&P500 Futures - BMF','US T-Note 10 BMF','USDBRLFuture','USDBRLOptionCall','USDBRLOptionPut','USDCAD Futures - BMF','USDCLP Futures - BMF','USDCNH Futures - BMF','USDJPY Futures - BMF','USDMXN Futures - BMF','USDZAR Futures - BMF']
CLASSE_PRODUTOS_CREDITO = ['CDB DI Spread','Compromissada - Título Privado','Compromissada CDI','CRA','CRI','Debenture','FIDC DI Spread','Letra Financeira DI Spread']
CLASSE_PRODUTOS_TITULOS_PUBLICOS = ['LFT','NTN-B']
CLASSE_PRODUTOS_OFF = ['30-Day Fed Funds Futures','90 Day Bank Accepted Bill - ASX','AUD Fixed-Float SWAP','AUD/USD Futures - CME','AUD/USD Options - CME','CAD Fixed-Float SWAP','CAD/USD Futures - CME','CAD/USD Options - CME','Canadian Bank Accept 3M Fut','Canadian Bond Futures 10Y - MSE','Canadian Bond Futures 2Y - MSE','Cash','CHF/USD Futures - CME','CLP Fixed-Float SWAP','COP Fixed-Float SWAP','Copper Future - CMX','Copper Future Options - CMX','Currencies Digital Options','Currencies Forward','Currencies NDF','Currencies NDO','Currencies Options','DAX Index Future - EUREX','DJ Euro STOXX 50 Future - EUREX','EUR ESTR OIS','EUR/USD Futures - CME','EUR/USD Options - CME','Euribor Futures','Euribor Futures Options','Euro-Bund Future Options - EUREX','Euro-Bund Futures - EUREX','Eurodollar Futures','Eurodollar Futures Options','Euro-Schatz Futures - EUREX','GBP/USD Futures - CME','GBP/USD Options - CME','Gold Future  - CMX','Iron Ore 62 Fe TSI - SGX','JGB 10-year Futures - TSE','JPY/USD Futures - CME','JPY/USD Options - CME','MSCI Emerging Mkt Index Future - ICE','MXN TIIE SWAP','MXN/USD Futures - CME','NASDAQ-100 E-mini Futures - CME','NASDAQ-100 E-mini Options - CME','Provisions and Costs','Russell 2000 Index Mini Futures - CME','Russell 2000 Index Options - CME','S&P500 E-mini Futures','S&P500 E-mini Options','Swap CAD OIS','Swap FixedxCPI','Swap GBP OIS','Swap USD OIS','Three-Month CORRA Futures - MSE','Three-Month SOFR Future Options - CME','Three-Month SOFR Futures - CME','Three-Month SONIA Futures - ICE','Three-Month SONIA Futures Options - ICE','US Treasury Bond Future','US Treasury Bond Future Options','VIX Futures - CBOE','WTI Crude Oil Future','WTI Crude Oil Future Options','ZAR/USD Futures - CME']

st.set_page_config(layout='wide')

col4, col5 = st.columns(2)

#! '''Funções responsáveis por carregar os arquivos:'''
def load_tables_blob(arquivo,separador=None):
    # Inicializando BlobServiceClient com a connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    # Pegando o container
    container_client = blob_service_client.get_container_client(container_name)
    # Nome do arquivo no Blob
    arquivo = arquivo
    # Obtendo o BlobClient para o arquivo específico
    blob_client = container_client.get_blob_client(arquivo)
    # Baixando o conteúdo do blob
    downloaded_blob = blob_client.download_blob()
    # Lendo o conteúdo do blob
    blob_content = downloaded_blob.content_as_text()
    
    if separador is None:
        df = pd.read_csv(StringIO(blob_content)) 
    elif separador == 'xlsx':
        blob_content = downloaded_blob.readall()
        df = pd.read_excel(io.BytesIO(blob_content))
    else:
        df = pd.read_csv(StringIO(blob_content), delimiter=separador) 

    return df
    # Convertendo o conteúdo em um DataFrame
    # (Assumindo que o arquivo seja um CSV com separador de vírgula, você pode ajustar para outros formatos)
    # df = pd.read_csv(StringIO(blob_content), sep='\t')  # Use o delimitador apropriado se necessário

    # Exibindo o DataFrame
    # print(df)

def load_nav_and_shares(data_selecionada_DBY):
    arquivo = f'HistoricalFundsNAVandShare-24Feb2022-{data_selecionada_DBY}.txt'
    HIST_NAV = load_tables_blob(arquivo,'\t')
    return HIST_NAV

def load_mapeamento_setorial():
    arquivo = 'TABELA_AUXILIAR.csv'
    classificacao_setorial = load_tables_blob(arquivo)
    classificacao_setorial.drop_duplicates(inplace=True)
    return classificacao_setorial

def load_primitivas(data_selecionada_DBY):
    arquivo = f'FundOverviewByPrimitive_{data_selecionada_DBY}.txt'
    primitivas = load_tables_blob(arquivo,'\t')
    return primitivas

def load_trades_lote(data_selecionada_DBY):
    arquivo = f'FundsTrades-{data_selecionada_DBY}.txt'
    trades_lote = load_tables_blob(arquivo,'\t')
    return trades_lote

def load_trades_off(data_selecionada_DBY):
    arquivo = f'IntradayTradeReport {data_selecionada_DBY}.csv'
    TRADES_OFF = load_tables_blob(arquivo,',')
    return TRADES_OFF

def load_de_para_b3(data_selecionada_DBY):
    arquivo = f'InstrumentsConsolidatedFile_{data_selecionada_DBY}_1.csv'
    de_para_b3 = load_tables_blob(arquivo,',')
    return de_para_b3

def load_trades_clearing(data_selecionada_DBY):
    arquivo = f'allocations {data_selecionada_DBY}.csv'
    trades_clearing = load_tables_blob(arquivo,',')
    return trades_clearing

#!'''Funções responsáveis por tratar os arquivos:'''
def remover_underline(value):
    if len(value) >= 3 and value[-3] == '_':
        return value[:-3]  # Remove o antipenúltimo caractere e tudo após ele
    return value

def tratar_trades_clearing_off(TRADES_OFF):
    TRADES_OFF = TRADES_OFF[['BBG Code 1','B/S','QTY','Trade Price']]
    TRADES_OFF.rename(columns={'BBG Code 1': 'Product','Trade Price':'PM_CLEARING'}, inplace=True)
    TRADES_OFF['Side'] = TRADES_OFF['B/S'].apply(lambda x: 'Buy' if x==1 else 'Sell')
    TRADES_OFF['Dealer'] = 'BOFA'
    TRADES_OFF['Product'] = TRADES_OFF['Product'].str.rstrip()
    TRADES_OFF['FONTE'] = 'CLEARING'
    return TRADES_OFF

def tratar_trades_lote(TRADES_LOTE):
    LISTA_BACK_RISC_COMPLIANCE = ['Adriano Bartolomeu','Vicente Fletes', 'Eduardo Teixeira', 'Aline Marins', 'Vitor Chiba'] 
    TRADES_LOTE = TRADES_LOTE[(TRADES_LOTE['ProductClass'] != 'Provisions and Costs') & (~TRADES_LOTE['Trader'].isin(LISTA_BACK_RISC_COMPLIANCE)) & ((TRADES_LOTE['IsReplicatedTrade'] == False)) & (~TRADES_LOTE['Trading Desk'].str.contains('Rateio')) & (TRADES_LOTE['Dealer'] != 'LOTE45')]
    TRADES_LOTE = TRADES_LOTE[['Trading Desk','ProductClass','Product', 'Amount','Price','FinancialPrice','Trader','Dealer','FinancialSettle']]
    TRADES_LOTE['Side'] = TRADES_LOTE['Amount'].apply(lambda x: 'Buy' if x > 0 else 'Sell')
    TRADES_LOTE['Financeiro'] = TRADES_LOTE['Amount'] * TRADES_LOTE['Price']    
    TRADES_LOTE['Product'] = TRADES_LOTE['Product'].apply(remover_underline)
    
    #Calculando preço médio BOVESPA
    TRADES_LOTE_BOVESPA = TRADES_LOTE[TRADES_LOTE['ProductClass'].isin(CLASSE_PRODUTOS_BOVESPA)]

    TRADES_LOTE_PM = TRADES_LOTE_BOVESPA.groupby(['Dealer','ProductClass','Product','Side']).agg(
        Quantidade_Boleta_Lote45=('Amount', 'sum'),
        Financeiro=('Financeiro', 'sum'
    )).reset_index()
    TRADES_LOTE_PM['Quantidade_Boleta_Lote45'] = abs(TRADES_LOTE_PM['Quantidade_Boleta_Lote45'])
    TRADES_LOTE_PM['PM_LOTE'] = round(abs(TRADES_LOTE_PM['Financeiro'] / TRADES_LOTE_PM['Quantidade_Boleta_Lote45']),4)

    #Calculando preço médio BMF
    TRADES_LOTE_BMF = TRADES_LOTE[TRADES_LOTE['ProductClass'].isin(CLASSE_PRODUTOS_BMF)]
    TRADES_LOTE_BMF = TRADES_LOTE_BMF.groupby(['Dealer','ProductClass','Product','Side','Price']).agg(
        Quantidade_Boleta_Lote45=('Amount', 'sum'),
        Financeiro=('Financeiro', 'sum'
    )).reset_index()
    TRADES_LOTE_BMF['Quantidade_Boleta_Lote45'] = abs(TRADES_LOTE_BMF['Quantidade_Boleta_Lote45'])
    TRADES_LOTE_BMF['PM_LOTE'] = round(abs(TRADES_LOTE_BMF['Financeiro'] / TRADES_LOTE_BMF['Quantidade_Boleta_Lote45']),4)

    #Calculando preço médio OFF
    TRADES_LOTE_OFF = TRADES_LOTE[TRADES_LOTE['ProductClass'].isin(CLASSE_PRODUTOS_OFF)]
    TRADES_LOTE_OFF = TRADES_LOTE_OFF.groupby(['Dealer','ProductClass','Product','Side','Price']).agg(
        Quantidade_Boleta_Lote45=('Amount', 'sum'),
        Financeiro=('Financeiro', 'sum'
    )).reset_index()
    TRADES_LOTE_OFF['Quantidade_Boleta_Lote45'] = abs(TRADES_LOTE_OFF['Quantidade_Boleta_Lote45'])
    TRADES_LOTE_OFF['PM_LOTE'] = round(abs(TRADES_LOTE_OFF['Financeiro'] / TRADES_LOTE_OFF['Quantidade_Boleta_Lote45']),8)

    TRADES_LOTE_OFF = ajustar_multiplicadores(TRADES_LOTE_OFF)
    
    
    #Concatenando
    TRADES_LOTE_FINAL = pd.concat([TRADES_LOTE_PM,TRADES_LOTE_BMF,TRADES_LOTE_OFF])
    TRADES_LOTE_FINAL['FONTE'] = 'LOTE45'

    return TRADES_LOTE_FINAL[['ProductClass','Product','Side','PM_LOTE','Quantidade_Boleta_Lote45','Dealer','FONTE']]

def tratar_trades_clearing(TRADES_CLEARING):
    # Mapeando Corretoras
    TRADES_CLEARING['Entering Firm'] = TRADES_CLEARING['Entering Firm'].replace(de_para_corretoras)
    TRADES_CLEARING = TRADES_CLEARING[['Exchange', 'Symbol', 'Side', 'Price', 'Qty', 'Entering Firm']]

    # Função para tratar cada exchange
    def tratar_exchange(exchange_code):
        trades_exchange = TRADES_CLEARING[TRADES_CLEARING['Exchange'] == exchange_code].copy()
        if exchange_code == 'XBSP':
            trades_exchange['Symbol'] = trades_exchange['Symbol'].apply(lambda x: x[:-1] if x.endswith('F') else x)
            return calcular_preco_medio_clearing_bovespa(trades_exchange, exchange_code)
        else:
            return calcular_preco_medio_clearing_bmf(trades_exchange, exchange_code)
    # Tratando as exchanges BOVESPA e BMF
    trades_bovespa_pm = tratar_exchange('XBSP')
    trades_bmf_pm = tratar_exchange('XBMF')

    # Concatenando resultados
    TRADES_CLEARING = pd.concat([trades_bovespa_pm, trades_bmf_pm])
    TRADES_CLEARING['FONTE'] = 'CLEARING'
    return TRADES_CLEARING

def ajustar_multiplicadores(TRADES_LOTE_OFF):
    CLASSES_COM_PRICELOT10 = ['MXN/USD Futures - CME']
    
    cond1 = TRADES_LOTE_OFF['ProductClass'].isin(CLASSES_COM_PRICELOT10)
    TRADES_LOTE_OFF.loc[cond1,'PM_LOTE'] = TRADES_LOTE_OFF['PM_LOTE']*10
    
    return TRADES_LOTE_OFF

#! '''Funções responsáveis por realizar cálculos os arquivos:'''
def calcular_preco_medio_clearing_bovespa(trades, exchange):
    trades['Financeiro'] = trades['Qty'] * trades['Price']
    trades_pm = trades.groupby(['Exchange', 'Entering Firm', 'Symbol', 'Side']).agg(
        Quantidade_Operada_CLEARING=('Qty', 'sum'),
        Financeiro=('Financeiro', 'sum')
    ).reset_index()
    trades_pm['PM_CLEARING'] = trades_pm['Financeiro'] / trades_pm['Quantidade_Operada_CLEARING']
    return trades_pm[['Exchange', 'Symbol', 'Side', 'PM_CLEARING', 'Quantidade_Operada_CLEARING', 'Entering Firm']]    

def calcular_preco_medio_clearing_bmf(trades, exchange):
    trades['Financeiro'] = trades['Qty'] * trades['Price']
    trades_pm = trades.groupby(['Exchange', 'Entering Firm', 'Symbol', 'Side','Price']).agg(
        Quantidade_Operada_CLEARING=('Qty', 'sum'),
        Financeiro=('Financeiro', 'sum')
    ).reset_index()
    trades_pm['PM_CLEARING'] = trades_pm['Price']
    return trades_pm[['Exchange', 'Symbol', 'Side', 'PM_CLEARING', 'Quantidade_Operada_CLEARING', 'Entering Firm']]

def calcular_preco_medio_bofa(trades, exchange):
    trades['Financeiro'] = trades['Qty'] * trades['Price']
    trades_pm = trades.groupby(['Exchange', 'Entering Firm', 'Symbol', 'Side','Price']).agg(
        Quantidade_Operada_CLEARING=('Qty', 'sum'),
        Financeiro=('Financeiro', 'sum')
    ).reset_index()
    trades_pm['PM_CLEARING'] = trades_pm['Price']
    return trades_pm[['Exchange', 'Symbol', 'Side', 'PM_CLEARING', 'Quantidade_Operada_CLEARING', 'Entering Firm']]

#!'''Funções de Pivot'''
def pivot_table_resumo(df,familia_de_fundos):
    # Filtra o DataFrame com base nas 'acoes' e reorganiza as colunas
    df_filtrado = df[df['TradingDesk'].isin(familia_de_fundos)][['TradingDesk','PL_D1_PCT', 'PL_MTD_PCT', 'PL_YTD_PCT', 'PL_INCEPT_PCT']]

    # Renomeia as colunas
    df_filtrado = df_filtrado.rename(columns={
        'PL_D1_PCT': 'D1',
        'PL_MTD_PCT': 'MTD',
        'PL_YTD_PCT': 'YTD',
        'PL_INCEPT_PCT': 'INCEPT'
    })

    # Cria uma tabela pivot, somando os valores e multiplicando por 100
    pivot_df = pd.pivot_table(df_filtrado, index='TradingDesk', aggfunc='sum') * 100
    pivot_df = pivot_df[['D1','MTD','YTD','INCEPT']]
    return pivot_df

def pivot_table_attribution(df,fundo_desejado):
    # Filtra o DataFrame com base nas 'acoes' e reorganiza as colunas
    df_filtrado = df[df['TradingDesk']==fundo_desejado][['Quebra_Relatorio','Setores','PL_D1_PCT', 'PL_MTD_PCT', 'PL_YTD_PCT', 'PL_INCEPT_PCT']]

    # Renomeia as colunas
    df_filtrado = df_filtrado.rename(columns={
        'PL_D1_PCT': 'D1',
        'PL_MTD_PCT': 'MTD',
        'PL_YTD_PCT': 'YTD',
        'PL_INCEPT_PCT': 'INCEPT'
    })
    # Cria uma tabela pivot, somando os valores e multiplicando por 100
    pivot_df = pd.pivot_table(df_filtrado, index=['Quebra_Relatorio','Setores'], aggfunc='sum') * 100
    pivot_df.reset_index(inplace=True)
    pivot_df['Quebra_Relatorio'] = pivot_df['Quebra_Relatorio'].where(pivot_df['Quebra_Relatorio'].ne(pivot_df['Quebra_Relatorio'].shift()))
    pivot_df = round(pivot_df[['Quebra_Relatorio','Setores','D1','MTD','YTD','INCEPT']],2)
    pivot_df = pivot_df.fillna('-')
    return pivot_df

#! '''Função para testar alguma sub'''
def sub_teste():
    date = datetime.datetime.today()
    data_selecionada_DBY = date.strftime('%Y%m%d')
    data_selecionada_DBY = '20241018'
    # load_trades_off(data_selecionada_DBY)
    TRADES_OFF = tratar_trades_clearing_off(load_trades_off(data_selecionada_DBY))

def base_tabela_final(TRADES_CLEARING,TRADES_LOTE,TRADES_OFF,DE_PARA_B3):
    # Renomeando as colunas 'Symbol' para 'Product' e 'Entering Firm' para 'Dealer'
    TRADES_CLEARING.rename(columns={'Symbol': 'Product', 'Entering Firm': 'Dealer'}, inplace=True)
    TRADES_CLEARING=TRADES_CLEARING.replace(DE_PARA_B3)
    # Fazendo o merge das duas tabelas usando Product, Side e Dealer como chave
    
    # BOVESPA
    TRADES_LOTE_BOVESPA = TRADES_LOTE[TRADES_LOTE['ProductClass'].isin(CLASSE_PRODUTOS_BOVESPA)]
    TRADES_CLEARING_BOVESPA = TRADES_CLEARING[TRADES_CLEARING['Exchange'] == 'XBSP']
    df_comparacao_BOVESPA = pd.merge(TRADES_CLEARING_BOVESPA, TRADES_LOTE_BOVESPA, how='outer', on=['Product', 'Side', 'Dealer'])
    
    #BMF
    TRADES_LOTE_BMF = TRADES_LOTE[TRADES_LOTE['ProductClass'].isin(CLASSE_PRODUTOS_BMF)]
    TRADES_CLEARING_BMF = TRADES_CLEARING[TRADES_CLEARING['Exchange'] == 'XBMF']
    TRADES_CLEARING_BMF['PM'] = TRADES_CLEARING_BMF['PM_CLEARING']
    TRADES_LOTE_BMF['PM'] = TRADES_LOTE_BMF['PM_LOTE']
    df_comparacao_BMF = pd.merge(TRADES_CLEARING_BMF, TRADES_LOTE_BMF, how='outer', on=['Product', 'Side', 'Dealer','PM'])

    #OFF
    TRADES_LOTE_OFF = TRADES_LOTE[TRADES_LOTE['ProductClass'].isin(CLASSE_PRODUTOS_OFF)]
    TRADES_LOTE_OFF['PM'] = TRADES_LOTE_OFF['PM_LOTE']
    TRADES_OFF['PM'] = TRADES_OFF['PM_CLEARING']
    df_comparacao_OFF = pd.merge(TRADES_OFF,TRADES_LOTE_OFF, how='outer',on=['Product', 'Side', 'Dealer','PM'])


    # col1,col2 = st.columns(2)
    # with col1:
    #     st.write('Bovespa')
    #     TRADES_LOTE_BOVESPA
    #     st.write('BMF')
    #     TRADES_LOTE_BMF
    #     st.write('OFF')
    #     TRADES_LOTE_OFF

    # with col2:
    #     st.write('Bovespa')
    #     TRADES_CLEARING_BOVESPA
    #     st.write('BMF')
    #     TRADES_CLEARING_BMF
    #     st.write('OFF')
    #     TRADES_OFF



    df_comparacao = pd.concat([df_comparacao_BOVESPA,df_comparacao_BMF,df_comparacao_OFF])
    df_comparacao = df_comparacao.fillna(0)
    # Calculando as diferenças de quantidade e preço médio
    df_comparacao['Diferença_Quantidade'] = df_comparacao['Quantidade_Boleta_Lote45'] - df_comparacao['Quantidade_Operada_CLEARING']
    df_comparacao['Diferença_PM'] = df_comparacao['PM_LOTE'] - df_comparacao['PM_CLEARING']
    
    
    #! Data Frane com unmatches:
    # df_comparacao_erro = df_comparacao[df_comparacao['Diferença_Quantidade']!=0]
    # df_comparacao_erro
    # df_comparacao_erro[['Product', 'Side', 'Dealer','PM']][df_comparacao_erro['Product']=='IBOVW126']
    
    return df_comparacao

#! '''Código base para o Batimento de Trades'''
def batimento_de_trades(TRADES_LOTE,TRADES_CLEARING,TRADES_OFF,DE_PARA_B3):
    
    st.title('Batimento de Trades')
    tabela_batimento = base_tabela_final(TRADES_CLEARING,TRADES_LOTE,TRADES_OFF,DE_PARA_B3)

    total_bmf = np.sum(TRADES_CLEARING['Quantidade_Operada_CLEARING'][TRADES_CLEARING['Exchange']=='XBMF'])
    total_bovespa = np.sum(TRADES_CLEARING['Quantidade_Operada_CLEARING'][TRADES_CLEARING['Exchange']=='XBSP'])

    total_bmf_lote = np.sum(TRADES_LOTE['Quantidade_Boleta_Lote45'][TRADES_LOTE['ProductClass'].isin(CLASSE_PRODUTOS_BMF)])
    total_bovespa_lote = np.sum(TRADES_LOTE['Quantidade_Boleta_Lote45'][TRADES_LOTE['ProductClass'].isin(CLASSE_PRODUTOS_BOVESPA)])


    # trader = st.selectbox("Escolha o Trader",['XBMF','BVSP', 'OFFSHORE','TODOS'])
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric(label='Total BMF',value=total_bmf,delta=round(total_bmf_lote/total_bmf,2)*100)
    with col2:
        st.metric(label='Total BOVESPA',value=total_bovespa,delta=round(total_bovespa_lote/total_bovespa,2)*100)
    
    col4,col5,col6,col7 = st.columns(4)
    with col4:
        mercado = st.selectbox("Escolha o mercado",['TODOS','XBMF','XBSP', 'OFFSHORE'])
    with col5:
        filtrar_erros = st.selectbox('Status:',['TODOS','OK','ERRO'])
    
    if mercado == 'TODOS':
        resumo_trades = tabela_batimento
    elif mercado =='OFFSHORE':
        resumo_trades = tabela_batimento[tabela_batimento['ProductClass'].isin(CLASSE_PRODUTOS_OFF)]
    elif mercado =='TÍTULO PÚBLICO':
        resumo_trades = tabela_batimento[tabela_batimento['ProductClass'].isin(CLASSE_PRODUTOS_TITULOS_PUBLICOS)]
    elif mercado =='CRÉDITO':
        resumo_trades = tabela_batimento[tabela_batimento['ProductClass'].isin(CLASSE_PRODUTOS_CREDITO)]
    else:
        resumo_trades = tabela_batimento[tabela_batimento['Exchange'] == mercado]

    if filtrar_erros=='ERRO':
        resumo_trades = resumo_trades[(resumo_trades['Diferença_Quantidade']!=0) & (resumo_trades['Diferença_PM']!=0)]
    if filtrar_erros=='OK':
        resumo_trades = resumo_trades[(resumo_trades['Diferença_Quantidade']==0) & (resumo_trades['Diferença_PM']==0)]

    # Exibindo o DataFrame comparativo
    st.dataframe(resumo_trades[['Product', 'Side', 'Dealer', 'Quantidade_Boleta_Lote45', 'Quantidade_Operada_CLEARING', 'Diferença_Quantidade', 'PM_LOTE', 'PM_CLEARING', 'Diferença_PM']],hide_index=True,use_container_width=True,)

def render_sidebar(auth_data):

    if auth_data:
        st.sidebar.write("Você está conectado")  
        st.sidebar.title('Escolha a funcionalidade')
        funcionalidades = ['Batimento de Trades', 'On Going']
        return st.sidebar.radio('Relatórios disponíveis:', funcionalidades)
    else:
        st.sidebar.write("Você não está conectado")
        return None

def handle_batimento_de_trades(date):
    data_selecionada_DBY = date.strftime('%Y%m%d')
    TRADES_LOTE = tratar_trades_lote(load_trades_lote(data_selecionada_DBY))
    TRADES_CLEARING = tratar_trades_clearing(load_trades_clearing(data_selecionada_DBY))
    TRADES_OFF = tratar_trades_clearing_off(load_trades_off(data_selecionada_DBY))
    DE_PARA_B3 = load_de_para_b3(data_selecionada_DBY)
    batimento_de_trades(TRADES_LOTE, TRADES_CLEARING,TRADES_OFF,DE_PARA_B3)

def main():
    st.sidebar.image('assinaturas_TENAX_RGB-02-removebg-preview.png')
    with st.sidebar:
        auth_data = Msal.initialize_ui(
            client_id=client_id,
            authority=authority,
            scopes=["User.Read"],
            connecting_label="Connecting",
            disconnected_label="Disconnected",
            sign_in_label="Sign in",
            sign_out_label="Sign out"
        )

    funcionalidade = render_sidebar(auth_data)

    if funcionalidade == 'Batimento de Trades':
        date = st.sidebar.date_input("Informe a data desejada:", format='DD-MM-YYYY')
        handle_batimento_de_trades(date)
    elif funcionalidade == 'On Going':
        sub_teste()

if __name__ == "__main__":
    main()


