import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from alat.db import Database

st.set_page_config(
    page_title="PEMILU",
    page_icon="💪",  # You can use an emoji as the logo
    layout="wide",
)

if 'admin' not in st.session_state:

	col1,col2 = st.columns(2)
	col1.image('https://png.pngtree.com/png-vector/20221124/ourmid/pngtree-recruitment-job-for-social-media-admin-png-image_6478542.png')
	col2.title("Login Admin")
	
	us = "admin"
	pwd = "admin"
	username = col2.text_input("Username")
	password = col2.text_input("Password")
	if col2.button("Login"):
		if username == us and password == pwd:
			st.session_state.admin = True
			with st.spinner("Loading..."):
				time.sleep(2)
			st.rerun()
		else:
			st.warning("Password Salah",icon="⚠️")
else:
	st.markdown("<center><h1>DASHBOARD</h1></center>",unsafe_allow_html=True)
	st.title("Data Pemilih")
	db = Database("db.csv")
	df = db.read_records()
	st.write(df)
	
	fig, ax = plt.subplots()
	candidate_counts = df["kandidat"].value_counts()
	ax.pie(candidate_counts, labels=candidate_counts.index, autopct='%1.1f%%', startangle=90)
	ax.set_title('Data Kandidat')
	st.pyplot(fig)

	col1,col2 = st.columns(2)
	fig, ax = plt.subplots()
	provinsiCounts = df["provinsi"].value_counts()
	ax.bar(provinsiCounts.index,provinsiCounts)
	ax.set_title('Data Provinsi')
	col1.pyplot(fig)
	
	fig, ax = plt.subplots()
	genderCounts = df["gender"].value_counts()
	ax.bar(genderCounts.index,genderCounts,color=['pink','blue'])
	ax.set_title('Data Jenis kelamin')
	col2.pyplot(fig)

