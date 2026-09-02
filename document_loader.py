import os
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("USER_AGENT", "langchain-jawad/1.0")

from langchain_community.document_loaders import TextLoader, WebBaseLoader, WikipediaLoader
from pypdf import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from config.llm_config import llm

TXT_FILE_PATH = "agentic_data/mytext.txt"
loader = TextLoader(TXT_FILE_PATH)

text = loader.load()

print(len(text))
print(text)


PDF_FILE_PATH = "agentic_data/history_book.pdf"
# loader = PdfReader(PDF_FILE_PATH)
loader = PyPDFLoader(PDF_FILE_PATH)

pages = loader.load()

print(len(pages))
print(pages[0].page_content[:500])

print("============\nPAGE 1 CONTENT HERE  (LIMITED TO 100 CHARs):\n============\n")
# print(pages[0].extract_text())
print(pages[0].page_content[:100])
print("============\nPAGE 3 CONTENT HERE (LIMITED TO 100 CHARs):\n============\n")
print(pages[2].page_content[:100])

# url = "https://www.jawadamin.com"
# # url = "https://www.forwardsols.com/"
# loader = WebBaseLoader(web_path=url)
# web_doc = loader.load()
# print("============\nWEB:\n============\n")
# print(len(web_doc[0].page_content))
# print("Number of documents:", len(web_doc))
# print("\nMetadata:")
# print(web_doc[0].metadata)
# print("\nContent preview:")
#
# print(web_doc[0].page_content[:1000].strip())


loader = WikipediaLoader(
    query="Python Development",
    lang="en",
    load_max_docs=2
)

try:
    pages = loader.load()
    print(len(pages))
    print(pages[0].page_content[:1000])
except Exception as e:
    print("WikipediaLoader failed:", e)
