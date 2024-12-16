import openai
from flask import Flask, request, jsonify
import streamlit as st

# Set your OpenAI API Key here
openai.api_key = "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"  # Replace with your OpenAI key

app = Flask(__name__)

def get_summary(topic):
    """Request OpenAI API for summarization."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Specify the engine
            prompt=f"Provide a brief summary about {topic}.",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

def chatbot_response(user_message):
    """Handle chatbot message logic."""
    if "summary" in user_message.lower():
        topic = user_message.lower().replace("summary", "").strip()
        if topic:
            return get_summary(topic)
        else:
            return "Please specify the topic you want summarized."
    else:
        return "I can help with summaries. Try asking: 'Summary of AI in education.'"

# Streamlit frontend
st.title("Chatbot with Summarization Feature")
st.write("Ask me for a summary on any topic, for example: 'Summary of AI in education.'")

user_input = st.text_input("Your Message")
if user_input:
    with st.spinner("Generating response..."):
        response_text = chatbot_response(user_input)
    st.write("**Response:**", response_text)

if __name__ == '__main__':
    app.run(debug=True)
