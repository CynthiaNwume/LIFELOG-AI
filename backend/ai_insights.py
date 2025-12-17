"""
ai_insights.py
--------------
Generates AI-based insights from recent LifeLog data.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_weekly_insight(logs: list) -> str:
    """
    Takes a list of daily logs and returns a short AI-generated insight.
    """

    if not logs:
        return "Not enough data to generate insights yet."

    # Convert logs into readable text for the AI
    formatted_logs = []
    for log in logs:
        formatted_logs.append(
            f"Date: {log.log_date}, "
            f"Mood: {log.mood}, "
            f"Sleep: {log.sleep_hours} hrs, "
            f"Steps: {log.steps}"
        )

    prompt = f"""
You are a personal analytics assistant.

Here are the last few days of personal wellness data:
{chr(10).join(formatted_logs)}

Provide:
- A concise summary (2–3 sentences)
- One pattern you notice
- One gentle recommendation

Keep the tone calm, practical, and non-judgmental.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze personal wellness data."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

