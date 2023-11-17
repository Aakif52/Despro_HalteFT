import streamlit as st

from google.cloud import firestore
from google.oauth2 import service_account
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore import Query

import threading
from queue import Queue
from time import sleep

import json

class StringVar:
    DESPRO_COL = "test_collection"
    DISPLAY_DOC = "data"
    BIKUN_DOC = ""
    RAMAI_DOC = ""

NUM_QUERY = 10

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)
cb_done = threading.Event()
q = Queue()

col_ref = db.collection(StringVar.DESPRO_COL)

last_log_query = col_ref.order_by("timestamp", direction=Query.DESCENDING).limit(NUM_QUERY)



# doc_ref = db.collection(StringVar.DESPRO_COL).document(StringVar.DISPLAY_DOC)

# def on_snapshot(doc_snapshot, changes, read_time):
#     print(f"Listener triggered!")
#     q.put(doc_snapshot[0])
#     cb_done.set()


# doc_watch = doc_ref.on_snapshot(on_snapshot)

q_last_log = Queue()
q_logs_arr = []

def get_last_log(col):
    return col.to_dict()


def last_log_listener(col_snapshot, changes, read_time):
    global q_logs_arr
    q_last_log.put(col_snapshot[-1].to_dict())
    q_logs_arr = []
    for log in col_snapshot:
        # print(log.to_dict())
        q_logs_arr.append(log.to_dict())

    cb_done.set()

last_log_watch = last_log_query.on_snapshot(last_log_listener)
# arr = =[
#     {
#         'Bikun': False,
#         'Ramai': False
#         'timestamp': 'ddwdw'
#     },
    
#     {
#         'Bikun': True,
#         'Ramai': False
#         'timestamp': 'ddwdw'
#     },
# ]

# x = []
# y = []

# for e in arr:
#     x.append(e.get('timestamp'))
#     y.append(e.get('Bikun'))

placeholder = st.empty()
while True:
    # data = q.get()
    # print(data.to_dict())

    last_log = q_last_log.get()
    print(q_logs_arr)
    # print(last_log)
    placeholder.empty()

    with placeholder.container():
        bikun_state = "Ada bikun" if last_log.get("Bikun") else "Gak ada bikun"
        keramaian_state = "Ramai" if last_log("Ramai") else "Tidak ramai"
        st.header('Bikun Detector')
        st.subheader(f"Keberadaan Bikun")
        st.write(bikun_state)
        st.subheader(f"Keramaian Halte")
        st.write(keramaian_state)