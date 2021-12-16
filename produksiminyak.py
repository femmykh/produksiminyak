import pandas as pd
import plotly.express as px
import streamlit as st

# Main Page
st.set_page_config(page_title="Pusat Informasi Negara Penghasil Minyak", page_icon="penguin", layout="wide")
col1, col2, col3 = st.columns((0.5, 1, 0.5))
col1.image("oil tumpah.png", width=200)
title = '<p style="font-family: sans-serif; font-size: 50px; text-align: center;"><b>Pusat Informasi Negara Penghasil Minyak</b></p>'
col2.markdown(title, unsafe_allow_html=True)
col3.image("logo_itb_1024.png", width=200)

# Creator
st.markdown("Created by **Femmy Khairany Hemas** — **12220110**")

# Membuat dataframe
data_produksi_minyak = pd.read_csv('produksi_minyak_mentah.csv')
data_kode_negara = pd.read_json('kode_negara_lengkap.json')
mergeResult = pd.merge(left=data_kode_negara, right=data_produksi_minyak, left_on='alpha-3', right_on='kode_negara')
dataframe = dataHasil=mergeResult[['name','tahun','produksi','alpha-3','country-code','iso_3166-2','region','sub-region','intermediate-region','region-code','sub-region-code']]
dataset = dataframe.rename({'name': 'Negara','produksi':'Produksi' ,'tahun': 'Tahun','alpha-3':'Kode'}, axis='columns')

# Data seluruh tahun
lihat_data = st.button('Lihat data produksi minyak seluruh tahun')
if lihat_data:
     # Negara dengan produksi minyak tertinggi
     st.subheader("Negara dengan produksi minyak tertinggi")
     info_data = dataset[['Negara','Tahun','Produksi','Kode','region','sub-region']]
     hasil = info_data[info_data['Produksi'] == info_data['Produksi'].max()]
     st.dataframe(hasil)
   
     # Negara dengan produksi minyak kumulatif tertinggi
     Data=dataset[dataset['Negara']=='Saudi Arabia']
     Data = Data[['Negara','Tahun','Produksi','Kode','region','sub-region']]
     Data['Produksi Kumulatif'] = Data['Produksi'].cumsum()
     total = Data[Data['Produksi Kumulatif'] == Data['Produksi Kumulatif'].max()]
     bar_chart = px.bar(Data, x='Tahun',y='Produksi')
     st.plotly_chart(bar_chart,use_container_width=True)
     st.subheader("Negara dengan produksi minyak tertinggi secara kumulatif")
     st.dataframe(total)

     # Negara dengan produksi minyak terendah
     st.subheader("Negara dengan produksi minyak terendah")
     Data = dataset[dataset['Produksi'] != 0]
     Data = Data[['Negara','Tahun','Produksi','Kode','region','sub-region']]
     total = Data[Data['Produksi']==Data['Produksi'].min()]
     st.dataframe(total)

     # Negara yang produksinya 0
     Data = dataset[dataset['Produksi'] == 0]
     st.subheader("Negara yang tidak memiliki produksi minyak")
     total = Data[['Negara','Tahun','Produksi','Kode','country-code','region','sub-region']]
     st.dataframe(total)

# Analisa data berdasarkan negara     
st.sidebar.subheader("Analisa data berdasarkan negara")
datanegara = pd.read_json('kode_negara_lengkap.json')
pilihanNegara = st.sidebar.selectbox('Pilih negara',datanegara['name'])
state_data = dataset[dataset['Negara'] == pilihanNegara]

def get_total_dataframe(dataset):
    total_dataframe = dataset[['Negara','Tahun','Produksi']]
    return total_dataframe
def get_data_info(dataset):
    info_data = dataset[['Negara','Kode','country-code','region','sub-region','Tahun','Produksi']]
    pd.set_option('display.max_colwidth', 0)
    return info_data

