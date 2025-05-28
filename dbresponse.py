import os
from dotenv import load_dotenv
from langchain_milvus import Zilliz
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pymongo import MongoClient
from helper import Helper

# Load environment variables
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=os.getenv("GOOGLE_API_KEY"))

mongoClient = MongoClient(os.getenv("MONGODB_URI"))
db=mongoClient["sdp_chatbot"]
collection=db["foodItems"]

class milvusDB():
    @staticmethod
    def vectorstore(document_id: str):
        return Zilliz(
            collection_name=document_id,
            connection_args={"uri": os.getenv("ZILLIZ_URI_ENDPOINT"), "token": os.getenv("ZILLIZ_TOKEN")},
            index_params={"index_type": "IVF_PQ", "metric_type": "COSINE"},
            embedding_function=embeddings
        )
            
    @staticmethod
    def nutritionChunks():
        vs = milvusDB.vectorstore("")
        return vs.similarity_search(query="micronutrients", k=1, filter={"chunk_category": "micronutrients"})

    @staticmethod
    def getchunks(query: str, collection: str, category: str | None, k: int = 3):
        vs = milvusDB.vectorstore(collection)
        return vs.similarity_search(
            query=query, k=k, filter={"chunk_category": category}
        )

class mongoDB():
    def mongoresponse(query: list):
        print("Mongo query that is running: ",query)
        documents = collection.aggregate(query)
        if documents:
            response =""
            for doc in documents:
                textDoc = Helper.textualizemongo(doc)
                response+=textDoc
            return response
        else:
            return "No relevant food items found for your condition"
        
    def getLastConv(id: str, sec: str):
        return collection.find_one({"userId": id, "section": sec}, sort=[("timestamp", -1)])
