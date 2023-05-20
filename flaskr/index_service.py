import os

from langchain import OpenAI
from llama_index import (GPTSimpleVectorIndex, LLMPredictor, PromptHelper,
                         SimpleDirectoryReader, download_loader)

from . import llm_service

llm_predictor, prompt_helper = llm_service.gen_llm()

PDFReader = download_loader("PDFReader")

index = None

def load_index_from_disk(index_name):
    global index
    if os.path.exists("./file_index/" + index_name + ".json"):
        index = GPTSimpleVectorIndex.load_from_disk(os.path.join("./file_index", index_name + ".json"), llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    else:
        loader = PDFReader()
        documents = loader.load_data(file=os.path.join("./documents", index_name + ".pdf"))
        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        index.save_to_disk(index_name)
    return index

def gen_index_with_pdf(index_name):
    if os.path.exists("./file_index/" + index_name + ".json"):
        return 'index has already exists'
    else:
        loader = PDFReader()
        documents = loader.load_data(file=os.path.join("./documents", index_name + ".pdf"))
        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        index.save_to_disk(os.path.join("./file_index", index_name))
        return 'index has been generated'


def initialize_index():
    """
    It loads the index from disk if it exists, otherwise it creates it from the documents in the
    `./documents` directory
    :return: The index is being returned.
    """
    # define prompt helper
    # set maximum input size
    max_input_size = 4000
    # set number of output tokens
    num_output = 1000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=num_output))
    
    global index
    index_name = 'test_index2.json'
    if os.path.exists(index_name):
        index = GPTSimpleVectorIndex.load_from_disk(index_name, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        # pinecone_index.create_pinecone_index(index_name="renjixilie-zhenjiu", documents=index)
    else:
        documents = SimpleDirectoryReader("./documents").load_data()
        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        index.save_to_disk(index_name)
    return index