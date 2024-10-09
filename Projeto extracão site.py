import cloudscraper
from bs4 import BeautifulSoup
import requests
import time

TOKEN = '' #privado
CHANNEL_ID = ''  #privado

scraper = cloudscraper.create_scraper()

def fetch_and_send_episodes():
    print("Iniciando a coleta e envio de episódios...")
    
    page = scraper.get('https://www.crunchyroll.com/pt-br/simulcastcalendar?filter=premium')

    soup = BeautifulSoup(page.content, 'html.parser')

    elements = soup.find('li', class_='day active today')

    if elements:
        print("Elemento 'li' encontrado.")
        episodios = elements.find_all(class_='release')
        
        if episodios:
            print(f"{len(episodios)} episódios encontrados.")
            messages = []
            for episodio in episodios:
                horario_element = episodio.find('time', class_='available-time')
                horario = horario_element.get_text(strip=True) if horario_element else 'Horário não encontrado'
                
                episodio_element = episodio.find('a', class_='available-episode-link')
                if episodio_element:
                    episodio_texto = episodio_element.get_text(separator=' ', strip=True)
                    episodio_texto = episodio_texto.split('em')[0].strip() 
                    episodio_texto = episodio_texto.replace('Disponível', '').strip() 
                    num_episodio = episodio_texto.replace('Episódio', '').strip()
                else:
                    num_episodio = 'Episódio não encontrado'
                
                nome_anime_element = episodio.find('cite', itemprop='name')
                nome_anime = nome_anime_element.get_text(strip=True) if nome_anime_element else 'Nome do anime não encontrado'
                
                resultado = f"Horário: {horario}, {nome_anime} Episódio {num_episodio}"
                messages.append(resultado)
            
            if messages:
                message_text = '\n'.join(messages)
                send_to_telegram(message_text)
                print("Informações enviadas para o Telegram.")
            else:
                send_to_telegram("Nenhuma informação de episódio encontrada.")
                print("Nenhuma informação de episódio encontrada.")
        else:
            send_to_telegram("Nenhum episódio encontrado.")
            print("Nenhum episódio encontrado.")
    else:
        send_to_telegram("Elemento 'li' com a classe 'day active today' não encontrado.")
        print("Elemento 'li' com a classe 'day active today' não encontrado.")

def send_to_telegram(message):
    url = f'' #privado
    payload = {
        'chat_id': CHANNEL_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    result = response.json()
    if result.get('ok'):
        print("Mensagem enviada com sucesso.")
    else:
        print("Erro ao enviar mensagem:", result)
    return result

fetch_and_send_episodes()

while True:
    time.sleep(10)
    fetch_and_send_episodes()
