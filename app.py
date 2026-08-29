import streamlit as st
import plotly.graph_objects as go
from supabase import create_client
import time
import io
import csv

# ─── CONFIG ───────────────────────────────────────────────────────────
st.set_page_config(page_title="🧠 Bias Cognitivi — Dashboard Live", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# ─── CUSTOM CSS ───────────────────────────────────────────────────────
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main-title { font-size: 3rem; font-weight: 900; background: linear-gradient(135deg, #6C63FF 0%, #FF6584 50%, #FFA600 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.2rem; }
.sub-title { font-size: 1.2rem; color: #888; text-align: center; margin-bottom: 2rem; }
.metric-card { background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%); border-radius: 16px; padding: 1.5rem; text-align: center; border: 1px solid rgba(108, 99, 255, 0.3); box-shadow: 0 4px 20px rgba(108, 99, 255, 0.15); }
.metric-value { font-size: 3.5rem; font-weight: 900; margin: 0.5rem 0; }
.metric-label { font-size: 0.95rem; color: #aaa; text-transform: uppercase; letter-spacing: 2px; }
.diff-card { background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%); border-radius: 16px; padding: 1.5rem; text-align: center; border: 1px solid rgba(0, 255, 136, 0.3); animation: pulse 2s infinite; }
.diff-value { font-size: 3.5rem; font-weight: 900; color: #00FF88; margin: 0.5rem 0; }
.count-badge { display: inline-block; background: rgba(108, 99, 255, 0.2); color: #6C63FF; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 600; }
.wow-divider { height: 3px; background: linear-gradient(90deg, transparent, #6C63FF, #FF6584, transparent); border: none; margin: 2rem 0; border-radius: 2px; }
.info-box { background: rgba(108, 99, 255, 0.1); border-left: 4px solid #6C63FF; padding: 1rem 1.5rem; border-radius: 0 12px 12px 0; margin: 1rem 0; color: #ccc; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# ─── SUPABASE ─────────────────────────────────────────────────────────
@st.cache_resource
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = get_supabase()

# ─── ESPERIMENTI DEFINITI ─────────────────────────────────────────────
ESPERIMENTI = {
    # A/B
    "macchina": {"titolo": "1. 🚗 Incidente Auto / Car Crash (Loftus & Palmer)", "desc": "Parole: 'Urtate' vs 'Disintegrate' / 'Hit' vs 'Smashed'.", "gruppo_a": "Urtate / Hit", "gruppo_b": "Disintegrate / Smashed", "unita": "km/h", "tipo": "ab_num"},
    "asian_disease": {"titolo": "2. 🦠 Malattia Asiatica / Asian Disease (Kahneman)", "desc": "Framing: Vite salvate vs Morti certe / Saved vs Dead.", "gruppo_a": "Salvati / Saved", "gruppo_b": "Morti / Dead", "unita": "% Rischio / Risk (Prog B)", "tipo": "ab_cat", "val_map": {0: "Sicuro / Certain A", 1: "Rischio / Risk B"}},
    "framing_ai": {"titolo": "3. 🤖 Framing Medico AI / Medical AI Framing", "desc": "90 sopravvivono vs 10 muoiono / 90 survive vs 10 die.", "gruppo_a": "Sopravvivono / Survive", "gruppo_b": "Muoiono / Die", "unita": "% Approvazione / Approval", "tipo": "ab_cat", "val_map": {0: "No", 1: "Sì / Yes"}},
    "gandhi": {"titolo": "4. 👴 Ancoraggio Età Gandhi / Gandhi's Age Anchoring", "desc": "Ancora: 114 anni vs 35 anni / Anchor 114 vs 35.", "gruppo_a": "Ancora / Anchor 114", "gruppo_b": "Ancora / Anchor 35", "unita": "Età Stimata / Estimated Age", "tipo": "ab_num"},
    "roulette": {"titolo": "5. 🎰 Ancoraggio Roulette / Roulette Anchoring", "desc": "Ruota finta 12 vs 65 / Wheel spin 12 vs 65.", "gruppo_a": "Ruota / Wheel 12", "gruppo_b": "Ruota / Wheel 65", "unita": "% Diagnosi Errate / Misdiagnoses", "tipo": "ab_num"},
    "loss_aversion": {"titolo": "6. 💶 Avversione Perdite / Loss Aversion", "desc": "Effetto certezza: vincite vs perdite / Gains vs Losses.", "gruppo_a": "Vincita / Gain", "gruppo_b": "Perdita / Loss", "unita": "% Rischio / Risk Choice", "tipo": "ab_cat", "val_map": {0: "Sicuro / Sure", 1: "Azzardo / Gamble"}},
    "illusione_verita": {"titolo": "7. 👁️ Illusione di Verità / Truth Illusion", "desc": "Grassetto/Arial vs Sbiadito/Comic Sans / Clear vs Faded.", "gruppo_a": "Chiaro / Clear", "gruppo_b": "Sbiadito / Faded", "unita": "Verità Percepita (1-10)", "tipo": "ab_num"},
    "availability": {"titolo": "8. 🧠 Availability Heuristic (Schwarz et al., 1991)", "desc": "Elencare 6 vs 12 esempi / List 6 vs 12 examples.", "gruppo_a": "Elenca / List 6", "gruppo_b": "Elenca / List 12", "unita": "Assertività (1-10)", "tipo": "ab_num"},
    "linda": {"titolo": "9. 👩‍🦰 Problema di Linda / Linda Problem (Kahneman)", "desc": "Fallacia della Congiunzione / Conjunction Fallacy.", "gruppo_a": "Solo Cassiera / Bank Teller", "gruppo_b": "Cassiera + Femminista / Teller + Feminist", "unita": "% Probabilità / Probability", "tipo": "ab_num"},
    "halo_asch": {"titolo": "10. 👤 Effetto Alone / Halo Effect (Asch)", "desc": "Alan (Positivo primo) vs Ben (Negativo primo).", "gruppo_a": "Alan (Positivo)", "gruppo_b": "Ben (Negativo)", "unita": "Voto / Rating (1-10)", "tipo": "ab_num"},
    "endow_mug": {"titolo": "11. ☕ Effetto Dote Tazza / Mug Endowment (Thaler)", "desc": "Venditori vs Compratori / Sellers vs Buyers.", "gruppo_a": "Venditori / Sellers (Min €)", "gruppo_b": "Compratori / Buyers (Max €)", "unita": "Euro (€)", "tipo": "ab_num"},
    "endow_ai": {"titolo": "12. 💻 Effetto Dote AI / AI License Endowment", "desc": "Vendere vs Comprare Licenza AI / Sell vs Buy AI License.", "gruppo_a": "Venditori / Sellers (Min €)", "gruppo_b": "Compratori / Buyers (Max €)", "unita": "Euro (€)", "tipo": "ab_num"},
    "sunk_theater": {"titolo": "13. 🎭 Costi Sommersi Teatro / Theater Sunk Cost", "desc": "Biglietto 50€ vs Regalato 0€ / Paid €50 vs Gift €0.", "gruppo_a": "Pagato / Paid 50€", "gruppo_b": "Regalato / Free 0€", "unita": "% Va a Teatro / Goes", "tipo": "ab_cat", "val_map": {0: "A casa / Home", 1: "A Teatro / Theater"}},
    "sunk_ai": {"titolo": "14. 🏭 Costi Sommersi AI / AI Project Sunk Cost", "desc": "Investito poco (0a) vs molto (4a) / 0 yrs vs 4 yrs.", "gruppo_a": "Investito 0 anni / 0 yrs", "gruppo_b": "Investito 4 anni / 4 yrs", "unita": "% Continua / Continues", "tipo": "ab_cat", "val_map": {0: "Abbandona / Abandon", 1: "Continua / Continue"}},
    "default_organ": {"titolo": "15. 🫀 Effetto Default / Default Effect (Organ Donation)", "desc": "Modulo Opt-IN vs Opt-OUT / Opt-IN vs Opt-OUT form.", "gruppo_a": "Opt-IN", "gruppo_b": "Opt-OUT", "unita": "% Donatori / Donors", "tipo": "ab_cat", "val_map": {0: "NON Donatore / Non-Donor", 1: "Donatore / Donor"}},
    "priming": {"titolo": "16. 🍝 Priming Associativo / Associative Priming", "desc": "Parole cibo vs igiene / Food vs Cleanliness.", "gruppo_a": "Cibo / Food", "gruppo_b": "Igiene / Cleanliness", "unita": "% Scelta / Choice", "tipo": "ab_cat", "val_map": {0: "-", 1: "SAPORE/SOUP", 2: "SAPONE/SOAP"}},
    "dunning": {"titolo": "17. 🎓 Dunning-Kruger / Superiorità Percepita", "desc": "vs Colleghi vs Premio Nobel / vs Classmates vs Nobel.", "gruppo_a": "vs Colleghi / Classmates", "gruppo_b": "vs Premio Nobel", "unita": "% Superiore / Above Avg", "tipo": "ab_cat", "val_map": {0: "Nella/Sotto media", 1: "Sopra media / Above"}},
    "wysiati": {"titolo": "18. 👁️ WYSIATI Visivo / Visual WYSIATI (Bruner & Potter)", "desc": "Testo libero: prima impressione / Open text: first impression.", "gruppo_a": "Messa a fuoco fluida (8s)", "gruppo_b": "4 Frame discreti presi dal processo", "unita": "% Risposte / Responses", "tipo": "ab_cat", "val_map": {0: "Prima Impressione / Error", 1: "Idrante / Hydrant"}},
    "focalizzazione": {"titolo": "19. 😊 Illusione Focalizzazione / Focusing Illusion", "desc": "Ordine domande felicità / Happiness question order.", "gruppo_a": "Felicità -> Uscite", "gruppo_b": "Uscite -> Felicità", "unita": "Felicità / Happiness (1-10)", "tipo": "ab_num"},
    
    # SINGLE DEMOS
    "base_rate": {"titolo": "20. 🔬 Base Rate Neglect / Paradosso Diagnostico", "desc": "Test 95%, malattia 1% / 95% test, 1% base rate.", "tipo": "single_num", "unita": "Probabilità Stimata / Probability", "verita": 16},
    "decoy": {"titolo": "21. 🗞️ Decoy Effect / L'Esca (The Economist)", "desc": "Opzione esca / Decoy option.", "tipo": "single_cat", "val_map": {1: "Web Only", 2: "Print Only (ESCA/DECOY)", 3: "Web + Print"}},
    "regression": {"titolo": "22. 🧑‍✈️ Regressione alla Media / Regression to Mean", "desc": "Spiegazione causale vs statistica / Causal vs Statistical.", "tipo": "single_cat", "val_map": {1: "Causale / Causal", 2: "Statistica / Statistical"}},
    "wason_246": {"titolo": "23. 🧮 Bias di Conferma / Confirmation Bias (Wason 2-4-6)", "desc": "Trappola verifica ipotesi / Hypothesis testing trap.", "tipo": "single_cat", "val_map": {1: "Conferma / Confirmation (8-10-12)", 2: "Test Dispari / Odd (1-3-5)", 3: "Test Generico / Generic (1-2-3)", 4: "Falsificazione / Falsification (6-4-2)"}},
}

# ─── SIDEBAR ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Elenco")
    esperimento_sel = st.selectbox("Scegli esperimento:", options=list(ESPERIMENTI.keys()), format_func=lambda x: ESPERIMENTI[x]["titolo"])
    st.markdown("---")
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
    if st.button("🔄 Aggiorna ora"): st.rerun()
    st.markdown("---")
    
    @st.cache_data(ttl=5)
    def fetch_data(exp):
        return supabase.table("Risposte").select("*").eq("esperimento", exp).execute().data
    
    data = fetch_data(esperimento_sel)
    if data:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        st.download_button(label="📥 Scarica Dati (CSV)", data=output.getvalue().encode('utf-8'), file_name=f"risposte_{esperimento_sel}.csv", mime="text/csv", use_container_width=True)
    
    with st.expander("🗑️ Cancella risposte"):
        st.warning("Azione irreversibile!")
        conferma = st.text_input("Scrivi CANCELLA:")
        if st.button("Elimina", type="primary"):
            if conferma == "CANCELLA":
                supabase.table("Risposte").delete().eq("esperimento", esperimento_sel).execute()
                st.success("Cancellato!")
                st.rerun()

# ─── MAIN ─────────────────────────────────────────────────────────────
exp = ESPERIMENTI[esperimento_sel]
st.markdown(f'<h1 class="main-title">{exp["titolo"][4:]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{exp["desc"]}</p>', unsafe_allow_html=True)
st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)

if not data:
    st.markdown('<div class="info-box"><h3>📱 In attesa di risposte...</h3><p>Fai Scannerizzare il QR Code! I risultati appariranno in tempo reale.</p></div>', unsafe_allow_html=True)
else:
    # ─── A/B EXPERIMENTS ──────────────────────────────────────────────
    if exp["tipo"].startswith("ab"):
        val_a = [r["valore"] for r in data if r["gruppo"] == "A"]
        val_b = [r["valore"] for r in data if r["gruppo"] == "B"]
        
        # Metriche Medie
        media_a = sum(val_a)/len(val_a) if val_a else 0
        media_b = sum(val_b)/len(val_b) if val_b else 0
        diff = abs(media_a - media_b)
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="metric-card"><p class="metric-label">{exp.get("gruppo_a", "A")}</p><p class="metric-value" style="color:#6C63FF">{media_a:.1f}</p><span class="count-badge">📊 {len(val_a)} resp</span></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="diff-card"><p class="metric-label">Differenza</p><p class="diff-value">Δ {diff:.1f}</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><p class="metric-label">{exp.get("gruppo_b", "B")}</p><p class="metric-value" style="color:#FF6584">{media_b:.1f}</p><span class="count-badge">📊 {len(val_b)} resp</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        
        if exp["tipo"] == "ab_num":
            with c1:
                fA = go.Figure()
                fA.add_trace(go.Histogram(x=val_a, marker_color='#6C63FF'))
                fA.add_vline(x=media_a, line_dash="dash", line_color="#FFF")
                fA.update_layout(title=exp["gruppo_a"], template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fA, use_container_width=True)
            with c2:
                fB = go.Figure()
                fB.add_trace(go.Histogram(x=val_b, marker_color='#FF6584'))
                fB.add_vline(x=media_b, line_dash="dash", line_color="#FFF")
                fB.update_layout(title=exp["gruppo_b"], template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fB, use_container_width=True)
        
        elif exp["tipo"] == "ab_cat":
            map_dict = exp["val_map"]
            counts_a = {map_dict[k]: val_a.count(k) for k in map_dict}
            counts_b = {map_dict[k]: val_b.count(k) for k in map_dict}
            
            with c1:
                fA = go.Figure(data=[go.Pie(labels=list(counts_a.keys()), values=list(counts_a.values()), hole=.3, marker_colors=['#444', '#6C63FF'])])
                fA.update_layout(title=exp["gruppo_a"], template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fA, use_container_width=True)
            with c2:
                fB = go.Figure(data=[go.Pie(labels=list(counts_b.keys()), values=list(counts_b.values()), hole=.3, marker_colors=['#444', '#FF6584'])])
                fB.update_layout(title=exp["gruppo_b"], template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fB, use_container_width=True)

    # ─── SINGLE DEMOS ─────────────────────────────────────────────────
    else:
        vals = [r["valore"] for r in data]
        st.markdown(f'<div class="metric-card"><p class="metric-label">PARTECIPANTI TOTALI</p><p class="metric-value">{len(vals)}</p></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)
        
        if exp["tipo"] == "single_num":
            fig = go.Figure(data=[go.Histogram(x=vals, marker_color='#00FF88')])
            fig.update_layout(title="Distribuzione Risposte", template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
        elif exp["tipo"] == "single_cat":
            map_dict = exp["val_map"]
            counts = {map_dict[k]: vals.count(k) for k in map_dict}
            fig = go.Figure(data=[go.Pie(labels=list(counts.keys()), values=list(counts.values()), hole=.4, marker_colors=['#444', '#00FF88', '#6C63FF'])])
            fig.update_layout(title="Voti Classe", template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

if auto_refresh:
    time.sleep(5)
    st.rerun()
