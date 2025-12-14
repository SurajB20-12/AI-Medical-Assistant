from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_groq import ChatGroq
from pydantic import SecretStr
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")


def get_llm_chain(retriever):
  llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=SecretStr(GROQ_API_KEY) if GROQ_API_KEY else None,
  )

  prompt=PromptTemplate(
    input_variables=["context","question"],
    template="""
     You are **Medibot**, an AI medical assistant to help users understand medical documents and answer their medical queries.

     Your job is to provide clear,accurate and  helpful responses based on the context provided. 

     **Context:**
      {context}
      **User Question:**
      {question}


      ---
      **Answer**:
      - Respond in a calm, factual, and respectful tone.
      - Use simple explanations when needed.
      - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
      - Do NOT make up facts.
      - Do NOT give medical advice or diagnoses.
      - Keep the answer concise and to the point. 




    """
  )
  return RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True

  )