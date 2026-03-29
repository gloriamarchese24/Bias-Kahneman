import os

nuovo_codice = """if "gruppo" not in st.session_state:
    try:
        res = supabase.table("Risposte").select("gruppo").eq("esperimento", NOME_ESPERIMENTO).execute()
        gruppi = [r["gruppo"] for r in res.data]
        count_a = gruppi.count("A")
        count_b = gruppi.count("B")
        
        # Assegna al gruppo con meno persone (bilanciamento perfetto)
        if count_a <= count_b:
            st.session_state.gruppo = "A"
        else:
            st.session_state.gruppo = "B"
    except Exception:
        # Fallback di sicurezza in caso di disconnessione momentanea
        st.session_state.gruppo = random.choice(["A", "B"])"""

vecchio_codice = """if "gruppo" not in st.session_state:
    st.session_state.gruppo = random.choice(["A", "B"])"""

modificati = 0
for file in os.listdir('pages'):
    if file.endswith('.py'):
        path = os.path.join('pages', file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if vecchio_codice in content:
            content = content.replace(vecchio_codice, nuovo_codice)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            modificati += 1

print(f"File aggiornati con bilanciamento rigoroso: {modificati}")
