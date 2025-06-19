import json
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from recommender import recommend_cards, summarize_cards

llm = OllamaLLM(model="mistral")

extraction_prompt = PromptTemplate.from_template("""
Extract the following fields from the user's message:
- income (monthly, in INR, number)
- credit_score (number or null if not specified)
- perks (list of keywords like "metal_card", "smart_app", "airport_lounge", etc.)
- spending_habits (list of categories like "shopping", "travel", "fuel", "dining", "entertainment", etc.)

If a field is not present or unclear, set it to null (for numbers) or an empty list (for arrays).

User message: "{message}"

Respond ONLY with a JSON object with no extra text, comments, or explanations in this exact format:

{{
  "income": number or null,
  "credit_score": number or null,
  "perks": [list of strings],
  "spending_habits": [list of strings]
}}
""")

def extract_user_profile(message: str):
    prompt = extraction_prompt.format(message=message)
    response = llm.invoke(prompt)
    try:
        profile = json.loads(response)
        return profile
    except json.JSONDecodeError:
        print("Failed to parse response. Got:\n", response)
        return None

def main():
    print(" Welcome to Credit Card Advisor Bot!")
    message = input("\nTell me about your salary, credit score, preferred perks and spending style:\n\n> ")

    profile = extract_user_profile(message)
    if not profile:
        print("\nSorry, I couldn’t understand your input.")
        return

    print("\nExtracted profile:", profile)

    cards = recommend_cards(
        income=profile.get("income", 0),
        credit_score=profile.get("credit_score", 0),
        perks=profile.get("perks", []),
        spending_habits=profile.get("spending_habits", [])
    )

    if not cards:
        print("\n Sorry, no cards matched your profile.")
        print("Try improving your credit score or relaxing perk/spending preferences.")
        return

    summary = summarize_cards(cards)

    recommendation_prompt = PromptTemplate.from_template(
        "Recommend credit cards to a user based on this list:\n\n{summary}\n\nExplain in a helpful tone."
    )

    print("\n Bot says:\n")
    print(llm.invoke(recommendation_prompt.format(summary=summary)))

if __name__ == "__main__":
    main() 

