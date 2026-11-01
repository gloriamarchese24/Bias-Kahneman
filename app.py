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
.main-title { font-size: 2.6rem; font-weight: 900; background: linear-gradient(135deg, #6C63FF 0%, #FF6584 50%, #FFA600 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.2rem; }
.sub-title { font-size: 1.15rem; color: #888; text-align: center; margin-bottom: 1.5rem; }
.metric-card { background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%); border-radius: 16px; padding: 1.5rem; text-align: center; border: 1px solid rgba(108, 99, 255, 0.3); box-shadow: 0 4px 20px rgba(108, 99, 255, 0.15); }
.metric-value { font-size: 3.3rem; font-weight: 900; margin: 0.5rem 0; }
.metric-label { font-size: 0.95rem; color: #aaa; text-transform: uppercase; letter-spacing: 2px; }
.diff-card { background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%); border-radius: 16px; padding: 1.5rem; text-align: center; border: 1px solid rgba(0, 255, 136, 0.3); }
.diff-value { font-size: 3.3rem; font-weight: 900; color: #00FF88; margin: 0.5rem 0; }
.count-badge { display: inline-block; background: rgba(108, 99, 255, 0.2); color: #6C63FF; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 600; }
.wow-divider { height: 3px; background: linear-gradient(90deg, transparent, #6C63FF, #FF6584, transparent); border: none; margin: 1.8rem 0; border-radius: 2px; }
.info-box { background: rgba(108, 99, 255, 0.1); border-left: 4px solid #6C63FF; padding: 1rem 1.2rem; border-radius: 0 12px 12px 0; margin: 0.6rem 0; color: #eee; font-size: 0.95rem; line-height: 1.4; }
.info-box-b { background: rgba(255, 101, 132, 0.1); border-left: 4px solid #FF6584; padding: 1rem 1.2rem; border-radius: 0 12px 12px 0; margin: 0.6rem 0; color: #eee; font-size: 0.95rem; line-height: 1.4; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# ─── SUPABASE ─────────────────────────────────────────────────────────
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = get_supabase()

# ─── ESPERIMENTI DEFINITI (BILINGUE IT / EN) ──────────────────────────
ESPERIMENTI = {
    # 1. MACCHINA
    "macchina": {
        "titolo_it": "1. 🚗 Incidente Stradale (Loftus & Palmer)",
        "titolo_en": "1. 🚗 Car Crash Experiment (Loftus & Palmer)",
        "desc_it": "Effetto del verbo: 'Toccate' vs 'Schiantate'.",
        "desc_en": "Wording effect: 'Hit' vs 'Smashed'.",
        "gruppo_a_it": "Toccate",
        "gruppo_b_it": "Schiantate",
        "gruppo_a_en": "Hit",
        "gruppo_b_en": "Smashed",
        "domanda_a_it": "A che velocità (in km/h) andavano le auto quando si sono toccate?",
        "domanda_b_it": "A che velocità (in km/h) andavano le auto quando si sono schiantate?",
        "domanda_a_en": "How fast (in km/h) were the cars going when they HIT each other?",
        "domanda_b_en": "How fast (in km/h) were the cars going when they SMASHED into each other?",
        "unita_it": "km/h",
        "unita_en": "km/h",
        "tipo": "ab_num"
    },

    # 2. MALATTIA ASIATICA
    "asian_disease": {
        "titolo_it": "2. 🦠 La Malattia Asiatica (Kahneman & Tversky)",
        "titolo_en": "2. 🦠 The Asian Disease Problem (Kahneman)",
        "desc_it": "Framing: Vite salvate (guadagno) vs Morti certe (perdita).",
        "desc_en": "Framing: Lives saved vs Certain deaths.",
        "gruppo_a_it": "Vite Salvate",
        "gruppo_b_it": "Morti Certe",
        "gruppo_a_en": "Lives Saved",
        "gruppo_b_en": "Certain Deaths",
        "domanda_a_it": "Programma A: 200 persone salvate (certo) | Programma B: 1/3 salva 600, 2/3 salva 0",
        "domanda_b_it": "Programma A: 400 persone muoiono (certo) | Programma B: 1/3 muore 0, 2/3 muoiono 600",
        "domanda_a_en": "Program A: 200 saved (certain) | Program B: 1/3 saves 600, 2/3 saves 0",
        "domanda_b_en": "Program A: 400 die (certain) | Program B: 1/3 dies 0, 2/3 dies 600",
        "unita_it": "% Scelta Rischiosa (Programma B)",
        "unita_en": "% Risk Choice (Program B)",
        "tipo": "ab_cat",
        "val_map_it": {0: "Certo (Programma A)", 1: "Rischio (Programma B)"},
        "val_map_en": {0: "Certain (Program A)", 1: "Risk (Program B)"}
    },

    # 3. FRAMING AI
    "framing_ai": {
        "titolo_it": "3. 🤖 Chirurgia Robotica AI (Framing Decisionale)",
        "titolo_en": "3. 🤖 Medical AI Software Framing",
        "desc_it": "90 sopravvivono vs 10 muoiono.",
        "desc_en": "90 survive vs 10 die.",
        "gruppo_a_it": "90 Sopravvivono",
        "gruppo_b_it": "10 Muoiono",
        "gruppo_a_en": "90 Survive",
        "gruppo_b_en": "10 Die",
        "domanda_a_it": "Se usi l'AI, 90 pazienti sopravviveranno. Autorizzi l'uso del software?",
        "domanda_b_it": "Se usi l'AI, 10 pazienti moriranno. Autorizzi l'uso del software?",
        "domanda_a_en": "If you use AI, 90 patients will survive. Authorize software?",
        "domanda_b_en": "If you use AI, 10 patients will die. Authorize software?",
        "unita_it": "% Approvazione AI",
        "unita_en": "% Approval",
        "tipo": "ab_cat",
        "val_map_it": {0: "Rifiuta AI (No)", 1: "Autorizza AI (Sì)"},
        "val_map_en": {0: "Reject AI", 1: "Authorize AI"}
    },

    # 4. GANDHI
    "gandhi": {
        "titolo_it": "4. 👴 Ancoraggio Età di Gandhi",
        "titolo_en": "4. 👴 Gandhi's Age Anchoring",
        "desc_it": "Ancora alta (114 anni) vs Ancora bassa (35 anni).",
        "desc_en": "High anchor (114 yrs) vs Low anchor (35 yrs).",
        "gruppo_a_it": "Ancora 114 anni",
        "gruppo_b_it": "Ancora 35 anni",
        "gruppo_a_en": "Anchor 114",
        "gruppo_b_en": "Anchor 35",
        "domanda_a_it": "Gandhi aveva più o meno di 114 anni? A che età esatta è morto?",
        "domanda_b_it": "Gandhi aveva più o meno di 35 anni? A che età esatta è morto?",
        "domanda_a_en": "Did Gandhi die before/after 114? Exactly how old was he when he died?",
        "domanda_b_en": "Did Gandhi die before/after 35? Exactly how old was he when he died?",
        "unita_it": "Età stimata (anni)",
        "unita_en": "Estimated Age (years)",
        "tipo": "ab_num"
    },

    # 5. ROULETTE
    "roulette": {
        "titolo_it": "5. 🎰 Ancoraggio Ruota della Fortuna (Diagnosi Mediche)",
        "titolo_en": "5. 🎰 Hospital Misdiagnoses Anchoring",
        "desc_it": "Numero ruota 12 vs 65.",
        "desc_en": "Wheel spin 12 vs 65.",
        "gruppo_a_it": "Ruota: 12",
        "gruppo_b_it": "Ruota: 65",
        "gruppo_a_en": "Wheel Spin 12",
        "gruppo_b_en": "Wheel Spin 65",
        "domanda_a_it": "Il numero estratto dalla ruota è 12. Percentuale stimata di diagnosi errate in ospedale?",
        "domanda_b_it": "Il numero estratto dalla ruota è 65. Percentuale stimata di diagnosi errate in ospedale?",
        "domanda_a_en": "Wheel spin landed on 12. Estimated % of hospital misdiagnoses?",
        "domanda_b_en": "Wheel spin landed on 65. Estimated % of hospital misdiagnoses?",
        "unita_it": "% Diagnosi Errate",
        "unita_en": "% Misdiagnoses",
        "tipo": "ab_num"
    },

    # 6. AVVERSIONE PERDITE
    "loss_aversion": {
        "titolo_it": "6. 💶 Avversione alle Perdite (Kahneman & Tversky)",
        "titolo_en": "6. 💶 Loss Aversion (Kahneman & Tversky)",
        "desc_it": "Effetto certezza: Guadagni vs Perdite.",
        "desc_en": "Certainty effect: Gains vs Losses.",
        "gruppo_a_it": "Scenario Guadagno (+1000€)",
        "gruppo_b_it": "Scenario Perdita (+2000€)",
        "gruppo_a_en": "Gain Scenario",
        "gruppo_b_en": "Loss Scenario",
        "domanda_a_it": "Ricevi 1000€: A) Vinci 500€ sicuri al 100% | B) Moneta: 50% 1000€, 50% 0€",
        "domanda_b_it": "Ricevi 2000€: A) Perdi 500€ sicuri al 100% | B) Moneta: 50% perdi 1000€, 50% perdi 0€",
        "domanda_a_en": "Given €1000: A) Sure €500 | B) 50% win €1000, 50% win €0",
        "domanda_b_en": "Given €2000: A) Sure lose €500 | B) 50% lose €1000, 50% lose €0",
        "unita_it": "% Scelta Rischiosa",
        "unita_en": "% Risk Choice",
        "tipo": "ab_cat",
        "val_map_it": {0: "Opzione Sicura (Certa)", 1: "Scommessa (Rischio)"},
        "val_map_en": {0: "Sure Option", 1: "Gamble"}
    },

    # 7. ILLUSIONE VERITA
    "illusione_verita": {
        "titolo_it": "7. 👁️ Illusione di Verità e Fluidità Cognitiva",
        "titolo_en": "7. 👁️ Truth Illusion & Cognitive Fluency",
        "desc_it": "Carattere Nitido/Arial vs Carattere Sbiadito/Comic Sans.",
        "desc_en": "Bold/Arial vs Faded/Comic Sans.",
        "gruppo_a_it": "Carattere Nitido (Arial)",
        "gruppo_b_it": "Carattere Sbiadito (Comic Sans)",
        "gruppo_a_en": "Clear Font (Bold/Arial)",
        "gruppo_b_en": "Faded Font (Comic Sans)",
        "domanda_a_it": "Frase in Arial nitido: Da 1 a 10 quanto ti sembra vera e scientifica?",
        "domanda_b_it": "Frase in Comic Sans sbiadito: Da 1 a 10 quanto ti sembra vera e scientifica?",
        "domanda_a_en": "Clear text in Arial: Rate perceived validity/truth (1-10)",
        "domanda_b_en": "Faded text in Comic Sans: Rate perceived validity/truth (1-10)",
        "unita_it": "Validità Percepita (1-10)",
        "unita_en": "Perceived Validity (1-10)",
        "tipo": "ab_num"
    },

    # 8. DISPONIBILITA
    "availability": {
        "titolo_it": "8. 🧠 Euristica della Disponibilità (Schwarz et al., 1991)",
        "titolo_en": "8. 🧠 Availability Heuristic (Schwarz et al., 1991)",
        "desc_it": "Sforzo di recupero mnemonico: 6 vs 12 esempi di assertività.",
        "desc_en": "Cognitive retrieval effort: List 6 vs 12 examples.",
        "gruppo_a_it": "Ricorda 6 Esempi",
        "gruppo_b_it": "Ricorda 12 Esempi",
        "gruppo_a_en": "List 6 Examples",
        "gruppo_b_en": "List 12 Examples",
        "domanda_a_it": "Richiama 6 esempi assertivi -> Quanto ti ritieni assertivo (1-10)?",
        "domanda_b_it": "Richiama 12 esempi assertivi -> Quanto ti ritieni assertivo (1-10)?",
        "domanda_a_en": "Recall 6 assertive examples -> Self-rated assertiveness (1-10)",
        "domanda_b_en": "Recall 12 assertive examples -> Self-rated assertiveness (1-10)",
        "unita_it": "Assertività Autovalutata (1-10)",
        "unita_en": "Self-Rated Assertiveness (1-10)",
        "tipo": "ab_num"
    },

    # 9. LINDA
    "linda": {
        "titolo_it": "9. 👩‍🦰 Problema di Linda (Fallacia della Congiunzione)",
        "titolo_en": "9. 👩‍🦰 Linda Problem (Conjunction Fallacy)",
        "desc_it": "Stima di probabilità: Cassiera vs Cassiera e Femminista.",
        "desc_en": "Probability estimation.",
        "gruppo_a_it": "Solo Cassiera",
        "gruppo_b_it": "Cassiera + Femminista",
        "gruppo_a_en": "Bank Teller Only",
        "gruppo_b_en": "Bank Teller + Feminist",
        "domanda_a_it": "Qual è la probabilità (0-100%) che Linda sia una cassiera di banca?",
        "domanda_b_it": "Qual è la probabilità (0-100%) che Linda sia cassiera di banca e attiva nel movimento femminista?",
        "domanda_a_en": "Probability (0-100%) Linda is a bank teller?",
        "domanda_b_en": "Probability (0-100%) Linda is a bank teller and active feminist?",
        "unita_it": "% Probabilità Stimata",
        "unita_en": "% Estimated Probability",
        "tipo": "ab_num"
    },

    # 10. ALONE
    "halo_asch": {
        "titolo_it": "10. 👤 Effetto Alone (Asch, 1946)",
        "titolo_en": "10. 👤 Halo Effect (Asch, 1946)",
        "desc_it": "Alan (qualità positive per prime) vs Ben (qualità negative per prime).",
        "desc_en": "Alan (Intelligent first) vs Ben (Envious first).",
        "gruppo_a_it": "Alan (Prima Positivo)",
        "gruppo_b_it": "Ben (Prima Negativo)",
        "gruppo_a_en": "Alan (Positive First)",
        "gruppo_b_en": "Ben (Negative First)",
        "domanda_a_it": "Alan: Intelligente, laborioso, impulsivo, critico, ostinato, invidioso. Voto (1-10)?",
        "domanda_b_it": "Ben: Invidioso, ostinato, critico, impulsivo, laborioso, intelligente. Voto (1-10)?",
        "domanda_a_en": "Alan: Intelligent, industrious, impulsive, critical, stubborn, envious. Rating (1-10)?",
        "domanda_b_en": "Ben: Envious, stubborn, critical, impulsive, industrious, intelligent. Rating (1-10)?",
        "unita_it": "Valutazione (1-10)",
        "unita_en": "Rating (1-10)",
        "tipo": "ab_num"
    },

    # 11. DOTE TAZZA
    "endow_mug": {
        "titolo_it": "11. ☕ Effetto Dote: Il Mercato delle Tazze (Thaler)",
        "titolo_en": "11. ☕ Mug Endowment Effect (Thaler)",
        "desc_it": "Venditori vs Acquirenti: valutazione dello stesso oggetto.",
        "desc_en": "Sellers vs Buyers valuation.",
        "gruppo_a_it": "Venditori (Prezzo Minimo)",
        "gruppo_b_it": "Acquirenti (Prezzo Massimo)",
        "gruppo_a_en": "Sellers (Min € Price)",
        "gruppo_b_en": "Buyers (Max € Price)",
        "domanda_a_it": "Hai la tazza: prezzo MINIMO a cui accetti di venderla?",
        "domanda_b_it": "Vuoi comprare la tazza: prezzo MASSIMO che sei disposto a pagare?",
        "domanda_a_en": "You own the mug: MINIMUM price to sell it?",
        "domanda_b_en": "You want the mug: MAXIMUM price to buy it?",
        "unita_it": "Prezzo (€)",
        "unita_en": "Price (€)",
        "tipo": "ab_num"
    },

    # 12. DOTE AI
    "endow_ai": {
        "titolo_it": "12. 💻 Effetto Dote: Licenza Software AI Medicale",
        "titolo_en": "12. 💻 Medical AI License Endowment",
        "desc_it": "Cedere vs Acquistare licenza diagnostica AI.",
        "desc_en": "Sell vs Buy AI License.",
        "gruppo_a_it": "Venditori (Prezzo Minimo)",
        "gruppo_b_it": "Acquirenti (Prezzo Massimo)",
        "gruppo_a_en": "Sellers (Min € Price)",
        "gruppo_b_en": "Buyers (Max € Price)",
        "domanda_a_it": "Possiedi la licenza: prezzo MINIMO per cederla all'ospedale?",
        "domanda_b_it": "L'ospedale vende la licenza: prezzo MASSIMO che saresti disposto a pagare?",
        "domanda_a_en": "You own AI license: MINIMUM price to sell?",
        "domanda_b_en": "Hospital sells AI license: MAXIMUM price to buy?",
        "unita_it": "Prezzo Licenza (€)",
        "unita_en": "Price (€)",
        "tipo": "ab_num"
    },

    # 13. COSTI SOMMERSI TEATRO
    "sunk_theater": {
        "titolo_it": "13. 🎭 Costi Sommersi: Biglietto Teatro",
        "titolo_en": "13. 🎭 Theater Ticket Sunk Cost",
        "desc_it": "Biglietto pagato 50€ vs Regalato 0€ durante una tormenta.",
        "desc_en": "Paid €50 ticket vs Free €0 ticket.",
        "gruppo_a_it": "Pagato 50€",
        "gruppo_b_it": "Regalato 0€",
        "gruppo_a_en": "Paid €50",
        "gruppo_b_en": "Gift €0",
        "domanda_a_it": "Biglietto pagato 50€, tormenta di neve: Vado a teatro o resto a casa?",
        "domanda_b_it": "Biglietto regalato 0€, tormenta di neve: Vado a teatro o resto a casa?",
        "domanda_a_en": "Paid €50 ticket, snowstorm: Go to theater or stay home?",
        "domanda_b_en": "Gift €0 ticket, snowstorm: Go to theater or stay home?",
        "unita_it": "% Partecipazione a Teatro",
        "unita_en": "% Going to Theater",
        "tipo": "ab_cat",
        "val_map_it": {0: "Resta a casa al caldo", 1: "Va a teatro con la tormenta"},
        "val_map_en": {0: "Stay Home", 1: "Go to Theater"}
    },

    # 14. COSTI SOMMERSI AI
    "sunk_ai": {
        "titolo_it": "14. 🏭 Costi Sommersi: Progetto di Ricerca AI",
        "titolo_en": "14. 🏭 AI Research Project Sunk Cost",
        "desc_it": "Iniziato oggi (0 anni) vs Iniziato da 4 anni.",
        "desc_en": "Invested 0 yrs vs 4 yrs.",
        "gruppo_a_it": "Iniziato Oggi (0 anni)",
        "gruppo_b_it": "Iniziato da 4 Anni",
        "gruppo_a_en": "Invested 0 Yrs",
        "gruppo_b_en": "Invested 4 Yrs",
        "domanda_a_it": "Iniziato oggi, Google rilascia software gratis migliore: Continui o abbandoni?",
        "domanda_b_it": "Lavori da 4 anni, Google rilascia software gratis migliore: Continui o abbandoni?",
        "domanda_a_en": "Started today, Google releases free superior tool: Continue or abandon?",
        "domanda_b_en": "Invested 4 years, Google releases free superior tool: Continue or abandon?",
        "unita_it": "% Continua Progetto",
        "unita_en": "% Continuing Project",
        "tipo": "ab_cat",
        "val_map_it": {0: "Abbandona il progetto", 1: "Continua a sviluppare"},
        "val_map_en": {0: "Abandon Project", 1: "Continue Project"}
    },

    # 15. DEFAULT ORGAN
    "default_organ": {
        "titolo_it": "15. 🫀 Effetto Default: Donazione Organi",
        "titolo_en": "15. 🫀 Default Effect (Organ Donation)",
        "desc_it": "Modulo Opt-IN (spunta per donare) vs Opt-OUT (spunta per NON donare).",
        "desc_en": "Opt-IN vs Opt-OUT enrollment form.",
        "gruppo_a_it": "Modulo Opt-IN",
        "gruppo_b_it": "Modulo Opt-OUT",
        "gruppo_a_en": "Opt-IN Form",
        "gruppo_b_en": "Opt-OUT Form",
        "domanda_a_it": "Spunta la casella se VUOI diventare donatore (default: non donatore)",
        "domanda_b_it": "Spunta la casella se NON VUOI diventare donatore (default: donatore)",
        "domanda_a_en": "Check box if you WANT to become donor (default: non-donor)",
        "domanda_b_en": "Check box if you DO NOT want to become donor (default: donor)",
        "unita_it": "% Donatori Effettivi",
        "unita_en": "% Effective Donors",
        "tipo": "ab_cat",
        "val_map_it": {0: "Non Donatore", 1: "Donatore di Organi"},
        "val_map_en": {0: "Non-Donor", 1: "Organ Donor"}
    },

    # 16. PRIMING
    "priming": {
        "titolo_it": "16. 🍝 Priming Associativo",
        "titolo_en": "16. 🍝 Associative Priming",
        "desc_it": "Prime cibo (Forchetta/Pranzo) vs Prime pulizia (Doccia/Schiuma).",
        "desc_en": "Food prime vs Shower prime.",
        "gruppo_a_it": "Prime Cibo (Forchetta, Fame)",
        "gruppo_b_it": "Prime Bagno (Doccia, Schiuma)",
        "gruppo_a_en": "Food Prime",
        "gruppo_b_en": "Shower Prime",
        "domanda_a_it": "Leggi: FORCHETTA, PRANZO, FAME. Completa la parola: S O _ P",
        "domanda_b_it": "Leggi: DOCCIA, SCHIUMA, PULITO. Completa la parola: S O _ P",
        "domanda_a_en": "Read: FORK, LUNCH, HUNGRY. Complete word: S O _ P",
        "domanda_b_en": "Read: SHOWER, SHAMPOO, SOAP. Complete word: S O _ P",
        "unita_it": "% Completamento Parola",
        "unita_en": "% Word Completion",
        "tipo": "ab_cat",
        "val_map_it": {0: "Altro", 1: "SOUP / ZUPPA (Cibo)", 2: "SOAP / SAPONE (Pulizia)"},
        "val_map_en": {0: "Other", 1: "SOUP", 2: "SOAP"}
    },

    # 17. DUNNING-KRUGER
    "dunning": {
        "titolo_it": "17. 🎓 Effetto Dunning-Kruger / Overconfidence",
        "titolo_en": "17. 🎓 Dunning-Kruger Effect / Overconfidence",
        "desc_it": "Confronto con compagni di classe vs Confronto con Premio Nobel.",
        "desc_en": "Peer comparison vs Nobel laureate comparison.",
        "gruppo_a_it": "vs Compagni di Classe",
        "gruppo_b_it": "vs Giorgio Parisi (Nobel)",
        "gruppo_a_en": "vs Classmates",
        "gruppo_b_en": "vs Nobel Laureate",
        "domanda_a_it": "Ritieni la tua abilità accademica superiore alla media della classe?",
        "domanda_b_it": "Ritieni la tua abilità accademica superiore a quella di Giorgio Parisi (Nobel)?",
        "domanda_a_en": "Do you consider your academic ability above class average?",
        "domanda_b_en": "Do you consider your academic ability above a Nobel laureate?",
        "unita_it": "% Autovalutazione Superiore",
        "unita_en": "% Perceived Superior",
        "tipo": "ab_cat",
        "val_map_it": {0: "Nella media / Sotto", 1: "Sopra la media"},
        "val_map_en": {0: "Average / Below", 1: "Above Average"}
    },

    # 18. WYSIATI
    "wysiati": {
        "titolo_it": "18. 👁️ WYSIATI Visivo (Bruner & Potter, 1964)",
        "titolo_en": "18. 👁️ Visual WYSIATI (Bruner & Potter, 1964)",
        "desc_it": "Messa a fuoco fluida continua vs 8 fotogrammi discreti a scatti.",
        "desc_en": "Open text unguided first impression.",
        "gruppo_a_it": "Messa a Fuoco Fluida (13s)",
        "gruppo_b_it": "8 Frame Discreti (1.5s/step)",
        "gruppo_a_en": "Continuous Fluid Unblurring (13s)",
        "gruppo_b_en": "8 Discrete Step Frames (1.5s/step)",
        "domanda_a_it": "Scrivi la prima cosa che vedi durante la messa a fuoco fluida continua:",
        "domanda_b_it": "Scrivi la prima cosa che vedi durante la sequenza di 8 fotogrammi:",
        "domanda_a_en": "Write the first thing you see during continuous fluid unblurring:",
        "domanda_b_en": "Write the first thing you see during discrete step unblurring:",
        "unita_it": "% Risposte Corrette",
        "unita_en": "% Responses",
        "tipo": "ab_cat",
        "val_map_it": {0: "Prima impressione errata", 1: "Idrante / Estintore"},
        "val_map_en": {0: "Initial Wrong Impression", 1: "Fire Hydrant / Extinguisher"}
    },

    # 19. FOCALIZZAZIONE
    "focalizzazione": {
        "titolo_it": "19. 😊 Illusione di Focalizzazione (Kahneman)",
        "titolo_en": "19. 😊 Focusing Illusion (Kahneman)",
        "desc_it": "Ordine delle domande: Felicità prima vs Uscite romantiche prima.",
        "desc_en": "Order of happiness questions.",
        "gruppo_a_it": "Felicità -> Uscite",
        "gruppo_b_it": "Uscite -> Felicità",
        "gruppo_a_en": "Happiness -> Dating",
        "gruppo_b_en": "Dating -> Happiness",
        "domanda_a_it": "1. Quanto sei felice (1-10)? -> 2. Quante uscite romantiche nell'ultimo mese?",
        "domanda_b_it": "1. Quante uscite romantiche nell'ultimo mese? -> 2. Quanto sei felice (1-10)?",
        "domanda_a_en": "1. How happy are you (1-10)? -> 2. How many dates last month?",
        "domanda_b_en": "1. How many dates last month? -> 2. How happy are you (1-10)?",
        "unita_it": "Voto Felicità (1-10)",
        "unita_en": "Happiness Rating (1-10)",
        "tipo": "ab_num"
    },

    # 20. BASE RATE
    "base_rate": {
        "titolo_it": "20. 🔬 Paradosso Diagnostico (Base Rate Neglect)",
        "titolo_en": "20. 🔬 Base Rate Neglect (Medical Paradox)",
        "desc_it": "Accuratezza test 95%, prevalenza 1% (Valore corretto: 16%).",
        "desc_en": "95% test accuracy, 1% prevalence (True: 16%).",
        "domanda_it": "Malattia colpisce 1% popolazione. Test infallibile al 95%. Risulti positivo: probabilità reale (0-100%) di essere malato?",
        "domanda_en": "Disease affects 1%. Test is 95% accurate. You test positive: true probability (0-100%) you have disease?",
        "tipo": "single_num",
        "unita_it": "Probabilità Stimata (%)",
        "unita_en": "Estimated Probability (%)",
        "verita": 16
    },

    # 21. DECOY
    "decoy": {
        "titolo_it": "21. 🗞️ Effetto Esca (The Economist)",
        "titolo_en": "21. 🗞️ Decoy Effect (The Economist)",
        "desc_it": "Opzione esca asimmetricamente dominata (Solo Cartaceo 120€).",
        "desc_en": "Asymmetric dominance decoy option.",
        "domanda_it": "Scegli l'abbonamento: A) Solo Web (50€) | B) Cartaceo (120€ - ESCA) | C) Web + Cartaceo (120€)",
        "domanda_en": "Choose subscription: A) Web Only ($50) | B) Print Only ($120 - DECOY) | C) Web + Print ($120)",
        "tipo": "single_cat",
        "val_map_it": {1: "Solo Web (50€)", 2: "Solo Cartaceo (120€ - ESCA)", 3: "Web + Cartaceo (120€)"},
        "val_map_en": {1: "Web Only ($50)", 2: "Print Only ($120 - DECOY)", 3: "Web + Print ($120)"}
    },

    # 22. REGRESSIONE
    "regression": {
        "titolo_it": "22. 🧑‍✈️ Regressione verso la Media (Istruttori di Volo)",
        "titolo_en": "22. 🧑‍✈️ Regression to the Mean",
        "desc_it": "Spiegazione Causale (psicologica) vs Spiegazione Statistica.",
        "desc_en": "Causal vs Statistical explanation.",
        "domanda_it": "Sgridare dopo una manovra pessima migliora la prova dopo. È merito della sgridata o statistica?",
        "domanda_en": "Punishing a bad flight maneuver leads to better performance next time. Causal or statistical?",
        "tipo": "single_cat",
        "val_map_it": {1: "Causale (Psicologica: sgridare serve)", 2: "Statistica (Regressione alla media)"},
        "val_map_en": {1: "Causal (Psychological)", 2: "Statistical (Regression)"}
    },

    # 23. WASON 2-4-6
    "wason_246": {
        "titolo_it": "23. 🧮 Bias di Conferma: Compito 2-4-6 (Wason, 1960)",
        "titolo_en": "23. 🧮 Confirmation Bias (Wason 2-4-6 Task)",
        "desc_it": "Trappola della verifica delle ipotesi positive.",
        "desc_en": "Hypothesis testing trap (Wason, 1960).",
        "domanda_it": "Sequenza: 2 - 4 - 6 (Regola segreta). Quale terna proveresti per prima per verificare la tua ipotesi?",
        "domanda_en": "Sequence: 2 - 4 - 6 (Secret rule). Which triad would you test first to verify your hypothesis?",
        "tipo": "single_cat",
        "val_map_it": {
            1: "Conferma: 8 - 10 - 12 (Pari +2)",
            2: "Test Dispari: 1 - 3 - 5",
            3: "Test Generico: 1 - 2 - 3 (Crescente)",
            4: "Falsificazione: 6 - 4 - 2 (Decrescente)"
        },
        "val_map_en": {
            1: "Confirmation (8 - 10 - 12)",
            2: "Test Odd (1 - 3 - 5)",
            3: "Test Generic (1 - 2 - 3)",
            4: "Falsification (6 - 4 - 2)"
        }
    }
}

# ─── SIDEBAR ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌐 Lingua / Language")
    lingua = st.radio("Seleziona lingua / Select language:", ["🇮🇹 Italiano", "🇬🇧 English"], index=0, label_visibility="collapsed")
    is_it = (lingua == "🇮🇹 Italiano")

    st.markdown("---")
    st.markdown("## 🧠 " + ("Elenco Esperimenti" if is_it else "Experiments List"))
    
    esperimento_sel = st.selectbox(
        "Scegli esperimento:" if is_it else "Choose experiment:",
        options=list(ESPERIMENTI.keys()),
        format_func=lambda x: ESPERIMENTI[x]["titolo_it"] if is_it else ESPERIMENTI[x]["titolo_en"]
    )
    st.markdown("---")
    
    auto_refresh = st.checkbox("🔄 " + ("Aggiornamento automatico (5s)" if is_it else "Auto-refresh (5s)"), value=True)
    if st.button("🔄 " + ("Aggiorna ora" if is_it else "Refresh now"), use_container_width=True):
        st.rerun()
    st.markdown("---")
    
    @st.cache_data(ttl=3)
    def fetch_data(exp_name):
        try:
            res_reset = supabase.table("Risposte").select("created_at").eq("esperimento", exp_name + "_reset").order("created_at", desc=True).limit(1).execute()
            if res_reset.data:
                latest_reset = res_reset.data[0]["created_at"]
                return supabase.table("Risposte").select("*").eq("esperimento", exp_name).gt("created_at", latest_reset).execute().data
        except Exception:
            pass
        return supabase.table("Risposte").select("*").eq("esperimento", exp_name).execute().data
    
    data = fetch_data(esperimento_sel)
    if data:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        st.download_button(
            label="📥 " + ("Scarica Dati (CSV)" if is_it else "Download Data (CSV)"),
            data=output.getvalue().encode('utf-8'),
            file_name=f"risposte_{esperimento_sel}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with st.expander("🗑️ " + ("Cancella Dati" if is_it else "Clear Data")):
        chk = st.checkbox("Conferma cancellazione" if is_it else "Confirm deletion", key="del_chk")
        if st.button("🗑️ " + ("CANCELLA ORA" if is_it else "DELETE NOW"), type="primary", use_container_width=True):
            if chk:
                try:
                    supabase.table("Risposte").insert({"esperimento": esperimento_sel + "_reset", "gruppo": "RESET", "valore": 0}).execute()
                    if esperimento_sel == "macchina":
                        supabase.table("Risposte").insert({"esperimento": "macchina_vetri_reset", "gruppo": "RESET", "valore": 0}).execute()
                except Exception:
                    pass
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("✅ " + ("Dati cancellati con successo!" if is_it else "Data cleared successfully!"))
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Spunta la casella di conferma sopra!" if is_it else "Please check the confirmation box above!")

# ─── MAIN ─────────────────────────────────────────────────────────────
exp_raw = ESPERIMENTI[esperimento_sel]
exp = {
    "titolo": exp_raw["titolo_it"] if is_it else exp_raw["titolo_en"],
    "desc": exp_raw["desc_it"] if is_it else exp_raw["desc_en"],
    "gruppo_a": exp_raw.get("gruppo_a_it", "Gruppo A") if is_it else exp_raw.get("gruppo_a_en", "Group A"),
    "gruppo_b": exp_raw.get("gruppo_b_it", "Gruppo B") if is_it else exp_raw.get("gruppo_b_en", "Group B"),
    "domanda_a": exp_raw.get("domanda_a_it", "") if is_it else exp_raw.get("domanda_a_en", ""),
    "domanda_b": exp_raw.get("domanda_b_it", "") if is_it else exp_raw.get("domanda_b_en", ""),
    "domanda": exp_raw.get("domanda_it", "") if is_it else exp_raw.get("domanda_en", ""),
    "unita": exp_raw.get("unita_it", "") if is_it else exp_raw.get("unita_en", ""),
    "val_map": exp_raw.get("val_map_it", {}) if is_it else exp_raw.get("val_map_en", {}),
    "tipo": exp_raw["tipo"],
    "verita": exp_raw.get("verita")
}

# Clean title for heading
h1_text = exp["titolo"]
if h1_text and h1_text[0].isdigit() and "." in h1_text:
    h1_text = h1_text.split(".", 1)[1].strip()

st.markdown(f'<h1 class="main-title">{h1_text}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{exp["desc"]}</p>', unsafe_allow_html=True)

# Question info box for the presenter / audience
if exp["tipo"].startswith("ab"):
    c_qa, c_qb = st.columns(2)
    with c_qa:
        st.markdown(f'<div class="info-box"><strong style="color:#6C63FF;">🔵 {exp["gruppo_a"]}</strong><br><em>{exp["domanda_a"]}</em></div>', unsafe_allow_html=True)
    with c_qb:
        st.markdown(f'<div class="info-box-b"><strong style="color:#FF6584;">🔴 {exp["gruppo_b"]}</strong><br><em>{exp["domanda_b"]}</em></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="info-box"><strong style="color:#6C63FF;">📌 {"Domanda posta al pubblico" if is_it else "Question asked to audience"}:</strong><br><em>{exp["domanda"]}</em></div>', unsafe_allow_html=True)

st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)

if not data:
    wait_title = "📱 In attesa di risposte..." if is_it else "📱 Waiting for responses..."
    wait_msg = "Fai scansionare il QR Code al pubblico! I risultati appariranno qui in tempo reale." if is_it else "Scan the QR Code! Results will appear here in real time."
    st.markdown(f'<div class="info-box"><h3>{wait_title}</h3><p>{wait_msg}</p></div>', unsafe_allow_html=True)
else:
    placeholder_ab = st.empty()
    placeholder_single = st.empty()
    placeholder_vetri = st.empty()
    
    placeholder_ab.empty()
    placeholder_single.empty()
    placeholder_vetri.empty()

    # ─── A/B EXPERIMENTS ──────────────────────────────────────────────
    if exp["tipo"].startswith("ab"):
        with placeholder_ab.container():
            val_a = [r["valore"] for r in data if r["gruppo"] == "A" and r["valore"] is not None]
            val_b = [r["valore"] for r in data if r["gruppo"] == "B" and r["valore"] is not None]
            
            # Medie
            media_a = sum(val_a)/len(val_a) if val_a else 0
            media_b = sum(val_b)/len(val_b) if val_b else 0
            diff = abs(media_a - media_b)
            
            lbl_resp = "risposte" if is_it else "resp"
            lbl_diff = "Differenza" if is_it else "Difference"
            
            c1, c2, c3 = st.columns(3)
            c1.markdown(f'<div class="metric-card"><p class="metric-label">{exp.get("gruppo_a", "A")}</p><p class="metric-value" style="color:#6C63FF">{media_a:.1f}</p><span class="count-badge">📊 {len(val_a)} {lbl_resp}</span></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="diff-card"><p class="metric-label">{lbl_diff}</p><p class="diff-value">Δ {diff:.1f}</p></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="metric-card"><p class="metric-label">{exp.get("gruppo_b", "B")}</p><p class="metric-value" style="color:#FF6584">{media_b:.1f}</p><span class="count-badge">📊 {len(val_b)} {lbl_resp}</span></div>', unsafe_allow_html=True)
            
            st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)
            
            if exp["tipo"] == "ab_num":
                fig = go.Figure(data=[
                    go.Bar(name=exp.get("gruppo_a", "A"), x=[exp.get("gruppo_a", "A")], y=[media_a], marker_color='#6C63FF', text=[f"{media_a:.1f}"], textposition='auto'),
                    go.Bar(name=exp.get("gruppo_b", "B"), x=[exp.get("gruppo_b", "B")], y=[media_b], marker_color='#FF6584', text=[f"{media_b:.1f}"], textposition='auto')
                ])
                chart_title = "Confronto Medie" if is_it else "Average Comparison"
                fig.update_layout(title=chart_title, template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", yaxis_title=exp.get("unita", ""))
                st.plotly_chart(fig, use_container_width=True, key=f"ab_num_bar_{esperimento_sel}")
                    
            elif exp["tipo"] == "ab_cat":
                c1_chart, c2_chart = st.columns(2)
                map_dict = exp["val_map"]
                counts_a = {map_dict[k]: val_a.count(k) for k in map_dict}
                counts_b = {map_dict[k]: val_b.count(k) for k in map_dict}
                
                labels = list(counts_a.keys())
                vals_a = list(counts_a.values())
                vals_b = list(counts_b.values())
                colors = ['#6C63FF', '#FF6584', '#00FF88', '#FFA600']
                
                with c1_chart:
                    fA = go.Figure(data=[go.Pie(labels=labels, values=vals_a, hole=.3, marker_colors=colors)])
                    fA.update_layout(title=exp["gruppo_a"], template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fA, use_container_width=True, key=f"ab_cat_pieA_{esperimento_sel}")
                with c2_chart:
                    fB = go.Figure(data=[go.Pie(labels=labels, values=vals_b, hole=.3, marker_colors=colors)])
                    fB.update_layout(title=exp["gruppo_b"], template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fB, use_container_width=True, key=f"ab_cat_pieB_{esperimento_sel}")

    # ─── SINGLE DEMOS ─────────────────────────────────────────────────
    else:
        with placeholder_single.container():
            vals = [r["valore"] for r in data if r["valore"] is not None]
            lbl_tot = "PARTECIPANTI TOTALI" if is_it else "TOTAL PARTICIPANTS"
            st.markdown(f'<div class="metric-card"><p class="metric-label">{lbl_tot}</p><p class="metric-value">{len(vals)}</p></div>', unsafe_allow_html=True)
            
            st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)
            
            if exp["tipo"] == "single_num":
                fig = go.Figure(data=[go.Histogram(x=vals, marker_color='#00FF88')])
                hist_title = "Distribuzione delle Risposte" if is_it else "Responses Distribution"
                if exp.get("verita") is not None:
                    hist_title += f" (" + ("Risposta reale corretta:" if is_it else "True value:") + f" {exp['verita']})"
                fig.update_layout(title=hist_title, template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True, key=f"single_num_hist_{esperimento_sel}")
                
            elif exp["tipo"] == "single_cat":
                map_dict = exp["val_map"]
                counts = {map_dict[k]: vals.count(k) for k in map_dict}
                fig = go.Figure(data=[go.Pie(labels=list(counts.keys()), values=list(counts.values()), hole=.4, marker_colors=['#6C63FF', '#FF6584', '#00FF88', '#FFA600'])])
                cat_title = "Voti dei Partecipanti" if is_it else "Group Votes"
                fig.update_layout(title=cat_title, template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True, key=f"single_cat_pie_{esperimento_sel}")

    # Special case: Broken Glass for Macchina
    if esperimento_sel == "macchina":
        with placeholder_vetri.container():
            st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)
            glass_heading = "Hai notato dei vetri rotti a terra?" if is_it else "Did you see any broken glass on the ground?"
            st.markdown(f'<h2 style="text-align:center;">{glass_heading}</h2>', unsafe_allow_html=True)
            
            data_vetri = fetch_data("macchina_vetri")
            if data_vetri:
                val_vetri_a = [r["valore"] for r in data_vetri if r["gruppo"] == "A"]
                val_vetri_b = [r["valore"] for r in data_vetri if r["gruppo"] == "B"]
                
                yes_lbl = "Sì" if is_it else "Yes"
                no_lbl = "No"
                
                counts_a = {yes_lbl: val_vetri_a.count(1), no_lbl: val_vetri_a.count(0)}
                counts_b = {yes_lbl: val_vetri_b.count(1), no_lbl: val_vetri_b.count(0)}
                
                c1_v, c2_v = st.columns(2)
                with c1_v:
                    fA_v = go.Figure(data=[go.Pie(labels=list(counts_a.keys()), values=list(counts_a.values()), hole=.3, marker_colors=['#FFA600', '#444'])])
                    fA_v.update_layout(title=f"{exp['gruppo_a']} ({len(val_vetri_a)} {'risposte' if is_it else 'resp'})", template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fA_v, use_container_width=True, key="macchina_vetri_A")
                with c2_v:
                    fB_v = go.Figure(data=[go.Pie(labels=list(counts_b.keys()), values=list(counts_b.values()), hole=.3, marker_colors=['#FFA600', '#444'])])
                    fB_v.update_layout(title=f"{exp['gruppo_b']} ({len(val_vetri_b)} {'risposte' if is_it else 'resp'})", template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fB_v, use_container_width=True, key="macchina_vetri_B")

if auto_refresh:
    time.sleep(5)
    st.rerun()
