import os

for fname in os.listdir('pages'):
    if not fname.endswith('.py'):
        continue
    p = os.path.join('pages', fname)
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sostituisce gli apici singoli con i tripli apici doppi per non rompere l'HTML quando ci sono apostrofi nel testo
    content = content.replace("st.markdown('<h1 class=\"exp-title\">", 'st.markdown("""<h1 class="exp-title">')
    content = content.replace("</h1>', unsafe_allow_html=True)", '</h1>""", unsafe_allow_html=True)')
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fix apostrofi completato!")
