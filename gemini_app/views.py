from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
from google import generativeai as genai
from dotenv import load_dotenv
import textwrap

# Çevre değişkenlerini yükle
load_dotenv()

# Google API anahtarını al ve yapılandır
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Markdown biçiminde metin döndüren fonksiyon
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# ChatSession sınıfı
class ChatSession:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])

    def ask_question(self, question):
        response = self.chat.send_message(question)
        return response

# ChatSession nesnesi
chat_session = ChatSession()

# Global chat history
chat_history = []

@csrf_exempt
def index(request):
    global chat_history

    if request.method == 'POST':
        # Sohbet geçmişini temizleme isteği
        if request.POST.get('clear_history'):
            chat_history.clear()
        else:
            # Kullanıcıdan gelen soruyu işleme
            input_text = request.POST.get('input_text')
            if input_text:
                response = chat_session.ask_question(input_text)
                chat_history.append({"role": "Sen", "text": input_text})
                chat_history.append({"role": "Gemini", "text": response.text})

    # HTML döndür
    return render(request, 'gemini_app/index.html', {'chat_history': chat_history})
