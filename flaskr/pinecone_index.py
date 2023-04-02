import pinecone
from llama_index import GPTPineconeIndex

api_key = "5ae0b92c-d593-4b2c-a625-477c36a557e3"

def create_pinecone_index(index_name = '', documents = []):
    """
    `create_pinecone_index(index_name = '', documents = [])`
    
    This function takes in two arguments:
    
    1. `index_name`: the name of the index you want to create
    2. `documents`: a list of documents you want to index
    
    The function will return a `GPTPineconeIndex` object
    
    :param index_name: the name of the index you want to create
    :param documents: a list of dictionaries, where each dictionary has a 'text' key and a 'metadata'
    key
    """
    print(documents);
    pinecone.init(api_key=api_key, environment="eu-west1-gcp")
    # check if index already exists (it shouldn't if this is first time)
    if index_name not in pinecone.list_indexes():
        # if does not exist, create index
        pinecone.create_index(
            index_name,
            dimension=4000,
            metric='cosine',
        )
        # get index
        pinecone_index = pinecone.Index(index_name)
        # load documents
        # documents = SimpleDirectoryReader('../paul_graham_essay/data').load_data()
        # initialize without metadata filter
        index = GPTPineconeIndex(documents, pinecone_index=pinecone_index)
        # [optional] initialize with metadata filters
        # can define filters specific to this vector index (so you can
        # reuse pinecone indexes)
        # metadata_filters = {"title": "paul_graham_essay"}
        # index = GPTPineconeIndex(documents, pinecone_index=pinecone_index, metadata_filters=metadata_filters)
        return index
    else:
        return 'index: ' + index_name + 'is already exists'

def query_pinecone_index():
    return ''