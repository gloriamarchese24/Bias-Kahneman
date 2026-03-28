import streamlit as st
import random
from supabase import create_client

st.set_page_config(page_title="✈️ Disponibilità", page_icon="✈️", layout="centered")

NOME_ESPERIMENTO = "disponibilita"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.question-card {
    background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%);
    border-radius: 20px; padding: 2rem;
    border: 1px solid rgba(108, 99, 255, 0.3);
    box-shadow: 0 8px 32px rgba(108, 99, 255, 0.2); margin: 1rem 0;
}
.exp-title {
    font-size: 2rem; font-weight: 900;
    background: linear-gradient(135deg, #6C63FF, #FF6584);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: 0.5rem;
}
.exp-subtitle { color: #888; text-align: center; font-size: 1rem; margin-bottom: 1.5rem; }
.thanks-box {
    background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%);
    border-radius: 20px; padding: 2rem; text-align: center;
    border: 1px solid rgba(0, 255, 136, 0.3);
    box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2);
}
.thanks-emoji { font-size: 4rem; }
.thanks-text { color: #00FF88; font-size: 1.5rem; font-weight: 700; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = get_supabase()

if "gruppo" not in st.session_state:
    try:
        res = supabase.table("Risposte").select("gruppo").eq("esperimento", NOME_ESPERIMENTO).execute()
        gruppi = [r["gruppo"] for r in res.data]
        count_a = gruppi.count("A")
        count_b = gruppi.count("B")
        
        # Assegna al gruppo con meno persone (bilanciamento perfetto)
        if count_a <= count_b:
            st.session_state.gruppo = "A"
        else:
            st.session_state.gruppo = "B"
    except Exception:
        # Fallback di sicurezza in caso di disconnessione momentanea
        st.session_state.gruppo = random.choice(["A", "B"])
if NOME_ESPERIMENTO not in st.session_state:
    st.session_state[NOME_ESPERIMENTO] = False

st.markdown('<h1 class="exp-title">✈️ Percezione del Rischio</h1>', unsafe_allow_html=True)
st.markdown('<p class="exp-subtitle">Quanto è pericoloso volare?</p>', unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    
    if st.session_state.gruppo == "A":
        st.markdown("#### 📰 Notizia recente")
        st.markdown(
            "> *\"Tragedia nei cieli: aereo precipitato ieri in Asia con 180 passeggeri a bordo. "
            "Le cause sono ancora in fase di indagine. È il terzo incidente aereo quest'anno.\"*"
        )
    else:
        st.markdown("#### 📊 Dati statistici")
        st.markdown(
            "> *Secondo i dati IATA, nel 2024 il tasso di incidenti aerei è stato di "
            "0.03 per milione di voli, rendendo l'aereo il mezzo di trasporto più sicuro al mondo.*"
        )
    
    st.markdown("---")
    st.markdown("**Secondo te, quanto è pericoloso viaggiare in aereo rispetto all'auto?**")
    st.markdown("0 = l'aereo è molto più sicuro, 100 = l'aereo è molto più pericoloso")
    
    rischio = st.slider(
        "La tua percezione di rischio aereo:",
        min_value=0, max_value=100, value=50, step=5,
        key="slider_rischio",
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("📨 Invia risposta", type="primary", use_container_width=True):
        supabase.table("Risposte").insert({
            "esperimento": NOME_ESPERIMENTO,
            "gruppo": st.session_state.gruppo,
            "valore": rischio,
        }).execute()
        st.session_state[NOME_ESPERIMENTO] = True
        st.rerun()
else:
    st.markdown("""
    <div class="thanks-box">
        <p class="thanks-emoji">🎉</p>
        <p class="thanks-text">Grazie per la tua risposta!</p>
        <p style="color: #aaa;">Statisticamente, l'aereo è <strong>95 volte più sicuro</strong> dell'auto! ✈️</p>
    </div>
    """, unsafe_allow_html=True)
