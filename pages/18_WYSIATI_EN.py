import streamlit as st
import random
import base64
import os
from supabase import create_client

st.set_page_config(page_title="Visual WYSIATI", page_icon="👁️", layout="centered")

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

st.markdown("""<h1 class="exp-title">👁️ Image Recognition (Bruner & Potter)</h1>""", unsafe_allow_html=True)
st.markdown("""<p class="exp-subtitle">Please answer the questions below</p>""", unsafe_allow_html=True)

if not st.session_state[NOME_ESPERIMENTO]:
    st.markdown("""**Scenario:** Carefully observe the visual sequence shown below.""")
    st.markdown("""---""")

    if st.session_state.gruppo == "A":
        b64_img = load_hydrant_b64()
        if b64_img:
            st.markdown(f'''<div style="text-align:center; padding:1.5rem; background:#111; border-radius:20px; margin-bottom:1.5rem; border:1px solid rgba(108,99,255,0.3);"><img id="hImgA" src="data:image/jpeg;base64,{b64_img}" style="width:240px; border-radius:16px; filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,0.5); transition: filter 0.1s linear;" /><p style="color:#6C63FF; font-weight:600; font-size:0.9rem; margin-top:12px;" id="txtA">🎥 Continuous fluid video unblurring in progress (8s)...</p><button onclick="playA()" style="background:#6C63FF; color:white; border:none; padding:8px 16px; border-radius:8px; font-weight:600; cursor:pointer; margin-top:6px;">▶️ Play again</button></div><script>function playA(){{var img=document.getElementById('hImgA');var txt=document.getElementById('txtA');var start=null;var dur=8000;txt.innerText="🎥 Continuous fluid video unblurring in progress (8s)...";function step(ts){{if(!start)start=ts;var progress=(ts-start)/dur;if(progress>1)progress=1;var curBlur=24-(progress*21);if(img)img.style.filter="blur("+curBlur+"px)";if(progress<1){{window.requestAnimationFrame(step);}}else{{txt.innerText="✅ Focus sequence completed.";}}}}window.requestAnimationFrame(step);}}setTimeout(playA, 400);</script>''', unsafe_allow_html=True)
        else:
            st.markdown("""<div style='text-align:center; padding:1.5rem; background:#111; border-radius:12px;'><div style='font-size:70px; filter:blur(9px); line-height:1;'>🧯🟡</div></div>""")
        scelta = st.radio('What do you believe this image primarily depicts?', ['A) A Minion / Animated character', 'B) A Fire Hydrant / Fire Extinguisher'], index=None, key='r1')

    else:
        b64_img = load_hydrant_b64()
        if b64_img:
            st.markdown(f'''<div style="text-align:center; padding:1.5rem; background:#111; border-radius:20px; margin-bottom:1.5rem; border:1px solid rgba(255,166,0,0.3);"><img id="hImgB" src="data:image/jpeg;base64,{b64_img}" style="width:240px; border-radius:16px; filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,0.5); transition: filter 0.3s ease;" /><p style="color:#FFA600; font-weight:600; font-size:0.9rem; margin-top:12px;" id="txtB">🖼️ Frame 1 of 4 (Initial blur 24px)...</p><button onclick="playB()" style="background:#FFA600; color:black; border:none; padding:8px 16px; border-radius:8px; font-weight:600; cursor:pointer; margin-top:6px;">▶️ Play again</button></div><script>function playB(){{var img=document.getElementById('hImgB');var txt=document.getElementById('txtB');var frames=[{{b:24,l:"🖼️ Frame 1 of 4 (Initial blur 24px)"}},{{b:16,l:"🖼️ Frame 2 of 4 (Heavy blur 16px)"}},{{b:10,l:"🖼️ Frame 3 of 4 (Medium blur 10px)"}},{{b:3,l:"🖼️ Frame 4 of 4 (Final focus 3px)"}}];var stepIdx=0;function show(){{if(img)img.style.filter="blur("+frames[stepIdx].b+"px)";if(txt)txt.innerText=frames[stepIdx].l;stepIdx++;if(stepIdx<frames.length){{setTimeout(show,2000);}}}}show();}}setTimeout(playB, 400);</script>''', unsafe_allow_html=True)
        else:
            st.markdown("""<div style='text-align:center; padding:1.5rem; background:#111; border-radius:12px;'><div style='font-size:70px; filter:blur(5px); line-height:1;'>🧯🔴</div></div>""")
        scelta = st.radio('What do you believe this image primarily depicts?', ['A) A Minion / Animated character', 'B) A Fire Hydrant / Fire Extinguisher'], index=None, key='r2')


    
    if st.button("📨 Submit response", type="primary", use_container_width=True):
        can_submit = True
        for var_name in ['scelta', 'val', 'eta', 'colpa', 'vetri', 'fiducia']:
            if var_name in locals() and locals()[var_name] is None:
                st.warning("⚠️ Please answer the question before submitting.")
                can_submit = False
                break
        
        if can_submit:
            v = 0 if 'Minion' in scelta else 1
            supabase.table('Risposte').insert({'esperimento': NOME_ESPERIMENTO, 'gruppo': st.session_state.gruppo, 'valore': v}).execute()

            st.session_state[NOME_ESPERIMENTO] = True
            st.rerun()
else:
    st.markdown('''<div class="thanks-box"><p class="thanks-emoji">🎉</p><p class="thanks-text">Thank you for participating!</p></div>''', unsafe_allow_html=True)
