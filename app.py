import streamlit as st
import plotly.graph_objects as go
from supabase import create_client
import time

# ─── CONFIG ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🧠 Bias Cognitivi — Dashboard Live",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Titolo principale con gradiente */
.main-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6C63FF 0%, #FF6584 50%, #FFA600 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}

.sub-title {
    font-size: 1.2rem;
    color: #888;
    text-align: center;
    margin-bottom: 2rem;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(108, 99, 255, 0.3);
    box-shadow: 0 4px 20px rgba(108, 99, 255, 0.15);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(108, 99, 255, 0.3);
}

.metric-value {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 0.5rem 0;
}

.metric-label {
    font-size: 0.95rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.group-a-color { color: #6C63FF; }
.group-b-color { color: #FF6584; }

/* Differenza animata */
.diff-card {
    background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(0, 255, 136, 0.3);
    box-shadow: 0 4px 20px rgba(0, 255, 136, 0.15);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 4px 20px rgba(0, 255, 136, 0.15); }
    50% { box-shadow: 0 8px 40px rgba(0, 255, 136, 0.4); }
}

.diff-value {
    font-size: 3.5rem;
    font-weight: 900;
    color: #00FF88;
    margin: 0.5rem 0;
}

/* Counter badge */
.count-badge {
    display: inline-block;
    background: rgba(108, 99, 255, 0.2);
    color: #6C63FF;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
}

/* Separatore */
.wow-divider {
    height: 3px;
    background: linear-gradient(90deg, transparent, #6C63FF, #FF6584, transparent);
    border: none;
    margin: 2rem 0;
    border-radius: 2px;
}

/* Info box */
.info-box {
    background: rgba(108, 99, 255, 0.1);
    border-left: 4px solid #6C63FF;
    padding: 1rem 1.5rem;
    border-radius: 0 12px 12px 0;
    margin: 1rem 0;
    color: #ccc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0E1117 0%, #1A1F2E 100%);
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── SUPABASE CLIENT ─────────────────────────────────────────────────
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

# ─── ESPERIMENTI DEFINITI ─────────────────────────────────────────────
ESPERIMENTI = {
    "macchina": {
        "titolo": "🚗 Loftus & Palmer — Velocità Auto",
        "desc": "A che velocità andava l'auto? Parole diverse → stime diverse.",
        "gruppo_a": "Colpito (Hit)",
        "gruppo_b": "Sfondato (Smashed)",
        "unita": "km/h",
        "tipo": "slider",
    },
    "framing": {
        "titolo": "🖼️ Framing Effect — Epidemia",
        "desc": "Lo stesso scenario, descritto in modo diverso, cambia la scelta.",
        "gruppo_a": "Positivo (si salvano)",
        "gruppo_b": "Negativo (moriranno)",
        "unita": "% scelta sicura",
        "tipo": "scelta",
    },
    "ancoraggio": {
        "titolo": "⚓ Anchoring — Popolazione Austria",
        "desc": "Un numero iniziale influenza la stima finale.",
        "gruppo_a": "Àncora alta (65M)",
        "gruppo_b": "Àncora bassa (6M)",
        "unita": "milioni",
        "tipo": "slider",
    },
    "disponibilita": {
        "titolo": "✈️ Availability Heuristic — Rischio",
        "desc": "Ciò che ricordiamo facilmente sembra più probabile.",
        "gruppo_a": "Notizia aereo",
        "gruppo_b": "Statistica oggettiva",
        "unita": "% rischio aereo",
        "tipo": "slider",
    },
    "conferma": {
        "titolo": "🔍 Confirmation Bias — Professione",
        "desc": "L'ordine delle opzioni influenza la scelta.",
        "gruppo_a": "Bibliotecario primo",
        "gruppo_b": "Contadino primo",
        "unita": "% bibliotecario",
        "tipo": "scelta",
    },
    "dunning_kruger": {
        "titolo": "🎓 Dunning-Kruger — Autovalutazione",
        "desc": "Quanto siamo bravi a valutare le nostre competenze?",
        "gruppo_a": "Stima personale",
        "gruppo_b": "Punteggio reale",
        "unita": "risposte",
        "tipo": "slider",
    },
    "costi_sommersi": {
        "titolo": "💸 Sunk Cost — Concerto",
        "desc": "Investimenti passati influenzano decisioni future.",
        "gruppo_a": "Biglietto regalato",
        "gruppo_b": "Biglietto pagato 50€",
        "unita": "% va al concerto",
        "tipo": "scelta",
    },
    "effetto_alone": {
        "titolo": "✨ Halo Effect — Competenza",
        "desc": "L'aspetto fisico influenza il giudizio di competenza?",
        "gruppo_a": "Con foto attraente",
        "gruppo_b": "Senza foto",
        "unita": "competenza (1-10)",
        "tipo": "slider",
    },
    "bandwagon": {
        "titolo": "🐑 Bandwagon — Preferenza",
        "desc": "Le scelte degli altri influenzano le nostre.",
        "gruppo_a": "Con info sociale",
        "gruppo_b": "Senza info",
        "unita": "% prodotto A",
        "tipo": "scelta",
    },
    "status_quo": {
        "titolo": "🏠 Status Quo — Assicurazione",
        "desc": "Tendiamo a mantenere l'opzione di default.",
        "gruppo_a": "Default base",
        "gruppo_b": "Default premium",
        "unita": "% mantiene default",
        "tipo": "scelta",
    },
}

# ─── SIDEBAR ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Esperimenti")
    esperimento_sel = st.selectbox(
        "Scegli esperimento:",
        options=list(ESPERIMENTI.keys()),
        format_func=lambda x: ESPERIMENTI[x]["titolo"],
    )
    
    st.markdown("---")
    
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
    
    if st.button("🔄 Aggiorna ora", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ⚠️ Gestione Dati")
    
    with st.expander("🗑️ Cancella risposte"):
        st.warning("I dati restano sempre su Supabase fino a cancellazione manuale.")
        conferma = st.text_input("Scrivi CANCELLA per confermare:", key="confirm_delete")
        if st.button("Elimina risposte esperimento", type="primary"):
            if conferma == "CANCELLA":
                supabase.table("Risposte").delete().eq(
                    "esperimento", esperimento_sel
                ).execute()
                st.success("✅ Risposte cancellate!")
                st.rerun()
            else:
                st.error("Scrivi CANCELLA per confermare")

# ─── FETCH DATA ───────────────────────────────────────────────────────
@st.cache_data(ttl=5)
def fetch_data(esperimento):
    response = supabase.table("Risposte").select("*").eq(
        "esperimento", esperimento
    ).execute()
    return response.data

exp = ESPERIMENTI[esperimento_sel]
data = fetch_data(esperimento_sel)

if data:
    import io
    import csv
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    csv_data = output.getvalue().encode('utf-8')
    
    st.sidebar.download_button(
        label="📥 Scarica Dati (CSV)",
        data=csv_data,
        file_name=f"risposte_{esperimento_sel}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Separare i gruppi
gruppo_a_vals = [r["valore"] for r in data if r["gruppo"] == "A"]
gruppo_b_vals = [r["valore"] for r in data if r["gruppo"] == "B"]

# ─── HEADER ───────────────────────────────────────────────────────────
st.markdown(f'<h1 class="main-title">{exp["titolo"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{exp["desc"]}</p>', unsafe_allow_html=True)
st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)

# ─── METRICS ROW ──────────────────────────────────────────────────────
total_responses = len(data)

if total_responses == 0:
    st.markdown("""
    <div class="info-box">
        <h3>📱 In attesa di risposte...</h3>
        <p>Gli studenti possono rispondere tramite le pagine nella sidebar.<br>
        I risultati appariranno qui in tempo reale!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    media_a = sum(gruppo_a_vals) / len(gruppo_a_vals) if gruppo_a_vals else 0
    media_b = sum(gruppo_b_vals) / len(gruppo_b_vals) if gruppo_b_vals else 0
    diff = abs(media_a - media_b)
    
    # ─── METRICS CARDS ────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">{exp['gruppo_a']}</p>
            <p class="metric-value group-a-color">{media_a:.1f}</p>
            <p><span class="count-badge">📊 {len(gruppo_a_vals)} risposte</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="diff-card">
            <p class="metric-label">Differenza</p>
            <p class="diff-value">Δ {diff:.1f}</p>
            <p style="color: #00FF88;">{exp['unita']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">{exp['gruppo_b']}</p>
            <p class="metric-value group-b-color">{media_b:.1f}</p>
            <p><span class="count-badge">📊 {len(gruppo_b_vals)} risposte</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)
    
    # ─── GRAFICI AFFIANCATI ───────────────────────────────────────────
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        if gruppo_a_vals:
            fig_a = go.Figure()
            fig_a.add_trace(go.Histogram(
                x=gruppo_a_vals,
                marker_color='rgba(108, 99, 255, 0.7)',
                marker_line=dict(color='#6C63FF', width=2),
                name=exp["gruppo_a"],
                hovertemplate="Valore: %{x}<br>Frequenza: %{y}<extra></extra>",
            ))
            fig_a.add_vline(
                x=media_a, line_dash="dash", line_color="#6C63FF", line_width=3,
                annotation_text=f"Media: {media_a:.1f}",
                annotation_font=dict(color="#6C63FF", size=16, family="Inter"),
                annotation_bgcolor="rgba(108, 99, 255, 0.15)",
            )
            fig_a.update_layout(
                title=dict(
                    text=f"📊 {exp['gruppo_a']}",
                    font=dict(size=20, color="#6C63FF", family="Inter"),
                ),
                xaxis_title=exp["unita"],
                yaxis_title="Frequenza",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(26, 31, 46, 0.8)",
                font=dict(family="Inter", color="#FAFAFA"),
                height=450,
                margin=dict(t=60, b=40, l=40, r=20),
                bargap=0.1,
            )
            st.plotly_chart(fig_a, use_container_width=True)
        else:
            st.info(f"Nessuna risposta per {exp['gruppo_a']}")
    
    with chart_col2:
        if gruppo_b_vals:
            fig_b = go.Figure()
            fig_b.add_trace(go.Histogram(
                x=gruppo_b_vals,
                marker_color='rgba(255, 101, 132, 0.7)',
                marker_line=dict(color='#FF6584', width=2),
                name=exp["gruppo_b"],
                hovertemplate="Valore: %{x}<br>Frequenza: %{y}<extra></extra>",
            ))
            fig_b.add_vline(
                x=media_b, line_dash="dash", line_color="#FF6584", line_width=3,
                annotation_text=f"Media: {media_b:.1f}",
                annotation_font=dict(color="#FF6584", size=16, family="Inter"),
                annotation_bgcolor="rgba(255, 101, 132, 0.15)",
            )
            fig_b.update_layout(
                title=dict(
                    text=f"📊 {exp['gruppo_b']}",
                    font=dict(size=20, color="#FF6584", family="Inter"),
                ),
                xaxis_title=exp["unita"],
                yaxis_title="Frequenza",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(26, 31, 46, 0.8)",
                font=dict(family="Inter", color="#FAFAFA"),
                height=450,
                margin=dict(t=60, b=40, l=40, r=20),
                bargap=0.1,
            )
            st.plotly_chart(fig_b, use_container_width=True)
        else:
            st.info(f"Nessuna risposta per {exp['gruppo_b']}")
    
    # ─── GRAFICO CONFRONTO MEDIE ──────────────────────────────────────
    st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)
    
    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        x=[exp["gruppo_a"]],
        y=[media_a],
        marker_color='#6C63FF',
        name=exp["gruppo_a"],
        text=[f"{media_a:.1f}"],
        textposition="outside",
        textfont=dict(size=24, color="#6C63FF", family="Inter"),
        width=0.35,
    ))
    fig_compare.add_trace(go.Bar(
        x=[exp["gruppo_b"]],
        y=[media_b],
        marker_color='#FF6584',
        name=exp["gruppo_b"],
        text=[f"{media_b:.1f}"],
        textposition="outside",
        textfont=dict(size=24, color="#FF6584", family="Inter"),
        width=0.35,
    ))
    fig_compare.update_layout(
        title=dict(
            text="⚡ Confronto Diretto delle Medie",
            font=dict(size=22, color="#FAFAFA", family="Inter"),
            x=0.5,
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26, 31, 46, 0.8)",
        font=dict(family="Inter", color="#FAFAFA"),
        height=400,
        showlegend=False,
        yaxis_title=exp["unita"],
        margin=dict(t=80, b=40, l=40, r=40),
    )
    st.plotly_chart(fig_compare, use_container_width=True)

# ─── FOOTER ───────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align: center; color: #555; margin-top: 2rem; font-size: 0.8rem;">
    📊 Totale risposte: {total_responses} | 
    🕐 Ultimo aggiornamento: {time.strftime('%H:%M:%S')}
</div>
""", unsafe_allow_html=True)

# ─── AUTO REFRESH ─────────────────────────────────────────────────────
if auto_refresh:
    time.sleep(5)
    st.rerun()
