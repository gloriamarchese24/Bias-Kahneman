import os
import shutil

if os.path.exists("pages"):
    shutil.rmtree("pages")
os.makedirs("pages")

def build_ab_page(filename, id, icon, titolo_breve, titolo_lungo, scenario, dom_a, dom_b, extra_comune, salvataggio, lang="IT", extra_css=""):
    salvataggio_indented = salvataggio.replace("\n        ", "\n            ").replace("        ", "            ", 1)
    
    sub_title = "Rispondi alle domande qui sotto" if lang == "IT" else "Please answer the questions below"
    btn_text = "📨 Invia risposta" if lang == "IT" else "📨 Submit response"
    warn_text = "⚠️ Per favore, rispondi alla domanda prima di inviare." if lang == "IT" else "⚠️ Please answer the question before submitting."
    thanks_text = "Grazie per aver risposto!" if lang == "IT" else "Thank you for participating!"
    
    template = f"""import streamlit as st
import random
import base64
import os
import streamlit.components.v1 as components
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

if "gruppo" not in st.session_state:
    if "g" in st.query_params and st.query_params["g"] in ["A", "B"]:
        st.session_state.gruppo = st.query_params["g"]
    else:
        try:
            r = supabase.table("Risposte").insert({{"esperimento": NOME_ESPERIMENTO + "_visit", "gruppo": "PENDING", "valore": 0}}).execute()
            row_id = r.data[0]["id"]
            st.session_state.gruppo = "A" if row_id % 2 == 1 else "B"
        except Exception:
            st.session_state.gruppo = random.choice(["A", "B"])

if NOME_ESPERIMENTO not in st.session_state:
    st.session_state[NOME_ESPERIMENTO] = False

st.markdown(\"\"\"<h1 class="exp-title">{icon} {titolo_lungo}</h1>\"\"\", unsafe_allow_html=True)
st.markdown(\"\"\"<p class="exp-subtitle">{sub_title}</p>\"\"\", unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
{scenario}
    if st.session_state.gruppo == "A":
{dom_a}
    else:
{dom_b}
{extra_comune}
    
    if st.button("{btn_text}", type="primary", use_container_width=True):
        can_submit = True
        for var_name in ['scelta', 'val', 'eta', 'colpa', 'vetri', 'fiducia']:
            if var_name in locals() and locals()[var_name] is None:
                st.warning("{warn_text}")
                can_submit = False
                break
        
        if can_submit:
{salvataggio_indented}
            st.session_state[NOME_ESPERIMENTO] = True
            st.rerun()
else:
    st.markdown('''<div class="thanks-box"><p class="thanks-emoji">🎉</p><p class="thanks-text">{thanks_text}</p></div>''', unsafe_allow_html=True)
"""
    with open(os.path.join("pages", filename), "w", encoding="utf-8") as f:
        f.write(template)

