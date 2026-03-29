import os
import shutil

if os.path.exists("pages"):
    shutil.rmtree("pages")
os.makedirs("pages")

def build_ab_page(filename, id, icon, titolo_breve, titolo_lungo, scenario, dom_a, dom_b, extra_comune, salvataggio, extra_css=""):
    template = f"""import streamlit as st
import random
from supabase import create_client

st.set_page_config(page_title="{titolo_breve}", page_icon="{icon}", layout="centered")

NOME_ESPERIMENTO = "{id}"

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.question-card {{ background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%); border-radius: 20px; padding: 2rem; border: 1px solid rgba(108, 99, 255, 0.3); box-shadow: 0 8px 32px rgba(108, 99, 255, 0.2); margin: 1rem 0; }}
.exp-title {{ font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #6C63FF, #FF6584); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.5rem; }}
.exp-subtitle {{ color: #888; text-align: center; font-size: 1rem; margin-bottom: 1.5rem; }}
.thanks-box {{ background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(0, 255, 136, 0.3); box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2); }}
.thanks-emoji {{ font-size: 4rem; }}
.thanks-text {{ color: #00FF88; font-size: 1.5rem; font-weight: 700; }}
{extra_css}
#MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}}
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

st.markdown(\"\"\"<h1 class="exp-title">{icon} {titolo_lungo}</h1>\"\"\", unsafe_allow_html=True)
st.markdown(\"\"\"<p class="exp-subtitle">Rispondi alle domande qui sotto</p>\"\"\", unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
{scenario}
    if st.session_state.gruppo == "A":
{dom_a}
    else:
{dom_b}
{extra_comune}
    
    if st.button("📨 Invia risposta", type="primary", use_container_width=True):
        # Validazione generica (cerca variabili comuni come 'scelta', 'val', 'eta', 'colpa')
        # In Streamlit, se index=None o value=None, la variabile esiste ma è None
        can_submit = True
        for var_name in ['scelta', 'val', 'eta', 'colpa', 'vetri']:
            if var_name in locals() and locals()[var_name] is None:
                st.warning("⚠️ Per favore, rispondi alla domanda prima di inviare.")
                can_submit = False
                break
        
        if can_submit:
{salvataggio}
            st.session_state[NOME_ESPERIMENTO] = True
            st.rerun()
else:
    st.markdown('''<div class="thanks-box"><p class="thanks-emoji">🎉</p><p class="thanks-text">Grazie per aver risposto!</p></div>''', unsafe_allow_html=True)
"""
    with open(os.path.join("pages", filename), "w", encoding="utf-8") as f:
        f.write(template)

def build_single_page(filename, id, icon, titolo_breve, titolo_lungo, dom, salvataggio, extra_css=""):
    template = f"""import streamlit as st
from supabase import create_client

st.set_page_config(page_title="{titolo_breve}", page_icon="{icon}", layout="centered")

NOME_ESPERIMENTO = "{id}"

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.question-card {{ background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%); border-radius: 20px; padding: 2rem; border: 1px solid rgba(108, 99, 255, 0.3); box-shadow: 0 8px 32px rgba(108, 99, 255, 0.2); margin: 1rem 0; }}
.exp-title {{ font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #6C63FF, #FF6584); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.5rem; }}
.exp-subtitle {{ color: #888; text-align: center; font-size: 1rem; margin-bottom: 1.5rem; }}
.thanks-box {{ background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(0, 255, 136, 0.3); box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2); }}
.thanks-emoji {{ font-size: 4rem; }}
.thanks-text {{ color: #00FF88; font-size: 1.5rem; font-weight: 700; }}
{extra_css}
#MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}}
</style>
''', unsafe_allow_html=True)

@st.cache_resource
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = get_supabase()

if NOME_ESPERIMENTO not in st.session_state:
    st.session_state[NOME_ESPERIMENTO] = False

st.markdown(\"\"\"<h1 class="exp-title">{icon} {titolo_lungo}</h1>\"\"\", unsafe_allow_html=True)
st.markdown(\"\"\"<p class="exp-subtitle">Rispondi alle domande qui sotto</p>\"\"\", unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
{dom}
    if st.button("📨 Invia risposta", type="primary", use_container_width=True):
        can_submit = True
        for var_name in ['scelta', 'val', 'eta', 'colpa', 'scelta_dom']:
            if var_name in locals() and locals()[var_name] is None:
                st.warning("⚠️ Per favore, rispondi alla domanda prima di inviare.")
                can_submit = False
                break
        
        if can_submit:
{salvataggio}
            st.session_state[NOME_ESPERIMENTO] = True
            st.rerun()
else:
    st.markdown('''<div class="thanks-box"><p class="thanks-emoji">🎉</p><p class="thanks-text">Grazie per aver risposto!</p></div>''', unsafe_allow_html=True)
"""
    with open(os.path.join("pages", filename), "w", encoding="utf-8") as f:
        f.write(template)

