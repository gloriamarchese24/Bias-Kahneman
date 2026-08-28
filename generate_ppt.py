import qrcode
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

BASE_URL = "https://bias-kahneman-ms2mgk3bueryreh4vj78ae.streamlit.app"

PAGINE_IT = [
    {
        "url_path": "Macchina",
        "title": "1. Loftus & Palmer — Falsi Ricordi (Velocità Auto)",
        "scenario": "Hai appena visto un breve video di un incidente tra due automobili.",
        "group_a": "A che velocità (in km/h) andavano le auto quando si sono urtate?",
        "group_b": "A che velocità (in km/h) andavano le auto quando si sono disintegrate?",
        "extra": "Domanda comune: Hai notato dei vetri rotti a terra? (Sì / No)"
    },
    {
        "url_path": "Malattia_Asiatica",
        "title": "2. Asian Disease Problem — Framing Effect",
        "scenario": "Un'epidemia asiatica minaccia 600 persone. Due programmi possibili:",
        "group_a": "Programma A: 200 salvati di sicuro.\nProgramma B: 1/3 probabilità di salvare tutti e 600, 2/3 nessuno.",
        "group_b": "Programma A: 400 morti di sicuro.\nProgramma B: 1/3 probabilità che non muoia nessuno, 2/3 che muoiano tutti e 600."
    },
    {
        "url_path": "Framing_AI",
        "title": "3. Chirurgia Robotica AI — Framing Medico",
        "scenario": "Un software robotico AI deve eseguire un intervento su 100 pazienti critici.",
        "group_a": "Dato statistico: 90 pazienti sopravviveranno.\nAutorizzi l'uso del software? (Sì / No)",
        "group_b": "Dato statistico: 10 pazienti moriranno.\nAutorizzi l'uso del software? (Sì / No)"
    },
    {
        "url_path": "Ancoraggio_Gandhi",
        "title": "4. Ancoraggio — Età di Gandhi",
        "scenario": "Stima dell'età di morte di Mahatma Gandhi.",
        "group_a": "1. Gandhi è morto prima o dopo i 114 anni?\n2. Stima l'età esatta alla morte (anni).",
        "group_b": "1. Gandhi è morto prima o dopo i 35 anni?\n2. Stima l'età esatta alla morte (anni)."
    },
    {
        "url_path": "Ancoraggio_Roulette",
        "title": "5. Ancoraggio Medico — Ruota della Fortuna",
        "scenario": "Una ruota della fortuna estrae un numero prima della stima diagnostica.",
        "group_a": "Numero estratto dalla ruota: 12\nDomanda: Qual è la % di diagnosi errate dovute a stanchezza del medico?",
        "group_b": "Numero estratto dalla ruota: 65\nDomanda: Qual è la % di diagnosi errate dovute a stanchezza del medico?"
    },
    {
        "url_path": "Avversione_Perdite",
        "title": "6. Avversione alle Perdite — Scelte Finanziarie",
        "scenario": "Valutazione del rischio tra vincite certe e perdite certe.",
        "group_a": "Ricevi 1.000€.\nA) Vinci altri 500€ sicuri (100%)\nB) Lancio moneta: 50% vinci 1.000€, 50% vinci 0€",
        "group_b": "Ricevi 2.000€.\nA) Perdi 500€ sicuri (100%)\nB) Lancio moneta: 50% perdi 1.000€, 50% perdi 0€"
    },
    {
        "url_path": "Illusione_Verita",
        "title": "7. Illusione di Verità — Effetto Font",
        "scenario": "Valutazione affermazione: 'L'assunzione di Omega-3 riduce del 15% le infiammazioni corporee.'",
        "group_a": "Formattazione: Arial grassetto nero ad alta visibilità.",
        "group_b": "Formattazione: Comic Sans sbiadito grigio a bassa visibilità.",
        "extra": "Domanda: Da 1 a 10, quanto ti sembra vera e scientifica questa frase?"
    },
    {
        "url_path": "Euristica_Disponibilita",
        "title": "8. Availability Heuristic — Euristica della Disponibilità",
        "scenario": "Richiamo alla memoria di comportamenti assertivi.",
        "group_a": "1. Elenca 2 situazioni in cui sei stato assertivo.\n2. Valuta quanto ti ritieni assertivo (1-10).",
        "group_b": "1. Elenca 12 situazioni in cui sei stato assertivo.\n2. Valuta quanto ti ritieni assertivo (1-10)."
    },
    {
        "url_path": "Problema_Linda",
        "title": "9. Il Problema di Linda — Fallacia della Congiunzione",
        "scenario": "Linda ha 31 anni, single, brillante, laureata in filosofia, attiva contro la discriminazione e nelle manifestazioni antinucleari.",
        "group_a": "Qual è la probabilità (0-100%) che Linda sia una cassiera di banca?",
        "group_b": "Qual è la probabilità (0-100%) che Linda sia una cassiera di banca e attiva nel movimento femminista?"
    },
    {
        "url_path": "Effetto_Alone",
        "title": "10. Effetto Alone — Modello Asch",
        "scenario": "Valutazione di un collega basata su un elenco ordinato di aggettivi.",
        "group_a": "Alan: Intelligente, laborioso, impulsivo, critico, ostinato, invidioso.\nValutazione sul lavoro (1-10).",
        "group_b": "Ben: Invidioso, ostinato, critico, impulsivo, laborioso, intelligente.\nValutazione sul lavoro (1-10)."
    },
    {
        "url_path": "Effetto_Dote_Tazza",
        "title": "11. Effetto Dote — Tazza di Thaler",
        "scenario": "Mercato libero di compravendita di una tazza dell'istituto.",
        "group_a": "Venditori: Ti è stata regalata la tazza.\nPrezzo minimo (€) a cui la venderesti.",
        "group_b": "Compratori: Un compagno ha ricevuto la tazza.\nPrezzo massimo (€) che pagheresti."
    },
    {
        "url_path": "Effetto_Dote_AI",
        "title": "12. Effetto Dote — Licenza Software AI",
        "scenario": "Mercato per una Licenza Software AI diagnostica.",
        "group_a": "Proprietario: Hai in regalo la licenza.\nPrezzo minimo (€) richiesto per cederla.",
        "group_b": "Acquirente: Un ospedale vende la licenza.\nPrezzo massimo (€) che pagheresti."
    },
    {
        "url_path": "Costi_Sommersi_Teatro",
        "title": "13. Costi Sommersi — Spettacolo a Teatro",
        "scenario": "Tormenta di neve la sera dello spettacolo teatrale.",
        "group_a": "Biglietto acquistato a 50€.\nA) Vado a teatro lo stesso (sfido la tormenta)\nB) Resto a casa al caldo",
        "group_b": "Biglietto regalato (0€).\nA) Vado a teatro lo stesso\nB) Resto a casa al caldo"
    },
    {
        "url_path": "Costi_Sommersi_AI",
        "title": "14. Costi Sommersi — Progetto di Ricerca AI",
        "scenario": "Google lancia un algoritmo gratuito e migliore mentre sviluppi il tuo.",
        "group_a": "Iniziato il progetto OGGI (0 anni investiti).\nA) Continuo a sviluppare il mio\nB) Abbandono il mio progetto",
        "group_b": "Lavori al progetto da 4 ANNI (al 90%).\nA) Continuo a sviluppare il mio\nB) Abbandono il mio progetto"
    },
    {
        "url_path": "Effetto_Default",
        "title": "15. Effetto Default — Donazione Organi",
        "scenario": "Firma del nuovo modulo per dipendenti ospedalieri.",
        "group_a": "Modulo Opt-IN: [ ] Spunta se VUOI diventare donatore.",
        "group_b": "Modulo Opt-OUT: [v] Spunta se NON VUOI diventare donatore."
    },
    {
        "url_path": "Priming_Associativo",
        "title": "16. Priming Associativo — Completamento Parole",
        "scenario": "Priming semantico sul completamento della parola S O _ P.",
        "group_a": "Lettura veloce: FORCHETTA, PRANZO, FAME.\nCompleta la parola: S O _ P",
        "group_b": "Lettura veloce: DOCCIA, SCHIUMA, PULITO.\nCompleta la parola: S O _ P"
    },
    {
        "url_path": "Dunning_Kruger",
        "title": "17. Illusione di Superiorità — Dunning-Kruger",
        "scenario": "Autovalutazione delle proprie abilità accademiche.",
        "group_a": "Ritieni la tua abilità accademica superiore alla media della classe?\n(Sopra la media / Nella media / Sotto la media)",
        "group_b": "Ritieni la tua abilità accademica superiore a quella di Giorgio Parisi (Nobel)?\n(Sopra la sua / Nella sua / Sotto la sua)"
    },
    {
        "url_path": "WYSIATI",
        "title": "18. WYSIATI — What You See Is All There Is",
        "scenario": "Verdetto in un processo penale con evidenze sbilanciate.",
        "group_a": "Presentata solo la testimonianza della Difesa.\nStima colpevolezza (0-100) e sicurezza (1-10).",
        "group_b": "Presentata solo la testimonianza del PM.\nStima colpevolezza (0-100) e sicurezza (1-10)."
    },
    {
        "url_path": "Illusione_Focalizzazione",
        "title": "19. Illusione di Focalizzazione — Felicità",
        "scenario": "Ordine delle domande sul benessere e vita sentimentale.",
        "group_a": "1. Quanto sei felice (1-10)?\n2. Quante uscite romantiche nell'ultimo mese?",
        "group_b": "1. Quante uscite romantiche nell'ultimo mese?\n2. Quanto sei felice (1-10)?"
    },
    {
        "url_path": "Base_Rate_Neglect",
        "title": "20. Base Rate Neglect — Paradosso Diagnostico",
        "scenario": "Malattia rara al 1% della popolazione. Test preciso al 95%. Risulti POSITIVO.",
        "single": "Qual è la probabilità effettiva (0-100%) che tu sia realmente malato?\n(Risposta statistica corretta: ~16%)"
    },
    {
        "url_path": "L_Esca",
        "title": "21. Decoy Effect — L'Esca (The Economist)",
        "scenario": "Scegli un abbonamento alla rivista The Economist:",
        "single": "A) Solo Web (50€)\nB) Solo Cartaceo (120€ - Opzione Esca)\nC) Web + Cartaceo (120€)"
    },
    {
        "url_path": "Regressione_Media",
        "title": "22. Regressione alla Media — Lode vs Castigo",
        "scenario": "Istruttori di volo: sgridare migliora l'atterraggio successivo, lodare lo peggiora.",
        "single": "A) Intuizione psicologica (la lode vizia, il castigo funziona)\nB) Errore statistico (regressione alla media)"
    }
]

