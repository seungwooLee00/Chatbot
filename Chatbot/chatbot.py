from langchain_core.messages import (
  AIMessage, 
  HumanMessage, 
  BaseMessage,
)
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

from typing_extensions import Annotated, TypedDict
from typing import Sequence
from Logger.logger import logger
from Retriever.retriever import Retriever
import json, os, sys

class State(TypedDict):
  input: str
  chat_history: Annotated[Sequence[BaseMessage], add_messages]
  context: str
  answer: str

class Chatbot:
  def __init__(self):
    logger.debug("Initializing Chatbot")
    
    self.retrievalModel, self.chatbotModel = self._init_model()
    self.memory = MemorySaver()
    
    retriever_instance = Retriever(self.retrievalModel, "./Data")
    self.retriever = retriever_instance.get()
    self.rag_chain = self._create_rag_chain()
    
    workflow = StateGraph(state_schema=State)
    workflow.add_node("model", self._call_model)
    workflow.add_edge(START, "model")
    self.app = workflow.compile(checkpointer=self.memory)

    logger.debug("Chatbot initialized")
  
  async def ainvoke(self, query, session_id):
    result = await self.app.ainvoke(
      {
        "input": query,
        "chat_history": []
      },
      config={"configurable": {"thread_id": session_id}},
    )
    return result["answer"]
    
  async def _call_model(self, state: State):
    response = await self.rag_chain.ainvoke(state)
    return {
      "chat_history": [
        HumanMessage(content=state["input"]),
        AIMessage(content=response["answer"]),
      ],
      "context": response["context"],
      "answer": response["answer"]
    }
  
  def _create_rag_chain(self):
    contextual_q_system_prompt = (
      "Given a chat history and the latest user question "
      "which might reference context in the chat history, "
      "formulate a standalone question which can be understood "
      "without the chat history. Do NOT answer the question, "
      "just reformulate it if needed and otherwise return it as is."
    )
    contextual_q_prompt = ChatPromptTemplate.from_messages([
      ("system", contextual_q_system_prompt),
      MessagesPlaceholder("chat_history"),
      ("human", "{input}")
    ])
    history_aware_retriever = create_history_aware_retriever(
      self.chatbotModel, self.retriever, contextual_q_prompt
    )

    system_prompt = """
      You are a supportive and friendly assistant dedicated to helping foreign students adapt to university life. 
      Your goal is to provide clear, accurate, and actionable information about academic guidance, campus resources, 
      and general advice. Always respond in a concise and positive tone, tailoring your answers to the user’s needs. 

      Answer the user's questions using the context provided below. If the context lacks sufficient information, 
      do not speculate or provide inaccurate answers. Instead, politely say, "I don't know," and, if possible, 
      suggest how the user might find the required information.

      <context>
      {context}
      </context>
    """
    qa_prompt = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      MessagesPlaceholder("chat_history"),
      ("human", "{input}")
    ])
    qa_chain = create_stuff_documents_chain(self.chatbotModel, qa_prompt)
    
    return create_retrieval_chain(history_aware_retriever, qa_chain)

  def _init_model(self) -> tuple[ChatOpenAI, ChatOpenAI]:
    try:
      sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
      with open("config.json", 'r') as f:
        config = json.load(f)
    except Exception as e:
      logger.debug(e)
      
    OPENAI_API_KEY = config['API_KEYS']['OPENAI']
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
    PORTKEY_API_KEY = config['API_KEYS']['PORTKEY_API_KEY']
    TRACE_ID = "retriever"
    portkey_headers = createHeaders(
      api_key=PORTKEY_API_KEY, provider="openai", trace_id=TRACE_ID
    )
    retrievalModel = ChatOpenAI(
      base_url=PORTKEY_GATEWAY_URL,
      default_headers=portkey_headers,
      model="gpt-4o-mini",
      temperature=0.3
    )
    
    TRACE_ID = "chatbot"
    portkey_headers = createHeaders(
      api_key=PORTKEY_API_KEY, provider="openai", trace_id=TRACE_ID
    )
    chatbotModel = ChatOpenAI(
      base_url=PORTKEY_GATEWAY_URL,
      default_headers=portkey_headers,
      model="gpt-4o",
      temperature=0.5
    )
    
    return retrievalModel, chatbotModel
    