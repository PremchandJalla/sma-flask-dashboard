import openai

def generate_insight(prompt, api_key):
    """
    Generates an insight based on the provided prompt using NVIDIA's Mistral model.
    """
    # Initialize OpenAI client with NVIDIA API settings
    client = openai.OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    # Request completion from the Mistral model
    completion = client.chat.completions.create(
        model="mistralai/mixtral-8x22b-instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=False
    )

    # Correctly access and return the generated content
    # Access message content as an attribute instead of subscripting
    return completion.choices[0].message.content