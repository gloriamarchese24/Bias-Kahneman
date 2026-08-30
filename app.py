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
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = get_supabase()

# ─── ESPERIMENTI DEFINITI ─────────────────────────────────────────────
ESPERIMENTI = {
    # A/B
    "macchina": {"titolo": "1. 🚗 Car Crash Experiment (Loftus & Palmer)", "desc": "Wording effect: 'Hit' vs 'Smashed'.", "gruppo_a": "Hit", "gruppo_b": "Smashed", "unita": "km/h", "tipo": "ab_num"},
    "asian_disease": {"titolo": "2. 🦠 The Asian Disease Problem (Kahneman)", "desc": "Framing: Lives saved vs Certain deaths.", "gruppo_a": "Lives Saved", "gruppo_b": "Certain Deaths", "unita": "% Risk Choice (Program B)", "tipo": "ab_cat", "val_map": {0: "Certain (Program A)", 1: "Risk (Program B)"}},
    "framing_ai": {"titolo": "3. 🤖 Medical AI Software Framing", "desc": "90 survive vs 10 die.", "gruppo_a": "90 Survive", "gruppo_b": "10 Die", "unita": "% Approval", "tipo": "ab_cat", "val_map": {0: "Reject AI", 1: "Authorize AI"}},
    "gandhi": {"titolo": "4. 👴 Gandhi's Age Anchoring", "desc": "High anchor (114 yrs) vs Low anchor (35 yrs).", "gruppo_a": "Anchor 114", "gruppo_b": "Anchor 35", "unita": "Estimated Age (years)", "tipo": "ab_num"},
    "roulette": {"titolo": "5. 🎰 Hospital Misdiagnoses Anchoring", "desc": "Wheel spin 12 vs 65.", "gruppo_a": "Wheel Spin 12", "gruppo_b": "Wheel Spin 65", "unita": "% Misdiagnoses", "tipo": "ab_num"},
    "loss_aversion": {"titolo": "6. 💶 Loss Aversion (Kahneman & Tversky)", "desc": "Certainty effect: Gains vs Losses.", "gruppo_a": "Gain Scenario", "gruppo_b": "Loss Scenario", "unita": "% Risk Choice", "tipo": "ab_cat", "val_map": {0: "Sure Option", 1: "Gamble"}},
    "illusione_verita": {"titolo": "7. 👁️ Truth Illusion & Cognitive Fluency", "desc": "Bold/Arial vs Faded/Comic Sans.", "gruppo_a": "Clear Font (Bold/Arial)", "gruppo_b": "Faded Font (Comic Sans)", "unita": "Perceived Validity (1-10)", "tipo": "ab_num"},
    "availability": {"titolo": "8. 🧠 Availability Heuristic (Schwarz et al., 1991)", "desc": "Cognitive retrieval effort: List 6 vs 12 examples.", "gruppo_a": "List 6 Examples", "gruppo_b": "List 12 Examples", "unita": "Self-Rated Assertiveness (1-10)", "tipo": "ab_num"},
    "linda": {"titolo": "9. 👩‍🦰 Linda Problem (Conjunction Fallacy)", "desc": "Probability estimation.", "gruppo_a": "Bank Teller Only", "gruppo_b": "Bank Teller + Feminist", "unita": "% Estimated Probability", "tipo": "ab_num"},
    "halo_asch": {"titolo": "10. 👤 Halo Effect (Asch, 1946)", "desc": "Alan (Intelligent first) vs Ben (Envious first).", "gruppo_a": "Alan (Positive First)", "gruppo_b": "Ben (Negative First)", "unita": "Rating (1-10)", "tipo": "ab_num"},
    "endow_mug": {"titolo": "11. ☕ Mug Endowment Effect (Thaler)", "desc": "Sellers vs Buyers valuation.", "gruppo_a": "Sellers (Min € Price)", "gruppo_b": "Buyers (Max € Price)", "unita": "Price (€)", "tipo": "ab_num"},
    "endow_ai": {"titolo": "12. 💻 Medical AI License Endowment", "desc": "Sell vs Buy AI License.", "gruppo_a": "Sellers (Min € Price)", "gruppo_b": "Buyers (Max € Price)", "unita": "Price (€)", "tipo": "ab_num"},
    "sunk_theater": {"titolo": "13. 🎭 Theater Ticket Sunk Cost", "desc": "Paid €50 ticket vs Free €0 ticket.", "gruppo_a": "Paid €50", "gruppo_b": "Gift €0", "unita": "% Going to Theater", "tipo": "ab_cat", "val_map": {0: "Stay Home", 1: "Go to Theater"}},
    "sunk_ai": {"titolo": "14. 🏭 AI Research Project Sunk Cost", "desc": "Invested 0 yrs vs 4 yrs.", "gruppo_a": "Invested 0 Yrs", "gruppo_b": "Invested 4 Yrs", "unita": "% Continuing Project", "tipo": "ab_cat", "val_map": {0: "Abandon Project", 1: "Continue Project"}},
    "default_organ": {"titolo": "15. 🫀 Default Effect (Organ Donation)", "desc": "Opt-IN vs Opt-OUT enrollment form.", "gruppo_a": "Opt-IN Form", "gruppo_b": "Opt-OUT Form", "unita": "% Effective Donors", "tipo": "ab_cat", "val_map": {0: "Non-Donor", 1: "Organ Donor"}},
    "priming": {"titolo": "16. 🍝 Associative Priming", "desc": "Food prime vs Shower prime.", "gruppo_a": "Food Prime", "gruppo_b": "Shower Prime", "unita": "% Word Completion", "tipo": "ab_cat", "val_map": {0: "Other", 1: "SOUP", 2: "SOAP"}},
    "dunning": {"titolo": "17. 🎓 Dunning-Kruger Effect / Overconfidence", "desc": "Peer comparison vs Nobel laureate comparison.", "gruppo_a": "vs Classmates", "gruppo_b": "vs Nobel Laureate", "unita": "% Perceived Superior", "tipo": "ab_cat", "val_map": {0: "Average / Below", 1: "Above Average"}},
    "wysiati": {"titolo": "18. 👁️ Visual WYSIATI (Bruner & Potter, 1964)", "desc": "Open text unguided first impression.", "gruppo_a": "Continuous Fluid Unblurring (8s)", "gruppo_b": "4 Discrete Step Frames", "unita": "% Responses", "tipo": "ab_cat", "val_map": {0: "Initial Wrong Impression", 1: "Fire Hydrant / Extinguisher"}},
    "focalizzazione": {"titolo": "19. 😊 Focusing Illusion (Kahneman)", "desc": "Order of happiness questions.", "gruppo_a": "Happiness -> Dating", "gruppo_b": "Dating -> Happiness", "unita": "Happiness Rating (1-10)", "tipo": "ab_num"},
    
    # SINGLE DEMOS
    "base_rate": {"titolo": "20. 🔬 Base Rate Neglect (Medical Paradox)", "desc": "95% test accuracy, 1% prevalence (True: 16%).", "tipo": "single_num", "unita": "Estimated Probability (%)", "verita": 16},
    "decoy": {"titolo": "21. 🗞️ Decoy Effect (The Economist)", "desc": "Asymmetric dominance decoy option.", "tipo": "single_cat", "val_map": {1: "Web Only ($50)", 2: "Print Only ($120 - DECOY)", 3: "Web + Print ($120)"}},
    "regression": {"titolo": "22. 🧑‍✈️ Regression to the Mean", "desc": "Causal vs Statistical explanation.", "tipo": "single_cat", "val_map": {1: "Causal (Psychological)", 2: "Statistical (Regression)"}},
    "wason_246": {"titolo": "23. 🧮 Confirmation Bias (Wason 2-4-6 Task)", "desc": "Hypothesis testing trap (Wason, 1960).", "tipo": "single_cat", "val_map": {1: "Confirmation (8 - 10 - 12)", 2: "Test Odd (1 - 3 - 5)", 3: "Test Generic (1 - 2 - 3)", 4: "Falsification (6 - 4 - 2)"}},
}