# --- 1. MACCHINA ---
build_ab_page(
    "1_Macchina.py", "macchina", "🚗", "Incidente Auto", "Incidente Stradale",
    "    st.markdown(\"\"\"**Scenario:** Hai appena visto un breve video della dashcam in cui due automobili si scontrano.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"**A che velocità (in km/h) andavano le auto quando si sono URTATE❓**\"\"\")\n        val = st.slider('Stima la velocità:', 0, 150, 50, 5, key='s1')\n",
    "        st.markdown(\"\"\"**A che velocità (in km/h) andavano le auto quando si sono DISINTEGRATE❓**\"\"\")\n        val = st.slider('Stima la velocità:', 0, 150, 50, 5, key='s2')\n",
    "    st.markdown(\"\"\"**2. Hai notato dei vetri rotti a terra?**\"\"\")\n    vetri = st.radio('Scegli:', ['Sì', 'No'], horizontal=True, index=None, key='v')\n",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n        supabase.table('Risposte').insert({'esperimento': 'macchina_vetri', 'gruppo': st.session_state.gruppo, 'valore': 1 if vetri=='Sì' else 0}).execute()\n"
)

# --- 2. FRAMING ASIAN DISEASE ---
build_ab_page(
    "2_Malattia_Asiatica.py", "asian_disease", "🦠", "Malattia Asiatica", "La Malattia Asiatica",
    "    st.markdown(\"\"\"**Scenario:** Immagina che l'Italia si stia preparando ad affrontare una malattia molto contagiosa asiatica, che dovrebbe uccidere 600 persone. Hai due programmi per affrontarla.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"Quale programma scegli?\"\"\")\n        scelta = st.radio('', ['Programma A: Saranno salvate 200 persone (risultato certo).', 'Programma B: C\\'è 1/3 di probabilità di salvare tutte e 600 le persone, e 2/3 di non salvare nessuno.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"Quale programma scegli?\"\"\")\n        scelta = st.radio('', ['Programma A: Moriranno 400 persone (risultato certo).', 'Programma B: C\\'è 1/3 di probabilità che non muoia nessuno, e 2/3 che muoiano tutte e 600 le persone.'], index=None, key='r2')\n",
    "",
    "        v = 0 if 'A:' in scelta else 1\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n"
)

# --- 3. FRAMING MEDICO AI ---
build_ab_page(
    "3_Framing_AI.py", "framing_ai", "🤖", "Software Medico", "Chirurgia Robotica AI",
    "    st.markdown(\"\"\"**Scenario:** Un nuovo software robotico AI deve compiere un'operazione complessa su 100 pazienti in condizioni critiche.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"**Dato statistico:** Se usi l'Intelligenza Artificiale, **90 pazienti sopravviveranno**.\\n\\nAutorizzi l'uso del software?\"\"\")\n        scelta = st.radio('', ['Sì', 'No'], horizontal=True, index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Dato statistico:** Se usi l'Intelligenza Artificiale, **10 pazienti moriranno**.\\n\\nAutorizzi l'uso del software?\"\"\")\n        scelta = st.radio('', ['Sì', 'No'], horizontal=True, index=None, key='r2')\n",
    "",
    "        v = 1 if scelta == 'Sì' else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n"
)

