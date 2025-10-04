import os
from dotenv import find_dotenv, load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents.agent_types import AgentType
from pypdf import PdfReader

import pandas as pd
import re



load_dotenv(find_dotenv())
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    print("API Key loaded successfully.")
else: 
    print("Failed to load API Key.")

llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-4",
)


def get_pdf_text(pdf_doc):

    pdf_reader = PdfReader(pdf_doc)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extracted_data(pages_data):
    template = """
    Extract the following information from the bill text: Invoice ID,
    Description, Issue Date, Unit Price, Amount, Bill for, From and Terms
    from {pages}

    Expected output format: Remove any currency symbols 
    {{'Invoice ID': '', 'Description': '', 'Issue Date': '', 'Unit Price': '', 'Amount': '', 'Bill for': '', 'From': '', 'Terms': ''}}
    """

    prompt = PromptTemplate(
        input_variables=["pages"],
        template=template,
    )
    
    response = llm.invoke(prompt.format(pages=pages_data))

    return response

def create_docs(user_pdf_list):
    df = pd.DataFrame({
        'Invoice ID': pd.Series(dtype='int'),
        'Description': pd.Series(dtype='str'),
        'Issue Date': pd.Series(dtype='str'),
        'Unit Price': pd.Series(dtype='float'),
        'Amount': pd.Series(dtype='float'),
        'Bill for': pd.Series(dtype='str'),
        'From': pd.Series(dtype='str'),
        'Terms': pd.Series(dtype='str')
    })

    for pdf in user_pdf_list:
        pdf_text = get_pdf_text(pdf)
        
        llm_extracted_data = extracted_data(pdf_text)

        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data.content, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            data_dict = eval('{' + extracted_text + '}')
            print(data_dict)
        else:
            print("No match found in the LLM response.")
            
        df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)

        print("DONE")

    df.head()
    return df