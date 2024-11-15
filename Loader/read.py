from langchain_community.document_loaders.pdf import PDFPlumberLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_core.documents.base import Document
from tqdm import tqdm
import json
from Logger.logger import logger
from typing import List, Callable

def readPDF(pdf_files) -> List[Document]:  
  docs = []
  for pdf_path in tqdm(pdf_files, desc="Reading PDFs", unit="file"):
    logger.debug(f"Loading {pdf_path}")
    loader = PDFPlumberLoader(pdf_path)
    doc = loader.load()
    docs.extend(doc)

  return docs

def readJson(json_files, data_type) -> List[Document]:
  parsers = {
    "course": parseCourse,
    "professor": parseProfessor
  }
  parser: Callable[[str], List[Document]] = parsers.get(data_type)
  
  docs = []
  for json_path in tqdm(json_files, desc="Reading JSONs", unit="file"):
    logger.debug(f"Loading {json_path}")
    doc = parser(json_path)
    docs.extend(doc)

  return docs

def readMarkdown(md_files) -> List[Document]:
  docs = []
  for md_path in tqdm(md_files, desc="Reading Markdowns", unit="file"):
    logger.debug(f"Loading {md_path}")
    loader = UnstructuredMarkdownLoader(md_path)
    doc = loader.load()
    docs.extend(doc)

  return docs

def parseProfessor(json_path) -> List[Document]:
  with open(json_path, "r") as f:
    data = json.load(f)
  
  docs = []
  for category, professors in data.get("faculty", {}).items():
    for professor in professors:
      content = professor.get("name", "")
      metadata = {
        key: value for key, value in {
          "specialization": professor.get("specialization"),
          "education": professor.get("education"),
          "lab": professor.get("lab"),
          "email": professor.get("email"),
          "category": category  
        }.items() if value is not None  
      }
      docs.append(Document(page_content=content, metadata=metadata))

  return docs

def parseCourse(json_path) -> List[Document]:
  with open(json_path, "r") as f:
    courses = json.load(f)
  
  docs = []
  for course in courses:
    content = f"{course.get('course_code', '')}-{course.get('section', '')}"
    metadata = {
      key: value for key, value in {
        "major": course.get("major"),
        "course_name": course.get("course_name"),
        "time": course.get("time"),
        "credits": course.get("credits"),
        "professor": course.get("professor"),
        "capacity": course.get("capacity"),
        "english_lecture": course.get("english_lecture"),
        "approval_subject": course.get("approval_subject"),
        "international_students": course.get("international_students"),
        "target": course.get("target"),
        "recommended_grade": course.get("recommended_grade"),
        "reference_notes": course.get("reference_notes"),
        "description": course.get("description"),
        "year": course.get("year"),
        "semester": course.get("semester"),
        "course_code": course.get("course_code"),
        "section": course.get("section"),
        "timetable": course.get("timetable"),
        "room": course.get("room")
      }.items() if value is not None
    }
    
    docs.append(Document(page_content=content, metadata=metadata))
  return docs