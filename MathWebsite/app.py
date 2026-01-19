# Import necessary modules from Flask for building web applications and handling HTTP requests and responses.
from flask import Flask, render_template, request, jsonify
# Import the OpenAI library for accessing the OpenAI API.
from openai import OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is missing or empty. Check dashboard.")

client = OpenAI(api_key=api_key)


solved = 0.0
attempted = 0.0


app = Flask(__name__, template_folder='templates', static_folder='static')# Initialize a Flask application.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/physics.html', methods=['GET', 'POST'])
def physics():
    if request.method == 'POST':# Extract the topic and number of questions from the form data.


        topic = request.form['topic']

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>

        difficulty = int(request.form['difficulty_level'])

    
        questions = generate_questions("physics", topic, num_questions, difficulty)# Generate questions using the generate_questions function.


        return render_template('physics.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('physics.html', questions=[])# Render the index.html template with an empty list of questions.


@app.route('/chemistry.html', methods=['GET', 'POST'])
def chemistry():
    if request.method == 'POST':# Extract the topic and number of questions from the form data.


        topic = request.form['topic']

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>

        difficulty = int(request.form['difficulty_level'])

    
        questions = generate_questions("chemistry", topic, num_questions, difficulty)# Generate questions using the generate_questions function.


        return render_template('chemistry.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('chemistry.html', questions=[])# Render the index.html template with an empty list of questions.

@app.route('/math.html', methods=['GET', 'POST'])# Define a route for the root URL. It accepts both GET and POST requests.
def math():    # If a POST request is received (i.e., when the user submits the form):


    if request.method == 'POST':# Extract the topic and number of questions from the form data.


        topic = request.form['topic']

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>

        difficulty = int(request.form['difficulty_level'])

    
        questions = generate_questions("math", topic, num_questions, difficulty)# Generate questions using the generate_questions function.


        return render_template('math.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('math.html', questions=[])# Render the index.html template with an empty list of questions.

@app.route('/biology.html', methods=['GET', 'POST'])# Define a route for the root URL. It accepts both GET and POST requests.
def biology():    # If a POST request is received (i.e., when the user submits the form):


    if request.method == 'POST':# Extract the topic and number of questions from the form data.


        topic = request.form['topic']

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>

        difficulty = int(request.form['difficulty_level'])

    
        questions = generate_questions("biology", topic, num_questions, difficulty)# Generate questions using the generate_questions function.


        return render_template('biology.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('biology.html', questions=[])# Render the index.html template with an empty list of questions.

def generate_questions(subject, topic, num_questions, difficulty):# Define a function to generate questions about a given topic using the OpenAI ChatCompletion model.
    try:
        
        response = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "user", "content": f"Create {num_questions} questions about {topic} with grade {difficulty} difficulty. Make it a contest question(uses thinking) not just using formulas. If {topic} is not a part of {subject}, return Please enter a valid topic, which relates to {subject}. However, if the topic is even semi-related, then continue normally. Remove most fluff, and each question should be on a new line. There should be no empty lines. Please don't use any special formatting or symbols including any HTML."}
  ])
        print(difficulty)
# Send a prompt to the OpenAI API asking to generate a specific number of questions about the given topic.
        
        text = response.choices[0].message.content# Extract and return the generated questions from the API response.
        return text.split('\n')
    except Exception as e:

        return [str(e)]# If an error occurs, return the error message.
    print("DHruv has a unibrow")


@app.route('/solve', methods=['POST'])# Define a route for solving questions. It accepts POST requests.
def solve():# Receive the question from the request data.
    
    data = request.json
    question = data["question"]
    try:# Send a prompt to the OpenAI API asking to solve the given question.
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": f"Create a answer to the question {question}. Make the answer one sentence or 2(in simple terminology) if its not a math question. If it is a math question, create a 1-5 step response to the question. Please don't use any special formatting or symbols for all types of questions including any HTML."}
            ])
        
        solution = response.choices[0].message.content# Extract and return the solution from the API response.
        return jsonify({'solution': solution})
    except Exception as e:

        return jsonify({'error': str(e)})# If an error occurs, return the error message.

@app.route('/answer', methods=['POST'])
def checkAnswer():

    data = request.json
    question = data["question"]
    answer = data["answer"]

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": f"Is {answer} the correct answer to {question}? Return a one word answer, either Correct or Incorrect. Even similar answers in terms of step can be considered correct."}
        ]
    )

    answer = response.choices[0].message.content

    # if answer == "Correct":
    #     solved += 1
    
    # attempted += 1

    return jsonify({"answer": answer})

if __name__ == '__main__': # Main execution: Start the Flask application in debug mode if the script is run directly.
    app.run(debug=True)
