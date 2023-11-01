import openai

# Set up your OpenAI API key.
openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_suggested_answer(question_text):
    """
    Queries the OpenAI API for a suggested answer to a given question.
    
    Args:
    - question_text (str): The question to get an answer for.

    Returns:
    - str: The suggested answer.
    """
    response = openai.Completion.create(
      engine="davinci",
      prompt=f"Given the job application question '{question_text}', what would be an appropriate answer?",
      max_tokens=50  # adjust as needed
    )
    return response.choices[0].text.strip()
