import os

for fname in os.listdir('pages'):
    if not fname.endswith('.py'):
        continue
    p = os.path.join('pages', fname)
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sostituisce i markdown con apici singoli con i tripli apici doppi per massima sicurezza
    content = content.replace("st.markdown('", 'st.markdown("""')
    content = content.replace("', unsafe_allow_html=True)", '""", unsafe_allow_html=True)')
    content = content.replace("')", '""")')
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

print("Sicurezza markdown completata su tutte le pagine!")
