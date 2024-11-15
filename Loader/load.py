from langchain_core.documents.base import Document
from Logger.logger import logger
import os
from typing import List
from Loader.read import (
  readJson, readPDF, readMarkdown
)

def loadCourses(data_path) -> List[Document]:
  json_files = []
  for root, _, files in os.walk(data_path):
    for file in files:
      if file.endswith(".json"):
        json_files.append(os.path.join(root, file))
        
  logger.debug(f"Read {len(json_files)} files")
  docs = readJson(json_files, "course")
  return docs
  
def loadMajorInfo(data_path) -> List[Document]:
  pdf_files = []
  md_files = []
  json_files = []
  for root, _, files in os.walk(data_path):
    for file in files:
      if file.endswith(".pdf"):
        pdf_files.append(os.path.join(root, file))
      elif file.endswith(".md"):
        md_files.append(os.path.join(root, file))
      elif file.endswith(".json"):
        json_files.append(os.path.join(root, file))
  
  logger.debug(f"Read {len(json_files)+len(pdf_files)+len(md_files)} files")
  pdf_docs = readPDF(pdf_files)
  md_docs = readMarkdown(md_files)
  json_docs = readJson(json_files, "professor")
  docs = pdf_docs + md_docs + json_docs
  return docs

def loadGuidance(data_path) -> List[Document]:
  pdf_files = []
  md_files = []
  for root, _, files in os.walk(data_path):
    for file in files:
      if file.endswith(".pdf"):
        pdf_files.append(os.path.join(root, file))
      elif file.endswith(".md"):
        md_files.append(os.path.join(root, file))
  
  logger.debug(f"Read {len(pdf_files)+len(md_files)} files")
  pdf_docs = readPDF(pdf_files)
  md_docs = readMarkdown(md_files)
  docs = pdf_docs + md_docs
  return docs