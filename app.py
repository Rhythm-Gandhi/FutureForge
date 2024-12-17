import openai
import streamlit as st
import os

# Load the OpenAI API key
openai.api_key = "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"

# --- Load CSS Styling ---
def load_css():
    with open("static/styles.css", "r") as css_file:
        css = f"<style>{css_file.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# --- Function for Chatbot ---
def get_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# --- Streamlit App ---
def main():
    # Page Configuration
    st.set_page_config(page_title="Future Forge", layout="wide")

    # Load CSS Styling
    load_css()

    # Hero Section
    st.markdown("""
        <section class="hero">
            <div class="hero-content">
                <h1>Forge Your Future with FutureForge</h1>
                <p>Your all-in-one platform for personalized career guidance and gamified learning experiences.</p>
                <a href="#features" class="cta-button">Explore Features</a>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <section class="features" id="features">
            <h2>Why Choose FutureForge?</h2>
            <div class="feature-cards">
                <div class="card">
                    <h3>Personalized Plans</h3>
                    <p>Tailored career roadmaps based on your level and interests.</p>
                </div>
                <div class="card">
                    <h3>Comprehensive Resources</h3>
                    <p>Access curated articles, notes, and video content all in one place.</p>
                </div>
                <div class="card">
                    <h3>Interactive Coach</h3>
                    <p>Chatbot support with practice questions, summaries, and tips.</p>
                </div>
                <div class="card">
                    <h3>Gamified Learning</h3>
                    <p>Earn badges and rewards as you achieve your milestones.</p>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # Chatbot Section
    st.sidebar.title("Chat with FutureForge")
    user_input = st.sidebar.text_input("Ask the chatbot:")
    if st.sidebar.button("Submit"):
        if user_input:
            with st.spinner("Processing..."):
                response = get_response(user_input)
                st.sidebar.write(f"**Response:** {response}")
        else:
            st.sidebar.warning("Please enter a message.")

    # How It Works Section
    st.markdown("""
        <section class="how-it-works" id="how-it-works">
            <h2>How It Works</h2>
            <div class="steps">
                <div class="step">
                    <h3>Step 1</h3>
                    <p>Create your profile and share your career goals.</p>
                </div>
                <div class="step">
                    <h3>Step 2</h3>
                    <p>Get a personalized roadmap tailored to your interests.</p>
                </div>
                <div class="step">
                    <h3>Step 3</h3>
                    <p>Track your progress with gamified milestones.</p>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # Contact Section
    st.markdown("""
        <footer class="contact" id="contact">
            <h2>Contact Us</h2>
            <p>Have questions? Reach out to us at 
            <a href="mailto:support@futureforge.com">support@futureforge.com</a>.</p>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
