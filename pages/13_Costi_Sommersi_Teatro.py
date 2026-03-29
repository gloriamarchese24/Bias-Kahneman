import streamlit as st
import random
from supabase import create_client

st.set_page_config(page_title="Spettacolo", page_icon="🎭", layout="centered")

NOME_ESPERIMENTO = "sunk_theater"

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

st.markdown('<h1 class="exp-title">🎭 Lo Spettacolo a Teatro</h1>', unsafe_allow_html=True)
st.markdown('<p class="exp-subtitle">Rispondi alle domande qui sotto</p>', unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)

    if st.session_state.gruppo == "A":
        st.markdown('**Scenario:** Hai acquistato a tue spese un biglietto da 50€ per vedere uno spettacolo teatrale che ti interessava.')
        st.markdown('Arriva la sera dello spettacolo ma c\'è una tormenta di neve spaventosa. Andare a teatro richiede di mettersi alla guida sulla neve per 40 minuti, sfidando il pericolo e il freddo estremo.')
        st.markdown('---')
        scelta = st.radio('Cosa decidi di fare?', ['A) Vado a teatro lo stesso (sfido la tormenta per non buttare i 50€).', 'B) Resto a casa al caldo rinunciando allo spettacolo e ai 50€.'], key='r1')

    else:
        st.markdown('**Scenario:** Un amico ti ha **regalato** stasera un biglietto per vedere uno spettacolo teatrale che ti interessava (costo per te: 0€).')
        st.markdown('Arriva la sera dello spettacolo ma c\'è una tormenta di neve spaventosa. Andare a teatro richiede di mettersi alla guida sulla neve per 40 minuti, sfidando il pericolo e il freddo estremo.')
        st.markdown('---')
        scelta = st.radio('Cosa decidi di fare?', ['A) Vado a teatro lo stesso (sfido la tormenta per non buttare il regalo).', 'B) Resto a casa al caldo rinunciando allo spettacolo.'], key='r2')

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("📨 Invia risposta", type="primary", use_container_width=True):
        v = 1 if 'Vado' in scelta else 0
        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()

        st.session_state[NOME_ESPERIMENTO] = True
        st.rerun()
else:
    st.markdown('''<div class="thanks-box"><p class="thanks-emoji">🎉</p><p class="thanks-text">Grazie per la tua risposta!</p><p style="color: #aaa;">I risultati appariranno sulla dashboard del professore.</p></div>''', unsafe_allow_html=True)
