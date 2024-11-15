# Chatbot Assistance for International Students in Sogang University (Seoul, Korea)

## Description
This chatbot is designed to assist international students at Sogang University, specifically freshmen majoring in Computer Science and Engineering in 2024. Due to time and resource limitations, the target audience is limited to this group. The chatbot provides guidance and information sourced from the Sogang University website.

## Features
- **Course Recommendation**: Helps students select appropriate courses.
- **Advice on School Life**: Offers tips for adapting to university life.
- **General Chatbot Assistance**: Provides answers to other general queries.

## Installation

1. **Install Dependencies**:
   Run the following command to install all required libraries:
   ```bash
   pip install -r requirements.txt
2. **Upload Data**: Prepare and upload the necessary data into the Data folder. This includes:
  - Course Information: Extracted from the Sogang SAINT system.
  - Major Information: Detailed information about the CSE department.
  - Guides from Sogang International Office: Resources for international students.
  Process the data into formats like JSON, Markdown (.md), or PDF.

## Usage

Here’s an example of how to use the chatbot:
```python
import asyncio
from Chatbot.chatbot import Chatbot

async def main():
    chatbot = Chatbot()
    answer = await chatbot.ainvoke("hi!")
    print(answer)

asyncio.run(main())
```

### Sample Conversations
See the samples directory for example conversations and expected outputs.

## Additional Notes
- Ensure the data files are preprocessed and correctly formatted before uploading them into the Data folder.
- For more advanced usage or integration, consult the codebase documentation.