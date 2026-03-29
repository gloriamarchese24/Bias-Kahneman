import os

for f in os.listdir('pages'):
    if f.endswith('.py'):
        with open(os.path.join('pages', f), 'r', encoding='utf-8') as file:
            content = file.read()
        
        content = content.replace('st.session_state.submitted_$NOME_ESPERIMENTO', 'st.session_state[NOME_ESPERIMENTO]')
        content = content.replace('"submitted_$NOME_ESPERIMENTO" not in', 'NOME_ESPERIMENTO not in')
        
        with open(os.path.join('pages', f), 'w', encoding='utf-8') as file:
            file.write(content)

print("Files modified.")