# --- 4. ANCORAGGIO GANDHI ---
build_ab_page(
    "4_Ancoraggio_Gandhi.py", "gandhi", "👴", "Biografia Età", "Età di Gandhi",
    "",
    "        st.markdown(\"\"\"**Mahatma Gandhi aveva più o meno di 114 anni quando è morto?**\"\"\")\n        st.radio('', ['Più di 114', 'Meno di 114'], horizontal=True, index=None, key='r1')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**A che età esatta è morto secondo te?**\"\"\")\n        eta = st.number_input('Inserisci una stima (anni):', 0, 150, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Mahatma Gandhi aveva più o meno di 35 anni quando è morto?**\"\"\")\n        st.radio('', ['Più di 35', 'Meno di 35'], horizontal=True, index=None, key='r2')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**A che età esatta è morto secondo te?**\"\"\")\n        eta = st.number_input('Inserisci una stima (anni):', 0, 150, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': eta}).execute()\n"
)

# --- 5. ANCORAGGIO ROULETTE ---
build_ab_page(
    "5_Ancoraggio_Roulette.py", "roulette", "🎰", "Ruota della Fortuna", "Statistica Ospedaliera",
    "",
    "        st.markdown(\"\"\"### Il numero estratto dalla ruota oggi è: **12**\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        val = st.slider('Considera il numero sopra. Secondo te, in Italia, qual è la percentuale esatta di diagnosi errate dovute a stanchezza del medico?', 0, 100, 50, key='s1')\n",
    "        st.markdown(\"\"\"### Il numero estratto dalla ruota oggi è: **65**\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        val = st.slider('Considera il numero sopra. Secondo te, in Italia, qual è la percentuale esatta di diagnosi errate dovute a stanchezza del medico?', 0, 100, 50, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n"
)

# --- 6. LOSS AVERSION ---
build_ab_page(
    "6_Avversione_Perdite.py", "loss_aversion", "💶", "Scommessa", "Decisioni Finanziarie",
    "",
    "        st.markdown(\"\"\"**Scenario:** Hai appena ricevuto 1.000€ in premio. Quale di queste due opzioni scegli ora?\"\"\")\n        scelta = st.radio('', ['A) Vinci altri 500€ sicuri al 100%', 'B) Lanci una moneta: 50% di probabilità di vincere altri 1000€, e 50% di vincere 0€.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** Hai appena ricevuto 2.000€ in premio. Quale di queste due opzioni scegli ora?\"\"\")\n        scelta = st.radio('', ['A) Perdi 500€ sicuri al 100%', 'B) Lanci una moneta: 50% di probabilità di perdere 1000€, e 50% di perdere 0€.'], index=None, key='r2')\n",
    "",
    "        v = 0 if 'sicuri' in scelta else 1\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n"
)

# --- 7. ILLUSIONE DI VERITA ---
build_ab_page(
    "7_Illusione_Verita.py", "illusione_verita", "👁️", "Scienza e Verità", "Valuta l'Affermazione",
    "",
    "        st.markdown(\"\"\"<p style=\"font-size:32px; font-weight:900; color:#FAFAFA; font-family:Arial; text-align:center;\">L'assunzione di Omega-3 riduce<br>del 15% le infiammazioni corporee.</p>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"---\"\"\")\n        val = st.slider('Da 1 a 10, quanto ti sembra vera e scientifica questa frase?', 1, 10, 5, key='s1')\n",
    "        st.markdown(\"\"\"<p style=\"font-size:12px; font-weight:300; color:#555555; font-family:'Comic Sans MS', cursive; text-align:center; padding: 2rem;\">L'assunzione di omega-3 riduce del 15% le infiammazioni corporee.</p>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"---\"\"\")\n        val = st.slider('Da 1 a 10, quanto ti sembra vera e scientifica questa frase?', 1, 10, 5, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n"
)

# --- 8. AVAILABILITY HEURISTIC ---
build_ab_page(
    "8_Euristica_Disponibilita.py", "availability", "🧠", "Ricordo", "Inventario della Personalità",
    "",
    "        st.markdown(\"\"\"1. Pensa ed elenca **2 situazioni** in cui sei riuscito a comportarti in modo molto assertivo (ossia in cui hai fatto rispettare fermamente il tuo punto di vista agli altri e ti sei imposto con sicurezza).\"\"\")\n        st.text_area('Scrivi in breve le 2 situazioni:', height=100, key='t1')\n        st.markdown(\"\"\"---\"\"\")\n        val = st.slider('In generale nella tua vita, considerando tutto, quanto ritieni di essere una persona assertiva?', 1, 10, 5, key='s1')\n",
    "        st.markdown(\"\"\"1. Pensa ed elenca **12 situazioni** in cui sei riuscito a comportarti in modo molto assertivo (ossia in cui hai fatto rispettare fermamente il tuo punto di vista agli altri e ti sei imposto con sicurezza).\"\"\")\n        st.text_area('Scrivi in breve le 12 situazioni:', height=200, key='t2')\n        st.markdown(\"\"\"---\"\"\")\n        val = st.slider('In generale nella tua vita, considerando tutto, quanto ritieni di essere una persona assertiva?', 1, 10, 5, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n"
)

