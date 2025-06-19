import json

def load_cards():
    with open("credit_card.json", "r") as f:
        return json.load(f)

def recommend_cards(income, credit_score, perks, spending_habits, top_n=5):
    cards = load_cards()
    scored_cards = []

    for card in cards:
        score = 0

        if income is not None:
            if income >= card.get("min_income", 0):
                score += 30
            else:
                score -= 20 
        if credit_score is not None:
            if credit_score >= card.get("min_score", 0):
                score += 30
            else:
                score -= 20
        matched_perks = set(perks).intersection(set(card.get("perks", [])))
        score += 10 * len(matched_perks)
        matched_spending = set(spending_habits).intersection(set(card.get("best_for", [])))
        score += 10 * len(matched_spending)
        if score > 0:
            scored_cards.append((score, card))
    scored_cards.sort(key=lambda x: x[0], reverse=True)
    return [card for score, card in scored_cards[:top_n]]

def summarize_cards(cards):
    if not cards:
        return "No cards matched the user's preferences."

    summary = ""
    for card in cards:
        summary += (
            f"- **{card['name']}** by {card['issuer']}\n"
            f"  - Joining Fee: ₹{card['joining_fee']}\n"
            f"  - Annual Fee: ₹{card['annual_fee']}\n"
            f"  - Reward: {card['reward_rate']} ({card['reward_type']})\n"
            f"  - Best for: {', '.join(card['best_for'])}\n"
            f"  - Perks: {', '.join(card['perks'])}\n"
            f"  - [Apply Now]({card['link']})\n\n"
        )
    return summary

