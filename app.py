import streamlit as st
import os
import time
from fpdf import FPDF
from io import BytesIO
import google.generativeai as palm

# Set the API Key
palm.configure(api_key="AIzaSyC8igDiWdUGzznMg6jYQjXSzJGFMKsWzdQ")  # Replace with your Gemini API Key

# --- Function for Chatbot Response ---
def get_response(user_message):
    try:
        # Use the correct method for interacting with Gemini
        response = palm.generate_response(
            messages=[{"role": "user", "content": user_message}],
            model="models/text-bison-001"  # Ensure this model is valid
        )
        return response.result['content']  # Return the response text
    except Exception as e:
        return f"Error: {str(e)}"



# Set the API Key
palm.configure(api_key="AIzaSyC8igDiWdUGzznMg6jYQjXSzJGFMKsWzdQ")  # Replace with your Gemini API Key

# --- Page Configuration (Must be the first Streamlit command) ---
st.set_page_config(page_title="Future Forge", layout="wide")

# --- Load CSS Styling ---
def load_css():
    with open("static/styles.css", "r") as css_file:
        css = f"<style>{css_file.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# --- Function to Generate PDF ---
def generate_pdf(content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)  # Add content with line wrapping

    # Save to a BytesIO buffer instead of a file
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)  # Reset the buffer's position to the start
    return pdf_buffer

# --- PDF Download Logic ---
if st.sidebar.button("Generate PDF"):
    # Compile chat history into a single string
    if 'chat_history' in st.session_state and st.session_state.chat_history:
        chat_history_text = "\n\n".join([f"User: {q}\nBot: {a}" for q, a in st.session_state.chat_history])
        pdf_file = generate_pdf(chat_history_text)

        # Provide a download button for the generated PDF
        st.sidebar.download_button(
            label="Download Chat History as PDF",
            data=pdf_file,
            file_name="FutureForge_ChatHistory.pdf",
            mime="application/pdf"
        )
    else:
        st.sidebar.warning("No chat history to export!")


# --- Initialize Session State ---
def initialize_session_state():
    if 'user_level' not in st.session_state:
        st.session_state.user_level = 1
    if 'experience_points' not in st.session_state:
        st.session_state.experience_points = 0
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "Adventurer"
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []  # Store chat history for PDF generation
    if 'chosen_character' not in st.session_state:
        st.session_state.chosen_character = None  # Default to None until selected
    if 'nickname' not in st.session_state:
        st.session_state.nickname = None  # Default nickname to None

# --- Upgrade User Character ---
def upgrade_character():
    if 'experience_points' in st.session_state and st.session_state.experience_points >= 100 * st.session_state.user_level:
        st.session_state.user_level += 1
        st.session_state.experience_points = 0
        return f"Congratulations! You've leveled up to level {st.session_state.user_level}!"
    return None

# --- Character Avatar Based on Level ---
def get_character_avatar(level, chosen_character):
    avatar_mapping = {
        "Cool Guy": {
            1: "static/images/avatar_level_1.png",  # Replace with actual local file paths
            2: "static/images/avatar_level_2.png",
            3: "static/images/avatar_level_3.png",
            4: "static/images/avatar_level_4.png",
        },
        "Cute Girl": {
            1: "static/images/avatar_level_1_character_2.png",  # Character 2 avatars
            2: "static/images/avatar_level_2_character_2.png",
            3: "static/images/avatar_level_3_character_2.png",
            4: "static/images/avatar_level_4_character_2.png",
        },
        "Fierce Dragon": {
            1: "static/images/avatar_level_1_character_3.png",  # Character 3 avatars
            2: "static/images/avatar_level_2_character_3.png",
            3: "static/images/avatar_level_3_character_3.png",
            4: "static/images/avatar_level_4_character_3.png",
        },
    }
    # Default to character 1 if something goes wrong
    return avatar_mapping.get(chosen_character, avatar_mapping["Cool Guy"]).get(level, "static/images/avatar_level_1.png")  # Default to level 1 avatar

# --- Streamlit App ---
def main():
    # Page Configuration
   

    # Load CSS
    load_css()

    # Initialize Session State
    initialize_session_state()
    
# --- Character Selection Section ---
if 'chosen_character' not in st.session_state:
    st.session_state.chosen_character = None  # Default to None until selected

if 'nickname' not in st.session_state:
    st.session_state.nickname = None  # Default nickname to None

