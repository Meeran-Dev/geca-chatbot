from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        with genai.Client() as client:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
                config=genai.types.GenerateContentConfig(
                system_instruction="You are 'GECA-Bot', a friendly, professional, and knowledgeable "
                                    "College Assistant for Govt. College of Engineering, Aurangabad specializing in academic support, "
                                    "campus information and general student inquiries. Keep your answers concise, helpful, "
                                    "and focused on college life and studies. Do not answer questions "
                                    "unrelated to education or general assistance."
            ))
            bot_response = response.text
            return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
