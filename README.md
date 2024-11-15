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
  - Course Information: Extracted from the Sogang SAINT system. (https://saint.sogang.ac.kr)
  - Major Information: Detailed information about the CSE department. (https://cs.sogang.ac.kr/cs/index_new.html)
  - Guides from Sogang International Office: Resources for international students. (http://oia.sogang.ac.kr/enter/html/main/main.asp)
  - All data should be placed under the Data directory. Process the data into formats like JSON, Markdown (.md), or PDF.
  Process the data into formats like JSON, Markdown (.md), or PDF.
3. **Get API keys**:
  - get openai api key at https://openai.com/index/openai-api/
  - get portkey api key at https://portkey.ai
  - make ```config.json``` file like follow
    ```json
    {
      "API_KEYS": {
        "OPENAI": "",
        "PORTKEY_API_KEY": "",
      }
    }
    ```

## Usage

Here’s an example of how to use the chatbot:
```python
import asyncio
from Chatbot.chatbot import Chatbot

async def main():
    chatbot = Chatbot()
    answer = await chatbot.ainvoke(
      query="hi!",
      session_id="1",
    )
    print(answer)

asyncio.run(main())
```

### Sample Conversations
See the samples directory for example conversations and expected outputs.

## Additional Notes
- Ensure the data files are preprocessed and correctly formatted before uploading them into the Data folder.
- For more advanced usage or integration, consult the codebase documentation.

##Acknowledgments

- Built using LangChain for retrieval and document processing.
- Data preprocessing inspired by official Sogang University resources.