from dotenv import load_dotenv
import os
import aiohttp
import logging

load_dotenv()
gemini_token = os.getenv("GEMINI_API_KEY")
if not gemini_token:
    raise ValueError("Missing Gemini API Key credential in environment variables.")


async def generate_gemini_review_answer(username, stars, text):
    text = (
        "Hi!"
        f"I am a feedback collection bot for a restaurant, and I’ve just received a new review from a user named {username}. "
        f"Here is the review he submitted: {text}."
        f"He also gave a rating of {stars} out of 5 stars. Could you please analyze his review and write a reply in 1–2 sentences?"
        "Please maintain a formal tone and absolutely avoid any offensive or inappropriate language in your response."
        "The reply should be written in the same language the user used in their review."
        "In your response to me, do not include any reasoning or reflections, because the reply is sent directly to the customer without any filtering."
        "You may offer the customer a discount of 5% to 15% on their next order in the following cases: the customer is extremely dissatisfied, their celebration"
        "was negatively affected, it was their first time at the restaurant and they were very pleased, or if there is a phrase or hint that the customer has already"
        "recommended our restaurant to their friends."
        "Thank you!"
    )
    return text


async def call_gemini(prompt: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_token}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                logging.error(f"❌ Error: {response.status}")
                return None
            data = await response.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                logging.error("⚠️ Couldn’t understand the response:", e)
                return data
