import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MY_NLP_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL = "models/gemini-flash-latest"

def gemini_response(prompt):

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text.replace("*", "").strip()



#SENTIMENT ANALYSIS
def sentiment_analysis(text):
    prompt = f"Analyze sentiment of this text and say Positive, Negative or Neutral:\n{text}"
    return gemini_response(prompt)


#ABUSE DETECTION
def abuse_detection(text):
    prompt = f"Check if this text is abusive or offensive. Reply Yes or No and short reason:\n{text}"
    return gemini_response(prompt)


#NAMED ENTITY RECOGNITION
def ner(text):
    prompt = f"""
Extract named entities from the text below.
Return result ONLY in this format:
Person: ...
Location: ...
Organization: ...
Date: ...

Text:
{text}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    raw_output = response.text.replace("*", "").strip()

    entities = []
    lines = raw_output.split("\n")

    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            entities.append({
                "type": key.strip(),
                "value": value.strip()
            })

    return entities



#PARAPHRASING
def paraphrase(text):
    prompt = f"Paraphrase the following text in simple language:\n{text}"
    return gemini_response(prompt)


#TRANSLATION
def translate_text(text, source_lang, target_lang):
    prompt = f"""
    Translate the following text
    from {source_lang} to {target_lang}.

    Text:
    {text}

    Provide only the translated text.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text



#LANGUAGE DETECTION
def language_detection(text):
    prompt = f"Detect the language of this text:\n{text}"
    return gemini_response(prompt)


#TEXT SUMMARIZATION
def summarization(text):
    prompt = f"Summarize the following text in short:\n{text}"
    return gemini_response(prompt)


#QUESTION ANSWERING
def question_answering(context, question):
    prompt = f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
    return gemini_response(prompt)


#SEMANTIC SEARCH
def semantic_search(query, documents):
    prompt = f"""
    Find the sentence from the documents that best matches
    the meaning of the user's query.

    Query:
    {query}

    Documents:
    {documents}

    Return only the most relevant sentence.
    """

    return gemini_response(prompt)





#SEMANTIC SIMILARITY
def semantic_similarity(text1, text2):
    prompt = f"""
    Compare the semantic similarity of the two texts.

    Text 1:
    {text1}

    Text 2:
    {text2}

    Give:
    1. A short explanation
    2. A similarity score between 0 and 1

    Format response exactly like:
    SCORE: <number>
    EXPLANATION:
    <explanation text>
    """

    response = gemini_response(prompt)

    score = "N/A"
    explanation = response

    if "SCORE:" in response:
        parts = response.split("EXPLANATION:")
        score = parts[0].replace("SCORE:", "").strip()
        explanation = parts[1].strip()

    return {
        "score": score,
        "explanation": explanation
    }



#EMOTION DETECTION
def emotion_detection(text):
    prompt = f"Detect emotion from text (happy, sad, angry, fear, surprise, neutral):\n{text}"
    return gemini_response(prompt)

