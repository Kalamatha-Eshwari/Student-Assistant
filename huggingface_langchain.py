# -*- coding: utf-8 -*-
"""HuggingFace-LangChain.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Wc8wXTCIeConDXqexOs3o52QeBi16KmK
"""

!pip install langchain-huggingface

!pip install huggingface_hub
!pip install transformers
!pip install accelerate
!pip install bitsandbytes
!pip install langchain

from google.colab import userdata
sec_key=userdata.get("HF_TOKEN")
print(sec_key)

from langchain_huggingface import HuggingFaceEndpoint

from google.colab import userdata
sec_key=userdata.get("HUGGINGFACEHUB_API_TOKEN")
print(sec_key)

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = sec_key

repo_id="mistralai/Mistral-7B-Instruct-v0.2"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=sec_key)

llm

llm.invoke("what is generative ai")

repo_id="mistralai/Mistral-7B-Instruct-v0.3"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=sec_key)

llm.invoke("what is generative ai")

"""RAG
Retrival Augmented Generation

"""

from langchain import PromptTemplate,LLMChain
question="who is prime minister  of India in 2018? "
template="""Question:{question}
Answer: Let's think step by step"""
prompt=PromptTemplate(template=template,input_variables=["question"])
print(prompt)

llm_chain=LLMChain(prompt=prompt,llm=llm)
print(llm_chain.invoke(question))

repo_id="openai-community/gpt2"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=sec_key)

llm.invoke("what is generative ai")

from langchain_huggingface import HuggingFaceEndpoint
from langchain import PromptTemplate, LLMChain

# Set your Hugging Face API token
sec_key = 'YOUR_HUGGINGFACEHUB_API_TOKEN'  # Replace with your actual API token

# Define the models
qa_repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
summarization_repo_id = "mistralai/Mistral-7B-Instruct-v0.3"  # Replace with a model suited for summarization if available
generation_repo_id = "mistralai/Mistral-7B-Instruct-v0.3"  # Updated model

# Initialize models
qa_llm = HuggingFaceEndpoint(
    repo_id=qa_repo_id,
    token=sec_key
)

summarization_llm = HuggingFaceEndpoint(
    repo_id=summarization_repo_id,
    token=sec_key
)

generation_llm = HuggingFaceEndpoint(
    repo_id=generation_repo_id,
    token=sec_key
)

# Define prompt templates
qa_prompt = PromptTemplate(
    template="Question: {question}\nAnswer: Let's find the answer.",
    input_variables=["question"]
)

summary_prompt = PromptTemplate(
    template="Summarize the following text:\n{text}",
    input_variables=["text"]
)

generation_prompt = PromptTemplate(
    template="""Generate a set of practice problems for the following math topic:

    Topic: {topic}
    Questions:
    """,
    input_variables=["topic"]
)

# Initialize LLM chains
qa_chain = LLMChain(prompt=qa_prompt, llm=qa_llm)
summary_chain = LLMChain(prompt=summary_prompt, llm=summarization_llm)
generation_chain = LLMChain(prompt=generation_prompt, llm=generation_llm)

def truncate_summary(text, word_limit=50):
    """Truncate text to a specified number of words."""
    words = text.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return text

def main():
    while True:
        print("\nPersonalized Study Assistant")
        print("1. Question Answering")
        print("2. Text Summarization")
        print("3. Practice Problems Generation")
        print("4. Exit")

        choice = input("Select an option (1/2/3/4): ").strip()

        if choice == '1':
            question = input("Enter your question: ").strip()
            if question:
                try:
                    answer_response = qa_chain.invoke({"question": question})
                    answer = answer_response.get("text", "No answer available.")
                    print(f"Answer: {answer}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("No question entered.")

        elif choice == '2':
            text = input("Paste the text you want to summarize: ").strip()
            if text:
                try:
                    summary_response = summary_chain.invoke({"text": text})
                    summary = summary_response.get("text", "No summary available.")
                    truncated_summary = truncate_summary(summary, word_limit=50)
                    print(f"Summary: {truncated_summary}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("No text entered.")

        elif choice == '3':
            topic = input("Enter a topic for practice problems: ").strip()
            if topic:
                try:
                    problems_response = generation_chain.invoke({"topic": topic})
                    problems = problems_response.get("text", "No practice problems available.")
                    print("Practice Problems:")
                    # Print each problem in a clear, numbered format
                    for i, line in enumerate(problems.split('\n')):
                        if line.strip():  # Avoid printing empty lines
                            print(f"{i + 1}. {line.strip()}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("No topic entered.")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()