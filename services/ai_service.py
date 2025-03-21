import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
github_key = os.getenv("GITHUB_TOKEN")

if not github_key:
    raise ValueError("API key not found. Please check your .env file.")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=github_key,
)

def generate_cover_letter(content: str) -> str:
    prompt = f"Create a cover letter based on the following content:\n\n{content}"
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a professional cover letter writer."},
            {"role": "user", "content": prompt},
        ],
        model="gpt-4o-mini",
        temperature=1,
        max_tokens=1000,
        top_p=1,
    )
    return response.choices[0].message.content
