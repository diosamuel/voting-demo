import streamlit as st
import pandas as pd
import time
from alat.db import Database
from st_clickable_images import clickable_images

st.set_page_config(
    page_title="PEMILU",
    page_icon="💪",  # You can use an emoji as the logo
    layout="wide",
)

if 'isVerif' not in st.session_state:
    st.session_state.isVerif = False

if 'isVoting' not in st.session_state:
    st.session_state.isVoting = False

class Voting:
	def __init__(self):
		self.nama = None
		self.nik = None
		self.calon = [{
			"nama":"Basuki Tjahaja Purnama",
			"foto":"https://upload.wikimedia.org/wikipedia/commons/d/dc/Gubernur_DKI_Basuki_TP_%E9%90%98%E8%90%AC%E5%AD%B8.jpg"
		},{
			"nama":"Anies Rasyid Baswedan",
			"foto":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Gubernur_Anies.jpg/1200px-Gubernur_Anies.jpg"
		},{
			"nama":"Megawati Soekarno Putri",
			"foto":"https://upload.wikimedia.org/wikipedia/commons/a/ac/Official_portrait_of_Megawati_Sukarnoputri.png"
		}]
		st.session_state.pilihan = None


	def Pemilih(self):
		self.nama = st.session_state.pemilih["nama"]
		self.nik = st.session_state.pemilih["nik"]

	def cekVerifikasi(self):
		return st.session_state.isVerif

	def cekVoting(self):
		return st.session_state.isVoting

	#Menampilkan foto kandidat agar dapat diklik
	def showKandidat(self):
		clicked = clickable_images([orang["foto"] for orang in self.calon],
    		div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap","gap":"10px"},
    		img_style={"height": "300px"})

		col1,col2,col3 = st.columns(3)
		col1.markdown(f"<center>{self.calon[0]['nama']}</center>",unsafe_allow_html=True)
		col2.markdown(f"<center>{self.calon[1]['nama']}</center>",unsafe_allow_html=True)
		col3.markdown(f"<center>{self.calon[2]['nama']}</center>",unsafe_allow_html=True)
		return clicked

	# Membuat tampilan voting
	def BuatVoting(self):
		if self.cekVerifikasi():
			self.Pemilih()
			st.markdown(f"<center><h2>Selamat datang di aplikasi Pemilu",unsafe_allow_html=True)
			st.markdown("<center><h3>Silahkan memilih kandidat</h3></center><br/>", unsafe_allow_html=True)
			kandidat = self.showKandidat()
			if kandidat >= 0:
				st.markdown(f"<br><h3><center>{self.calon[kandidat]['nama']}</center></h3>", unsafe_allow_html=True)
				tombolSubmit = st.empty()
				if tombolSubmit.button("Submit",use_container_width=True,type="primary"):
					db = Database("db.csv")
					df = db.read_records()
					userIndex = db.find_index_by_nik(self.nik)
					st.session_state.pemilih["kandidat"] = self.calon[int(kandidat)]["nama"]
					db.update_record(userIndex, st.session_state.pemilih)
					st.session_state.isVerif = False
					st.session_state.isVoting = True
					with st.spinner("Loading..."):
						time.sleep(2)
					st.rerun()

		else:
			if self.cekVoting():
				st.markdown("""<center>
					<img src="https://upload.wikimedia.org/wikipedia/commons/c/c6/Sign-check-icon.png" height=200/>
					<h1>Terimakasih, Sukses Voting!</h1>
					</center>""",unsafe_allow_html=True)
			else:
				st.markdown("""<center>
					<img src="https://www.pngall.com/wp-content/uploads/13/Red-X-PNG-Cutout.png" height=200/>
					<h1>Anda belum terverifikasi! Silahkan verifikasi terlebih dahulu</h1>
					</center>""",unsafe_allow_html=True)


Evote = Voting()
Evote.BuatVoting()

