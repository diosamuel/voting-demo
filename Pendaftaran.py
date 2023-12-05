import streamlit as st
import pandas as pd
import time
import cv2
from datetime import datetime
from alat.db import Database
# import random
# randnumber = random.randint(1, 100)
st.set_page_config(
    page_title="PEMILU",
    page_icon="💪",  # You can use an emoji as the logo
    layout="wide",
)

st.sidebar.title("Pemilihan Umum")
st.sidebar.write("Pemilu adalah singkatan dari Pemilihan Umum, yang merupakan suatu proses dimana warga negara suatu negara memberikan suara mereka untuk memilih para wakil mereka dalam pemerintahan. Pemilu merupakan salah satu prinsip dasar demokrasi yang memungkinkan rakyat untuk berpartisipasi dalam menentukan pemimpin dan kebijakan negara.")

class RegistrasiVoting:
	def __init__(self):
		self.ProvinsiIndonesia = ['Aceh', 'Sumatera Barat', 'Yogyakarta', 'Sumatera Utara', 'Bangka-Belitung', 'Papua Barat', 'Jawa Timur', 'Kalimantan Barat', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kepulauan Riau', 'Lampung', 'Maluku', 'Maluku Utara', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Papua', 'Riau', 'Sulawesi Selatan', 'Bengkulu', 'Sulawesi Tengah', 'Sulawesi Utara', 'Sulawesi Tenggara', 'Bali', 'Banten', 'Gorontalo', 'Jakarta Raya', 'Jambi', 'Jawa Barat', 'Jawa Tengah', 'Kalimantan Tengah', 'Sulawesi Barat', 'Sumatera Selatan', 'Kalimantan Utara']
		if 'pemilih' not in st.session_state:
			st.session_state.isVerif = False
			st.session_state.kamera = None
			st.session_state["pemilih"] = {
				"nama":None,
				"nik":None,
				"waktu":None,
				"gender":None,
				"provinsi":None,
			}
			self.nama = None
			self.nik = None
			self.waktu = None
			self.gender = None
			self.provinsi = None
			self.kamera = None
		else:
			self.nama = st.session_state["pemilih"]["nama"]
			self.nik = st.session_state["pemilih"]["nik"]
			self.waktu = st.session_state["pemilih"]["waktu"]
			self.gender = st.session_state["pemilih"]["gender"]
			self.provinsi = st.session_state["pemilih"]["provinsi"]
			self.kamera = st.session_state.kamera

		self.temp_con = None

	#setter verifikasi
	def sudahVerifikasi(self):
		st.session_state['isVerif'] = True

	#getter verifikasi
	def apakahTerverifikasi(self):
		return st.session_state['isVerif']

	def batalVerifikasi(self):
		st.session_state['isVerif'] = False

	def tampilBiodata(self):
		st.success("Sukses mendaftar!")
		st.header("Biodata")
		st.write(f"Nama : {self.nama}")
		st.write(f"NIK : {self.nik}")
		st.write(f"Kelamin : {self.gender}")
		st.write(f"Provinsi : {self.provinsi}")
		st.write(f"Waktu : {self.waktu}")

		#img detection
		imagePath = 'test.jpg'
		img = cv2.imread(imagePath)
		img_with_faces = detect_faces(img)
		st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Wajah Pemilih")
		# st.image(self.kamera)

	# Layouting
	def buatFormulir(self):
		self.temp_con={
			"nama":st.empty(),
			"nik":st.empty(),
			"gender":st.empty(),
			"provinsi":st.empty(),
			"camera":st.empty(),
			"tombol":st.empty()
		}

		formContainer = {
			"nama":self.temp_con["nama"].text_input('Nama Lengkap'),
			"nik":self.temp_con["nik"].number_input('NIK'),
			"gender":self.temp_con["gender"].selectbox("Jenis kelamin",["Laki-Laki","Perempuan"]),
			"provinsi":self.temp_con["provinsi"].selectbox("Pilih Provinsi",self.ProvinsiIndonesia),
			"camera":self.temp_con["camera"].camera_input("Verifikasi Wajah"),
			"tombol":self.temp_con["tombol"].button("Verifikasi",use_container_width=True,type="primary")
		}

		return formContainer

	#hapus semua element
	def hapusContainer(self):
		for i in self.temp_con:
			self.temp_con[i].empty()

	def aturFormulir(self,container):
		if self.apakahTerverifikasi():
			self.hapusContainer()
			self.tampilBiodata()
		else:
			self.nama = container["nama"]
			self.nik = container["nik"]
			self.kamera = container["camera"]
			self.gender = container["gender"]
			self.provinsi = container["provinsi"]
			self.waktu = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			tombolVerifikasi = container["tombol"]
			if tombolVerifikasi and self.kamera and self.nama and self.nik:
				st.session_state["pemilih"] = {
					"nama":self.nama,
					"nik":self.nik,
					"waktu":self.waktu,
					"gender":self.gender,
					"provinsi":self.provinsi,
				}

				st.session_state.kamera = self.kamera

				with open('test.jpg','wb') as file:
					file.write(self.kamera.getbuffer())
				imagePath = 'test.jpg'
				img = cv2.imread(imagePath)
				img_with_faces = detect_faces(img)

				if img_with_faces["isVerified"]:
					time.sleep(1)
					#hapus semua element
					self.sudahVerifikasi()
					self.hapusContainer()
					self.tampilBiodata()
				else:
					st.warning("Wajah tidak terdeteksi, silakan foto ulang")


def detect_faces(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return {
        "image":image,
        "isVerified":bool(len(faces))
    }

# Layout
st.title("Pendaftaran E-Voting Pemilu")
Pemilu = RegistrasiVoting()
formulir = Pemilu.buatFormulir()

Pemilu.aturFormulir(formulir)

