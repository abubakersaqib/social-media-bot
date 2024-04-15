import json
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI and Flask application
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__, static_folder='frontend1', static_url_path='')
CORS(app, supports_credentials=True)

@app.route('/')
def home():
    # Serve the static HTML file for the chat interface
    return send_from_directory('frontend1', 'chat.html')

@app.route('/start', methods=['GET'])
def start():
    # Example initialization logic (logging, setting flags, etc.)
    print("Conversation started")
    return jsonify({'message': 'Conversation started successfully'})

def create_response(user_input):
    """Generate a response using OpenAI's chat API based on user input with embedded instructions."""
    instructions = """
    
    Objective: Transform your online presence with dynamic, visually captivating content designed to deeply engage and interact with your audience, using rich language and strategic link integration for enhanced connectivity and interaction.

    Input Format:
    Detail your content needs with descriptions or URLs, such as 'Write website copy for a new energy drink called Rush, made from green tea' or 'Instagram post for https://example.com/product.'
    Tone: Define the desired tone (e.g., Exciting, Professional, Friendly).
    Audience: Identify your target audience (Health-conscious individuals, Busy professionals, Athletes).
    Keywords: Include specific keywords to be highlighted (Energy boost, Green tea, Natural ingredients).
    Link Incorporation Preference: Specify if including direct links for further info is preferred or if highlighting key details is more desirable.

    Output Strategy:
    Kick off with an eye-catching introduction designed to immediately draw in your target audience.
    Craft content using vibrant language and actionable phrases. If links are preferred, integrate them seamlessly; otherwise, focus on highlighting key product benefits and reasons to buy, presented in bullet points for easy reading and visual appeal.
    Benefits of the Product: Highlight the unique advantages of your product, such as its health benefits, eco-friendliness, or innovative features.
    Why to Buy: Clearly articulate compelling reasons for purchase, like superior quality, affordability, or the positive impact of using the product.
    Conclude with an impactful call to action, encouraging your audience to engage, give feedback, or make a purchase.

    Optimization Tips:
    Emphasize visual elements, including emojis and imagery, to grab attention.
    Leverage hashtags and mentions to increase visibility and foster community engagement.
    A clear, direct call to action should be present in each content piece, guiding your audience on what step to take next.
    
    """
    try:
        # Using the correct endpoint for chat models
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1500
        )
        # Extract the text of the response
        return response.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)



@app.route("/chat", methods=["POST"])
@cross_origin(supports_credentials=True)
def chat():
    data = request.json
    user_input = data.get("message", "")

    # Generate response using the create_response function
    response_text = create_response(user_input)

    # Optionally save the response for tracking or logging
    response_data = {'input': user_input, 'response': response_text}
    with open('response_log.json', 'w') as json_file:
        json.dump(response_data, json_file)

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
