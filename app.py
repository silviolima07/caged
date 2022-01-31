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

    activities = ["Home",'Gráficos',"About"]
    choice = st.sidebar.selectbox("Selecione uma opção",activities)

    # Definir a data da última atualização


    #f = open("update", "r")
    #data_update = f.read()
    
    

    #parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
    #resp = urllib.request.urlopen(url_caged)
    #soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    #url_tabela='http://pdet.mte.gov.br'
    
    from lxml import html
    
    url_caged = "http://pdet.mte.gov.br/novo-caged"
    url_tabela= 'http://pdet.mte.gov.br'
    
    page = requests.get(url_caged)
    webpage = html.fromstring(page.content)

    
    for link in webpage.xpath('//a/@href'):
        if "tabelas.xlsx" in link:
            #print("Link:",link)
            #print("Url tabela: ", url_tabela+str(link))
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
    
    #st.title("Apos carregar a tabela")
    #st.table(df_tab6[:27])
    
    df_teste = df_tab6.dropna()
    teste_colunas = df_teste.columns
    mes_ano_inicial = teste_colunas[2][0]
    
    mes_inicial, ano_inicial = mes_ano_inicial.split('/')
    
    st.subheader("Inicial  -> "+mes_inicial+'/'+ano_inicial)
    st.subheader("  Atual  -> "+meses[mes_final]+'/'+ano_final)
    
    mes_ano_final = meses[mes_final]+'/'+ano_final
    
    lista_meses = [meses['Jan'], meses['Fev'], meses['Mar'],
                   meses['Abr'], meses['Mai'], meses['Jun'],
                   meses['Jul'], meses['Ago'], meses['Set'],
                   meses['Out'], meses['Nov'], meses['Dez']]
    lista_anos = [ano_inicial, ano_final]
    
    html_page3 = """
    <div style="background-color:white;padding=25px">
        <p style='text-align:left;font-size:25px;font-weight:bold;color:blue'>Pesquisar</p>
    </div>
              """
    st.markdown(html_page3, unsafe_allow_html=True)
    
    opcao_mes = st.selectbox(
     'MÊS',lista_meses)
     
    opcao_ano = st.selectbox(
     'ANO',lista_anos)
    

    #st.write("--> "+opcao_mes+'/'+opcao_ano)
    
    filtro_mes_ano = opcao_mes+'/'+opcao_ano
    
    colunas = ['Grupamento de Atividades Econômicas e Seção CNAE 2.0', filtro_mes_ano]
    
    df_tab6.rename(columns={'Unnamed: 1_level_1':"Grupamento de Atividades Econômicas e Seção CNAE 2.0"}, inplace=True)
   
    df_tab6 = df_tab6.fillna("Sem informação")
    
    #df_tab6.droplevel(level=0)
    
    #df_tab6.columns = df_tab6.columns.droplevel(0)
    #df_tab6.columns = [col[0] for col in df_tab6.columns]    Quase
    
    df_tab6_1 = df_tab6[colunas][:27]
    
    #df_tab6_1.columns = df_tab6_1.columns.droplevel()
    
    teste = ['Grupamento de Atividades Econômicas e Seção CNAE 2.0', filtro_mes_ano * 5]
    
    df_tab6_1 = df_tab6_1.xs(teste, axis=1, drop_level=True)
    
    st.write(df_tab6_1.columns)
    
    st.table(df_tab6_1) # TESTE
    
    
    """
    #colunas = list(df_tab6_1.columns)
    
    #st.write("Colunas")
    #st.write(colunas)
 
    df_tab6_1.columns = df_tab6_1.columns.droplevel()
    
    
    html_page3 = """
    #<div style="background-color:blue;padding=40px">
    #    <p style='text-align:center;font-size:40px;font-weight:bold;color:red'>Relatório</p>
    #</div>
    """
    st.markdown(html_page3, unsafe_allow_html=True)
    
    #st.table(df_tab6_1)# TESTE
    
    st.subheader(filtro_mes_ano)
        
    #colunas = list(df_tab6_1.columns)
    
    if (filtro_mes_ano == 'Janeiro/2020'):
        colunas = list(df_tab6_1.columns)[:-1]
    else:
        colunas = list(df_tab6_1.columns)
    
    st.write("Colunas")
    st.write(colunas)
               
    df_tab6_1.to_csv("caged.csv", index=False, header=colunas, columns = colunas)
        
    df_tab6_1 = pd.read_csv('./caged.csv')
        
    temp1 = df_tab6_1.loc[df_tab6_1['Grupamento de Atividades Econômicas e Seção CNAE 2.0'] != 'Não identificado***']
    df_tab6_2= temp1.loc[temp1['Grupamento de Atividades Econômicas e Seção CNAE 2.0'] != 'Total']
        
    df_tab6_2.to_csv("caged.csv", index=False, header=colunas)
    
    with open('caged.csv', encoding="latin-1") as f:
        nome = 'caged_'+opcao_mes+'_'+opcao_ano+'.csv'
        st.download_button('Download CSV', f, nome)  # Defaults to 'text/plain
    """
    if choice == activities[0]:
         st.write("TESTE")
        #st.table(df_tab6_2.style.format('{:7,.1}'))
        #st.table(df_tab6_2)
        
    elif choice == activities[1]:
        #st.sidebar.image(aguia1,caption="", width=300)
        #df = pd.read_csv(file_csv[0])
        #total = str(len(df))
        st.title(activities[1])
        #st.table(df_tab6_2)

        
        # link is the column with hyperlinks
        #df['Link'] = df['Link'].apply(make_clickable)
        #df = df.to_html(escape=False)
        #st.markdown(df, unsafe_allow_html=True)

        
        #st.table(df)
        #if st.button('Download Dataframe as CSV'):
        #    cargo = activities[1].replace(' ', '_')
        #    filename = 'indeed_'+cargo+'.csv'
        #    st.subheader("Salvando: "+filename)
        #    tmp_download_link = download_link(df, filename, 'Click here to download your data!')
        #    st.markdown(tmp_download_link, unsafe_allow_html=True)
     
  
    elif choice == 'About':
        #st.sidebar.image(about,caption="", width=300, height= 200)
        st.subheader("Built with Streamlit")
        
        st.write("Dados coletados via scrap usando: Selenium e BeautifulSoup.")
        #st.markdown("A coleta dos dados é feita às 9h, 12h, 15h e 18h")
        st.write("Executados via crontab scripts realizam o scrap e atualização do app.")
        st.write("Foram definidos 4 cargos apenas para validar o processo.")
        st.write("O scrap para o cargo de Engenheiro de Machine Learning trouxe poucas linhas.")
        st.write("Para os demais cargos, foram encontradas mais de 100 vagas, distribuídas em diversas páginas.")
        st.write("Esse app traz as 10 primeiras páginas apenas.")
        st.subheader("Observacao:")
        st.write("O codigo html da pagina muda ao longo do tempo e ajustes no scrap são necessarios.")
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
