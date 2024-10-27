import os

from langchain import PromptTemplate
import json

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

def getinfos(email):

    # Initialize the Ollama LLM for LLAMA 3.2
    llm = ChatOllama(
        model=os.getenv("OLLAMA_MODEL"),
        temperature=0,
        format="json",
        base_url=os.getenv("OLLAMA_BASE_URL")
    )

    # Define your prompt template
    template = """
    Du bist ein sehr hilfreicher Assistent der sich auf die Extraktion von Informationen aus allen Emails spezialisiert hat. 
    Aus dem untenstehenden E-Mail-Text, extrahiere die folgenden Informationen:

    Betreff
    Schlagworte (relevante Schlüsselwörter oder Themen)
    Kurzbeschreibung (eine Zusammenfassung in einem Satz)
    Langbeschreibung (eine detaillierte Zusammenfassung)
    
    E-Mail-Text: "{email_text}"

    Gib das Ergebnis als JSON-Objekt mit den folgenden Schlüsseln aus: "title", "tags", "short", "transcript".
    Bitte halte dich bei der Ausgabe an die deutsche Sprache. Fülle unbedingt alle Schlüssel aus! 
    """

    # Set up the prompt with LangChain
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | JsonOutputParser()

    query_chain = chain.invoke({
        "email_text": email
    })

    return query_chain

# Function to extract information
def extract_email_info(email):
    if email is None:
        return
    response = getinfos(email)
    if len(response) == 0:
        return None
    try:
        result = json.dumps(response, ensure_ascii=False)
        return result
    except json.JSONDecodeError:
        print("Error decoding JSON. Response:", response)
        return None
