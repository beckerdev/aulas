import os
import shutil
import time
import subprocess

# URL do seu site hospedado (ex: 'http://seudominio.com')
SITE_URL = 'https://beckerdev.github.io/aulas/'  # Altere para a URL do seu site

# Pasta temporária para baixar o site
FOLDER_SITE = '/thomep/site-temporario'  # Pode ser alterada se desejar

# Função para detectar pendrive (Linux, Windows, Mac, Chrome OS)
def find_usb_drive():
    # Chrome OS: normalmente monta dispositivos USB em /media/removable/
    chrome_os_path = '/media/removable'
    if os.path.exists(chrome_os_path):
        for d in os.listdir(chrome_os_path):
            path = os.path.join(chrome_os_path, d)
            if os.path.ismount(path):
                return path
    # Linux/Mac: normalmente montado em /media ou /Volumes
    for base in ['/media', '/Volumes']:
        if os.path.exists(base):
            for d in os.listdir(base):
                path = os.path.join(base, d)
                if os.path.ismount(path):
                    return path
    # Windows: verifica letras de unidade removíveis
    from string import ascii_uppercase
    for letter in ascii_uppercase:
        drive = f"{letter}:/"
        if os.path.exists(drive):
            try:
                if os.path.isdir(drive) and os.path.ismount(drive):
                    return drive
            except Exception:
                continue
    return None

# Função para baixar o site hospedado
def baixar_site():
    if os.path.exists(FOLDER_SITE):
        shutil.rmtree(FOLDER_SITE)
    os.makedirs(FOLDER_SITE, exist_ok=True)
    print("Baixando site da web...")
    comando = [
        'wget',
        '--mirror',
        '--convert-links',
        '--adjust-extension',
        '--page-requisites',
        '--no-parent',
        '-P', FOLDER_SITE,
        SITE_URL
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode == 0:
        print("Site baixado com sucesso.")
    else:
        print("Erro ao baixar o site:", resultado.stderr)

# Função para copiar arquivos modificados para o pendrive
def sync_site_to_usb():
    usb_path = find_usb_drive()
    if not usb_path:
        print("Pendrive não encontrado. Insira o pendrive.")
        return
    dest = os.path.join(usb_path, 'backup_site')
    if not os.path.exists(dest):
        os.makedirs(dest)
    # Copia todos os arquivos do site para o pendrive
    for root, dirs, files in os.walk(FOLDER_SITE):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, FOLDER_SITE)
            dest_file = os.path.join(dest, rel_path)
            dest_dir = os.path.dirname(dest_file)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                shutil.copy2(src_file, dest_file)
                print(f"Arquivo atualizado: {rel_path}")

if __name__ == "__main__":
    print("Monitorando alterações do site hospedado...")
    last_sync = 0
    while True:
        # Sincroniza a cada 30 segundos
        if time.time() - last_sync > 30:
            baixar_site()
            sync_site_to_usb()
            last_sync = time.time()
        time.sleep(5)