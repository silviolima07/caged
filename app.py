import streamlit as st

from bokeh.models.widgets import Div

import pandas as pd

from PIL import Image

pd.set_option('precision',2)

import base64

import sys

import numpy as np
import requests

from lxml import html


@st.cache
def convert_df(df):
    return df.to_csv().encode('ISO-8859-1')


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

def main():

    """Indeed App """

    # Titulo do web app
    html_page1 = """
    <div style="background-color:red;padding=50px">
        <p style='text-align:center;font-size:50px;font-weight:bold;color:blue'>CAGED</p>
    </div>
              """
    st.markdown(html_page1, unsafe_allow_html=True)
   
    html_page2 = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:left;font-size:30px;font-weight:bold;color:blue'>Relatórios</p>
    </div>
              """
    st.markdown(html_page2, unsafe_allow_html=True)

    activities = ["Home",'Relatórios',"About"]
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
    
    st.subheader("Inicial  -> "+mes_inicial+'/'+ano_inicial)
    st.subheader("  Atual  -> "+meses[mes_final]+'/'+ano_final)
    
    mes_ano_final = meses[mes_final]+'/'+ano_final
    
    if choice == activities[0]:
        st.write("Informações do Caged")
    
    elif choice == activities[1]:
        html_page2 = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:left;font-size:30px;font-weight:bold;color:blue'>Relatórios</p>
    </div>
              """
        st.markdown(html_page2, unsafe_allow_html=True)    
    
        lista_meses = [meses['Jan'], meses['Fev'], meses['M ar'],
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
   
        df_tab6 = df_tab6.fillna("Sem informação")
    
        #df_tab6.droplevel(level=0)
    
        #df_tab6.columns = df_tab6.columns.droplevel(0)
        #df_tab6.columns = [col[0] for col in df_tab6.columns]    Quase
    
        df_tab6_1 = df_tab6[colunas][:27]
    
        #df_tab6_1.columns = df_tab6_1.columns.droplevel()
    
        df_tab6_1.columns=df_tab6_1.columns.get_level_values(1)
    
        #st.write(df_tab6_1.columns)
    
        st.table(df_tab6_1) # TESTE
    
        df_tab6_1.to_csv("caged.csv", index=False, encoding='ISO-8859-1')
    
    
        #Download

        csv = convert_df(df_tab6_1)
    
        filename = 'caged_'+opcao_mes+'_'+str(opcao_ano)+'.csv'
    st.download_button(
   "Press to Download",csv, filename,"text/csv",key='download-csv'
    )
    
        df_tab6_1.to_csv("caged.csv", index=False)
    
    
  
    elif choice == 'About':
        #st.sidebar.image(about,caption="", width=300, height= 200)
        st.subheader("Built with Streamlit")
        
        st.write("Dados coletados via scrap do Caged")
        #st.markdown("A coleta dos dados é feita às 9h, 12h, 15h e 18h")
        #st.write("Executados via crontab scripts realizam o scrap e atualização do app.")
        #st.write("Foram definidos 4 cargos apenas para validar o processo.")
        #st.write("O scrap para o cargo de Engenheiro de Machine Learning trouxe poucas linhas.")
        #st.write("Para os demais cargos, foram encontradas mais de 100 vagas, distribuídas em diversas páginas.")
        #st.write("Esse app traz as 10 primeiras páginas apenas.")
        #st.subheader("Observacao:")
        #st.write("O codigo html da pagina muda ao longo do tempo e ajustes no scrap são necessarios.")
        #st.subheader("Versão 02")
        #st.write(" - incluído o link encurtado da vaga")
        st.subheader("by Silvio Lima")
        
        if st.button("Linkedin"):
            js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
    

       

   
    
    
if __name__ == '__main__':
    main()
