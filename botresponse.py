from groq import Groq
from prompts import Prompt
import os
from dotenv import load_dotenv

load_dotenv()

llm = Groq(api_key=os.getenv("GROQ_API_KEY"))

class BotResponse:
    def answer(prompt: str):
        '''Generate response.'''
        return llm.chat.completions.create(
            # model="llama-3.1-8b-instant",
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            stream=True,
        )
    
    def nonStreamingAnswer(prompt: str):
        '''Generate followup question response from chathistory.'''
        response = llm.chat.completions.create(
            # model="llama-3.1-8b-instant",
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    
    def aggQuery(prompt: str):
        '''Generate aggregate query from userQuestion based on user question.'''
        response = llm.chat.completions.create(
            # model="llama-3.1-8b-instant",
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content

    def checkfollowup(query: str, conversations: str):
        '''Check if the question is a followup question or not?'''
        prompt = Prompt.checkfollowup(query = query, conversation = conversations)
        response = llm.chat.completions.create(
            # model="llama-3.1-8b-instant",
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    
    def mongofollowup(query: str, conversations: str | None):
        '''Check if the question is a followup question or not for Conditions VDB? I am making this same followup function again to reduce LLM call.'''
        if conversations is None:
            prompt = Prompt.mongofollowup(query = query, conversations = None)
        else:
            prompt = Prompt.mongofollowup(query = query, conversations = conversations)
        response = llm.chat.completions.create(
            # model="llama-3.1-8b-instant",
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content