# --- 9. LINDA PROBLEM ---
build_ab_page(
    "9_Problema_Linda.py", "linda", "👩‍🦰", "Profilo Persona", "Il Profilo di Linda",
    "    st.markdown(\"\"\"**Profilo:** Linda ha 31 anni, è single, molto schietta e brillante. È laureata in filosofia. Da studentessa era profondamente preoccupata per le questioni relative alla discriminazione e alla giustizia sociale, e ha anche partecipato a manifestazioni antinucleari.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        val = st.slider('Alla luce della sua descrizione, qual è la probabilità (0-100%) che oggi Linda sia **una cassiera di banca**?', 0, 100, 50, key='s1')\n",
    "        val = st.slider('Alla luce della sua descrizione, qual è la probabilità (0-100%) che oggi Linda sia **una cassiera di banca e che sia attiva nel movimento femminista**?', 0, 100, 50, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n"
)

# --- 10. EFFETTO ALONE ASCH ---
build_ab_page(
    "10_Effetto_Alone.py", "halo_asch", "👤", "Valutazione", "Valutazione del Profilo",
    "",
    "        st.markdown(\"\"\"Considera **Alan**. I suoi colleghi lo descrivono così:\"\"\")\n        st.markdown(\"\"\"> *Intelligente, laborioso, impulsivo, critico, ostinato, invidioso.*\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        val = st.slider('Da 1 a 10, quanto valuti positivamente Alan come persona sul posto di lavoro?', 1, 10, 5, key='s1')\n",
    "        st.markdown(\"\"\"Considera **Ben**. I suoi colleghi lo descrivono così:\"\"\")\n        st.markdown(\"\"\"> *Invidioso, ostinato, critico, impulsivo, laborioso, intelligente.*\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        val = st.slider('Da 1 a 10, quanto valuti positivamente Ben come persona sul posto di lavoro?', 1, 10, 5, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n"
)

# --- 11. ENDOWMENT TAZZA ---
build_ab_page(
    "11_Effetto_Dote_Tazza.py", "endow_mug", "☕", "Mercato Libre", "Il Mercato delle Tazze",
    "",
    "        st.markdown(\"\"\"**Scenario:** Complimenti! Ti è appena stata **REGALATA** questa bellissima tazza del nostro istituto (ora è rigorosamente di tua proprietà).\"\"\")\n        st.markdown(\"\"\"<div style=\"text-align: center; font-size: 60px;\">☕🎓</div>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"Un tuo compagno arriva e vorrebbe comprarla da te. Qual è il **PREZZO MINIMO** a cui saresti disposto a vendergliela?\"\"\")\n        val = st.number_input('Prezzo in Euro (€):', 0.0, 50.0, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Scenario:** Un tuo compagno ha appena ricevuto in regalo una bellissima tazza del nostro istituto. Tu al momento sei a mani vuote.\"\"\")\n        st.markdown(\"\"\"<div style=\"text-align: center; font-size: 60px;\">☕🎓</div>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"Lui è disposto a venderla. Qual è il **PREZZO MASSIMO** che saresti disposto a sborsare ORA per acquistarla da lui?\"\"\")\n        val = st.number_input('Prezzo in Euro (€):', 0.0, 50.0, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n"
)

# --- 12. ENDOWMENT SOFTWARE ---
build_ab_page(
    "12_Effetto_Dote_AI.py", "endow_ai", "💻", "Licenze AI", "Software Medicale",
    "",
    "        st.markdown(\"\"\"**Scenario:** Ti abbiamo regalato a vita una rarissima Licenza Software per diagnosi AI (è tua di diritto).\"\"\")\n        st.markdown(\"\"\"Un ospedale vorrebbe comprarla da te. Qual è il **prezzo minimo** che pretendi per cederla?\"\"\")\n        val = st.number_input('Valore in Euro (€):', 0, 50000, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Scenario:** Un ospedale ha appena messo in vendita una rarissima Licenza Software per diagnosi AI.\"\"\")\n        st.markdown(\"\"\"A te farebbe molto comodo. Qual è il **prezzo massimo** che sei disposto a pagare per averla?\"\"\")\n        val = st.number_input('Valore in Euro (€):', 0, 50000, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n"
)

