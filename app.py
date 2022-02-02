import streamlit as st

from bokeh.models.widgets import Div

import pandas as pd

from PIL import Image

#pd.set_option('precision',2)

#pd.options.display.float_format = '${:. ,2f}'.format

import base64

import sys

import numpy as np
import requests

from lxml import html





def download_link(df, texto1, texto2):
    st.write("Efetuar download")
    if isinstance(df,pd.DataFrame):
        object_to_download = df.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{texto1}">{texto2}</a>'

def excel_to_pandas2(URL, local_path, sheet, header):
    resp = requests.get(URL)
    with open(local_path, 'wb') as output:
        output.write(resp.content)
    df = pd.read_excel(local_path,sheet_name=sheet,header=header)
    return df    

@st.cache
def convert_df(df):
    return df.to_csv().encode('ISO-8859-1')

def main():

    """Indeed App """

    # Titulo do web app
    html_page1 = """
    <div style="background-color:red;padding=50px">
        <p style='text-align:center;font-size:50px;font-weight:bold;color:blue'>CAGED</p>
    </div>
              """
    st.markdown(html_page1, unsafe_allow_html=True)
   
    #html_page2 = """
    #<div style="background-color:white;padding=30px">
    #    <p style='text-align:left;font-size:30px;font-weight:bold;color:blue'>Relatórios</p>
    #</div>
    #          """
    #st.markdown(html_page2, unsafe_allow_html=True)

    activities = ['Relatórios',"About"]
    choice = st.sidebar.selectbox("Selecione uma opção",activities)  
    
    
    url_caged = "http://pdet.mte.gov.br/novo-caged"
    url_tabela= 'http://pdet.mte.gov.br'
    
    page = requests.get(url_caged)
    webpage = html.fromstring(page.content)

    
    for link in webpage.xpath('//a/@href'):
        if "tabelas.xlsx" in link:
            url_tabela = url_tabela+str(link)
    
    
    meses={'Jan':'Janeiro', 'Fev':"Fevereiro",
       'Mar':'Março', 'Abr': 'Abril',
       'Mai': 'Maio', 'Jun':'Junho',
       'Jul':'Julho', 'Ago': 'Agosto',
       'Set': 'Setembro', 'Out':"Outubro",
       'Nov':"Novembro", 'Dez': "Dezembro"}
       
    mesano = url_tabela.split('/')[5]
    mes_final = mesano[0:3]
    ano_final = mesano[3:]
    
    df_tab6 = excel_to_pandas2(url_tabela,'caged.xlsx', 'Tabela 6', [4,5] )
    
    df_teste = df_tab6.dropna()
    teste_colunas = df_teste.columns
    mes_ano_inicial = teste_colunas[2][0]
    
    mes_inicial, ano_inicial = mes_ano_inicial.split('/')
    
    mes_ano_final = meses[mes_final]+'/'+ano_final
    
    if choice == activities[1]:
        st.subheader("Informações")
        st.write("")
        st.markdown("O  CAGED constitui importante fonte de informação do mercado de trabalho")
        st.write("de âmbito nacional e de periodicidade mensal. Foi criado como instrumento")
        st.write("de acompanhamento e de fiscalização do processo de admissão e de dispensa")
        st.write("de trabalhadores regidos pela CLT, com o objetivo de assistir os desempregados")
        st.write("e de apoiar medidas contra o desemprego. A partir de 1986, passou a ser utilizado")
        st.write("como suporte ao pagamento do seguro-desemprego e, mais recentemente, tornou-se,")
        st.write("também, um relevante instrumento à reciclagem profissional e à recolocação do trabalhador")
        st.write("no mercado de trabalho.")
        st.write("")
        #if st.button("Caged"):
        #    js = "window.open('http://pdet.mte.gov.br/caged'/)"
        #    html = '<img src onerror="{}">'.format(js)
        #    div = Div(text=html)
        #    st.bokeh_chart(div)
        
        
    
    elif choice == activities[0]:
    
        st.subheader("Inicial  -> "+mes_inicial+'/'+ano_inicial)
        st.subheader("  Atual  -> "+meses[mes_final]+'/'+ano_final)
    
       
        lista_meses = [meses['Jan'], meses['Fev'], meses['Mar'],
                   meses['Abr'], meses['Mai'], meses['Jun'],
                   meses['Jul'], meses['Ago'], meses['Set'],
                   meses['Out'], meses['Nov'], meses['Dez']]
        lista_anos = [ano_inicial, ano_final]
    
        opcao_mes = st.selectbox(
     'MÊS',lista_meses)
     
        opcao_ano = st.selectbox(
     'ANO',lista_anos)
    

        st.subheader(opcao_mes+'/'+str(opcao_ano))
    
        filtro_mes_ano = opcao_mes+'/'+opcao_ano
    
        colunas = ['Grupamento de Atividades Econômicas e Seção CNAE 2.0', filtro_mes_ano]
    
        df_tab6.rename(columns={'Unnamed: 1_level_1':"Grupamento de Atividades Econômicas e Seção CNAE 2.0"}, inplace=True)
   
        df_tab6 = df_tab6.fillna(0.0)
    
        #df_tab6.droplevel(level=0)
    
        #df_tab6.columns = df_tab6.columns.droplevel(0)
        #df_tab6.columns = [col[0] for col in df_tab6.columns]    Quase
    
        df_tab6_1 = df_tab6[colunas][:27]
    
        #df_tab6_1.columns = df_tab6_1.columns.droplevel()
    
        df_tab6_1.columns=df_tab6_1.columns.get_level_values(1)
    
        #st.write(df_tab6_1.columns)
        
        
        
        coluna_float = df_tab6_1.columns
        
        #st.write(coluna_float)
        
        #df_tab6_1[coluna_float] = df_tab6_1.style.format(subset=[float(coluna_float)], formatter="{:.2f}")
        
        
        
        float = df_tab6_1['Variação Relativa (%)']
        
        
        #df_tab6_1[df_tab6_1.columns[5]] = float.style.format("{:.2}")
        
        st.table(df_tab6_1.style.format(subset=[coluna_float[5]], formatter="{:.2f}"))
    
        #st.table(df_tab6_1)
    
        #df_tab6_1.to_csv("caged.csv", index=False, encoding='ISO-8859-1')
    
    
        #Download
        
        

        csv = convert_df(df_tab6_1)
    
        filename = 'caged_'+opcao_mes+'_'+str(opcao_ano)+'.csv'
        st.download_button("Download",csv, filename,"text/csv",key='download-csv')
    
        #df_tab6_1.to_csv("caged.csv", index=False)
    
    
   
    
    
if __name__ == '__main__':
    main()
