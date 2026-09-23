# FutureForge

FutureForge is an AI-powered career guidance platform designed to help users turn broad career goals into structured, personalized learning roadmaps.

The platform uses a concise onboarding flow to understand a user’s education level, current work status, industry interests, career goals, existing skills, and preferred learning style. It then uses Google Gemini to generate a tailored career roadmap and provides an interactive AI career assistant for continued guidance.

FutureForge also adds gamification through selectable avatars, XP-based progression, level upgrades, and milestone-driven learning to make career planning more engaging.

---

## Features

### Personalized Career Roadmaps
FutureForge collects a focused set of user preferences and generates a personalized roadmap based on:

- Education level
- Current work status
- Industry interests
- Career goals
- Existing skills
- Preferred learning mode

The roadmap is generated dynamically using the Gemini API.

### AI Career Assistant

The built-in assistant, **Forge Lord**, allows users to ask questions related to:

- Career paths
- Learning strategies
- Skill development
- Career transitions
- General career guidance

The assistant is integrated directly into the application through Google Gemini.

### Gamified Progression

FutureForge introduces a lightweight gamification layer to make the experience more interactive.

Users can:

- Select a character avatar
- Choose a nickname
- Earn experience points through interaction
- Progress through different levels
- See their avatar evolve as they advance

### Personalized User Experience

The application maintains user-specific state throughout the session, including:

- Selected character
- Nickname
- Career preferences
- Experience points
- Current level
- Chat history

### Curated Learning Resources

The platform also provides access to learning resources that complement the personalized career roadmap.

---

## Tech Stack

### Backend and AI
- Python
- Google Gemini API
- Google Generative AI SDK

### Application Framework
- Streamlit

### Supporting Technologies
- Flask
- HTML
- CSS
- Python Dotenv

### AI Model
- Gemini 2.0 Flash

---

## How It Works

1. **Choose your character**
   - Select an avatar and personalize it with a nickname.

2. **Complete the career questionnaire**
   - Provide information about your education, goals, interests, skills, and preferred learning approach.

3. **Generate your roadmap**
   - FutureForge sends the collected context to Gemini and generates a personalized career development plan.

4. **Interact with Forge Lord**
   - Ask follow-up questions and receive AI-powered career guidance.

5. **Progress through the experience**
   - Earn XP through interactions and advance your character level over time.

---

## Project Architecture

```text
FutureForge
│
├── app.py
│   ├── Streamlit application
│   ├── Gemini integration
│   ├── Career questionnaire
│   ├── Personalized roadmap generation
│   ├── Avatar system
│   ├── XP and level progression
│   └── AI assistant
│
├── chatbot.py
│   └── Flask-based chatbot implementation
│
├── index.html
├── chatbot.html
├── login.html
├── signup.html
├── style.css
├── requirements.txt
└── assets / images
