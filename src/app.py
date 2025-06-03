from dotenv import load_dotenv
import openai
import os
import random
import sys

# Load the environment variables
load_dotenv()

# Configure the OpenAI client
client = openai.OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv('BASE_URL', 'https://api.openai.com/v1/')
)
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')


def generate_math_question():
    """Generate a math question using the AI model"""
    try:
        # Add a random seed to prevent caching
        random_seed = random.randint(1, 10000)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=1.0,
            messages=[
                {
                    "role": "system",
                    "content": "Generate a simple math question randomly. Provide the question and correct answer in the format: 'QUESTION: <question>\nANSWER: <answer>'"
                },
                {
                    "role": "user",
                    "content": f"Generate a math question. Make it different from previous ones. Random seed: {random_seed}"
                }
            ]
        )

        content = response.choices[0].message.content
        parts = content.split('\n')
        question = parts[0].replace('QUESTION: ', '')
        answer = parts[1].replace('ANSWER: ', '')
        return question, answer
    except Exception as e:
        print(f"Error generating question: {e}")
        sys.exit(1)

def explain_answer(user_answer, correct_answer, question):
    """Get AI explanation for the answer"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "Explain whether the answer is correct and why. Be encouraging and helpful."
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\nCorrect answer: {correct_answer}\nUser's answer: {user_answer}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting explanation: {e}"

def main():
    print(f"Welcome to Math Practice! Using model: {MODEL_NAME}")
    print("Press Enter without input or type '/bye' to exit")

    while True:
        # Generate question
        question, correct_answer = generate_math_question()
        print("\nQuestion:", question)

        # Get user input
        user_input = input("Your answer: ").strip()

        # Check for exit conditions
        if user_input.lower() == '/bye' or user_input == '':
            print("Thanks for practicing! Goodbye!")
            break

        # Get and show explanation
        explanation = explain_answer(user_input, correct_answer, question)
        print("\nFeedback:", explanation)

if __name__ == "__main__":
    main()