if not st.session_state.get('chosen_character'):
    st.title("Welcome to Future Forge!")
    st.write("Select your character to begin:")
    
    # Character selection dropdown
    character_choice = st.selectbox(
        "Choose your Forge Master",
        ["Cool Guy", "Cute Girl", "Fierce Dragon"]
    )
    
    # Input field for nickname
    nickname_input = st.text_input("Give your character a nickname:", placeholder="Enter a nickname")
    
    # Button to confirm character and nickname
    if st.button("Select Character"):
        if nickname_input.strip():  # Check if nickname is provided
            st.session_state.chosen_character = character_choice
            st.session_state.nickname = nickname_input.strip()
            st.success(f"Character '{character_choice}' is selected with nickname '{nickname_input}'!")
            st.experimental_rerun()
        else:
            st.warning("Please provide a nickname for your character!")

# Display the chosen character and nickname
if st.session_state.get('chosen_character') and st.session_state.get('nickname'):
    st.sidebar.write(f"**Character:** {st.session_state.chosen_character}")
    st.sidebar.write(f"**Nickname:** {st.session_state.nickname}")

    # Upgrade Character if conditions met
    upgrade_message = upgrade_character()
    if upgrade_message:
        st.sidebar.success(upgrade_message)

    # --- Hero Section ---
    st.markdown(
        """
        <div class="hero" style="color: black;">
            <h1>Forge Your Future with FutureForge</h1>
            <p>Explore personalized career guidance, interactive learning, and gamified experiences!</p>
            <a href="#features" class="cta-button">Explore Features</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Features Section with Blocks ---
    st.markdown(
        """
        <div class="features" id="features" style="color: black;">
            <h2>Why Choose FutureForge?</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create 3 columns for the blocks of options
    col1, col2, col3 = st.columns(3)

    # Column 1: Personalized Plans
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>📋 Personalized Plans</h3>
                <p>Get tailored career roadmaps that suit your goals and aspirations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Column 2: Comprehensive Resources
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>📚 Comprehensive Resources</h3>
                <p>Access articles, notes, and videos curated for your learning needs.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Column 3: Interactive Chatbot
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🤖 Interactive Chatbot</h3>
                <p>Chat with our AI coach to get answers, summaries, and tips.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- Add more rows if needed ---
    col4, col5 = st.columns(2)

    # Column 4: Gamified Learning
    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🏆 Gamified Learning</h3>
                <p>Earn rewards and badges as you achieve your milestones!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Column 5: Additional Feature (if needed)
    with col5:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🌱 Continuous Growth</h3>
                <p>Keep progressing with continuous learning and development paths.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- Chatbot Section ---
    st.sidebar.title(f"Chat with {st.session_state.user_name} 🤖 (Level {st.session_state.user_level})")
    
    # Display Character Avatar
    avatar_url = get_character_avatar(st.session_state.user_level, st.session_state.chosen_character)
    st.sidebar.image(avatar_url, width=100)  # Display avatar image

    st.sidebar.markdown(
        "Ask the chatbot anything related to your career goals, summaries, or topics of interest!",
        unsafe_allow_html=True
    )
    
    # Add a text area for multi-line input
    user_input = st.sidebar.text_area("Type your question:", placeholder="Ask me anything...")

    # Display responses interactively with styled text box
    if st.sidebar.button("Submit"):
        if user_input:
            with st.spinner("Thinking... 🤔"):
                response = get_response(user_input)
                
                st.sidebar.markdown(f"""
                    <div style='
                        background-color: #f8f9fa; 
                        color: black; /* Make text color black */
                        padding: 10px; 
                        border-radius: 5px;
                        font-size: 14px;
                        border: 1px solid #ddd;
                        '>
                        <strong>Response:</strong> {response}
                    </div>
                """, unsafe_allow_html=True)
                
                # Increase experience points after each interaction
                st.session_state.experience_points += 10  # Increment by 10 points for each chatbot interaction
                   # Option to generate and download the chat history as a PDF
                
        else:
            st.sidebar.warning("Please enter a question!")

    # --- How It Works Section ---

    st.markdown(
        """
        <section class="how-it-works" id="how-it-works" style="color: black;">
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
        """,
        unsafe_allow_html=True
    )

    # --- Contact Section ---
    st.markdown(
        """
        <footer class="contact" id="contact" style="color: black;">
            <h2>Contact Us</h2>
            <p>Have questions? Reach out to us at <a href="mailto:support@futureforge.com" style="color: black;">support@futureforge.com</a>.</p>
        </footer>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
