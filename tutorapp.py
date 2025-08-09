from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
import openai
from openai import OpenAI
import os


key = ''
client = OpenAI(api_key=key)


def load_pdf():
    # Step 1: Load PDF
    loader = PyPDFLoader("gecu110.pdf")
    pages = loader.load()

    # Step 2: Chunking
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(pages)

    for chunk in docs:
        chunk.metadata["subject"] = "Science"
        chunk.metadata["chapter"] = "Life Processes in Plants"
        chunk.metadata["class"] = "Class-7"
        


    # Step 3: Local Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Step 4: Store in Chroma
    db = Chroma.from_documents(docs, embedding=embeddings, persist_directory="./chroma_db")
    db.persist()



def generate_mcqs_openai(chapter_text: str, chapter_title: str, mcq_count: int = 5, model="gpt-3.5-turbo") -> str:
    system_prompt = "You are an expert school teacher and quiz creator. You generate age-appropriate, curriculum-aligned MCQs for school students. Do not mention 'as per text' in any question"

    user_prompt = f"""
Generate {mcq_count} multiple-choice questions (MCQs) from the following chapter titled "{chapter_title}":

\"\"\"
{chapter_text}
\"\"\"

Each question should have 4 options and highlight the correct one clearly. Format the output as:

Q1. Question text?
A. Option A
B. Option B
C. Option C
D. Option D
Answer: B
"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


#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

load_pdf()
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 1: Initialize DB
db = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")

# Step 5: Load Ollama LLM
#llm = Ollama(model="deepseek-r1")  # or "qwen:1.8b"

# Retrieve all chunks with metadata for specific chapter
chapter_docs = db.get(include=["documents", "metadatas"])

# Filter docs by chapter
target_chapter = "Life Processes in Plants"
chapter_chunks = [
    doc for doc, meta in zip(chapter_docs["documents"], chapter_docs["metadatas"])
    if meta.get("chapter") == target_chapter
]

# Combine text (limit to avoid context overflow)
combined_text = "\n".join(chapter_chunks)[:10000]  # adjust token size for model

mcqs_output = generate_mcqs_openai(combined_text, target_chapter, mcq_count=10)
print(mcqs_output)

# prompt = f"""
# Here is the content from a social science chapter titled '{target_chapter}':

# \"\"\"
# {combined_text}
# \"\"\"

# Generate 5 multiple-choice questions (MCQs) with 4 options each and mark the correct answer. Keep questions at 6th grade level.
# """
# response = llm(prompt)
# print(response)

