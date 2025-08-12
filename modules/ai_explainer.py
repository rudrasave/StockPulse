from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")

# Create OpenAI client
client = OpenAI(api_key=api_key)

def get_explanation(question: str, df: pd.DataFrame) -> str:
    """Use OpenAI to explain portfolio data based on user question."""
    if df.empty:
        return "No data available to analyze."

    # Convert small snapshot of data to give the AI context
    sample_data = df.head(5).to_string()

    prompt = (
        f"You are a financial market analyst. The user has the following portfolio data:\n"
        f"{sample_data}\n\n"
        f"User question: {question}\n"
        f"Give a clear, insightful answer."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # use "gpt-4" or "gpt-3.5-turbo" if available
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating explanation: {e}"
