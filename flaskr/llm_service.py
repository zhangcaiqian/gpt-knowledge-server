import os

from langchain import OpenAI
from llama_index import LLMPredictor, PromptHelper

# NOTE: for local testing only, do NOT deploy with your key hardcoded
os.environ['OPENAI_API_KEY'] = "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"


def gen_llm(model_name="text-davinci-003"):
    """
    It creates a prompt helper and a language model predictor
    
    :param model_name: the name of the model to use, defaults to text-davinci-003 (optional)
    :return: A predictor and a prompt helper
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
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name=model_name, max_tokens=num_output))
    return llm_predictor, prompt_helper
