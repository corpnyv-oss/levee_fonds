def update_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les URLs HTTPS par HTTP
    content = content.replace('https://sandbox-api.singpay.com', 'http://sandbox-api.singpay.com')
    content = content.replace('https://api.example.com', 'http://api.example.com')
    content = content.replace('https://app.example.com', 'http://app.example.com')
    
    # Sauvegarder les modifications
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Mettre à jour les fichiers
update_urls('c:\\Users\\njipn\\OneDrive\\Documents\\backend FAPAG\\.env.example')
update_urls('c:\\Users\\njipn\\OneDrive\\Documents\\backend FAPAG\\fapag_collecte_backend\\settings.py')
