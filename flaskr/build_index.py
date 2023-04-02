import os

from langchain import OpenAI
from llama_index import (GPTKeywordTableIndex, GPTSimpleVectorIndex,
                         LLMPredictor, PromptHelper, SimpleDirectoryReader)

# NOTE: for local testing only, do NOT deploy with your key hardcoded
os.environ['OPENAI_API_KEY'] = "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"

index = None

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