state_total = get_total_dataframe(state_data)
if st.sidebar.checkbox("Lihat negara"):
     st.header("Analisa data negara")
     st.subheader("Tampilan data produksi minyak Negara "+pilihanNegara)
     st.write(state_total,width=2024,height=2000)

     if st.sidebar.checkbox("Lihat grafik"):
          st.subheader("Tampilan grafik produksi minyak pada Negara "+pilihanNegara)
          state_total_graph = px.bar(state_total, x='Tahun',y='Produksi',labels=("Negara penghasil minyak = "+pilihanNegara))
          st.plotly_chart(state_total_graph,use_container_width=True)

          # Menampilkan data banyak tahun yang ingin dilihat
          st.subheader("Tahun dengan produksi minyak terbanyak pada Negara "+pilihanNegara)
          jumlah_data = st.text_input("Masukkan banyak tahun yang ingin dilihat:")
          if jumlah_data:
               data__tampil = state_total.nlargest(int(jumlah_data), 'Produksi')
               data_hasil = data__tampil[['Negara','Tahun','Produksi']]
               max_data = px.bar(data_hasil, x='Tahun',y='Produksi',labels={'Jumlah':'Produksi tahun %s' % (pilihanNegara)})
               st.plotly_chart(max_data,use_container_width=True)
          
          # Menampilkan detail data negara
          if st.sidebar.checkbox("Lihat detail produksi minyak Negara "+pilihanNegara):
               st.header("Data lengkap produksi minyak untuk Negara "+pilihanNegara)
               info_negara = get_data_info(state_data)
               st.write(info_negara)
            
# Analisa data berdasarkan tahun
st.sidebar.subheader("Analisa data berdasarkan tahun")
pilihanTahun = st.sidebar.selectbox('Pilih tahun',dataset['Tahun'])
tahun = dataset[dataset['Tahun'] == pilihanTahun]

def get_total_year(dataset):
    tahun = dataset[dataset["Tahun"] == pilihanTahun]
    year_dataframe = tahun[['Negara','Tahun','Produksi']]
    return year_dataframe
year_total = get_total_year(tahun)

if st.sidebar.checkbox("Lihat tahun"):
     dataset_bersih = dataset[dataset['Produksi'] != 0]
     dataset_tahun = dataset_bersih[['Negara','Tahun','Produksi','Kode','region','sub-region']]
     st.header("Analisa data produksi minyak berdasarkan tahun")
     if st.sidebar.checkbox("Grafik berdasarkan tahun"):
          st.subheader("Data negara penghasil minyak pada tahun "+str(pilihanTahun))
          year_total_graph = px.bar(year_total,x='Produksi',y='Negara',labels={'Jumlah':'Produksi tahun %s' % (pilihanTahun)})
          st.plotly_chart(year_total_graph,use_container_width=True)
          
          # Menampilkan data negara dengan jumlah produksi minyak terbanyak
          st.subheader("Negara dengan produksi minyak terbanyak pada tahun "+str(pilihanTahun))
          jumlah_tampil = st.text_input('Masukkan banyak negara yang ingin dilihat:')
          if jumlah_tampil:
               data_5 = year_total.nlargest(int(jumlah_tampil), 'Produksi')
               data_hasil = data_5[['Negara','Tahun','Produksi']]
               max_data = px.bar(data_hasil, x='Produksi',y='Negara',labels={'Jumlah':'Produksi tahun %s' % (pilihanTahun)})
               st.plotly_chart(max_data,use_container_width=True)
               
     if st.sidebar.checkbox("Informasi data berdasarkan tahun"):
          # Negara dengan jumlah produksi minyak tertinggi
          st.subheader("Negara dengan produksi minyak tertinggi pada tahun "+str(pilihanTahun))
          data_tahun =dataset_tahun[dataset_tahun["Tahun"] == pilihanTahun]
          data_tahun=data_tahun[data_tahun['Produksi']==data_tahun['Produksi'].max()]
          st.write(data_tahun)

          # Negara dengan jumlah produksi minyak terendah
          st.subheader("Negara dengan produksi minyak terendah pada tahun "+str(pilihanTahun))
          data_rendah =dataset_tahun[dataset_tahun["Tahun"] == pilihanTahun]
          data_rendah=data_rendah[data_rendah['Produksi']==data_rendah['Produksi'].min()]
          st.write(data_rendah)
          
          # Negara dengan jumlah produksi minyak 0
          st.subheader("Negara yang tidak memiliki produksi minyak pada tahun "+str(pilihanTahun))
          data = dataset[dataset["Tahun"] == pilihanTahun]
          data = data[data['Produksi'] == 0]
          hasil = data[['Negara','Tahun','Produksi','Kode','region','sub-region']]
          st.write(hasil)
