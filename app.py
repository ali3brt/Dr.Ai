import os

from flask import Flask, render_template, request, jsonify, session
from transformers import BartForConditionalGeneration, BartTokenizer
import torch

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session storage

# Load the fine-tuned BART model and tokenizer
model_path = os.path.join(os.getcwd(), "model", "BART-FineTuned", "Final")
model = BartForConditionalGeneration.from_pretrained(model_path,  use_safetensors=True)
tokenizer = BartTokenizer.from_pretrained(model_path)

# Move model to the appropriate device (GPU if available, otherwise CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


# Route to render the frontend HTML page
@app.route('/')
def index():
    return render_template('index.html')


# Route to generate diagnosis based on symptoms
@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.json.get("message")

    # Retrieve previous symptoms from session (if any)
    symptoms_history = session.get("symptoms_history", "")

    # Add new symptoms to the history
    updated_symptoms = symptoms_history + " " + user_input

    # Store the updated symptoms back in the session
    session["symptoms_history"] = updated_symptoms

    # Generate diagnosis based on the updated symptoms
    diagnosis = generate_diagnosis(updated_symptoms)

    return jsonify({"response": diagnosis})


# Function to generate diagnosis based on symptoms using the model
def generate_diagnosis(symptoms):
    inputs = tokenizer(symptoms, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_length=300)
    diagnosis = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return diagnosis


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
