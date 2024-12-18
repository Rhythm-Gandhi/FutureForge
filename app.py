import streamlit as st
import os
import time
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Access the API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    raise ValueError("API Key is missing in the environment variables")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)
chat_session = model.start_chat(
    history=[]
)

# --- Function to Get Response from Chatbot ---
def get_response(user_message):
    try:
        # Send message to the chat session
        response = chat_session.send_message(user_message)  # Use the chat_session's send_message method
        return response.text  # Return the response text
    except Exception as e:
        return f"Error: {str(e)}"

# --- Page Configuration ---
st.set_page_config(page_title="Future Forge", layout="wide")

# --- Load CSS Styling ---
def load_css():
    with open("static/styles.css", "r") as css_file:
        css = f"<style>{css_file.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# --- Initialize Session State ---
def initialize_session_state():
    if 'user_level' not in st.session_state:
        st.session_state.user_level = 1
    if 'experience_points' not in st.session_state:
        st.session_state.experience_points = 0
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "Adventurer"
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chosen_character' not in st.session_state:
        st.session_state.chosen_character = None
    if 'nickname' not in st.session_state:
        st.session_state.nickname = None
    if 'education_level' not in st.session_state:
        st.session_state.education_level = None
    if 'work_status' not in st.session_state:
        st.session_state.work_status = None
    if 'industry' not in st.session_state:
        st.session_state.industry = None
    if 'career_goals' not in st.session_state:
        st.session_state.career_goals = None
    if 'skills' not in st.session_state:
        st.session_state.skills = None
    if 'learning_modes' not in st.session_state:
        st.session_state.learning_modes = None

# --- Character Avatar Based on Level ---
def get_character_avatar(level, chosen_character):
    avatar_mapping = {
        "Cool Guy": {
            1: "static/images/avatar_level_1.png",
            2: "static/images/avatar_level_2.png",
            3: "static/images/avatar_level_3.png",
            4: "static/images/avatar_level_4.png",
        },
        "Cute Girl": {
            1: "static/images/avatar_level_1_character_2.png",
            2: "static/images/avatar_level_2_character_2.png",
            3: "static/images/avatar_level_3_character_2.png",
            4: "static/images/avatar_level_4_character_2.png",
        },
        "Fierce Dragon": {
            1: "static/images/avatar_level_1_character_3.png",
            2: "static/images/avatar_level_2_character_3.png",
            3: "static/images/avatar_level_3_character_3.png",
            4: "static/images/avatar_level_4_character_2.png",
        },
    }
    return avatar_mapping.get(chosen_character, avatar_mapping["Cool Guy"]).get(level, "static/images/avatar_level_1.png")

# --- Upgrade User Character ---
def upgrade_character():
    if 'experience_points' in st.session_state and st.session_state.experience_points >= 100 * st.session_state.user_level:
        st.session_state.user_level += 1
        st.session_state.experience_points = 0
        return f"Congratulations! You've leveled up to level {st.session_state.user_level}!"
    return None

# --- Streamlit App ---
def main():
    
    # Load CSS
    load_css()

    # Initialize Session State
    initialize_session_state()

# --- Character Selection Section ---
if not st.session_state.get('chosen_character'):
    st.title("Welcome to Future Forge!")
    st.write("Select your character to begin:")

    # Define character options and their images
    characters = {
        "Cool Guy": "static/images/avatar_level_1.png",
        "Cute Girl": "static/images/avatar_level_1_character_2.png",
        "Fierce Dragon": "static/images/avatar_level_1_character_3.png"
    }

    # Display character options as clickable buttons with images
    col1, col2, col3 = st.columns(3)  # Create three columns for layout
    with col1:
        if st.button("Cool Guy"):
            st.session_state.chosen_character = "Cool Guy"
    with col2:
        if st.button("Cute Girl"):
            st.session_state.chosen_character = "Cute Girl"
    with col3:
        if st.button("Fierce Dragon"):
            st.session_state.chosen_character = "Fierce Dragon"

    # Display character images in columns
    col1.image(characters["Cool Guy"], use_column_width=True)
    col2.image(characters["Cute Girl"], use_column_width=True)
    col3.image(characters["Fierce Dragon"], use_column_width=True)

    # Provide feedback if a character is chosen
    if st.session_state.get('chosen_character'):
        st.success(f"You have chosen: {st.session_state.chosen_character}!")
        st.experimental_rerun()  # Rerun to refresh the session state

