from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ["GEMINI_API_KEY"]

def get_responce(chunks, query):
    client = genai.Client(api_key = API_KEY)
    found = '\n\n'.join(f"Фрагмент {n}: {c}" for n, c in enumerate(chunks, start=1))
    prompt = f""" 
    Ты - поискова система сцен. Пользователь просит тебя найти сцену в файле. Ты получаешь фрагменты текста, наиболее подходящие под описание пользователя, и на основе этой информации выдаешь ответ пользователю
    Вопрос пользователя:
    {query}
    Найденные сцены:
    {found}
    """

    response = client.models.generate_content(model = 'gemini-2.5-flash', contents=prompt)
    return response.text

