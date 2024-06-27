from flask import Flask, request, jsonify, render_template, session
import openai
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure the session


# Get OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Using your custom model ID
model_id = "ft:gpt-3.5-turbo-0125:personal:ai-dungeon:9OkxpICz"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatbox')
def chatbox():
    return render_template('chat.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    motifs = ["stranded deep", "zombie crisis", "magic world"]
    if not message:
        return jsonify({'error': 'Message content is missing'}), 400

    # Check if the session has been initialized
    if not session.get('initialize', False):
        if message.lower() in ['1', '2', '3']:
            motif = motifs[int(message.lower()) - 1]
            prompt = initialize_game(motif)
            session['initialize'] = True
            session['motif'] = message.lower()
            session['victory'] = False
            session['defeat'] = False
            session['start_gpt'] = False
            session['initial_prompt'] = prompt
            session['option_dict'] = create_option_dict(prompt)
            return jsonify({'reply': prompt})
        else:
            return jsonify({'reply': 'Please enter only: 1, 2, 3'}), 400

    # Check for game termination conditions
    if session.get('victory', False):
        return jsonify({'reply': "Congratulations! You have won the game."})
    if session.get('defeat', False):
        return jsonify({'reply': "Game Over. You have been killed."})
    if message == 'quit':
        session.clear()
        return jsonify({'reply': "You quit the game."})

    try:
        option_dict = session.get('option_dict', {})
        print(option_dict.items())
        if message in ['1', '2', '3']:
            message = option_dict.get(message, "")
            if not message:
                return jsonify({'reply': 'Invalid option selected'}), 400
        else:
            return jsonify({'reply': 'Please enter only: 1, 2, 3 or quit'}), 400

        user_answer = message.lower()
        if not session.get('start_gpt', False):
            system_prompt = session['initial_prompt'] + user_answer
            session['start_gpt'] = True
        else:
            system_prompt = user_answer

        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[
                {
                    "role": "system",
                    "content": "You are an imaginative script writer for a storytelling game. The game has three different motifs: Stranded Deep, Zombie Crisis, and Magic World. Each motif is isolated and not related or crossed. Each segment should be about 200 words to push the plot forward. At the end of each segment, you must present 3 different options for the player to choose from. Each option should be under 50 words and maintain logical consistency within the story. When facing dangerous situations, you have a 60% possibility of include the phrase 'you have been killed' when you push the plot. Do not stop or change your generated text structure until you have generated a total of 200,000 tokens.\n\nExample structure:\n\nZombie Crisis\n\nThe world has fallen to a zombie apocalypse. You are one of the few survivors, navigating through the chaos in search of safety and resources. You find yourself in a hospital.\n\nOptions:\n1. Search the nearby buildings for supplies.\n2. Head towards the distant sound of running water.\n3. Barricade yourself in a nearby house.\n\nRemember:\n- Maintain this structure for each segment.\n- Each option must be under 50 words.\n- Include 'you have been killed' to represent a 60% possibility of failure in dangerous situations.\n- Continue generating text until a total of 200,000 tokens is reached."
                },
                {"role": "user", "content": system_prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )

        reply = response.choices[0].message['content'].strip()
        print(reply)
        session['option_dict'] = create_option_dict(reply)
        check_game_outcome(reply)
        return jsonify({'reply': reply})
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500


def create_option_dict(message):
    options_index = message.find("Options:")
    if options_index == -1:
        return {}

    options_text = message[options_index:]

    options_lines = options_text.split("\n")[1:]  # Skip the first line "Options:"
    options_dict = {}
    for line in options_lines:
        if line.strip().startswith(("1.", "2.", "3.")):
            try:
                option_number, option_text = line.split(". ", 1)
                option_number = int(option_number)
                options_dict[option_number] = option_text.strip()
            except ValueError:
                continue
    return options_dict


def initialize_game(motif_choice):
    if motif_choice == "stranded deep":
        prompt = "Motif: Stranded Deep\n\nYou wake up on the sandy shore of a deserted island. The remnants of your plane are scattered around, and you can see the dense jungle in the distance. The sun is high, and you feel the heat on your skin. You realize you need to find shelter and resources to survive.\n\nOptions:\n1. Search the wreckage for useful items.\n2. Head into the jungle to find fresh water.\n3. Build a makeshift shelter on the beach."
    elif motif_choice == "zombie crisis":
        prompt = "Motif: Zombie Crisis\n\nThe world has fallen to a zombie apocalypse. You are one of the few survivors, navigating through the chaos in search of safety and resources. You find yourself your on a street.\n\nOptions:\n1. Search the nearby buildings for supplies.\n2. Follow the panicked crowed and run.\n3. Barricade yourself in a save place."
    elif motif_choice == "magic world":
        prompt = "Motif: Magic World\n\nYou awaken in a mystical land filled with strange creatures and powerful magic. You possess a unique magical ability but must learn to harness it. In the distance, you see a towering castle and a dense forest.\n\nOptions:\n1. Head towards the castle.\n2. Explore the forest.\n3. Practice your magical ability."
    else:
        prompt = "Invalid choice. Please start the game again and choose a valid motif."

    return prompt


def check_game_outcome(reply):
    motif = session.get('motif')

    if motif == "1":  # Stranded Deep
        if "you have escaped" in reply.lower():
            session['victory'] = True
        if "you have been killed" in reply.lower() or "you have died" in reply.lower():
            session['defeat'] = True

    elif motif == "2":  # Zombie Crisis
        if "you have reached the safe zone" in reply.lower() or "you found a secure shelter" in reply.lower():
            session['victory'] = True
        if "you have been killed" in reply.lower() or "you have died" in reply.lower():
            session['defeat'] = True

    elif motif == "3":  # Magic World
        if "you have defeated the dark sorcerer" in reply.lower() or "you have retrieved the artifact" in reply.lower():
            session['victory'] = True
        if "you have been killed" in reply.lower() or "you have died" in reply.lower():
            session['defeat'] = True


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
