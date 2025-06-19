import streamlit as st
from recommender import recommend_cards, summarize_cards
from app_cli import extract_user_profile
st.set_page_config(page_title="Credit Card Advisor", page_icon="$")
st.title("Credit Card Advisor Bot")
if "step" not in st.session_state:
    st.session_state.step = "start"
if "cards" not in st.session_state:
    st.session_state.cards = []
if "profile" not in st.session_state:
    st.session_state.profile = None

def restart_flow():
    st.session_state.step = "start"
    st.session_state.cards = []
    st.session_state.profile = None

if st.session_state.step == "start":
    st.subheader(" Tell us about your financial profile")
    user_input = st.text_area("Describe your income, credit score, perks, and spending habits:")

    if st.button("Get Recommendations"):
        profile = extract_user_profile(user_input)
        if profile:
            cards = recommend_cards(
                income=profile.get("income", 0),
                credit_score=profile.get("credit_score", 0),
                perks=profile.get("perks", []),
                spending_habits=profile.get("spending_habits", [])
            )
            if cards:
                st.session_state.step = "recommend"
                st.session_state.cards = cards
                st.session_state.profile = profile
            else:
                st.warning("No cards matched your profile. Try relaxing your preferences.")
        else:
            st.error("Could not understand your input. Please rephrase and try again.")

elif st.session_state.step == "recommend":
    st.subheader(" Recommended Credit Cards")
    for i, card in enumerate(st.session_state.cards):
        st.markdown(f"**{i+1}. {card['name']}**")
        st.markdown(f"- Best for: {', '.join(card.get('best_for', []))}")
        st.markdown(f"- Perks: {', '.join(card.get('perks', []))}")
        st.markdown("---")

    st.subheader(" Compare Cards")
    compare_indices = st.multiselect(
        "Select cards to compare (by number):",
        options=list(range(1, len(st.session_state.cards)+1)),
        format_func=lambda i: f"{i}. {st.session_state.cards[i-1]['name']}"
    )

    if st.button("Compare Selected") and compare_indices:
        for i in compare_indices:
            card = st.session_state.cards[i-1]
            st.markdown(f"### {card['name']}")
            st.write("Best For:", card.get("best_for", []))
            st.write("Perks:", card.get("perks", []))
            st.markdown("---")

    if st.button(" Restart Conversation"):
        restart_flow()

