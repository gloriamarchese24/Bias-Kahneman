import streamlit as st
import random
import base64
import os
from supabase import create_client

st.set_page_config(page_title="Profile Evaluation", page_icon="👩‍🦰", layout="centered")

NOME_ESPERIMENTO = "linda"

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

supabase = get_supabase()

if "gruppo" not in st.session_state:
    try:
        res = supabase.table("Risposte").select("gruppo").eq("esperimento", NOME_ESPERIMENTO).execute()
        gruppi = [r["gruppo"] for r in res.data]
        st.session_state.gruppo = "A" if gruppi.count("A") <= gruppi.count("B") else "B"
    except Exception:
        st.session_state.gruppo = random.choice(["A", "B"])

if NOME_ESPERIMENTO not in st.session_state:
    st.session_state[NOME_ESPERIMENTO] = False

st.markdown("""<h1 class="exp-title">👩‍🦰 Linda's Profile</h1>""", unsafe_allow_html=True)
st.markdown("""<p class="exp-subtitle">Please answer the questions below</p>""", unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
    st.markdown("""**Profile:** Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice, and also participated in anti-nuclear demonstrations.""")
    st.markdown("""---""")

    if st.session_state.gruppo == "A":
        val = st.number_input('In light of her description, what is the probability (0-100%) that Linda is today **a bank teller**?', 0, 100, value=None, key='s1')

    else:
        val = st.number_input('In light of her description, what is the probability (0-100%) that Linda is today **a bank teller and active in the feminist movement**?', 0, 100, value=None, key='s2')


    
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
