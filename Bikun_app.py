import streamlit as st
from streamlit_autorefresh import st_autorefresh

from google.cloud import firestore
from google.oauth2 import service_account

import json

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

doc_ref = db.collection("Bikun").document("e52tYFjerfyvXiRk6AIm")
doc_ref2 = db.collection("Keramaian").document("KsTOlpqVJmt2bmrDRlsv")

st_autorefresh(interval = 60 * 1000, key="dataframerefresh")

doc = doc_ref.get()
doc2 = doc_ref2.get()

st.header('Bikun Detector')

st.subheader(f"Keberadaan Bikun")

st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())

st.subheader(f"Keramaian Halte")

st.write("The id is: ", doc2.id)
st.write("The contents are: ", doc2.to_dict())