import uvicorn
import json
import ast
from typing import AsyncGenerator
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from botresponse import BotResponse
from prompts import Prompt
from history import History
from helper import Helper
from dbresponse import milvusDB, mongoDB

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def Home():
    return {"message": "Its Live"}

@app.post("/chat")
async def chat(request:dict = Body(...)):
    session = request.get("id")
    knowledgeBase = request.get("knowledge_base")
    userQuery = request.get("query")
    section = request.get("section")
    category = request.get("chunk_category")
    context = "Its A followup question"
    chats = History.getHistory(userId=session, section=section)
    
    # If Conversation has already begun
    if chats:
        conversations = "\n".join(f"User: {c['user']}\nAssistant: {c['assistant']}" for c in (json.loads(conv) for conv in chats.values()))
        conversationsWithContext = "\n".join(f"User: {c['user']}\nContext: {c['system']}\nAssistant: {c['assistant']}" for c in (json.loads(conv) for conv in chats.values()))

    # Answer is available in NutritionVDB
    if knowledgeBase == "NutritionVDB":
        # print("Needs to be answered from Nutrition VDB")
        
        # No Chat history and flag is also true than *Return Top 5 Micronutrients*
        if chats is None:
            
            # print("Its a first question in Nutrition VDB give top 5 nutrients")
            userQuery = "top 5 micronutrients i should consume"
            userData = request.get("user_data")
            # print(userData)
            textualData = Helper.textualize(userData)
            docs = milvusDB.getchunks(query=userQuery, collection=knowledgeBase, k=1, category="micronutrients")
            context = docs[0].page_content or ""
            prompt = Prompt.micronutrients(userQuery, context, textualData)
            assistant = ast.literal_eval(BotResponse.nonStreamingAnswer(prompt))
            History.setHistory(userId=session, section=section, newConversation={"user": userQuery,"system": context, "assistant": assistant})
            return assistant
        
        # Conversation already started
        else:
            
            # conversations = "\n".join(f"User: {conv['user']}\nAssistant: {conv['assistant']}" for conv in chatHistory.values())
            response = ast.literal_eval(BotResponse.checkfollowup(userQuery, conversations))
            
            # Its a followup question
            if response["followup"]:
                
                # It needs additional context
                if response["need_context"] == True:
                    # print("It needs additional context in Nutrition VDB")
                    temp = json.loads(chats[str(len(chats)-1)])
                    newquestion = temp["user"] + userQuery
                    docs = milvusDB.getchunks(query=newquestion, collection=knowledgeBase, category=category)
                    context = "\n".join(doc.page_content.strip() for doc in docs) if docs else ""
                    prompt = Prompt.followupWithContext(query=userQuery, context=context, conversations=conversationsWithContext)
                
                # It does not need additional context
                else:
                    # print("It does not need additional context in Nutrition VDB")
                    prompt = Prompt.followup(userQuery)
                    prompt+=f"Conversation History: {conversationsWithContext}"
            
            # Its a standalone question
            else:
                # print("Its a standalone question in Nutrition VDB")
                docs = milvusDB.getchunks(query=userQuery, collection=knowledgeBase, category=category)
                context = "\n".join(doc.page_content.strip() for doc in docs) if docs else ""
                prompt = Prompt.general(query=userQuery, context=context)
    
    # Answer is available in ConditionVDB
    elif knowledgeBase == "ConditionVDB":
        # print("Needs to be answered from Condition VDB")
        userData = request.get("user_data")
        textualData = Helper.textualize(userData)

        # Conversation has already started
        if chats:
            isFollowUp = ast.literal_eval(BotResponse.mongofollowup(userQuery, conversations))
            
            # Its a follow up question
            if isFollowUp["followup"]:
                # print("Its a follow up question in Condition VDB")
                
                # It needs additional context
                if isFollowUp["need_context"]:
                    temp = json.loads(chats[str(len(chats)-1)])
                    newquestion = temp["user"] + userQuery
                    
                    # Needs to generate answer from Mongo Database
                    if isFollowUp["knowledge_base"] == "MongoDB":
                        # print("It needs additional context from Mongo DB in Condition VDB")
                        prompt = Prompt.monogoQuery(query = newquestion, data = textualData)
                        aggquery = ast.literal_eval(BotResponse.aggQuery(prompt))
                        context = mongoDB.mongoresponse(query=aggquery)
                        prompt = Prompt.followupWithContext(query=newquestion, context=context, conversations=conversationsWithContext)

                    # Needs to generate answer from Vector Database.
                    else:
                        # print("It needs additional context from Vector DB in Condition VDB")
                        docs = milvusDB.getchunks(query=newquestion, collection=knowledgeBase, category=category)
                        context = "\n".join(doc.page_content.strip() for doc in docs) if docs else ""
                        prompt = Prompt.followupWithContext(query=userQuery, context=context, conversations=conversationsWithContext)
                
                # It does not need additional context
                else:
                    # print("It does not need additional context in Condition VDB")
                    prompt = Prompt.followup(userQuery)
                    prompt+=f"Conversation History: {conversationsWithContext}"
            
            # Its a standalone question
            else:
                
                # Needs to generate answer from Mongo Database
                if isFollowUp["knowledge_base"] == "MongoDB":
                    # print("Needs to generate answer from Mongo DB in Condition VDB")
                    prompt = Prompt.monogoQuery(userQuery, textualData)
                    aggquery = ast.literal_eval(BotResponse.aggQuery(prompt))
                    context = mongoDB.mongoresponse(query=aggquery)
                    prompt = Prompt.general(query=userQuery, context=context)

                # Needs to generate answer from Vector Database.
                else:
                    # print("Needs to generate answer from Vector DB in Condition VDB")
                    docs = milvusDB.getchunks(query=userQuery, collection=knowledgeBase, category=category)
                    context = "\n".join(doc.page_content.strip() for doc in docs) if docs else ""
                    prompt = Prompt.general(query=userQuery, context=context)

        # Its the first question
        else:
            db = ast.literal_eval(BotResponse.mongofollowup(userQuery, None))

            # Needs to generate answer from Mongo Database
            if db["knowledge_base"] == "MongoDB":
                # print("Needs to generate answer from Mongo DB in Condition VDB")
                # prompt = Prompt.monogoQuery(query = userQuery, data = textualData)
                prompt = Prompt.monogoQuery(query = userQuery, data = "I am suffering from Diabetes, I am 22 years old Male.")
                aggquery = ast.literal_eval(BotResponse.aggQuery(prompt))
                context = mongoDB.mongoresponse(query=aggquery)
                prompt = Prompt.general(query=userQuery, context=context)
            
            # Needs to generate answer from Vector Database.
            else:
                # print("Needs to generate answer from Vector DB in Condition VDB")
                docs = milvusDB.getchunks(query=userQuery, collection=knowledgeBase, category=category)
                context = "\n".join(doc.page_content.strip() for doc in docs) if docs else ""
                prompt = Prompt.general(query=userQuery, context=context)

    # Answer is available in some other DB
    else:
        # print("Needs to be answered from "+knowledgeBase)
        
        # Check if conversation history exists?
        if chats:
            isFollowUp = ast.literal_eval(BotResponse.checkfollowup(userQuery, conversations))
            
            # Its a follow up question
            if isFollowUp["followup"]:
                # print("Its a follow up question in "+knowledgeBase)
                
                # It needs additional context
                if isFollowUp["need_context"]:
                    # print("It needs additional context in "+knowledgeBase)
                    temp = json.loads(chats[str(len(chats)-1)])
                    newquestion = temp["user"] + userQuery
                    docs = milvusDB.getchunks(query=newquestion, collection=knowledgeBase, category=category)
                    context = "\n".join(doc.page_content.strip() for doc in docs) if docs else ""
                    prompt = Prompt.followupWithContext(query=userQuery, context=context, conversations=conversations)
                
                # It does not need additional context
                else:
                    # print("It does not need additional context in "+knowledgeBase)
                    prompt = Prompt.followup(userQuery)
                    prompt+=f"Conversation History: {conversations}"
            
            # Its a standalone question
            else:
                # print("Its a standalone question in "+knowledgeBase)
                docs = milvusDB.getchunks(query=userQuery, collection=knowledgeBase, category=category)
                context = "\n".join(doc.page_content.strip() for doc in docs) if docs else ""
                prompt = Prompt.general(query=userQuery, context=context)
        
        # Its the first question
        else:
            # print("Its a first question in "+knowledgeBase)
            docs = milvusDB.getchunks(query=userQuery, collection=knowledgeBase, category=category)
            context = "\n".join(doc.page_content.strip() for doc in docs) if docs else ""
            prompt = Prompt.general(query=userQuery, context=context)

    try:
        response = BotResponse.answer(prompt)
        async def stream_response() -> AsyncGenerator[str, None]:
            assistant = ""
            try:
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        assistant += content
                        yield content
            except Exception as e:
                yield f"Error: {str(e)}"
            History.setHistory(userId=session, section=section, newConversation={"user": userQuery,"system": context, "assistant": assistant})
        return StreamingResponse(stream_response(), media_type="text/plain")
    except Exception as e:
        return {"error": str(e)}
    
# @app.delete("/delete")
# async def delete_chunk(data: dict = Body(...)):
#     knowledgeBase = data.get("knowledgeBase")
#     partitionKey = data.get("partitionKey")
#     file_ids = [f"{partitionKey}_{i}" for i in range(3855)]
#     vector_store = get_vector_store(knowledgeBase)
#     vector_store.delete(ids= file_ids)
#     return {"message": "Chunk deleted successfully"}

# if __name__ == "__main__":
#     uvicorn.run("api:app", host="localhost", port=8000, reload=True)