from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents.base import Document
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables.base import Runnable

from typing import List
import os
from Logger.logger import logger
from Loader.load import (
  loadCourses, loadGuidance, loadMajorInfo
)

class Retriever:
  def __init__(self, model: ChatOpenAI, data_path: str):
    self.llm = model
    docs = self._load(data_path)
    self.retriever = self._init_retriever(docs)
    
  def get(self):
    return self.retriever
    
  async def ainvoke(self, query):
    docs = await self.retriever.ainvoke(query)
    for d in docs:
      logger.debug(f"{d}")
    return docs
  
  def _init_retriever(self, docs: List[Document]) -> Runnable:
    logger.debug("start to create retriever")
    
    vectorstore = Chroma(
      embedding_function=OpenAIEmbeddings(),
      persist_directory="./cache"
    )
    
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
    pd_retriever = ParentDocumentRetriever(
      vectorstore=vectorstore,
      docstore=InMemoryStore(),
      child_splitter=child_splitter,
      parent_splitter=parent_splitter,
    )
    pd_retriever.add_documents(docs)
    
    llm_chain = self._getLLMchain()
    mq_retriever = MultiQueryRetriever(
      retriever=pd_retriever,
      llm_chain=llm_chain,
      parser_key="lines"
    )
    
    logger.debug("Successfully create retriever")
    return mq_retriever
  
  def _load(self, data_path) -> List[Document]:
    logger.debug("convert raw data to document")
    docs = []
    
    for category in os.listdir(data_path):
      path = os.path.join(data_path, category)
      if category == "courses":
        docs.extend(loadCourses(path))
      elif category == "guidance":
        docs.extend(loadGuidance(path))
      elif category == "major":
        docs.extend(loadMajorInfo(path))
        
    logger.debug(f"Successfully done ({len(docs)})")
    return docs

  def _getLLMchain(self):
    output_parser = LineListOutputParser()
    QUERY_PROMPT = PromptTemplate(
      input_variables=["question"],
      template="""You are an AI language model assistant. Your task is to generate five 
        different versions of the given user question to retrieve relevant documents from a vector 
        database. Generate these alternative questions in both English and Korean to help the user 
        overcome limitations of distance-based similarity search due to mixed-language data.
        Provide these alternative questions separated by newlines.

        Original question (English): {question}
        """,
    )
    llm_chain = QUERY_PROMPT | self.llm | output_parser
    
    return llm_chain
  
class LineListOutputParser(BaseOutputParser[List[str]]):
  """Output parser for a list of lines."""
  def parse(self, text: str) -> List[str]:
    lines = text.strip().split("\n")
    return list(filter(None, lines)) 