# ─── SIDEBAR ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Elenco")
    esperimento_sel = st.selectbox("Scegli esperimento:", options=list(ESPERIMENTI.keys()), format_func=lambda x: ESPERIMENTI[x]["titolo"])
    st.markdown("---")
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
    if st.button("🔄 Aggiorna ora"): st.rerun()
    st.markdown("---")
    
    @st.cache_data(ttl=3)
    def fetch_data(exp):
        try:
            res_reset = supabase.table("Risposte").select("created_at").eq("esperimento", exp + "_reset").order("created_at", desc=True).limit(1).execute()
            if res_reset.data:
                latest_reset = res_reset.data[0]["created_at"]
                return supabase.table("Risposte").select("*").eq("esperimento", exp).gt("created_at", latest_reset).execute().data
        except Exception:
            pass
        return supabase.table("Risposte").select("*").eq("esperimento", exp).execute().data
    
    data = fetch_data(esperimento_sel)
    if data:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        st.download_button(label="📥 Scarica Dati (CSV)", data=output.getvalue().encode('utf-8'), file_name=f"risposte_{esperimento_sel}.csv", mime="text/csv", use_container_width=True)
    
    with st.expander("🗑️ Cancella Risposte / Clear Data"):
        st.warning("⚠️ Azione Irreversibile / Irreversible Action")
        chk = st.checkbox("Confermo cancellazione / Confirm deletion", key="del_chk")
        if st.button("🗑️ CANCELLA ORA / DELETE NOW", type="primary", use_container_width=True):
            if chk:
                try:
                    supabase.table("Risposte").insert({"esperimento": esperimento_sel + "_reset", "gruppo": "RESET", "valore": 0}).execute()
                    if esperimento_sel == "macchina":
                        supabase.table("Risposte").insert({"esperimento": "macchina_vetri_reset", "gruppo": "RESET", "valore": 0}).execute()
                except Exception:
                    pass
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("✅ Risposte cancellate con successo!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Spunta la casella di conferma sopra!")

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
