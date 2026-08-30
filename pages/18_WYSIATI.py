import streamlit as st
import random
import base64
import os
import streamlit.components.v1 as components
from supabase import create_client

st.set_page_config(page_title="WYSIATI Visivo", page_icon="👁️", layout="centered")

NOME_ESPERIMENTO = "wysiati"

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.question-card { background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%); border-radius: 20px; padding: 2rem; border: 1px solid rgba(108, 99, 255, 0.3); box-shadow: 0 8px 32px rgba(108, 99, 255, 0.2); margin: 1rem 0; }
.exp-title { font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #6C63FF, #FF6584); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.5rem; }
.exp-subtitle { color: #888; text-align: center; font-size: 1rem; margin-bottom: 1.5rem; }
.thanks-box { background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(0, 255, 136, 0.3); box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2); }
.thanks-emoji { font-size: 4rem; }
.thanks-text { color: #00FF88; font-size: 1.5rem; font-weight: 700; }

#MainMenu {visibility: hidden;} footer {visibility: hidden;}
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
            r = supabase.table("Risposte").insert({"esperimento": NOME_ESPERIMENTO + "_visit", "gruppo": "PENDING", "valore": 0}).execute()
            row_id = r.data[0]["id"]
            st.session_state.gruppo = "A" if row_id % 2 == 1 else "B"
        except Exception:
            st.session_state.gruppo = random.choice(["A", "B"])

if NOME_ESPERIMENTO not in st.session_state:
    st.session_state[NOME_ESPERIMENTO] = False

st.markdown("""<h1 class="exp-title">👁️ Riconoscimento Immagine (Bruner & Potter)</h1>""", unsafe_allow_html=True)
st.markdown("""<p class="exp-subtitle">Rispondi alle domande qui sotto</p>""", unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
    st.markdown("""**Scenario:** Guarda con attenzione la sequenza visiva qui sotto.\n\n⚡ **IMPORTANTE:** Scrivi nello spazio sottostante **LA PRIMA COSA CHE VEDI** (la tua primissima impressione non appena l'immagine compare) e invia subito la risposta!""")
    st.markdown("""---""")

    if st.session_state.gruppo == "A":
        b64_img = load_hydrant_b64()
        if b64_img:
            html_a = f'''<!DOCTYPE html><html><head><style>body {{ margin:0; padding:0; background:#111; font-family:sans-serif; text-align:center; color:white; }} .box {{ padding:1.2rem; background:#111; border-radius:20px; border:1px solid rgba(108,99,255,0.3); }} img {{ width:220px; border-radius:16px; filter:blur(24px); -webkit-filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,0.5); transition: filter 0.1s linear; }} p {{ color:#6C63FF; font-weight:600; font-size:0.9rem; margin-top:12px; }} button {{ background:#6C63FF; color:white; border:none; padding:10px 20px; border-radius:10px; font-weight:700; font-size:0.95rem; cursor:pointer; margin-top:8px; box-shadow:0 4px 12px rgba(108,99,255,0.4); }} button:active {{ transform: scale(0.96); }}</style></head><body><div class="box"><img id="imgA" src="data:image/jpeg;base64,{b64_img}" style="filter:blur(24px); -webkit-filter:blur(24px);" /><p id="txtA">🎥 Messa a fuoco video fluida (13s)...</p><button id="btnA" onclick="playA()">▶️ Riproduci Animazione</button></div><script>function playA() {{ var img=document.getElementById('imgA'); var txt=document.getElementById('txtA'); var btn=document.getElementById('btnA'); var start=null; var dur=13000; if(img) {{ img.style.filter="blur(24px)"; img.style.webkitFilter="blur(24px)"; }} txt.innerText="🎥 Messa a fuoco video fluida in corso (13s)..."; btn.disabled=true; btn.style.opacity="0.6"; function step(ts) {{ if(!start) start=ts; var progress=(ts-start)/dur; if(progress>1) progress=1; var curBlur=24-(progress*21); if(img) {{ img.style.filter="blur("+curBlur+"px)"; img.style.webkitFilter="blur("+curBlur+"px)"; }} if(progress<1) {{ window.requestAnimationFrame(step); }} else {{ txt.innerText="✅ Messa a fuoco completata!"; btn.disabled=false; btn.style.opacity="1"; }} }} window.requestAnimationFrame(step); }} window.onload=playA; setTimeout(playA, 100);</script></body></html>'''
            components.html(html_a, height=360)
        else:
            st.markdown("""<div style='text-align:center; padding:1.5rem; background:#111; border-radius:12px;'><div style='font-size:70px; filter:blur(9px); line-height:1;'>🧯🟡</div></div>""")
        scelta = st.text_input('Scrivi qui la PRIMA COSA che vedi / prima impressione:', key='t_wys1')

    else:
        b64_img = load_hydrant_b64()
        if b64_img:
            html_b = f'''<!DOCTYPE html><html><head><style>body {{ margin:0; padding:0; background:#111; font-family:sans-serif; text-align:center; color:white; }} .box {{ padding:1.2rem; background:#111; border-radius:20px; border:1px solid rgba(255,166,0,0.3); }} img {{ width:220px; border-radius:16px; filter:blur(24px); -webkit-filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,0.5); transition: filter 0.3s ease; }} p {{ color:#FFA600; font-weight:600; font-size:0.9rem; margin-top:12px; }} button {{ background:#FFA600; color:black; border:none; padding:10px 20px; border-radius:10px; font-weight:700; font-size:0.95rem; cursor:pointer; margin-top:8px; box-shadow:0 4px 12px rgba(255,166,0,0.4); }} button:active {{ transform: scale(0.96); }}</style></head><body><div class="box"><img id="imgB" src="data:image/jpeg;base64,{b64_img}" style="filter:blur(24px); -webkit-filter:blur(24px);" /><p id="txtB">🖼️ Frame 1 di 8 (Sfocatura iniziale 24px)...</p><button id="btnB" onclick="playB()">▶️ Riproduci Animazione</button></div><script>var timerId=null; function playB() {{ if(timerId) clearTimeout(timerId); var img=document.getElementById('imgB'); var txt=document.getElementById('txtB'); var btn=document.getElementById('btnB'); if(img) {{ img.style.filter="blur(24px)"; img.style.webkitFilter="blur(24px)"; }} btn.disabled=true; btn.style.opacity="0.6"; var frames=[{{b:24,l:"🖼️ Frame 1 di 8 (24px)"}},{{b:21,l:"🖼️ Frame 2 di 8 (21px)"}},{{b:18,l:"🖼️ Frame 3 di 8 (18px)"}},{{b:15,l:"🖼️ Frame 4 di 8 (15px)"}},{{b:12,l:"🖼️ Frame 5 di 8 (12px)"}},{{b:9,l:"🖼️ Frame 6 di 8 (9px)"}},{{b:6,l:"🖼️ Frame 7 di 8 (6px)"}},{{b:3,l:"🖼️ Frame 8 di 8 (Messa a fuoco 3px)"}}]; var idx=0; function showNext() {{ if(img) {{ img.style.filter="blur("+frames[idx].b+"px)"; img.style.webkitFilter="blur("+frames[idx].b+"px)"; }} if(txt) txt.innerText=frames[idx].l; idx++; if(idx<frames.length) {{ timerId=setTimeout(showNext, 1500); }} else {{ btn.disabled=false; btn.style.opacity="1"; }} }} showNext(); }} window.onload=playB; setTimeout(playB, 100);</script></body></html>'''
            components.html(html_b, height=360)
        else:
            st.markdown("""<div style='text-align:center; padding:1.5rem; background:#111; border-radius:12px;'><div style='font-size:70px; filter:blur(5px); line-height:1;'>🧯🔴</div></div>""")
        scelta = st.text_input('Scrivi qui la PRIMA COSA che vedi / prima impressione:', key='t_wys2')


    
    if st.button("📨 Invia risposta", type="primary", use_container_width=True):
        can_submit = True
        for var_name in ['scelta', 'val', 'eta', 'colpa', 'vetri', 'fiducia']:
            if var_name in locals() and locals()[var_name] is None:
                st.warning("⚠️ Per favore, rispondi alla domanda prima di inviare.")
                can_submit = False
                break
        
        if can_submit:
            v = 1 if any(w in scelta.lower() for w in ['idrant', 'estintor', 'hydrant', 'extinguish', 'fuoco', 'antincend', 'firehy', 'fire hy']) else 0
            supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()

            st.session_state[NOME_ESPERIMENTO] = True
            st.rerun()
else:
    st.markdown('''<div class="thanks-box"><p class="thanks-emoji">🎉</p><p class="thanks-text">Grazie per aver risposto!</p></div>''', unsafe_allow_html=True)