# --- Nickname Input Section ---
if st.session_state.get('chosen_character') and not st.session_state.get('nickname'):
    st.title("Personalize Your Character")
    st.write(f"You have selected **{st.session_state.chosen_character}**. Now, give your character a nickname to proceed!")

    # Input field for nickname
    nickname_input = st.text_input("Enter your character's nickname:", placeholder="Enter a nickname")

    # Button to confirm nickname
    if st.button("Confirm Nickname"):
        if nickname_input.strip():
            st.session_state.nickname = nickname_input.strip()
            st.success(f"Welcome, {st.session_state.nickname} the {st.session_state.chosen_character}!")
            st.experimental_rerun()  # Refresh to update the session
        else:
            st.warning("Please provide a valid nickname to continue.")

# --- Continue to Main App After Character and Nickname Selection ---
if st.session_state.get('chosen_character') and st.session_state.get('nickname'):
    st.title(f"Welcome {st.session_state.nickname}!")
    st.write(f"Your journey as **{st.session_state.chosen_character}** begins now. 🎉")
    # The rest of the app's features can be implemented here


    # --- Post Character Selection: Collect Career Information ---
    if st.session_state.get('chosen_character') and st.session_state.get('nickname'):
        st.title(f"Welcome {st.session_state.nickname}!")

        # Collect user career-related data
        st.write("Please answer the following questions to help us provide you with a tailored roadmap:")

        # 1. Education Level
        st.session_state.education_level = st.selectbox(
            "What is your current education level?",
            ["High school diploma", "Undergraduate degree", "Graduate degree", "Other (please specify)"]
        )

        # 2. Work Status
        st.session_state.work_status = st.selectbox(
            "What is your current work status?",
            ["Employed full-time", "Employed part-time", "Unemployed", "Student", "Freelance/self-employed"]
        )

        # 3. Industry Interest
        st.session_state.industry = st.selectbox(
            "What industry are you interested in?",
            ["Technology/IT", "Business/Finance", "Creative Arts/Design", "Healthcare", "Engineering", "Other (please specify)"]
        )

        # 4. Career Goals
        st.session_state.career_goals = st.selectbox(
            "What are your career goals?",
            ["Start my own business", "Climb the corporate ladder", "Change industry", "Transition into a different role", "Advance in my current field", "Other (please specify)"]
        )

        # 5. Skills
        st.session_state.skills = st.selectbox(
            "What skills do you currently have?",
            ["Technical skills (programming, data analysis, etc.)", "Soft skills (communication, leadership, etc.)", "Creative skills (design, writing, etc.)", "None yet"]
        )

        # 6. Learning Modes
        st.session_state.learning_modes = st.selectbox(
            "What are your preferred learning modes?",
            ["Online courses", "In-person classes", "Blended learning (a mix of online and in-person)", "Self-paced learning"]
        )

        # Button to generate roadmap
        if st.button("Generate Roadmap"):
            # Create a personalized roadmap message
            roadmap_message = f"""
            Based on your responses, here is your personalized roadmap:

            **Education Level:** {st.session_state.education_level}
            **Work Status:** {st.session_state.work_status}
            **Industry Interest:** {st.session_state.industry}
            **Career Goals:** {st.session_state.career_goals}
            **Current Skills:** {st.session_state.skills}
            **Preferred Learning Mode:** {st.session_state.learning_modes}
            
            Based on this information, Forge Lord will now suggest a step-by-step career path including potential exams or certifications.
            """
            st.write(roadmap_message)
            response = get_response(roadmap_message)
            # Responses will now appear in the sidebar only, not in the main section.
            st.sidebar.write(f"**Forge Lord Response:** {response}")

        # --- Chatbot in Sidebar ---
        st.sidebar.title(f"Chat with Forge Lord 🤖 (Level {st.session_state.user_level})")

        # Display Character Avatar in Sidebar
        avatar_url = get_character_avatar(st.session_state.user_level, st.session_state.chosen_character)
        st.sidebar.image(avatar_url, width=100)

        st.sidebar.markdown(
            "Ask Forge Lord anything related to your career goals, summaries, or topics of interest!",
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
                        color: black; 
                        padding: 10px; 
                        border-radius: 5px;
                        font-size: 14px;
                        border: 1px solid #ddd;
                        '>
                        <strong>Response:</strong> {response}
                    </div>
                    """, unsafe_allow_html=True)

                    # Increase experience points after each interaction
                    st.session_state.experience_points += 10

                    # Store chat history
                    st.session_state.chat_history.append((user_input, response))

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