PAGINE_EN = [
    {
        "url_path": "Macchina_EN",
        "title": "1. Loftus & Palmer — Car Crash Experiment (False Memories)",
        "scenario": "You have just watched a short video clip of an automobile accident.",
        "group_a": "How fast (in km/h) were the cars going when they HIT each other?",
        "group_b": "How fast (in km/h) were the cars going when they SMASHED into each other?",
        "extra": "Common question: Did you see any broken glass on the ground? (Yes / No)"
    },
    {
        "url_path": "Malattia_Asiatica_EN",
        "title": "2. Asian Disease Problem — Framing Effect",
        "scenario": "An unusual Asian disease is expected to kill 600 people. Two programs proposed:",
        "group_a": "Program A: 200 people saved for sure.\nProgram B: 1/3 probability 600 saved, 2/3 nobody saved.",
        "group_b": "Program A: 400 people die for sure.\nProgram B: 1/3 probability nobody dies, 2/3 all 600 die."
    },
    {
        "url_path": "Framing_AI_EN",
        "title": "3. AI Robotic Surgery — Medical Framing",
        "scenario": "An AI robotic surgical software will perform surgery on 100 patients in critical condition.",
        "group_a": "Statistical data: 90 patients will survive. Do you authorize the software? (Yes / No)",
        "group_b": "Statistical data: 10 patients will die. Do you authorize the software? (Yes / No)"
    },
    {
        "url_path": "Ancoraggio_Gandhi_EN",
        "title": "4. Anchoring Effect — Gandhi's Age",
        "scenario": "Estimating Mahatma Gandhi's age at death.",
        "group_a": "1. Did Gandhi die before or after age 114?\n2. Estimate his exact age at death (years).",
        "group_b": "1. Did Gandhi die before or after age 35?\n2. Estimate his exact age at death (years)."
    },
    {
        "url_path": "Ancoraggio_Roulette_EN",
        "title": "5. Medical Anchoring — Roulette Wheel",
        "scenario": "A roulette wheel spins an apparently random number before diagnostic estimation.",
        "group_a": "Wheel number: 12\nQuestion: What % of misdiagnoses are caused by doctor fatigue?",
        "group_b": "Wheel number: 65\nQuestion: What % of misdiagnoses are caused by doctor fatigue?"
    },
    {
        "url_path": "Avversione_Perdite_EN",
        "title": "6. Loss Aversion — Financial Risk Decisions",
        "scenario": "Evaluating risk choices between certain gains and certain losses.",
        "group_a": "You are given €1,000.\nA) Win €500 more for sure (100%)\nB) Coin flip: 50% win €1,000, 50% win €0",
        "group_b": "You are given €2,000.\nA) Lose €500 for sure (100%)\nB) Coin flip: 50% lose €1,000, 50% lose €0"
    },
    {
        "url_path": "Illusione_Verita_EN",
        "title": "7. Illusion of Truth — Font Legibility Effect",
        "scenario": "Evaluation of statement: 'Taking Omega-3 reduces bodily inflammation by 15%.'",
        "group_a": "Presented in high-contrast bold Arial font.",
        "group_b": "Presented in low-contrast faded Comic Sans font.",
        "extra": "Question: On a scale of 1 to 10, how true and scientific does this statement seem?"
    },
    {
        "url_path": "Euristica_Disponibilita_EN",
        "title": "8. Availability Heuristic — Memory Recall",
        "scenario": "Recalling assertive personal behaviors.",
        "group_a": "1. List 2 situations where you were assertive.\n2. Rate how assertive you consider yourself (1-10).",
        "group_b": "1. List 12 situations where you were assertive.\n2. Rate how assertive you consider yourself (1-10)."
    },
    {
        "url_path": "Problema_Linda_EN",
        "title": "9. The Linda Problem — Conjunction Fallacy",
        "scenario": "Linda is 31, single, outspoken, bright, philosophy major, deeply concerned with social justice and anti-nuclear protests.",
        "group_a": "What is the probability (0-100%) that Linda is a bank teller?",
        "group_b": "What is the probability (0-100%) that Linda is a bank teller and active in the feminist movement?"
    },
    {
        "url_path": "Effetto_Alone_EN",
        "title": "10. Halo Effect — Asch Personality Impression",
        "scenario": "Rating a colleague based on an ordered list of personality traits.",
        "group_a": "Alan: Intelligent, industrious, impulsive, critical, stubborn, envious.\nRate Alan as a coworker (1-10).",
        "group_b": "Ben: Envious, stubborn, critical, impulsive, industrious, intelligent.\nRate Ben as a coworker (1-10)."
    },
    {
        "url_path": "Effetto_Dote_Tazza_EN",
        "title": "11. Endowment Effect — Thaler's Mug",
        "scenario": "Trading market for an official university mug.",
        "group_a": "Sellers: You were GIVEN the mug.\nWhat is the minimum price (€) you will sell it for?",
        "group_b": "Buyers: A classmate has the mug.\nWhat is the maximum price (€) you are willing to pay?"
    },
    {
        "url_path": "Effetto_Dote_AI_EN",
        "title": "12. Endowment Effect — AI Software License",
        "scenario": "Market for a rare AI diagnostic software license.",
        "group_a": "Owner: You were GIFTED the license.\nMinimum price (€) demanded to sell it.",
        "group_b": "Buyer: A hospital is selling the license.\nMaximum price (€) willing to pay."
    },
    {
        "url_path": "Costi_Sommersi_Teatro_EN",
        "title": "13. Sunk Cost Fallacy — Theater Ticket",
        "scenario": "A severe snowstorm hits on the night of the theater performance.",
        "group_a": "Ticket bought for €50.\nA) Go to the theater anyway\nB) Stay home warm",
        "group_b": "Ticket received for free (€0).\nA) Go to the theater anyway\nB) Stay home warm"
    },
    {
        "url_path": "Costi_Sommersi_AI_EN",
        "title": "14. Sunk Cost Fallacy — AI Research Project",
        "scenario": "Google releases a free superior algorithm while your team works on one.",
        "group_a": "Project started TODAY (0 years invested).\nA) Continue developing mine\nB) Abandon my project",
        "group_b": "Worked for 4 YEARS on the algorithm (90% done).\nA) Continue developing mine\nB) Abandon my project"
    },
    {
        "url_path": "Effetto_Default_EN",
        "title": "15. Default Effect — Organ Donation",
        "scenario": "Signing hospital employee onboarding consent form.",
        "group_a": "Opt-IN Form: [ ] Check the box if you WANT to become an organ donor.",
        "group_b": "Opt-OUT Form: [v] Check the box if you DO NOT WANT to become an organ donor."
    },
    {
        "url_path": "Priming_Associativo_EN",
        "title": "16. Associative Priming — Word Completion",
        "scenario": "Effect of semantic priming on completing the word S O _ P.",
        "group_a": "Quick reading: FORK, LUNCH, HUNGER.\nComplete the word: S O _ P",
        "group_b": "Quick reading: SHOWER, FOAM, CLEAN.\nComplete the word: S O _ P"
    },
    {
        "url_path": "Dunning_Kruger_EN",
        "title": "17. Illusion of Superiority — Dunning-Kruger",
        "scenario": "Self-evaluation of personal academic ability.",
        "group_a": "Do you consider your academic ability above class average?\n(Above average / Average / Below average)",
        "group_b": "Do you consider your academic ability superior to Giorgio Parisi (Nobel)?\n(Above his / Equal to his / Below his)"
    },
    {
        "url_path": "WYSIATI_EN",
        "title": "18. WYSIATI — What You See Is All There Is",
        "scenario": "Criminal trial verdict based on one-sided evidence.",
        "group_a": "Presented only with Defense testimony.\nEstimate guilt (0-100) and confidence (1-10).",
        "group_b": "Presented only with Prosecution testimony.\nEstimate guilt (0-100) and confidence (1-10)."
    },
    {
        "url_path": "Illusione_Focalizzazione_EN",
        "title": "19. Focusing Illusion — Life Satisfaction",
        "scenario": "Survey on happiness and dating frequency.",
        "group_a": "1. How happy are you with your life (1-10)?\n2. How many dates in the last month?",
        "group_b": "1. How many dates in the last month?\n2. How happy are you with your life (1-10)?"
    },
    {
        "url_path": "Base_Rate_Neglect_EN",
        "title": "20. Base Rate Neglect — Diagnostic Paradox",
        "scenario": "A rare disease affects 1% of the population. A test is 95% accurate. You test POSITIVE.",
        "single": "What is the actual probability (0-100%) that you actually have the disease?\n(True statistical answer: ~16%)"
    },
    {
        "url_path": "L_Esca_EN",
        "title": "21. Decoy Effect — The Economist",
        "scenario": "Choose a subscription to The Economist:",
        "single": "A) Web Only ($50)\nB) Print Only ($120 - Decoy Option)\nC) Web + Print ($120)"
    },
    {
        "url_path": "Regressione_Media_EN",
        "title": "22. Regression to the Mean — Praise vs Punishment",
        "scenario": "Flight instructors notice reprimanding after a bad landing leads to a better landing, while praising leads to a worse one.",
        "single": "A) Psychological intuition (praise spoils, punishment works)\nB) Statistical effect (regression to the mean)"
    }
]

