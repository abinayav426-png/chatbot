
import json
import streamlit as st
from openai import OpenAI


# Initialize the OpenAI client (⚠️ Use your real key)
client = OpenAI(api_key="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")

# 





JSON_FILE = "smart_ai_chat.json"


# ---------- Helper Functions ----------

def find_related_keyword(question):
    """Extract a single or double word keyword related to the question."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract one or two related keywords from the question. Return only the keyword(s)."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()


def generate_answer(question):
    """Generate AI explanation for the question."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI teacher explaining AI topics in simple, clear language."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()


def save_to_json(data):
    """Save Q&A data into JSON file."""
    try:
        with open(JSON_FILE, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    history.append(data)

    with open(JSON_FILE, "w") as f:
        json.dump(history, f, indent=4)


def load_from_json():
    """Load all saved Q&A data."""
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# ---------- Streamlit UI ----------

st.set_page_config(page_title="🤖 Smart Keyword Chatbot", layout="centered")

st.title("🤖 Smart Keyword-Based AI Chatbot")
st.write("Ask me any question about Artificial Intelligence — and click on keywords to learn more!")

# Store state
if "last_data" not in st.session_state:
    st.session_state.last_data = None

# Input box
question = st.text_input("💬 Enter your question:")

if st.button("Ask"):
    if question.strip():
        keyword = find_related_keyword(question)
        answer = generate_answer(question)

        st.session_state.last_data = {
            "question": question,
            "keyword": keyword,
            "answer": answer
        }

        save_to_json(st.session_state.last_data)

        st.markdown(f"### 🤖 Bot Answer:")
        st.write(answer)
        st.markdown(f"#### 🔑 Keyword: **{keyword}**")

else:
    st.info("Type a question above and click **Ask**.")

# Show button for keyword (if exists)
if st.session_state.last_data:
    keyword = st.session_state.last_data["keyword"]

    if st.button(f"Learn about {keyword}"):
        # Try to fetch explanation for keyword from saved JSON
        data = load_from_json()
        match = next((item for item in data if item["keyword"].lower() == keyword.lower()), None)

        if match:
            st.markdown(f"### 📘 Explanation for **{keyword}**")
            st.write(match["answer"])
        else:
            st.warning("No information found for this keyword yet.")
