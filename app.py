import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API Key here
openai.api_key = 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  # Replace with your OpenAI key

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response_text = ""

    if "summary" in user_message.lower():
        # Extract the topic for summarization
        topic = user_message.lower().replace("summary", "").strip()
        if topic:
            # Request OpenAI API for summarization
            response = openai.Completion.create(
                engine="text-davinci-003",  # You can change to another engine if required
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