os.makedirs("qrcodes", exist_ok=True)

def build_presentation(data_list, output_filename, main_title_text, subtitle_text, banner_text, lang="IT"):
    prs = Presentation()
    
    # Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = main_title_text
    subtitle.text = subtitle_text

    # Experiment Slides
    for item in data_list:
        url_path = item["url_path"]
        url = f"{BASE_URL}/{url_path}"
        
        # Generate QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = f"qrcodes/{url_path}.png"
        img.save(img_path)

        # Create Slide
        blank_layout = prs.slide_layouts[6] # Blank slide layout
        slide = prs.slides.add_slide(blank_layout)
        
        # Header / Title Box
        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(9.0), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = item["title"]
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = RGBColor(108, 99, 255)
        
        # Left Side Content Box (Questions & Scenario)
        content_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.5))
        ctf = content_box.text_frame
        ctf.word_wrap = True

        # Scenario
        p_scen = ctf.paragraphs[0]
        p_scen.text = f"📌 Scenario:\n{item['scenario']}\n"
        p_scen.font.size = Pt(13)
        p_scen.font.color.rgb = RGBColor(60, 60, 60)

        # Questions
        if "group_a" in item:
            p_a = ctf.add_paragraph()
            p_a.text = f"🅰️ Gruppo A / Group A:\n{item['group_a']}\n"
            p_a.font.size = Pt(12)
            p_a.font.bold = True
            p_a.font.color.rgb = RGBColor(30, 90, 200)

            p_b = ctf.add_paragraph()
            p_b.text = f"🅱️ Gruppo B / Group B:\n{item['group_b']}\n"
            p_b.font.size = Pt(12)
            p_b.font.bold = True
            p_b.font.color.rgb = RGBColor(200, 50, 90)
        
        if "single" in item:
            p_s = ctf.add_paragraph()
            p_s.text = f"❓ Domanda / Question:\n{item['single']}\n"
            p_s.font.size = Pt(13)
            p_s.font.bold = True
            p_s.font.color.rgb = RGBColor(30, 150, 90)

        if "extra" in item:
            p_ex = ctf.add_paragraph()
            p_ex.text = f"💡 Extra:\n{item['extra']}"
            p_ex.font.size = Pt(11)
            p_ex.font.italic = True
            p_ex.font.color.rgb = RGBColor(100, 100, 100)

        # Right Side QR Code Image
        left_img = Inches(6.6)
        top_img = Inches(1.8)
        width_img = Inches(3.0)
        slide.shapes.add_picture(img_path, left_img, top_img, width=width_img)

        # Banner / Instruction text below QR Code
        banner_box = slide.shapes.add_textbox(Inches(6.4), Inches(5.1), Inches(3.4), Inches(1.2))
        btf = banner_box.text_frame
        btf.word_wrap = True
        bp = btf.paragraphs[0]
        bp.text = banner_text
        bp.font.size = Pt(14)
        bp.font.bold = True
        bp.font.color.rgb = RGBColor(108, 99, 255)
        bp.alignment = PP_ALIGN.CENTER

    prs.save(output_filename)
    print(f"Presentazione {output_filename} generata con successo!")

# Build Italian PowerPoint
build_presentation(
    PAGINE_IT,
    "QR_Esperimenti_Bias_Domande_IT.pptx",
    "Lezione Interattiva sui Bias Cognitivi",
    "Tutti i 22 Esperimenti Kahneman\n(Inquadra i QR code per rispondere in tempo reale!)",
    "📱 Inquadra il QR code con la tua fotocamera per partecipare",
    lang="IT"
)

# Build English PowerPoint
build_presentation(
    PAGINE_EN,
    "QR_Experiments_Cognitive_Biases_EN.pptx",
    "Interactive Lesson on Cognitive Biases",
    "All 22 Kahneman Experiments\n(Scan the QR code to answer in real-time!)",
    "📱 Scan the QR code with your smartphone camera to participate",
    lang="EN"
)