def build_single_page(filename, id, icon, titolo_breve, titolo_lungo, dom, salvataggio, lang="IT", extra_css=""):
    salvataggio_indented = salvataggio.replace("\n        ", "\n            ").replace("        ", "            ", 1)
    
    sub_title = "Rispondi alle domande qui sotto" if lang == "IT" else "Please answer the questions below"
    btn_text = "📨 Invia risposta" if lang == "IT" else "📨 Submit response"
    warn_text = "⚠️ Per favore, rispondi alla domanda prima di inviare." if lang == "IT" else "⚠️ Please answer the question before submitting."
    thanks_text = "Grazie per aver risposto!" if lang == "IT" else "Thank you for participating!"
    
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
st.markdown(\"\"\"<p class="exp-subtitle">{sub_title}</p>\"\"\", unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
{dom}
    if st.button("{btn_text}", type="primary", use_container_width=True):
        can_submit = True
        for var_name in ['scelta', 'val', 'eta', 'colpa', 'scelta_dom', 'fiducia']:
            if var_name in locals() and locals()[var_name] is None:
                st.warning("{warn_text}")
                can_submit = False
                break
        
        if can_submit:
{salvataggio_indented}
            st.session_state[NOME_ESPERIMENTO] = True
            st.rerun()
else:
    st.markdown('''<div class="thanks-box"><p class="thanks-emoji">🎉</p><p class="thanks-text">{thanks_text}</p></div>''', unsafe_allow_html=True)
"""
    with open(os.path.join("pages", filename), "w", encoding="utf-8") as f:
        f.write(template)

# ==========================================
# ITALIAN PAGES (1-23)
# ==========================================

build_ab_page(
    "1_Macchina.py", "macchina", "🚗", "Incidente Auto", "Incidente Stradale",
    "    st.markdown(\"\"\"**Scenario:** Hai appena visto un breve video di un incidente tra due automobili.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"**A che velocità (in km/h) andavano le auto quando si sono urtate?**\"\"\")\n        val = st.number_input('Stima la velocità (km/h):', 0, 200, value=None, key='s1')\n",
    "        st.markdown(\"\"\"**A che velocità (in km/h) andavano le auto quando si sono disintegrate?**\"\"\")\n        val = st.number_input('Stima la velocità (km/h):', 0, 200, value=None, key='s2')\n",
    "    st.markdown(\"\"\"**2. Hai notato dei vetri rotti a terra?**\"\"\")\n    vetri = st.radio('Scegli:', ['Sì', 'No'], horizontal=True, index=None, key='v')\n",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n        supabase.table('Risposte').insert({'esperimento': 'macchina_vetri', 'gruppo': st.session_state.gruppo, 'valore': 1 if vetri=='Sì' else 0}).execute()\n",
    lang="IT"
)

build_ab_page(
    "2_Malattia_Asiatica.py", "asian_disease", "🦠", "Malattia Asiatica", "La Malattia Asiatica",
    "    st.markdown(\"\"\"**Scenario:** Immagina che l'Italia si stia preparando ad affrontare una malattia molto contagiosa asiatica, che dovrebbe uccidere 600 persone. Hai due programmi per affrontarla.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"Quale programma scegli?\"\"\")\n        scelta = st.radio('', ['Programma A: Saranno salvate 200 persone (risultato certo).', 'Programma B: C\\'è 1/3 di probabilità di salvare tutte e 600 le persone, e 2/3 di non salvare nessuno.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"Quale programma scegli?\"\"\")\n        scelta = st.radio('', ['Programma A: Moriranno 400 persone (risultato certo).', 'Programma B: C\\'è 1/3 di probabilità che non muoia nessuno, e 2/3 che muoiano tutte e 600 le persone.'], index=None, key='r2')\n",
    "",
    "        v = 0 if 'A:' in scelta else 1\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

build_ab_page(
    "3_Framing_AI.py", "framing_ai", "🤖", "Software Medico", "Chirurgia Robotica AI",
    "    st.markdown(\"\"\"**Scenario:** Un nuovo software robotico AI deve compiere un'operazione complessa su 100 pazienti in condizioni critiche.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"**Dato statistico:** Se usi l'Intelligenza Artificiale, **90 pazienti sopravviveranno**.\\n\\nAutorizzi l'uso del software?\"\"\")\n        scelta = st.radio('', ['Sì', 'No'], horizontal=True, index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Dato statistico:** Se usi l'Intelligenza Artificiale, **10 pazienti moriranno**.\\n\\nAutorizzi l'uso del software?\"\"\")\n        scelta = st.radio('', ['Sì', 'No'], horizontal=True, index=None, key='r2')\n",
    "",
    "        v = 1 if scelta == 'Sì' else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

build_ab_page(
    "4_Ancoraggio_Gandhi.py", "gandhi", "👴", "Biografia Età", "Età di Gandhi",
    "",
    "        st.markdown(\"\"\"**Gandhi aveva più o meno di 114 anni quando è morto?**\"\"\")\n        st.radio('', ['Più di 114', 'Meno di 114'], horizontal=True, index=None, key='r1')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**A che età esatta è morto secondo te?**\"\"\")\n        eta = st.number_input('Inserisci una stima (anni):', 0, 150, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Gandhi aveva più o meno di 35 anni quando è morto?**\"\"\")\n        st.radio('', ['Più di 35', 'Meno di 35'], horizontal=True, index=None, key='r2')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**A che età esatta è morto secondo te?**\"\"\")\n        eta = st.number_input('Inserisci una stima (anni):', 0, 150, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': eta}).execute()\n",
    lang="IT"
)

build_ab_page(
    "5_Ancoraggio_Roulette.py", "roulette", "🎰", "Ruota della Fortuna", "Statistica Ospedaliera",
    "",
    "        val = st.number_input('Secondo te, qual è la percentuale esatta di diagnosi errate dovute a stanchezza del medico?', 0, 100, value=None, key='s1')\n",
    "        val = st.number_input('Secondo te, qual è la percentuale esatta di diagnosi errate dovute a stanchezza del medico?', 0, 100, value=None, key='s2')\n",
    "    st.markdown(\"\"\"---\"\"\")\n    st.markdown(\"\"\"### Il numero estratto dalla ruota oggi è: **12**\"\"\" if st.session_state.gruppo == 'A' else \"\"\"### Il numero estratto dalla ruota oggi è: **65**\"\"\")\n",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="IT"
)

build_ab_page(
    "6_Avversione_Perdite.py", "loss_aversion", "💶", "Scommessa", "Decisioni Finanziarie",
    "",
    "        st.markdown(\"\"\"**Scenario:** Hai appena ricevuto 1.000€ in premio. Quale di queste due opzioni scegli ora?\"\"\")\n        scelta = st.radio('', ['A) Vinci altri 500€ sicuri al 100%', 'B) Lanci una moneta: 50% di probabilità di vincere altri 1000€, e 50% di vincere 0€.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** Hai appena ricevuto 2.000€ in premio. Quale di queste due opzioni scegli ora?\"\"\")\n        scelta = st.radio('', ['A) Perdi 500€ sicuri al 100%', 'B) Lanci una moneta: 50% di probabilità di perdere 1000€, e 50% di perdere 0€.'], index=None, key='r2')\n",
    "",
    "        v = 0 if 'sicuri' in scelta else 1\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

build_ab_page(
    "7_Illusione_Verita.py", "illusione_verita", "👁️", "Scienza e Verità", "Valuta l'Affermazione",
    "",
    "        st.markdown(\"\"\"<p style=\"font-size:32px; font-weight:900; color:#FAFAFA; font-family:Arial; text-align:center;\">L'assunzione di Omega-3 riduce<br>del 15% le infiammazioni corporee.</p>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**Da 1 a 10, quanto ti sembra vera e scientifica questa frase?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1')\n",
    "        st.markdown(\"\"\"<p style=\"font-size:16px; font-weight:300; color:#AAAAAA; font-family:'Comic Sans MS', cursive; text-align:center; padding: 2rem;\">L'assunzione di omega-3 riduce del 15% le infiammazioni corporee.</p>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**Da 1 a 10, quanto ti sembra vera e scientifica questa frase?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="IT"
)

build_ab_page(
    "8_Euristica_Disponibilita.py", "availability", "🧠", "Ricordo", "Inventario della Personalità",
    "",
    "        st.markdown(\"\"\"1. Pensa ed elenca **6 situazioni** in cui sei riuscito a comportarti in modo molto assertivo (ossia in cui hai fatto rispettare fermamente il tuo punto di vista agli altri e ti sei imposto con sicurezza).\"\"\")\n        st.text_area('Scrivi in breve le 6 situazioni:', height=140, key='t1')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**In generale nella tua vita, quanto ritieni di essere una persona assertiva (1-10)?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1')\n",
    "        st.markdown(\"\"\"1. Pensa ed elenca **12 situazioni** in cui sei riuscito a comportarti in modo molto assertivo (ossia in cui hai fatto rispettare fermamente il tuo punto di vista agli altri e ti sei imposto con sicurezza).\"\"\")\n        st.text_area('Scrivi in breve le 12 situazioni:', height=200, key='t2')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**In generale nella tua vita, quanto ritieni di essere una persona assertiva (1-10)?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="IT"
)

build_ab_page(
    "9_Problema_Linda.py", "linda", "👩‍🦰", "Profilo Persona", "Il Profilo di Linda",
    "    st.markdown(\"\"\"**Profilo:** Linda ha 31 anni, è single, molto schietta e brillante. È laureata in filosofia. Da studentessa era profondamente preoccupata per le questioni relative alla discriminazione e alla giustizia sociale, e ha anche partecipato a manifestazioni antinucleari.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        val = st.number_input('Alla luce della sua descrizione, qual è la probabilità (0-100%) che oggi Linda sia **una cassiera di banca**?', 0, 100, value=None, key='s1')\n",
    "        val = st.number_input('Alla luce della sua descrizione, qual è la probabilità (0-100%) che oggi Linda sia **una cassiera di banca e che sia attiva nel movimento femminista**?', 0, 100, value=None, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="IT"
)

build_ab_page(
    "10_Effetto_Alone.py", "halo_asch", "👤", "Valutazione", "Valutazione del Profilo",
    "",
    "        st.markdown(\"\"\"Considera **Alan**. I suoi colleghi lo descrivono così:\"\"\")\n        st.markdown(\"\"\"> *Intelligente, laborioso, impulsivo, critico, ostinato, invidioso.*\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**Da 1 a 10, quanto valuti positivamente Alan come persona sul posto di lavoro?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1')\n",
    "        st.markdown(\"\"\"Considera **Ben**. I suoi colleghi lo descrivono così:\"\"\")\n        st.markdown(\"\"\"> *Invidioso, ostinato, critico, impulsivo, laborioso, intelligente.*\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**Da 1 a 10, quanto valuti positivamente Ben come persona sul posto di lavoro?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="IT"
)

build_ab_page(
    "11_Effetto_Dote_Tazza.py", "endow_mug", "☕", "Mercato Libre", "Il Mercato delle Tazze",
    "",
    "        st.markdown(\"\"\"**Scenario:** Complimenti! Ti è appena stata **REGALATA** questa bellissima tazza del nostro istituto (ora è rigorosamente di tua proprietà).\"\"\")\n        st.markdown(\"\"\"<div style=\"text-align: center; font-size: 60px;\">☕🎓</div>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"Un tuo compagno arriva e vorrebbe comprarla da te. Qual è il **PREZZO MINIMO** a cui saresti disposto a vendergliela?\"\"\")\n        val = st.number_input('Prezzo in Euro (€):', 0.0, 50.0, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Scenario:** Un tuo compagno ha appena ricevuto in regalo una bellissima tazza del nostro istituto. Tu al momento sei a mani vuote.\"\"\")\n        st.markdown(\"\"\"<div style=\"text-align: center; font-size: 60px;\">☕🎓</div>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"Lui è disposto a venderla. Qual è il **PREZZO MASSIMO** che saresti disposto a sborsare ORA per acquistarla da lui?\"\"\")\n        val = st.number_input('Prezzo in Euro (€):', 0.0, 50.0, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="IT"
)

build_ab_page(
    "12_Effetto_Dote_AI.py", "endow_ai", "💻", "Licenze AI", "Software Medicale",
    "",
    "        st.markdown(\"\"\"**Scenario:** Ti abbiamo regalato a vita una rarissima Licenza Software per diagnosi AI (è tua di diritto).\"\"\")\n        st.markdown(\"\"\"Un ospedale vorrebbe comprarla da te. Qual è il **prezzo minimo** che pretendi per cederla?\"\"\")\n        val = st.number_input('Valore in Euro (€):', 0, 50000, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Scenario:** Un ospedale ha appena messo in vendita una rarissima Licenza Software per diagnosi AI.\"\"\")\n        st.markdown(\"\"\"A te farebbe molto comodo. Qual è il **prezzo massimo** che sei disposto a pagare per averla?\"\"\")\n        val = st.number_input('Valore in Euro (€):', 0, 50000, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="IT"
)

build_ab_page(
    "13_Costi_Sommersi_Teatro.py", "sunk_theater", "🎭", "Spettacolo", "Lo Spettacolo a Teatro",
    "",
    "        st.markdown(\"\"\"**Scenario:** Hai acquistato a tue spese un biglietto da 50€ per vedere uno spettacolo teatrale che ti interessava.\"\"\")\n        st.markdown(\"\"\"Arriva la sera dello spettacolo ma c'è una tormenta di neve spaventosa.\"\"\")\n        scelta = st.radio('Cosa decidi di fare?', ['A) Vado a teatro lo stesso (sfido la tormenta per non buttare i 50€).', 'B) Resto a casa al caldo rinunciando allo spettacolo.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** Un amico ti ha **regalato** un biglietto per vedere uno spettacolo teatrale che ti interessava (costo per te: 0€).\"\"\")\n        st.markdown(\"\"\"Arriva la sera dello spettacolo ma c'è una tormenta di neve spaventosa.\"\"\")\n        scelta = st.radio('Cosa decidi di fare?', ['A) Vado a teatro lo stesso.', 'B) Resto a casa al caldo.'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Vado' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

build_ab_page(
    "14_Costi_Sommersi_AI.py", "sunk_ai", "🏭", "Progetto Ricerca", "Investimento Ricerca",
    "",
    "        st.markdown(\"\"\"**Scenario:** Sei il capo di un team. Hai deciso proprio OGGI di iniziare a programmare un nuovo algoritmo diagnostico.\"\"\")\n        st.markdown(\"\"\"Mentre bevi il caffè, vedi una news: Google ha appena rilasciato un algoritmo gratuito tecnicamente superiore al tuo.\"\"\")\n        scelta = st.radio('Che decisione prendi?', ['Continuo a sviluppare il mio', 'Abbandono il mio progetto'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** Sei il capo di un team. Da **4 anni precisi** tu e i tuoi uomini lavorate senza sosta a un nuovo algoritmo (siete al 90% dell'opera).\"\"\")\n        st.markdown(\"\"\"Mentre bevi il caffè, vedi una news: Google ha appena rilasciato un algoritmo gratuito tecnicamente superiore al tuo.\"\"\")\n        scelta = st.radio('Che decisione prendi?', ['Continuo a sviluppare il mio', 'Abbandono il mio progetto'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Continuo' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

build_ab_page(
    "15_Effetto_Default.py", "default_organ", "🫀", "Assicurazione", "Modulo Assicurativo",
    "    st.markdown(\"\"\"**Firma del nuovo modulo per dipendenti ospedalieri.**\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        opt = st.checkbox('⚠️ Spunta la casella se **VUOI** acconsentire a diventare un donatore di organi.', value=False, key='c1')\n",
    "        opt = st.checkbox('⚠️ Spunta la casella se **NON VUOI** diventare un donatore di organi.', value=True, key='c2')\n",
    "",
    "        v = 1 if (st.session_state.gruppo == 'A' and opt == True) or (st.session_state.gruppo == 'B' and opt == False) else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

build_ab_page(
    "16_Priming_Associativo.py", "priming", "🍝", "Associazioni", "Parole e Associazioni",
    "",
    "        st.markdown(\"\"\"Leggi veloce: FORCHETTA, PRANZO, FAME.\"\"\")\n        val = st.text_input('Completa la parola: S O _ P', key='t1')\n",
    "        st.markdown(\"\"\"Leggi veloce: DOCCIA, SCHIUMA, PULITO.\"\"\")\n        val = st.text_input('Completa la parola: S O _ P', key='t2')\n",
    "",
    "        v = 1 if 'sapore' in val.lower() or 'soup' in val.lower() else (2 if 'sapone' in val.lower() or 'soap' in val.lower() else 0)\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

build_ab_page(
    "17_Dunning_Kruger.py", "dunning", "🎓", "Stima di Sé", "Autovalutazione",
    "",
    "        scelta = st.radio('Ritieni la tua abilità accademica superiore alla media della classe?', ['Sopra la media', 'Nella media', 'Sotto la media'], index=None, key='r1')\n",
    "        scelta = st.radio('Ritieni la tua abilità accademica superiore a quella di Giorgio Parisi (Premio Nobel)?', ['Sopra la sua', 'Nella sua', 'Sotto la sua'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Sopra' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

# 18. WYSIATI / BRUNER & POTTER (Fire Hydrant vs Minion) IT
# Open Text Input (No hints/multiple-choice!) + Immediate First Impression Instruction
build_ab_page(
    "18_WYSIATI.py", "wysiati", "👁️", "WYSIATI Visivo", "Riconoscimento Immagine (Bruner & Potter)",
    "    st.markdown(\"\"\"**Scenario:** Guarda con attenzione la sequenza visiva qui sotto.\\n\\n⚡ **IMPORTANTE:** Scrivi nello spazio sottostante **LA PRIMA COSA CHE VEDI** (la tua primissima impressione non appena l'immagine compare) e invia subito la risposta!\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        b64_img = load_hydrant_b64()\n        if b64_img:\n            html_a = f'''<!DOCTYPE html><html><head><style>body {{ margin:0; padding:0; background:#111; font-family:sans-serif; text-align:center; color:white; }} .box {{ padding:1.2rem; background:#111; border-radius:20px; border:1px solid rgba(108,99,255,0.3); }} img {{ width:220px; border-radius:16px; filter:blur(24px); -webkit-filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,0.5); transition: filter 0.1s linear; }} p {{ color:#6C63FF; font-weight:600; font-size:0.9rem; margin-top:12px; }} button {{ background:#6C63FF; color:white; border:none; padding:10px 20px; border-radius:10px; font-weight:700; font-size:0.95rem; cursor:pointer; margin-top:8px; box-shadow:0 4px 12px rgba(108,99,255,0.4); }} button:active {{ transform: scale(0.96); }}</style></head><body><div class=\"box\"><img id=\"imgA\" src=\"data:image/jpeg;base64,{b64_img}\" style=\"filter:blur(24px); -webkit-filter:blur(24px);\" /><p id=\"txtA\">🎥 Messa a fuoco video fluida (8s)...</p><button id=\"btnA\" onclick=\"playA()\">▶️ Riproduci Animazione</button></div><script>function playA() {{ var img=document.getElementById('imgA'); var txt=document.getElementById('txtA'); var btn=document.getElementById('btnA'); var start=null; var dur=8000; if(img) {{ img.style.filter=\"blur(24px)\"; img.style.webkitFilter=\"blur(24px)\"; }} txt.innerText=\"🎥 Messa a fuoco video fluida in corso (8s)...\"; btn.disabled=true; btn.style.opacity=\"0.6\"; function step(ts) {{ if(!start) start=ts; var progress=(ts-start)/dur; if(progress>1) progress=1; var curBlur=24-(progress*21); if(img) {{ img.style.filter=\"blur(\"+curBlur+\"px)\"; img.style.webkitFilter=\"blur(\"+curBlur+\"px)\"; }} if(progress<1) {{ window.requestAnimationFrame(step); }} else {{ txt.innerText=\"✅ Messa a fuoco completata!\"; btn.disabled=false; btn.style.opacity=\"1\"; }} }} window.requestAnimationFrame(step); }} window.onload=playA; setTimeout(playA, 100);</script></body></html>'''\n            components.html(html_a, height=360)\n        else:\n            st.markdown(\"\"\"<div style='text-align:center; padding:1.5rem; background:#111; border-radius:12px;'><div style='font-size:70px; filter:blur(9px); line-height:1;'>🧯🟡</div></div>\"\"\")\n        scelta = st.text_input('Scrivi qui la PRIMA COSA che vedi / prima impressione:', key='t_wys1')\n",
    "        b64_img = load_hydrant_b64()\n        if b64_img:\n            html_b = f'''<!DOCTYPE html><html><head><style>body {{ margin:0; padding:0; background:#111; font-family:sans-serif; text-align:center; color:white; }} .box {{ padding:1.2rem; background:#111; border-radius:20px; border:1px solid rgba(255,166,0,0.3); }} img {{ width:220px; border-radius:16px; filter:blur(24px); -webkit-filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,0.5); transition: filter 0.3s ease; }} p {{ color:#FFA600; font-weight:600; font-size:0.9rem; margin-top:12px; }} button {{ background:#FFA600; color:black; border:none; padding:10px 20px; border-radius:10px; font-weight:700; font-size:0.95rem; cursor:pointer; margin-top:8px; box-shadow:0 4px 12px rgba(255,166,0,0.4); }} button:active {{ transform: scale(0.96); }}</style></head><body><div class=\"box\"><img id=\"imgB\" src=\"data:image/jpeg;base64,{b64_img}\" style=\"filter:blur(24px); -webkit-filter:blur(24px);\" /><p id=\"txtB\">🖼️ Frame 1 di 4 (Sfocatura iniziale 24px)...</p><button id=\"btnB\" onclick=\"playB()\">▶️ Riproduci Animazione</button></div><script>var timerId=null; function playB() {{ if(timerId) clearTimeout(timerId); var img=document.getElementById('imgB'); var txt=document.getElementById('txtB'); var btn=document.getElementById('btnB'); if(img) {{ img.style.filter=\"blur(24px)\"; img.style.webkitFilter=\"blur(24px)\"; }} btn.disabled=true; btn.style.opacity=\"0.6\"; var frames=[{{b:24,l:\"🖼️ Frame 1 di 4 (Sfocatura iniziale 24px)\"}},{{b:16,l:\"🖼️ Frame 2 di 4 (Sfocatura marcata 16px)\"}},{{b:10,l:\"🖼️ Frame 3 di 4 (Sfocatura media 10px)\"}},{{b:3,l:\"🖼️ Frame 4 di 4 (Messa a fuoco finale 3px)\"}}]; var idx=0; function showNext() {{ if(img) {{ img.style.filter=\"blur(\"+frames[idx].b+\"px)\"; img.style.webkitFilter=\"blur(\"+frames[idx].b+\"px)\"; }} if(txt) txt.innerText=frames[idx].l; idx++; if(idx<frames.length) {{ timerId=setTimeout(showNext, 2000); }} else {{ btn.disabled=false; btn.style.opacity=\"1\"; }} }} showNext(); }} window.onload=playB; setTimeout(playB, 100);</script></body></html>'''\n            components.html(html_b, height=360)\n        else:\n            st.markdown(\"\"\"<div style='text-align:center; padding:1.5rem; background:#111; border-radius:12px;'><div style='font-size:70px; filter:blur(5px); line-height:1;'>🧯🔴</div></div>\"\"\")\n        scelta = st.text_input('Scrivi qui la PRIMA COSA che vedi / prima impressione:', key='t_wys2')\n",
    "",
    "        v = 1 if any(w in scelta.lower() for w in ['idrante', 'estintore', 'hydrant', 'extinguisher']) else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="IT"
)

build_ab_page(
    "19_Illusione_Focalizzazione.py", "focalizzazione", "😊", "Questionario Benessere", "Sondaggio sul Benessere",
    "",
    "        st.markdown(\"\"\"**1. Quanto sei felice (1-10)?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1a')\n        eta = st.number_input('2. Quante uscite romantiche nell\\'ultimo mese?', 0, 30, value=None, key='n1b')\n",
    "        eta = st.number_input('1. Quante uscite romantiche nell\\'ultimo mese?', 0, 30, value=None, key='n2a')\n        st.markdown(\"\"\"**2. Quanto sei felice (1-10)?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2b')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="IT"
)

build_single_page(
    "20_Base_Rate_Neglect.py", "base_rate", "🔬", "Diagnosi Medica", "Paradosso Diagnostico",
    "    st.markdown(\"\"\"**Scenario:** Immagina che Una grave malattia genetica colpisca esattamente l'1% della popolazione mondiale.\"\"\")\n    st.markdown(\"\"\"Un test in grado di individuarla è infallibile al 95% (5% falsi positivi/negativi).\"\"\")\n    st.markdown(\"\"\"Fai il test e risulti **POSITIVO**.\"\"\")\n    val = st.number_input('Qual è la probabilità effettiva (0-100%) che tu abbia davvero la malattia?', 0, 100, value=None)\n",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': val}).execute()\n",
    lang="IT"
)

build_single_page(
    "21_L_Esca.py", "decoy", "🗞️", "Abbonamento", "Rivista The Economist",
    "    scelta = st.radio('Scegli:', ['A) Solo Web (50€)', 'B) Cartaceo (120€)', 'C) Web+Cartaceo (120€)'], index=None)\n",
    "        v = 1 if 'A)' in scelta else (2 if 'B)' in scelta else 3)\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': v}).execute()\n",
    lang="IT"
)

build_single_page(
    "22_Regressione_Media.py", "regression", "🧑‍✈️", "Psicologia Umana", "L'Effetto Lode/Castigo",
    "    st.markdown(\"\"\"Istruttori israeliani: sgridare migliora, lodare peggiora. Credi che sia:\"\"\")\n    scelta_dom = st.radio('', ['A) Sia intuizione corretta.', 'B) Sia errore statistico.'], index=None)\n",
    "        v = 1 if 'A)' in scelta_dom else 2\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': v}).execute()\n",
    lang="IT"
)

build_single_page(
    "23_Bias_Conferma_Wason.py", "wason_246", "🧮", "Bias di Conferma", "Compito 2-4-6 (Wason, 1960)",
    "    st.markdown(\"\"\"**Scenario:** Ti viene mostrata la sequenza numerica: **2 - 4 - 6**.\"\"\")\n    st.markdown(\"\"\"Questa sequenza rispetta una **regola segreta** inventata dal docente.\"\"\")\n    st.markdown(\"\"\"Quale tra queste terterne di numeri proveresti per prima per verificare se la tua ipotesi sulla regola è corretta?\"\"\")\n    scelta_dom = st.radio('', ['A) 8 - 10 - 12 (Continua la serie dei numeri pari)', 'B) 1 - 3 - 5 (Prova numeri dispari con passo +2)', 'C) 1 - 2 - 3 (Prova sequenza generica crescente)', 'D) 6 - 4 - 2 (Prova sequenza decrescente)'], index=None)\n",
    "        v = 1 if 'A)' in scelta_dom else (2 if 'B)' in scelta_dom else (3 if 'C)' in scelta_dom else 4))\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': v}).execute()\n",
    lang="IT"
)


# ==========================================
# ENGLISH PAGES (1-23)
# ==========================================

build_ab_page(
    "1_Macchina_EN.py", "macchina", "🚗", "Car Crash", "Car Crash Experiment",
    "    st.markdown(\"\"\"**Scenario:** You have just watched a short video clip of an automobile accident.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"**How fast (in km/h) were the cars going when they HIT each other?**\"\"\")\n        val = st.number_input('Estimate speed (km/h):', 0, 200, value=None, key='s1')\n",
    "        st.markdown(\"\"\"**How fast (in km/h) were the cars going when they SMASHED into each other?**\"\"\")\n        val = st.number_input('Estimate speed (km/h):', 0, 200, value=None, key='s2')\n",
    "    st.markdown(\"\"\"**2. Did you see any broken glass on the ground?**\"\"\")\n    vetri = st.radio('Choose:', ['Yes', 'No'], horizontal=True, index=None, key='v')\n",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n        supabase.table('Risposte').insert({'esperimento': 'macchina_vetri', 'gruppo': st.session_state.gruppo, 'valore': 1 if vetri in ['Sì', 'Yes'] else 0}).execute()\n",
    lang="EN"
)

build_ab_page(
    "2_Malattia_Asiatica_EN.py", "asian_disease", "🦠", "Asian Disease", "The Asian Disease Problem",
    "    st.markdown(\"\"\"**Scenario:** Imagine that your country is preparing for the outbreak of an unusual Asian disease, which is expected to kill 600 people. Two alternative programs to combat the disease have been proposed.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"Which program do you choose?\"\"\")\n        scelta = st.radio('', ['Program A: 200 people will be saved (certain outcome).', 'Program B: 1/3 probability that 600 people will be saved, and 2/3 probability that no people will be saved.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"Which program do you choose?\"\"\")\n        scelta = st.radio('', ['Program A: 400 people will die (certain outcome).', 'Program B: 1/3 probability that nobody will die, and 2/3 probability that 600 people will die.'], index=None, key='r2')\n",
    "",
    "        v = 0 if 'Program A:' in scelta else 1\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

build_ab_page(
    "3_Framing_AI_EN.py", "framing_ai", "🤖", "Medical AI", "AI Robotic Surgery",
    "    st.markdown(\"\"\"**Scenario:** A new AI robotic surgical software is set to perform a complex procedure on 100 patients in critical condition.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        st.markdown(\"\"\"**Statistical Data:** If you use the AI software, **90 patients will survive**.\\n\\nDo you authorize the software's use?\"\"\")\n        scelta = st.radio('', ['Yes', 'No'], horizontal=True, index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Statistical Data:** If you use the AI software, **10 patients will die**.\\n\\nDo you authorize the software's use?\"\"\")\n        scelta = st.radio('', ['Yes', 'No'], horizontal=True, index=None, key='r2')\n",
    "",
    "        v = 1 if scelta == 'Yes' else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

build_ab_page(
    "4_Ancoraggio_Gandhi_EN.py", "gandhi", "👴", "Gandhi's Age", "Gandhi's Age Anchoring",
    "",
    "        st.markdown(\"\"\"**Did Gandhi die before or after the age of 114?**\"\"\")\n        st.radio('', ['After 114', 'Before 114'], horizontal=True, index=None, key='r1')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**How old was he when he died according to your estimate?**\"\"\")\n        eta = st.number_input('Enter age estimate (years):', 0, 150, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Did Gandhi die before or after the age of 35?**\"\"\")\n        st.radio('', ['After 35', 'Before 35'], horizontal=True, index=None, key='r2')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**How old was he when he died according to your estimate?**\"\"\")\n        eta = st.number_input('Enter age estimate (years):', 0, 150, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': eta}).execute()\n",
    lang="EN"
)

build_ab_page(
    "5_Ancoraggio_Roulette_EN.py", "roulette", "🎰", "Roulette Wheel", "Hospital Misdiagnosis Statistics",
    "",
    "        val = st.number_input('In your opinion, what is the exact percentage of misdiagnoses caused by physician fatigue?', 0, 100, value=None, key='s1')\n",
    "        val = st.number_input('In your opinion, what is the exact percentage of misdiagnoses caused by physician fatigue?', 0, 100, value=None, key='s2')\n",
    "    st.markdown(\"\"\"---\"\"\")\n    st.markdown(\"\"\"### The number spun on the wheel today is: **12**\"\"\" if st.session_state.gruppo == 'A' else \"\"\"### The number spun on the wheel today is: **65**\"\"\")\n",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="EN"
)

build_ab_page(
    "6_Avversione_Perdite_EN.py", "loss_aversion", "💶", "Loss Aversion", "Financial Decisions",
    "",
    "        st.markdown(\"\"\"**Scenario:** You have just been given €1,000 as a bonus. Which of these two options do you choose?\"\"\")\n        scelta = st.radio('', ['A) Win an additional €500 for sure (100% certainty)', 'B) Flip a coin: 50% chance to win €1,000, and 50% chance to win €0.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** You have just been given €2,000 as a bonus. Which of these two options do you choose?\"\"\")\n        scelta = st.radio('', ['A) Lose €500 for sure (100% certainty)', 'B) Flip a coin: 50% chance to lose €1,000, and 50% chance to lose €0.'], index=None, key='r2')\n",
    "",
    "        v = 0 if 'for sure' in scelta else 1\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

build_ab_page(
    "7_Illusione_Verita_EN.py", "illusione_verita", "👁️", "Truth Illusion", "Evaluate the Statement",
    "",
    "        st.markdown(\"\"\"<p style=\"font-size:32px; font-weight:900; color:#FAFAFA; font-family:Arial; text-align:center;\">Taking Omega-3 reduces<br>bodily inflammation by 15%.</p>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**On a scale of 1 to 10, how true and scientifically valid does this statement seem?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1')\n",
    "        st.markdown(\"\"\"<p style=\"font-size:16px; font-weight:300; color:#AAAAAA; font-family:'Comic Sans MS', cursive; text-align:center; padding: 2rem;\">Taking omega-3 reduces bodily inflammation by 15%.</p>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**On a scale of 1 to 10, how true and scientifically valid does this statement seem?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="EN"
)

build_ab_page(
    "8_Euristica_Disponibilita_EN.py", "availability", "🧠", "Memory Recall", "Personality Inventory",
    "",
    "        st.markdown(\"\"\"1. Think of and list **6 situations** in which you managed to behave very assertively (standing up firmly for your point of view).\"\"\")\n        st.text_area('Briefly list the 6 situations:', height=140, key='t1')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**In general, how assertive do you consider yourself to be (1-10)?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1')\n",
    "        st.markdown(\"\"\"1. Think of and list **12 situations** in which you managed to behave very assertively (standing up firmly for your point of view).\"\"\")\n        st.text_area('Briefly list the 12 situations:', height=200, key='t2')\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**In general, how assertive do you consider yourself to be (1-10)?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="EN"
)

build_ab_page(
    "9_Problema_Linda_EN.py", "linda", "👩‍🦰", "Profile Evaluation", "Linda's Profile",
    "    st.markdown(\"\"\"**Profile:** Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice, and also participated in anti-nuclear demonstrations.\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        val = st.number_input('In light of her description, what is the probability (0-100%) that Linda is today **a bank teller**?', 0, 100, value=None, key='s1')\n",
    "        val = st.number_input('In light of her description, what is the probability (0-100%) that Linda is today **a bank teller and active in the feminist movement**?', 0, 100, value=None, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="EN"
)

build_ab_page(
    "10_Effetto_Alone_EN.py", "halo_asch", "👤", "Impression", "Profile Evaluation",
    "",
    "        st.markdown(\"\"\"Consider **Alan**. His colleagues describe him as:\"\"\")\n        st.markdown(\"\"\"> *Intelligent, industrious, impulsive, critical, stubborn, envious.*\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**On a scale of 1 to 10, how favorably do you rate Alan as a coworker?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1')\n",
    "        st.markdown(\"\"\"Consider **Ben**. His colleagues describe him as:\"\"\")\n        st.markdown(\"\"\"> *Envious, stubborn, critical, impulsive, industrious, intelligent.*\"\"\")\n        st.markdown(\"\"\"---\"\"\")\n        st.markdown(\"\"\"**On a scale of 1 to 10, how favorably do you rate Ben as a coworker?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="EN"
)

build_ab_page(
    "11_Effetto_Dote_Tazza_EN.py", "endow_mug", "☕", "Mug Market", "Thaler's Mug Experiment",
    "",
    "        st.markdown(\"\"\"**Scenario:** Congratulations! You have just been **GIVEN** this official university mug (it is now your property).\"\"\")\n        st.markdown(\"\"\"<div style=\"text-align: center; font-size: 60px;\">☕🎓</div>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"A classmate wants to buy it from you. What is the **MINIMUM PRICE** at which you are willing to sell it?\"\"\")\n        val = st.number_input('Price in Euros (€):', 0.0, 50.0, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Scenario:** A classmate has just been given an official university mug. You currently do not have one.\"\"\")\n        st.markdown(\"\"\"<div style=\"text-align: center; font-size: 60px;\">☕🎓</div>\"\"\", unsafe_allow_html=True)\n        st.markdown(\"\"\"They are willing to sell it. What is the **MAXIMUM PRICE** you are willing to pay right now to buy it from them?\"\"\")\n        val = st.number_input('Price in Euros (€):', 0.0, 50.0, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="EN"
)

build_ab_page(
    "12_Effetto_Dote_AI_EN.py", "endow_ai", "💻", "AI Software", "Medical Software License",
    "",
    "        st.markdown(\"\"\"**Scenario:** You have been gifted a lifetime license for a rare AI diagnostic software (it belongs to you).\"\"\")\n        st.markdown(\"\"\"A hospital wants to buy it. What is the **minimum price** you demand to sell it?\"\"\")\n        val = st.number_input('Value in Euros (€):', 0, 50000, value=None, key='n1')\n",
    "        st.markdown(\"\"\"**Scenario:** A hospital has just put up for sale a rare AI diagnostic software license.\"\"\")\n        st.markdown(\"\"\"It would be very useful to you. What is the **maximum price** you are willing to pay to buy it?\"\"\")\n        val = st.number_input('Value in Euros (€):', 0, 50000, value=None, key='n2')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="EN"
)

build_ab_page(
    "13_Costi_Sommersi_Teatro_EN.py", "sunk_theater", "🎭", "Theater Show", "The Theater Ticket Scenario",
    "",
    "        st.markdown(\"\"\"**Scenario:** You purchased a €50 ticket for a theater show you were really interested in seeing.\"\"\")\n        st.markdown(\"\"\"On the evening of the show, a severe snowstorm strikes.\"\"\")\n        scelta = st.radio('What do you decide to do?', ['A) Go to the theater anyway (brave the storm to not waste €50).', 'B) Stay home warm and miss the show.'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** A friend **gave you a free ticket** (€0 cost to you) for a theater show you were interested in seeing.\"\"\")\n        st.markdown(\"\"\"On the evening of the show, a severe snowstorm strikes.\"\"\")\n        scelta = st.radio('What do you decide to do?', ['A) Go to the theater anyway.', 'B) Stay home warm.'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Go' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

build_ab_page(
    "14_Costi_Sommersi_AI_EN.py", "sunk_ai", "🏭", "Research Project", "AI Research Investment",
    "",
    "        st.markdown(\"\"\"**Scenario:** You are the lead of a research team. TODAY you decided to start coding a new diagnostic algorithm.\"\"\")\n        st.markdown(\"\"\"While drinking coffee, you read a news story: Google has just released a free algorithm that is technically superior to yours.\"\"\")\n        scelta = st.radio('What decision do you make?', ['Continue developing mine', 'Abandon my project'], index=None, key='r1')\n",
    "        st.markdown(\"\"\"**Scenario:** You are the lead of a research team. For **4 full years** you and your team have worked tirelessly on a new algorithm (90% complete).\"\"\")\n        st.markdown(\"\"\"While drinking coffee, you read a news story: Google has just released a free algorithm that is technically superior to yours.\"\"\")\n        scelta = st.radio('What decision do you make?', ['Continue developing mine', 'Abandon my project'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Continue' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

build_ab_page(
    "15_Effetto_Default_EN.py", "default_organ", "🫀", "Employee Form", "Organ Donor Agreement",
    "    st.markdown(\"\"\"**Signing the new hospital employee onboarding form.**\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        opt = st.checkbox('⚠️ Check the box if you **WANT** to consent to becoming an organ donor.', value=False, key='c1')\n",
    "        opt = st.checkbox('⚠️ Check the box if you **DO NOT WANT** to become an organ donor.', value=True, key='c2')\n",
    "",
    "        v = 1 if (st.session_state.gruppo == 'A' and opt == True) or (st.session_state.gruppo == 'B' and opt == False) else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

build_ab_page(
    "16_Priming_Associativo_EN.py", "priming", "🍝", "Word Associations", "Words and Associations",
    "",
    "        st.markdown(\"\"\"Read quickly: FORK, LUNCH, HUNGER.\"\"\")\n        val = st.text_input('Complete the word: S O _ P', key='t1')\n",
    "        st.markdown(\"\"\"Read quickly: SHOWER, FOAM, CLEAN.\"\"\")\n        val = st.text_input('Complete the word: S O _ P', key='t2')\n",
    "",
    "        v = 1 if 'soup' in val.lower() or 'sapore' in val.lower() else (2 if 'soap' in val.lower() or 'sapone' in val.lower() else 0)\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

build_ab_page(
    "17_Dunning_Kruger_EN.py", "dunning", "🎓", "Self-Assessment", "Academic Self-Evaluation",
    "",
    "        scelta = st.radio('Do you consider your academic ability to be above average compared to your classmates?', ['Above average', 'Average', 'Below average'], index=None, key='r1')\n",
    "        scelta = st.radio('Do you consider your academic ability to be superior to that of Giorgio Parisi (Nobel Laureate)?', ['Above his', 'Equal to his', 'Below his'], index=None, key='r2')\n",
    "",
    "        v = 1 if 'Above' in scelta else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

# 18. WYSIATI / BRUNER & POTTER (Fire Hydrant vs Minion) EN
# Open Text Input (No hints/multiple-choice!) + Immediate First Impression Instruction
build_ab_page(
    "18_WYSIATI_EN.py", "wysiati", "👁️", "Visual WYSIATI", "Image Recognition (Bruner & Potter)",
    "    st.markdown(\"\"\"**Scenario:** Carefully observe the visual sequence shown below.\\n\\n⚡ **IMPORTANT:** Type in the box below **THE VERY FIRST THING YOU SEE** (your immediate first impression as soon as the image appears) and submit immediately!\"\"\")\n    st.markdown(\"\"\"---\"\"\")\n",
    "        b64_img = load_hydrant_b64()\n        if b64_img:\n            html_a = f'''<!DOCTYPE html><html><head><style>body {{ margin:0; padding:0; background:#111; font-family:sans-serif; text-align:center; color:white; }} .box {{ padding:1.2rem; background:#111; border-radius:20px; border:1px solid rgba(108,99,255,0.3); }} img {{ width:220px; border-radius:16px; filter:blur(24px); -webkit-filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,0.5); transition: filter 0.1s linear; }} p {{ color:#6C63FF; font-weight:600; font-size:0.9rem; margin-top:12px; }} button {{ background:#6C63FF; color:white; border:none; padding:10px 20px; border-radius:10px; font-weight:700; font-size:0.95rem; cursor:pointer; margin-top:8px; box-shadow:0 4px 12px rgba(108,99,255,0.4); }} button:active {{ transform: scale(0.96); }}</style></head><body><div class=\"box\"><img id=\"imgA\" src=\"data:image/jpeg;base64,{b64_img}\" style=\"filter:blur(24px); -webkit-filter:blur(24px);\" /><p id=\"txtA\">🎥 Continuous fluid video unblurring in progress (8s)...</p><button id=\"btnA\" onclick=\"playA()\">▶️ Play Animation</button></div><script>function playA() {{ var img=document.getElementById('imgA'); var txt=document.getElementById('txtA'); var btn=document.getElementById('btnA'); var start=null; var dur=8000; if(img) {{ img.style.filter=\"blur(24px)\"; img.style.webkitFilter=\"blur(24px)\"; }} txt.innerText=\"🎥 Continuous fluid video unblurring in progress (8s)...\"; btn.disabled=true; btn.style.opacity=\"0.6\"; function step(ts) {{ if(!start) start=ts; var progress=(ts-start)/dur; if(progress>1) progress=1; var curBlur=24-(progress*21); if(img) {{ img.style.filter=\"blur(\"+curBlur+\"px)\"; img.style.webkitFilter=\"blur(\"+curBlur+\"px)\"; }} if(progress<1) {{ window.requestAnimationFrame(step); }} else {{ txt.innerText=\"✅ Focus sequence completed!\"; btn.disabled=false; btn.style.opacity=\"1\"; }} }} window.requestAnimationFrame(step); }} window.onload=playA; setTimeout(playA, 100);</script></body></html>'''\n            components.html(html_a, height=360)\n        else:\n            st.markdown(\"\"\"<div style='text-align:center; padding:1.5rem; background:#111; border-radius:12px;'><div style='font-size:70px; filter:blur(9px); line-height:1;'>🧯🟡</div></div>\"\"\")\n        scelta = st.text_input('Type here THE VERY FIRST THING YOU SEE / initial impression:', key='t_wys1_en')\n",
    "        b64_img = load_hydrant_b64()\n        if b64_img:\n            html_b = f'''<!DOCTYPE html><html><head><style>body {{ margin:0; padding:0; background:#111; font-family:sans-serif; text-align:center; color:white; }} .box {{ padding:1.2rem; background:#111; border-radius:20px; border:1px solid rgba(255,166,0,0.3); }} img {{ width:220px; border-radius:16px; filter:blur(24px); -webkit-filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,0.5); transition: filter 0.3s ease; }} p {{ color:#FFA600; font-weight:600; font-size:0.9rem; margin-top:12px; }} button {{ background:#FFA600; color:black; border:none; padding:10px 20px; border-radius:10px; font-weight:700; font-size:0.95rem; cursor:pointer; margin-top:8px; box-shadow:0 4px 12px rgba(255,166,0,0.4); }} button:active {{ transform: scale(0.96); }}</style></head><body><div class=\"box\"><img id=\"imgB\" src=\"data:image/jpeg;base64,{b64_img}\" style=\"filter:blur(24px); -webkit-filter:blur(24px);\" /><p id=\"txtB\">🖼️ Frame 1 of 4 (Initial blur 24px)...</p><button id=\"btnB\" onclick=\"playB()\">▶️ Play Animation</button></div><script>var timerId=null; function playB() {{ if(timerId) clearTimeout(timerId); var img=document.getElementById('imgB'); var txt=document.getElementById('txtB'); var btn=document.getElementById('btnB'); if(img) {{ img.style.filter=\"blur(24px)\"; img.style.webkitFilter=\"blur(24px)\"; }} btn.disabled=true; btn.style.opacity=\"0.6\"; var frames=[{{b:24,l:\"🖼️ Frame 1 of 4 (Initial blur 24px)\"}},{{b:16,l:\"🖼️ Frame 2 of 4 (Heavy blur 16px)\"}},{{b:10,l:\"🖼️ Frame 3 of 4 (Medium blur 10px)\"}},{{b:3,l:\"🖼️ Frame 4 of 4 (Final focus 3px)\"}}]; var idx=0; function showNext() {{ if(img) {{ img.style.filter=\"blur(\"+frames[idx].b+\"px)\"; img.style.webkitFilter=\"blur(\"+frames[idx].b+\"px)\"; }} if(txt) txt.innerText=frames[idx].l; idx++; if(idx<frames.length) {{ timerId=setTimeout(showNext, 2000); }} else {{ btn.disabled=false; btn.style.opacity=\"1\"; }} }} showNext(); }} window.onload=playB; setTimeout(playB, 100);</script></body></html>'''\n            components.html(html_b, height=360)\n        else:\n            st.markdown(\"\"\"<div style='text-align:center; padding:1.5rem; background:#111; border-radius:12px;'><div style='font-size:70px; filter:blur(5px); line-height:1;'>🧯🔴</div></div>\"\"\")\n        scelta = st.text_input('Type here THE VERY FIRST THING YOU SEE / initial impression:', key='t_wys2_en')\n",
    "",
    "        v = 1 if any(w in scelta.lower() for w in ['idrante', 'estintore', 'hydrant', 'extinguisher']) else 0\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()\n",
    lang="EN"
)

build_ab_page(
    "19_Illusione_Focalizzazione_EN.py", "focalizzazione", "😊", "Wellbeing Survey", "Life Satisfaction Survey",
    "",
    "        st.markdown(\"\"\"**1. How happy are you with your life (1-10)?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s1a')\n        eta = st.number_input('2. How many dates did you go on in the last month?', 0, 30, value=None, key='n1b')\n",
    "        eta = st.number_input('1. How many dates did you go on in the last month?', 0, 30, value=None, key='n2a')\n        st.markdown(\"\"\"**2. How happy are you with your life (1-10)?**\"\"\")\n        val = st.radio('', [1,2,3,4,5,6,7,8,9,10], horizontal=True, index=None, key='s2b')\n",
    "",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': val}).execute()\n",
    lang="EN"
)

build_single_page(
    "20_Base_Rate_Neglect_EN.py", "base_rate", "🔬", "Medical Diagnosis", "Diagnostic Paradox",
    "    st.markdown(\"\"\"**Scenario:** Imagine that a serious genetic condition affects exactly 1% of the world population.\"\"\")\n    st.markdown(\"\"\"A diagnostic test for it is 95% accurate (5% false positive/negative rate).\"\"\")\n    st.markdown(\"\"\"You take the test and result **POSITIVE**.\"\"\")\n    val = st.number_input('What is the actual probability (0-100%) that you actually have the condition?', 0, 100, value=None)\n",
    "        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': val}).execute()\n",
    lang="EN"
)

build_single_page(
    "21_L_Esca_EN.py", "decoy", "🗞️", "Subscription", "The Economist Subscription",
    "    scelta = st.radio('Choose:', ['A) Web Only ($50)', 'B) Print Only ($120)', 'C) Web + Print ($120)'], index=None)\n",
    "        v = 1 if 'A)' in scelta else (2 if 'B)' in scelta else 3)\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': v}).execute()\n",
    lang="EN"
)

build_single_page(
    "22_Regressione_Media_EN.py", "regression", "🧑‍✈️", "Human Behavior", "Praise vs Punishment Effect",
    "    st.markdown(\"\"\"Flight instructors notice: reprimanding leads to better subsequent maneuvers, while praising leads to worse ones. Do you believe this is:\"\"\")\n    scelta_dom = st.radio('', ['A) Correct psychological intuition.', 'B) Statistical mistake (regression to the mean).'], index=None)\n",
    "        v = 1 if 'A)' in scelta_dom else 2\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': v}).execute()\n",
    lang="EN"
)

build_single_page(
    "23_Bias_Conferma_Wason_EN.py", "wason_246", "🧮", "Confirmation Bias", "2-4-6 Task (Wason, 1960)",
    "    st.markdown(\"\"\"**Scenario:** You are shown the number sequence: **2 - 4 - 6**.\"\"\")\n    st.markdown(\"\"\"This sequence conforms to a **secret rule** created by the instructor.\"\"\")\n    st.markdown(\"\"\"Which of the following triplets of numbers would you test first to check if your hypothesis about the rule is correct?\"\"\")\n    scelta_dom = st.radio('', ['A) 8 - 10 - 12 (Continue even numbers sequence)', 'B) 1 - 3 - 5 (Test odd numbers sequence)', 'C) 1 - 2 - 3 (Test generic increasing sequence)', 'D) 6 - 4 - 2 (Test decreasing sequence)'], index=None)\n",
    "        v = 1 if 'A)' in scelta_dom else (2 if 'B)' in scelta_dom else (3 if 'C)' in scelta_dom else 4))\n        supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': 'A', 'valore': v}).execute()\n",
    lang="EN"
)

print("Rigenerazione completata con campo di testo libero (Open Text Input)!")
