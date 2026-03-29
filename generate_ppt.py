import qrcode
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import os

BASE_URL = "https://bias-kahneman-ms2mgk3bueryreh4vj78ae.streamlit.app"

PAGINE = [
    ("1_Macchina.py", "1. Loftus & Palmer (Velocità Auto)", "Macchina"),
    ("2_Malattia_Asiatica.py", "2. Asian Disease (Malattia Asiatica)", "Malattia_Asiatica"),
    ("3_Framing_AI.py", "3. Framing Medico AI", "Framing_AI"),
    ("4_Ancoraggio_Gandhi.py", "4. Ancoraggio (Età Gandhi)", "Ancoraggio_Gandhi"),
    ("5_Ancoraggio_Roulette.py", "5. Ancoraggio Medico (Roulette)", "Ancoraggio_Roulette"),
    ("6_Avversione_Perdite.py", "6. Avversione alle Perdite", "Avversione_Perdite"),
    ("7_Illusione_Verita.py", "7. Illusione di Verità (Font)", "Illusione_Verita"),
    ("8_Euristica_Disponibilita.py", "8. Availability Heuristic", "Euristica_Disponibilita"),
    ("9_Problema_Linda.py", "9. Problema di Linda", "Problema_Linda"),
    ("10_Effetto_Alone.py", "10. Effetto Alone (Asch)", "Effetto_Alone"),
    ("11_Effetto_Dote_Tazza.py", "11. Effetto Dote (Tazze Thaler)", "Effetto_Dote_Tazza"),
    ("12_Effetto_Dote_AI.py", "12. Effetto Dote (Licenza AI)", "Effetto_Dote_AI"),
    ("13_Costi_Sommersi_Teatro.py", "13. Costi Sommersi (Teatro Kahneman)", "Costi_Sommersi_Teatro"),
    ("14_Costi_Sommersi_AI.py", "14. Costi Sommersi (Progetto AI)", "Costi_Sommersi_AI"),
    ("15_Effetto_Default.py", "15. Effetto Default (Organ Donation)", "Effetto_Default"),
    ("16_Priming_Associativo.py", "16. Priming Associativo", "Priming_Associativo"),
    ("17_Dunning_Kruger.py", "17. Illusione di Superiorità", "Dunning_Kruger"),
    ("18_WYSIATI.py", "18. WYSIATI (Giudizio Processo)", "WYSIATI"),
    ("19_Base_Rate_Neglect.py", "19. Base Rate Neglect", "Base_Rate_Neglect"),
    ("20_L_Esca.py", "20. Decoy Effect (L'Esca)", "L_Esca"),
    ("21_Regressione_Media.py", "21. Regressione alla Media", "Regressione_Media")
]

os.makedirs("qrcodes", exist_ok=True)
prs = Presentation()

title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Lezione Interattiva sui Bias Cognitivi"
subtitle.text = "Tutti i 21 Esperimenti Kahneman\n(Inquadra i QR code per rispondere!)"

for file_name, titolo, url_path in PAGINE:
    url = f"{BASE_URL}/{url_path}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_path = f"qrcodes/{url_path}.png"
    img.save(img_path)
    
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title_shape = slide.shapes.title
    title_shape.text = titolo
    
    left = Inches(3.5)
    top = Inches(2.5)
    height = Inches(4)
    pic = slide.shapes.add_picture(img_path, left, top, height=height)
    
    txBox = slide.shapes.add_textbox(Inches(1), Inches(6.8), Inches(8), Inches(1))
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = "Inquadra il QR code con la tua fotocamera"
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(108, 99, 255)
    tf.paragraphs[0].alignment = 2

prs.save("QR_Esperimenti_Bias_21.pptx")
print("PPT creato con successo 21 slides!")
