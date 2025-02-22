# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
from mistralai import Mistral

# def initialize_llm_pipeline(model_name="mistralai/Mistral-7B-Instruct-v0.2"):

#     tokenizer = AutoTokenizer.from_pretrained(model_name)

#     model = AutoModelForCausalLM.from_pretrained(
#         model_name,
#         device_map="auto",
#         # cache_dir="/Users/jitendrakolli/Downloads/Infosys/Project/cache",
#         # load_in_8bit=True  # Enable 8-bit quantization if needed
#     )


#     llm_pipeline = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         device_map="auto",
#         batch_size=1
#     )

#     return llm_pipeline

def summarize_table( table_text, max_new_tokens=100, num_return_sequences=1):
   
    prompt = (
        "Summarize the following table data:\n\n" 
        f"{table_text}\n\n"
        "Provide a concise summary of the key points."
    )

    # response = llm_pipeline(prompt, max_new_tokens=max_new_tokens, num_return_sequences=num_return_sequences) #Use This if you run LLM model locally
    # summary = response[0]['generated_text']

    api_key = "MMNlnPxuMxBfeIGG4pIGIfSwBdIgjlVA" #use this if you want to run LLM model with

    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )

    return chat_response.choices[0].message.content
    # return summary

