from openai import OpenAI
import string

EMBEDDING_MODEL = "text-embedding-3-small"


def convert_into_tokens(document_content: str):
    clean_document_content = clean_text(document_content)
    return get_embeddings(clean_document_content)

def get_embeddings(document_content: str):
    client = OpenAI()
    return client.embeddings.create(input = [document_content], model=EMBEDDING_MODEL).data[0].embedding


def clean_text(document_content: str) -> str:
    """clean document

    Args:
        document_content (str):

    Returns:
        str: cleand text
    """
    document_content = document_content.lower()
    document_content = document_content.translate(str.maketrans('', '', string.punctuation))
    document_content = ' '.join(document_content.split())
    
    return document_content
