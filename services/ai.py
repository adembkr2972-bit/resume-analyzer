import os
import time
from google.genai.errors import ServerError
from dotenv import load_dotenv
from google import genai
from google.genai import types
from .models import ResumeAnalysis

DEV_MODE = false if os.getenv("ENV") == "production" else True

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_resume(prompt):
    if DEV_MODE:

        with open(
        "sample_data/sample_result.json",
        "r",
        encoding="utf-8"
        ) as f:

            return ResumeAnalysis.model_validate_json(f.read())

    retries = 3

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="models/gemini-3.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ResumeAnalysis,
                    temperature=0.3,
                ),
            )

            return response.parsed

        except ServerError:
            if attempt < retries - 1:
                time.sleep(5)
            else:
                raise Exception(
                    "Gemini is currently overloaded. Please try again in a minute."
                )