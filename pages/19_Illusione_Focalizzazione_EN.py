import streamlit as st
import random
import base64
import os
import streamlit.components.v1 as components
from supabase import create_client

st.set_page_config(page_title="Wellbeing Survey", page_icon="😊", layout="centered")

NOME_ESPERIMENTO = "focalizzazione"

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.question-card { background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%); border-radius: 20px; padding: 2rem; border: 1px solid rgba(108, 99, 255, 0.3); box-shadow: 0 8px 32px rgba(108, 99, 255, 0.2); margin: 1rem 0; }
.exp-title { font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #6C63FF, #FF6584); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.5rem; }
.exp-subtitle { color: #888; text-align: center; font-size: 1rem; margin-bottom: 1.5rem; }
.thanks-box { background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(0, 255, 136, 0.3); box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2); }
.thanks-emoji { font-size: 4rem; }
.thanks-text { color: #00FF88; font-size: 1.5rem; font-weight: 700; }

#MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

@st.cache_resource
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def load_hydrant_b64():
    candidates = [
        'fire_hydrant.jpg',
        os.path.join(os.path.dirname(__file__), '..', 'fire_hydrant.jpg'),
        os.path.join(os.path.dirname(__file__), 'fire_hydrant.jpg')
    ]
    for c in candidates:
        if os.path.exists(c):
            with open(c, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
    return ''

@st.cache_resource
def get_group_counter():
    return {"count": 0}

def get_next_group():
    c = get_group_counter()
    c["count"] += 1
    return "A" if c["count"] % 2 == 1 else "B"

if "gruppo" not in st.session_state:
    if "g" in st.query_params and st.query_params["g"] in ["A", "B"]:
        st.session_state.gruppo = st.query_params["g"]
    else:
        st.session_state.gruppo = get_next_group()

if NOME_ESPERIMENTO not in st.session_state:
    st.session_state[NOME_ESPERIMENTO] = False

st.markdown("""<h1 class="exp-title">😊 Life Satisfaction Survey</h1>""", unsafe_allow_html=True)
st.markdown("""<p class="exp-subtitle">Please answer the questions below</p>""", unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:

    if st.session_state.gruppo == "A":
        st.markdown("""**1. How happy are you with your life (1-10)?**""")
        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1a')
        eta = st.number_input('2. How many dates did you go on in the last month?', 0, 30, value=None, key='n1b')

    else:
        eta = st.number_input('1. How many dates did you go on in the last month?', 0, 30, value=None, key='n2a')
        st.markdown("""**2. How happy are you with your life (1-10)?**""")
        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2b')


    
    if st.button("📨 Submit response", type="primary", use_container_width=True):
        can_submit = True
        for var_name in ['scelta', 'val', 'eta', 'colpa', 'vetri', 'fiducia']:
            if var_name in locals() and locals()[var_name] is None:
                st.warning("⚠️ Please answer the question before submitting.")
                can_submit = False
                break
        
        if can_submit:
            supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()

            st.session_state[NOME_ESPERIMENTO] = True
            st.rerun()
else:
    st.markdown('''<div class="thanks-box"><p class="thanks-emoji">🎉</p><p class="thanks-text">Thank you for participating!</p></div>''', unsafe_allow_html=True)
