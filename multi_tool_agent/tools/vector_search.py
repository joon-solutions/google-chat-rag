import vertexai
from google.cloud import firestore
from vertexai.generative_models import GenerativeModel, GenerationConfig
from langchain_google_vertexai import VertexAIEmbeddings
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
import os
from dotenv import load_dotenv

load_dotenv()

database_name = os.environ.get("VECTOR_DB_NAME","")
project_id = os.environ.get("VECTOR_DB_PROJECT","")
location = os.environ.get("VECTOR_DB_LOCATION","")
collection_name = os.environ.get("VECTOR_DB_COLLECTION_NAME","")


db = firestore.Client(project=project_id, database=database_name)
collection = db.collection(collection_name)
embedding_model = VertexAIEmbeddings(model_name="text-embedding-005")

gen_model = model = GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=GenerationConfig(temperature=0))


def search_vector_database(query: str) -> list:
    # For debugging - check if collection has documents
    all_docs = list(collection.limit(3).stream())
    # print(f"Collection has {len(all_docs)} documents")
    if not all_docs:
        return ["No documents found in the collection."]

    # 1. Generate the embedding of the query using the same model as data loading
    try:

        query_embedding = embedding_model.embed_query(query)

        # Create a Vector object from the embedding values
        query_vector = Vector(query_embedding)

        # 2. Get the 5 nearest neighbors
        vector_query = collection.find_nearest(
            vector_field="embedding_map",
            query_vector=query_vector,  # Use Vector object, not dictionary
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=10,
        )

        # 3. Process results
        docs = list(vector_query.stream())  # Convert to list to avoid stream consumption issues
        print(f"Vector query returned {len(docs)} documents")

        if not docs:
            return ["No relevant documents found for your query."]

        # Extract content from documents
        context = [
            {
                "content": result.to_dict().get('content', ''),
                "url": result.to_dict().get('url', '')
                }
            for result in docs
            ]

    except Exception as e:
        print(f"Error in vector search: {e}")
        context = f"Error performing vector search: {str(e)}"

    return context