# --- 13. SUNK COST THEATER ---
build_ab_page(
    "13_Costi_Sommersi_Teatro.py", "sunk_theater", "🎭", "Spettacolo", "Lo Spettacolo a Teatro",
    "",
    "        st.markdown(\"\"\"**Scenario:** Hai acquistato a tue spese un biglietto da 50€ per vedere uno spettacolo teatrale che ti interessava.\"\"\")\n        st.markdown(\"\"\"Arriva la sera dello spettacolo ma c'è una tormenta di neve spaventosa. Andare a teatro richiede di mettersi alla guida sulla neve per 40 minuti, sfidando il pericolo e il freddo estremo.\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        scelta = st.radio('Cosa decidi di fare?', ['A) Vado a teatro lo stesso (sfido la tormenta per non buttare i 50€).', 'B) Resto a casa al caldo rinunciando allo spettacolo e ai 50€.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** Un amico ti ha **regalato** stasera un biglietto per vedere uno spettacolo teatrale che ti interessava (costo per te: 0€).\"\"\")\n        st.markdown(\"\"\"Arriva la sera dello spettacolo ma c'è una tormenta di neve spaventosa. Andare a teatro richiede di mettersi alla guida sulla neve per 40 minuti, sfidando il pericolo e il freddo estremo.\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        scelta = st.radio('Cosa decidi di fare?', ['A) Vado a teatro lo stesso (sfido la tormenta per non buttare il regalo).', 'B) Resto a casa al caldo rinunciando allo spettacolo.'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Vado' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n"
)

# --- 14. SUNK COST AI ---
build_ab_page(
    "14_Costi_Sommersi_AI.py", "sunk_ai", "🏭", "Progetto Ricerca", "Investimento Ricerca",
    "",
    "        st.markdown(\"\"\"**Scenario:** Sei il capo di un team. Hai deciso proprio OGGI (0 ore di lavoro svolte da te) di iniziare a programmare un nuovo algoritmo diagnostico.\"\"\")\n        st.markdown(\"\"\"Mentre bevi il caffè, vedi una news: Google ha appena rilasciato gratuitamente un algoritmo che è tecnicamente molto superiore al tuo in tutto.\"\"\")\n        scelta = st.radio('Che decisione prendi?', ['Continuo a sviluppare il mio', 'Abbandono il mio progetto'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** Sei il capo di un team. Da **4 anni precisi** tu e i tuoi uomini lavorate senza sosta e con immensi sacrifici a un nuovo algoritmo diagnostico (siete al 90% dell'opera).\"\"\")\n        st.markdown(\"\"\"Mentre bevi il caffè, vedi una news: Google ha appena rilasciato gratuitamente un algoritmo che è tecnicamente molto superiore al tuo in tutto.\"\"\")\n        scelta = st.radio('Che decisione prendi?', ['Continuo a sviluppare il mio', 'Abbandono il mio progetto'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Continuo' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n"
)

# --- 15. EFFETTO DEFAULT ---
build_ab_page(
    "15_Effetto_Default.py", "default_organ", "🫀", "Assicurazione", "Modulo Assicurativo",
    "    st.markdown(\"\"\"**Firma del nuovo modulo per dipendenti ospedalieri.**\"\"\")\n    st.markdown(\"\"\"Leggi il campo sulla donazione e procedi per confermare.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        opt = st.checkbox('⚠️ Spunta la casella seguente se **VUOI** e acconsenti esplicitamente a diventare un donatore di organi in caso di morte fulminea.', value=False, key='c1')\n",
    "        opt = st.checkbox('⚠️ Spunta la casella seguente se **NON VUOI** diventare un donatore di organi in caso di morte fulminea.', value=True, key='c2')\n",
    "",
    "        v = 1 if (st.session_state.gruppo == 'A' and opt == True) or (st.session_state.gruppo == 'B' and opt == False) else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n"
)

