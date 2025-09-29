import os
import logging
from flask import Flask
from flask_ask import Ask, statement, question, session
import requests

# Configuração para logs (opcional, mas útil para depuração)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, '/')

# URL base do servidor web do ESP32
# Substitua pelo IP local do seu ESP32 (ex: "192.168.1.100")
# Certifique-se de que o ESP32 e este servidor estão na mesma rede
ESP32_BASE_URL = "http://IP_DO_SEU_ESP32" 

@ask.launch
def start_skill():
    """Função de boas-vindas quando a skill é iniciada."""
    welcome_message = "Bem-vindo à automação do painel. Você pode dizer, acender ou desligar a lâmpada."
    return question(welcome_message)

@ask.intent("AcenderLampadaIntent")
def acender_lampada():
    """
    Função que recebe a intent 'AcenderLampadaIntent' da Alexa,
    identifica o comando e envia a requisição para o ESP32.
    """
    try:
        # Envia uma requisição GET para o endpoint '/ligar' do ESP32
        response = requests.get(f"{ESP32_BASE_URL}/ligar")
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            return statement("Lâmpada do painel acesa!")
        else:
            logging.error(f"Erro ao ligar a lâmpada. Status: {response.status_code}")
            return statement("Desculpe, houve um erro ao tentar ligar a lâmpada.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de conexão com o ESP32: {e}")
        return statement("Ocorreu um erro de conexão. Verifique o ESP32.")

@ask.intent("DesligarLampadaIntent")
def desligar_lampada():
    """
    Função que recebe a intent 'DesligarLampadaIntent' da Alexa,
    identifica o comando e envia a requisição para o ESP32.
    """
    try:
        # Envia uma requisição GET para o endpoint '/desligar' do ESP32
        response = requests.get(f"{ESP32_BASE_URL}/desligar")
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            return statement("Lâmpada do painel desligada.")
        else:
            logging.error(f"Erro ao desligar a lâmpada. Status: {response.status_code}")
            return statement("Desculpe, houve um erro ao tentar desligar a lâmpada.")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de conexão com o ESP32: {e}")
        return statement("Ocorreu um erro de conexão. Verifique o ESP32.")

@app.route('/')
def homepage():
    """
    Rota de entrada simples para verificar se o servidor está funcionando.
    """
    return "Servidor Flask para Alexa rodando!"

if __name__ == '__main__':
    # Define a porta 5000 para o servidor Flask
    # (ngrok irá apontar para esta porta)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
