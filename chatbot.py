import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API Key
openai.api_key = "your_openai_api_key"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response_text = ""

    if "summary" in user_message.lower():
        # Extract the topic for summarization
        topic = user_message.lower().replace("summary", "").strip()
        if topic:
            # Call OpenAI API for the summary
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Provide a brief summary about {topic}.",
                max_tokens=150
            )
            response_text = response.choices[0].text.strip()
        else:
            response_text = "Please specify the topic you want summarized."
    else:
        # General chatbot response
        response_text = "I can help with summaries. Try asking: 'Summary of AI in education.'"

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
