from openai import OpenAI

client = OpenAI(
    base_url='http://host.docker.internal:11434/v1',
    api_key='ollama',  # required, but unused
)

def get_llm_response(prompt):
    """
    Sends a prompt to the LLM and gets a response, expecting True or False.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-oss:20b",  # default model
            messages=[
                {"role": "system", "content": "You are a reseller evaluating listings. "
                "Tech items are consumer and personal electronics like computers, phones, and audio equipment (e.g., speakers, headphones). "
                "This does not include home appliances (like fans or blenders), cars, or furniture. "
                "You must respond with only 'True' or 'False'."},
                {"role": "user", "content": prompt}
            ],
        )
        response_text = response.choices[0].message.content.strip().lower()
        if response_text == 'true':
            return True
        elif response_text == 'false':
            return False
        else:
            # Handle cases where the model doesn't follow instructions
            print(f"Warning: Model returned an unexpected value: {response.choices[0].message.content}")
            return None # Or some other default/error handling
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    user_prompt = "Is lagos the capital of Nigeria?"
    llm_response = get_llm_response(user_prompt)

    if llm_response is not None:
        print(f"User Prompt: {user_prompt}")
        print(f"LLM Response: {llm_response}")
