from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = PyPDFLoader("/home/amuller/Documents/mirinae/Day-Traders-Manual-pdf")
pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(
    length_function = len,
    chuck_size = 300,
    chuck_overlap = 50,
    add_start_index = True,
)

texts = text_splitter.create_documents(pages)

