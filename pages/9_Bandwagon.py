import streamlit as st
import random
from supabase import create_client

st.set_page_config(page_title="🐑 Bandwagon", page_icon="🐑", layout="centered")

NOME_ESPERIMENTO = "bandwagon"

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
    st.session_state.gruppo = random.choice(["A", "B"])
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.markdown('<h1 class="exp-title">🐑 Scelta del Prodotto</h1>', unsafe_allow_html=True)
st.markdown('<p class="exp-subtitle">Quale preferisci?</p>', unsafe_allow_html=True)

if not st.session_state.submitted:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    
    st.markdown("#### 🛍️ Due prodotti a confronto")
    st.markdown(
        "Stai scegliendo tra **due app di streaming musicale** "
        "con le stesse funzionalità e lo stesso prezzo."
    )
    
    if st.session_state.gruppo == "A":
        st.markdown("---")
        st.markdown(
            "> 📊 *Sondaggio recente: l'**87% degli utenti** preferisce l'App Alpha rispetto all'App Beta.*"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🅰️ App Alpha**")
        st.markdown("- Catalogo musicale ampio\n- Interfaccia moderna\n- 9.99€/mese")
    with col2:
        st.markdown("**🅱️ App Beta**")
        st.markdown("- Catalogo musicale ampio\n- Interfaccia moderna\n- 9.99€/mese")
    
    st.markdown("---")
    
    scelta = st.radio(
        "**Quale app scegli?**",
        ["🅰️ App Alpha", "🅱️ App Beta"],
        key="radio_app",
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("📨 Invia risposta", type="primary", use_container_width=True):
        valore = 1 if "Alpha" in scelta else 0
        supabase.table("Risposte").insert({
            "esperimento": NOME_ESPERIMENTO,
            "gruppo": st.session_state.gruppo,
            "valore": valore,
        }).execute()
        st.session_state.submitted = True
        st.rerun()
else:
    st.markdown("""
    <div class="thanks-box">
        <p class="thanks-emoji">🎉</p>
        <p class="thanks-text">Grazie per la tua risposta!</p>
        <p style="color: #aaa;">Le due app sono <strong>identiche</strong>... ma un gruppo ha visto un sondaggio! 📊</p>
    </div>
    """, unsafe_allow_html=True)
