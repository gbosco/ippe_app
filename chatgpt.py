import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

OPENAI_APIKEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_APIKEY)


def make_openai_request(messages):
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices


def get_keywords(text: str) -> List[str]:
    choices = make_openai_request([
        {"role": "user", "content": f'extract keywords from this statement {text}'}])

    content = choices[0].message.content
    return [keyword.strip() for keyword in content.split(",")]


def run_sentiment_analysis(text: str):
    prompt = f"Analyze the sentiment of the following text and classify it as positive, negative, or neutral:\n\n{text}"
    choices = make_openai_request([{"role": "user", "content": prompt}])
    return choices[0].message.content


def generate_text_response(text: str):
    sentiment = run_sentiment_analysis(text)
    print(f"Sentiment analysis result: {sentiment}")
    keywords = get_keywords(text)
    print(f"Extracted keywords: {keywords}")
    prompt = f"Generate an professional, appropriate response for the text by a customer: \n\n{text},"
    choices = make_openai_request([{"role": "user", "content": prompt}])
    return choices[0].message.content


def translate_text(text: str, lang="portuguese"):
    prompt = f"translate the given text {text} to {lang}"
    choices = make_openai_request([{"role": "user", "content": prompt}])
    return choices[0].message.content
