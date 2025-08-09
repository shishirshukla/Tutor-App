import fitz  # PyMuPDF
import tiktoken
from typing import List
from openai import OpenAI




def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def split_text_into_chunks(text: str, max_tokens: int = 500, overlap: int = 50, model: str = "gpt-3.5-turbo") -> List[str]:
    tokenizer = tiktoken.encoding_for_model(model)
    tokens = tokenizer.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += max_tokens - overlap  # overlap for context retention

    return chunks


def pdf_to_chunks(pdf_path: str, max_tokens: int = 500, overlap: int = 50, model: str = "gpt-3.5-turbo") -> List[str]:
    full_text = extract_text_from_pdf(pdf_path)
    chunks = split_text_into_chunks(full_text, max_tokens, overlap, model)
    return chunks

#qwen/qwen2.5-vl-72b-instruct:free
def openAI():
    key = ''
    client = OpenAI(api_key=key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a skilled teacher who specializes in creating question papers"},
            {"role": "user", "content": f"Here are some PDF chunks:\n\n{context}\n\n Generate a question paper having questions from all the topics covered in the PDF chunk with same difficulty level as per the chunk"}
        ],
        temperature=0.3
    )
    print(response.choices[0].message.content.strip())




# Example usage
if __name__ == "__main__":
    pdf_path = "sample1.pdf"  # Replace with your PDF file path
    chunks = []
    chunks = pdf_to_chunks(pdf_path, max_tokens=400, overlap=50)
    print(type(chunks))
    pdf_path = "sample2.pdf"  # Replace with your PDF file path
    chunks.extend(pdf_to_chunks(pdf_path, max_tokens=400, overlap=50))
    print(type(chunks))
    pdf_path = "sample3.pdf"  # Replace with your PDF file path
    chunks.extend(pdf_to_chunks(pdf_path, max_tokens=400, overlap=50))

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i + 1} ---\n")
        print(chunk)
    
    context = "\n\n".join(chunks)  # Limit to first few if too large
    
    # 
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="",
    )

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="qwen/qwen2.5-vl-72b-instruct:free",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
          }
        }
      ]
    }
  ]
)
print(completion.choices[0].message.content)

    