# --- 16. PRIMING EAT WASH ---
build_ab_page(
    "16_Priming_Associativo.py", "priming", "🍝", "Associazioni", "Parole e Associazioni",
    "",
    "        st.markdown(\"\"\"Leggi le seguenti parole velocemente:\"\"\")\n        st.markdown(\"\"\"### FORCHETTA<br>PRANZO<br>FAME\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"Ora compila e completa mentalmente i campi mancanti in questa parola:\"\"\")\n        st.markdown(\"\"\"## S O _ P\"\"\")\n        val = st.text_input('Scrivi la parola completa in italiano (una di uso comune che ti viene in mente istintivamente):', key='t1')\n",
    "        st.markdown(\"\"\"Leggi le seguenti parole velocemente:\"\"\")\n        st.markdown(\"\"\"### DOCCIA<br>SCHIUMA<br>PULITO\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"Ora compila e completa mentalmente i campi mancanti in questa parola:\"\"\")\n        st.markdown(\"\"\"## S O _ P\"\"\")\n        val = st.text_input('Scrivi la parola completa in italiano (una di uso comune che ti viene in mente istintivamente):', key='t2')\n",
    "",
    "        v = 1 if 'sapore' in val.lower() or 'soup' in val.lower() or 'zuppa' in val.lower() else (2 if 'sapone' in val.lower() or 'soap' in val.lower() else 0)\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n"
)

# --- 17. DUNNING KRUGER ---
build_ab_page(
    "17_Dunning_Kruger.py", "dunning", "🎓", "Stima di Sé", "Autovalutazione",
    "",
    "        st.markdown(\"\"\"Pensa in totale onestà. Ritieni che la tua abilità accademica, intellettuale e di pensiero analitico sia... **superiore o inferiore alla media degli altri studenti attualmente presenti in quest'aula?**\"\"\")\n        scelta = st.radio('', ['Sopra la media di questa classe', 'Nella media', 'Sotto la media di questa classe'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"Pensa in totale onestà. Ritieni che la tua abilità accademica, intellettuale e di pensiero analitico sia... **superiore o inferiore alla mente del Premio Nobel italiano Giorgio Parisi?**\"\"\")\n        scelta = st.radio('', ['Sopra la sua media', 'Nella sua media', 'Sotto la sua media'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Sopra' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n"
)

# --- 18. WYSIATI ---
build_ab_page(
    "18_WYSIATI.py", "wysiati", "⚖️", "Giudice", "Verdetto Giudiziario",
    "",
    "        st.markdown(\"\"\"**Testimonianza (Avvocato Difensore):** \"Il mio cliente è un pilastro della comunità. Ha donato soldi in beneficienza, ama la famiglia e il giorno della rapina era al telefono con sua madre, benché lei purtroppo sia deceduta e non possa confermarlo.\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        colpa = st.slider('Quanto ritieni sia colpevole (0=Innocente, 100=Max Colpevolezza)?', 0, 100, 50, key='s1a')\n        fiducia = st.slider('Da 1 a 10, quanto ti senti **sicuro e fiducioso** della tua scelta, basandoti sulle info in tuo possesso?', 1, 10, 5, key='s1b')\n",
    "        st.markdown(\"\"\"**Testimonianza (Avvocato Difensore):** \"Il mio cliente è un pilastro della comunità, ama la famiglia e il giorno della rapina era al telefono con sua madre (deceduta e incapace di confermare).\"\"\")\n        st.markdown(\"\"\"**Testimonianza (Pubblico Ministero):** \"La maschera ritrovata sulla scena ha tracce del suo DNA e la cella telefonica lo fissa a pochi metri dalla banca, rendendo la storiella della madre puramente ridicola.\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        colpa = st.slider('Quanto ritieni sia colpevole (0=Innocente, 100=Max Colpevolezza)?', 0, 100, 50, key='s2a')\n        fiducia = st.slider('Da 1 a 10, quanto ti senti **sicuro e fiducioso** della tua scelta, basandoti sulle info in tuo possesso?', 1, 10, 5, key='s2b')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': colpa}).execute()\n        supabase.table('Risposte').insert({'esperimento': 'wysiati_fiducia', 'gruppo': st.session_state.gruppo, 'valore': fiducia}).execute()\n"
)

