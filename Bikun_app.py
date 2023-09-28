import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

# db = firestore.Client.from_service_account_json("firestore-key.json.json")
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

doc_ref = db.collection("Bikun").document("e52tYFjerfyvXiRk6AIm")

doc = doc_ref.get()

st.header('Bikun Detector')

st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())