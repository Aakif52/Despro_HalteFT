import streamlit as st
from streamlit_autorefresh import st_autorefresh

from google.cloud import firestore
from google.oauth2 import service_account

import threading
from queue import Queue

import json

class StringVar:
    BIKUN_COL = "Bikun"

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)
cb_done = threading.Event()
q = Queue()

doc_ref = db.collection(StringVar.BIKUN_COL).document("e52tYFjerfyvXiRk6AIm")

def on_snapshot(doc_snapshot, changes, read_time):
    print(f"Listener triggered!")
    q.put(doc_snapshot[0])
    cb_done.set()


doc_watch = doc_ref.on_snapshot(on_snapshot)

placeholder = st.empty()
while True:
    data = q.get()
    print(data.to_dict())
    placeholder.empty()

    with placeholder.container():
        bikun_state = "Ada bikun" if data.to_dict()["Ada Bikun"] else "Gak ada bikun"
        keramaian_state = "Ramai" if data.to_dict()["Ramai"] else "Tidak ramai"
        st.header('Bikun Detector')
        st.subheader(f"Keberadaan Bikun")
        st.write(bikun_state)
        st.subheader(f"Keramaian Halte")
        st.write(keramaian_state)