# --- 19. FOCALIZZAZIONE ---
build_ab_page(
    "19_Illusione_Focalizzazione.py", "focalizzazione", "😊", "Questionario Benessere", "Sondaggio sul Benessere",
    "    st.markdown(\"\"\"Rispondi con sincerità alle seguenti due domande sulla tua vita attuale.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        val = st.slider('1. Nel complesso, quanto ti ritieni felice della tua vita in questo periodo?', 1, 10, 5, key='s1a')\n        st.markdown('<br>', unsafe_allow_html=True)\n        st.number_input('2. Quanti appuntamenti romantici o uscite serali di svago hai avuto nell\\'ultimo mese?', 0, 30, value=None, key='n1b')\n",
    "        st.number_input('1. Quanti appuntamenti romantici o uscite serali di svago hai avuto nell\\'ultimo mese?', 0, 30, value=None, key='n2a')\n        st.markdown('<br>', unsafe_allow_html=True)\n        val = st.slider('2. Nel complesso, quanto ti ritieni felice della tua vita in questo periodo?', 1, 10, 5, key='s2b')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n"
)

# --- SINGLE DEMOS ---

# --- 20. BASE RATE NEGLECT ---
build_single_page(
    "20_Base_Rate_Neglect.py", "base_rate", "🔬", "Diagnosi Medica", "Paradosso Diagnostico",
    "    st.markdown(\"\"\"Una grave malattia genetica colpisce **esattamente l'1%** della popolazione mondiale.\"\"\")\n    st.markdown(\"\"\"Un test in grado di individuarla è **infallibile al 95%** (cioè restituisce falsi positivi solo nel 5% dei casi e falsi negativi solo nel 5% dei casi).\"\"\")\n    st.markdown(\"\"\"Fai questo test e il medico ti dice che **SEI RISULTATO POSITIVO**.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n    val = st.slider('Qual è l\\'effettiva probabilità (da 0 a 100%) che tu abbia DAVVERO la malattia in questione?', 0, 100, 50)\n",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': val}).execute()\n"
)

# --- 21. DECOY EFFECT ---
build_single_page(
    "21_L_Esca.py", "decoy", "🗞️", "Abbonamento", "Rivista The Economist",
    "    st.markdown(\"\"\"Scegli liberamente quale abbonamento fa per te alla rivista The Economist:\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n    scelta = st.radio('Scegli un\\'opzione:', ['A) Abbonamento SOLO Web (Accesso illimitato al sito) -> **50 €**', 'B) Abbonamento SOLO Cartaceo (Fascicolo mensile a casa) -> **120 €**', 'C) Abbonamento WEB + CARTACEO -> **120 €**'], index=None)\n",
    "        v = 1 if 'A)' in scelta else (2 if 'B)' in scelta else 3)\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': v}).execute()\n"
)

# --- 22. REGRESSIONE VERSO LA MEDIA ---
build_single_page(
    "22_Regressione_Media.py", "regression", "🧑‍✈️", "Psicologia Umana", "L'Effetto Lode/Castigo",
    "    st.markdown(\"\"\"Tra gli istruttori di volo militare israeliani era prassi comune sgridare duramente gli allievi dopo una manovra disastrosa, e complimentarsi con loro dopo una manovra eccezionale e perfetta.\"\"\")\n    st.markdown(\"\"\"Nel tempo notarono che **chi veniva sgridato, il volo successivo migliorava** enormemente. Invece **chi veniva elogiato per una manovra fantastica, il volo successivo faceva nettamente peggio**.\"\"\")\n    st.markdown(\"\"\"Da questo, gli istruttori militari conclusero che i castighi verbali spronano all'apprendimento, mentre la lode spinge i cadetti ad adagiarsi sugli allori peggiorando le performance.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n    st.markdown(\"\"\"Alla luce del rigore scientifico e cognitivo, credi che la conclusione tratta dagli istruttori militari:\"\"\")\n    scelta = st.radio('', ['A) Sia una intuizione psicologicamente corretta ed efficace in addestramento.', 'B) Sia un colossale errore statistico, legato a come funzionano gli estremi.'], index=None)\n",
    "        v = 1 if 'A)' in scelta else 2\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': v}).execute()\n"
)

print("Tutti i 22 file sono stati RIGENERATI con widget senza valori predefiniti!")
