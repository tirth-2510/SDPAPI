import redis
import json
from collections import deque
import os
from dotenv import load_dotenv

load_dotenv()

# Use this for production
r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), password=os.getenv("REDIS_PASSWORD"), ssl=True, db=0)

# Use this for local testing
# r = redis.Redis(host="localhost", port=6379, db=0)

class History:
    @staticmethod
    def getHistory(userId: str, section: str):
        '''Get a specific section of the user session history.

        Args:
            userId (str): User Id.
            section (str): section of the session history to get.
        '''
        response = r.hget(userId, section)
        return(json.loads(response) if response else None)
    
    @staticmethod
    def setHistory(userId: str, section:str, newConversation: dict):
        '''Add a new conversation to the user session history. Length of session is limited to 3, older conversations are overwritten. 

        Args:
            userId (str): User Id.
            section (str): section of the session history to get.
            newConversation (dict): New conversation to add.
        
        Example of newConversation to pass: 
        
        {
            "user": "Marco",
            "assistant": "Polo"
        }
        '''
        response = History.getHistory(userId, section)
        # Conversation exists
        if response:
            conversationArray = deque(maxlen=5)
            for conv in response.values():
                conversationArray.append(json.loads(conv))
            conversationArray.append(newConversation)
            updatedConversationMemory = {str(i) : json.dumps(conv) for i, conv in enumerate(conversationArray)}
            r.hset(userId, mapping={section: json.dumps(updatedConversationMemory)})
    
        # Its the first question
        else:
            r.hset(userId, mapping={section: json.dumps({"0": json.dumps(newConversation)})})
            if r.ttl(userId) == -1:
                r.expire(userId, 43200) # 12 hours