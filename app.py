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
    "macchina": {"titolo": "1. 🚗 Falsi Ricordi (Loftus & Palmer)", "desc": "Parole estreme: 'Urtate' vs 'Disintegrate'.", "gruppo_a": "Urtate", "gruppo_b": "Disintegrate", "unita": "km/h", "tipo": "ab_num"},
    "asian_disease": {"titolo": "2. 🦠 Asian Disease (Framing Kahneman)", "desc": "La storica formula Vite salvate vs Morti certe.", "gruppo_a": "Salvati", "gruppo_b": "Morti", "unita": "% Rischio (Programma B)", "tipo": "ab_cat", "val_map": {0: "Sicuro A", 1: "Rischio B"}},
    "framing_ai": {"titolo": "3. 🤖 Framing Medico AI", "desc": "90 sopravvivono vs 10 muoiono.", "gruppo_a": "Sopravvivono", "gruppo_b": "Muoiono", "unita": "% Approvazione", "tipo": "ab_cat", "val_map": {0: "No", 1: "Sì"}},
    "gandhi": {"titolo": "4. 👴 Ancoraggio (Età Gandhi)", "desc": "L'ancora dei 114 anni vs 35 anni.", "gruppo_a": "Ancora 114", "gruppo_b": "Ancora 35", "unita": "Età Stimata", "tipo": "ab_num"},
    "roulette": {"titolo": "5. 🎰 Ancoraggio Medico (Roulette)", "desc": "Ruota finta 12 vs 65.", "gruppo_a": "Ruota su 12", "gruppo_b": "Ruota su 65", "unita": "% Diagnosi errate", "tipo": "ab_num"},
    "loss_aversion": {"titolo": "6. 💶 Avversione alle Perdite", "desc": "Effetto certezza: vincite vs perdite.", "gruppo_a": "Scenario: Vincita", "gruppo_b": "Scenario: Perdita", "unita": "% Sceglie il Rischio", "tipo": "ab_cat", "val_map": {0: "Sicuro", 1: "Azzardo"}},
    "illusione_verita": {"titolo": "7. 👁️ Illusione di Verità (Font)", "desc": "Grassetto/Arial vs Sbiadito/Comic Sans.", "gruppo_a": "Chiaro", "gruppo_b": "Sbiadito", "unita": "Verità Percepita (1-10)", "tipo": "ab_num"},
    "availability": {"titolo": "8. 🧠 Availability Heuristic", "desc": "Sforzo cognitivo: elencare 2 vs 12 esempi.", "gruppo_a": "Elenca 2", "gruppo_b": "Elenca 12", "unita": "Autovalutazione 1-10", "tipo": "ab_num"},
    "linda": {"titolo": "9. 👩‍🦰 Problema di Linda", "desc": "Fallacia della Congiunzione.", "gruppo_a": "Solo Cassiera", "gruppo_b": "Cassiera + Femminista", "unita": "% Probabilità stimata", "tipo": "ab_num"},
    "halo_asch": {"titolo": "10. 👤 Effetto Alone (Asch)", "desc": "Alan (Intelligente per primo) vs Ben (Invidioso per primo).", "gruppo_a": "Alan (Positivo)", "gruppo_b": "Ben (Negativo)", "unita": "Voto (1-10)", "tipo": "ab_num"},
    "endow_mug": {"titolo": "11. ☕ Effetto Dote (Tazza Thaler)", "desc": "Venditori vs Compratori.", "gruppo_a": "Venditori (Min €)", "gruppo_b": "Compratori (Max €)", "unita": "Euro (€)", "tipo": "ab_num"},
    "endow_ai": {"titolo": "12. 💻 Effetto Dote Medico", "desc": "Vendere vs Comprare Licenza AI.", "gruppo_a": "Venditori (Min €)", "gruppo_b": "Compratori (Max €)", "unita": "Euro (€)", "tipo": "ab_num"},
    "sunk_theater": {"titolo": "13. 🎭 Costi Sommersi (Teatro Kahneman)", "desc": "Biglietto pagato a caro prezzo vs biglietto regalato.", "gruppo_a": "Pagato 50€", "gruppo_b": "Regalato 0€", "unita": "% Andrebbe a teatro", "tipo": "ab_cat", "val_map": {0: "Resta a casa", 1: "Va a Teatro"}},
    "sunk_ai": {"titolo": "14. 🏭 Costi Sommersi (Progetto AI)", "desc": "Nessun investimento vs 4 anni di fatica.", "gruppo_a": "Investito poco (0 anni)", "gruppo_b": "Investito molto (4 anni)", "unita": "% Continuerà", "tipo": "ab_cat", "val_map": {0: "Abbandona", 1: "Continua"}},
    "default_organ": {"titolo": "15. 🫀 Effetto Default (Organ Donation)", "desc": "Scelta opt-in vs opt-out nel modulo.", "gruppo_a": "Opt-IN (Deve spuntare per aderire)", "gruppo_b": "Opt-OUT (Deve spuntare per NON aderire)", "unita": "% Efficace Donatore", "tipo": "ab_cat", "val_map": {0: "NON Donatore", 1: "DIVENTA Donatore"}},
    "priming": {"titolo": "16. 🍝 Priming (Associativo)", "desc": "Cibo vs Detersivo.", "gruppo_a": "Pausa Pranzo", "gruppo_b": "Pausa Doccia", "unita": "% Scelta", "tipo": "ab_cat", "val_map": {0: "-", 1: "SAPORE/SOUP", 2: "SAPONE/SOAP"}},
    "dunning": {"titolo": "17. 🎓 Illusione di Superiorità", "desc": "Confronti tra coetanei vs confronto limite.", "gruppo_a": "vs Colleghi", "gruppo_b": "vs Premio Nobel", "unita": "% Si sente Superiore", "tipo": "ab_cat", "val_map": {0: "Uguale/Inf", 1: "Sopra Media"}},
    "wysiati": {"titolo": "18. ⚖️ WYSIATI", "desc": "Testimonianze parziali vs piene e sicurezza.", "gruppo_a": "Difesa", "gruppo_b": "Difesa+Accusa", "unita": "Colpevolezza", "tipo": "ab_num"},
    
    # SINGLE DEMOS
    "base_rate": {"titolo": "19. 🔬 Base Rate Neglect (Paradosso Medico)", "desc": "Test al 95%, malattia all'1% (Vero: 16%).", "tipo": "single_num", "unita": "Probabilità Stimata", "verita": 16},
    "decoy": {"titolo": "20. 🗞️ Decoy Effect (L'Esca)", "desc": "L'opzione inutile per pilotare verso la costosa.", "tipo": "single_cat", "val_map": {1: "Solo Web", 2: "Solo Carta (ESCA)", 3: "Entrambi"}},
    "regression": {"titolo": "21. 🧑‍✈️ Regressione alla Media", "desc": "Istinto causale vs Istinto statistico (Lode/Castighi).", "tipo": "single_cat", "val_map": {1: "Causale (Psicologica)", 2: "Statistica (Regressione)"}},
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
