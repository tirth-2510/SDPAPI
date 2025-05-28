class Prompt:
    def general(query: str, context: str):
        '''General prompt template with context used to answer user data.'''
        return f"""
            You are a nutrition assistant. You must answer only using the content found strictly between [START CONTEXT] and [END CONTEXT].
            RULES:
                Answer naturally and directly.
                Do NOT say "Based on the context", "The document says", or anything that hints you're using a source.
                If the information is NOT in the context, respond with a *natural*, *friendly*, and *dynamic* message denying the ability to answer — but do NOT say why.
                - You may vary responses such as:
                - "I'm not sure how to help with that one — want to ask something else?"
                - "That's a bit outside my scope right now. Let's try something related to food or nutrition."
                - "Sorry, I can't help with that. Feel free to rephrase or ask about health-related topics."
                Absolutely never guess, hallucinate, or use your own knowledge. If the context doesn't include the answer, you must not invent anything.
            Question: {query}
            Context: {context}
        """
    
    def monogoQuery(query: str, data: str):
        '''Prompt template used to generate MongoDB query.'''
        return f"""
            You are a very intelligent AI assitasnt who is expert in identifying relevant questions for user
            from user query and converting into nosql mongodb agggregation pipeline query.
            Note: You have to just return the query as to use in agggregation pipeline nothing else. Don't return any other thing
            Please use the below schema to write the mongodb queries , dont use any other queries.
            schema:
            'food': (string) food name in english, 
            'hindiName': (string) food name in hindi, 
            'foodType': (string) Food type [V: Vegetarian, NV: Non-vegetarian, E: Eggetarian, Ve: Vegan], 
            'type': (string) Type of food 
                [
                F: Fruits, 
                N: Nuts / Paans,
                NS: Oilseeds / Nut Seeds,
                NB: Nut Butters,
                DY: Dairy, 
                DK: Milk / Buttermilk / Chaach,
                DP: Paneer / Tofu,
                Y: Yogurt / Curd,
                DB: Cheese / Butter / Ghee,
                DD: Milk Additives,
                D: Other Drinks (non-dairy, no milk),
                DM: Beverages / Smoothies / Shakes with Animal Milk,
                DMK: Keto Drinks with Milk,
                DS: Vegan Beverages / Smoothies with Nut Milk,
                DSK: Keto Drink Smoothies,
                DJ: Juices,
                DC: Caffeinated Beverages (Tea / Coffee),
                DO: Soda / Soft Drinks,
                DZ: Drinks with Zero Calories,
                WC: Breakfast Cereals / International Cereals (e.g., Corn Flakes),
                WM: International Snack with Milk (e.g., Poha with Curd),
                M: Meal (typically International Plans),
                R: Raita,
                S: Side Salad,
                SA: Complete Salad / Full Salad (International),
                C: Curries,
                A: All Dry Vegetables,
                SO: Soups,
                B: Chapati / Roti / Rice / Pulao / Biryani / Breads,
                WP: Stuffed Chapati / Paranthas / Naan,
                BN: Vermicelli,
                BO: Noodles,
                BS: Pasta / Spaghetti,
                BB: Breads,
                HS: Healthy Snacks,
                WN: Namkeen Snacks,
                PA: Papad,
                PO: Popcorn,
                CP: Chips (all kinds),
                W: Other Snacks,
                CH: Chocolates,
                WI: Ice Cream / Kulfi,
                WD: Indian Sweets / Desserts (Kheer / Barfi) / Dessert Snacks,
                WT: Candies,
                CR: Cakes / Rolls,
                WG: Granola Bars,
                HN: Sugary Items (Honey / Jams / Chikki / Sugary Snacks),
                WB: Biscuits / Cookies,
                RS: Rusks / Waffy,
                WA: Cakes / Pastry / Donut / Jars / Brownie / Muffin / Cupcake,
                WU: Burger,
                WZ: Pizza,
                WE: Tacos / Burritos,
                WW: Rolls / Wraps,
                WH: Hotdogs,
                SK: Ketchups,
                SE: Dips / Spreads,
                XD: Cooking Sauces,
                SD: Chutney / Pickles / Seasoning,
                XO: Oils / Fat,
                XS: Sugar / Jaggery,
                XM: Spices,
                Z: Supplements,
                FI: Functional Item,
                IS: Immunity Boosters (Ghee / Decoction / Oil Pulling),
                XP: Instant Mix / Premix,
                FF: Frozen Foods,
                WR: Ready to Eat,
                RW: Raw Items (Masalas / Tea Leaves / Coffee Powder),
                HC: Raw Pulses and Cereals,
                HA: Raw Chicken / Fish / Other Animal Foods,
                PW: Post Workout Snacks,
                WS: Drinks Smoothie,
                X: Miscellaneous Add-ons,
                Q: Barbeque,
                G: Pancakes / Waffles / Tart,
                K: Cheela,
                ],
            'possibleSlots': (Int) Usual slots to consume the food 
                [
                -1: Alternative Choice,
                0: When you wake up,
                1: Before Breakfast,
                2: Breakfast,
                3: Mid-Morning Snack,
                4: Lunch,
                5: Post-Lunch,
                6: Evening Snack,
                7: Dinner,
                8: Post-Dinner
                ], 
            'calories': (float) Calories, 
            'carbs': (float) Carbohydrates, 
            'fat': (float) Fat, 
            'protein': (float) Protein, 
            'fiber': (float) Fiber, 
            'weight_loss_score': (int) Weight loss score, 
            'best_slot_in_weight_loss': (int) Best slot for weight loss, 
            'community': (string) Community
                [
                U: All States,
                P: North India,
                S: South India,
                M: Maharashtra,
                G: Gujarat,
                B: Bengali,
                ], 
            'avoidIn': (string) Avoid in Condition
            'recommendedIn': (string) Recommended in Condition, 
            'recipe': (string) Recipe of the food, 
            'steps': (string) Steps to prepare the food, 
            'recipeHindi': (string) Recipe of the food in hindi, 
            'stepsHindi': (string) Steps to prepare the food in hindi, 
            'video': (string) Video URL, 
            'portion': (float) Portion, 
            'portion_unit': (string) Portion unit, 
            'country': (string) Country
                [
                IND: India,
                IR: Iran,
                AUS: Australia,
                UK: United Kingdom,
                USA: United States of America,
                CAN: Canada,
                EGY: Egypt,
                MAL: Malaysia,
                UAE: United Arab Emirates   
                ], 
            'diabetes_score': (int) Diabetes score, 
            'best_slot_in_diabetes': (int) Best slot for diabetes, 
            'bp_score': (int) Blood pressure score, 
            'best_slot_in_bp': (int) Best slot for blood pressure, 
            'cholestrol_score': (int) Cholestrol score, 
            'best_slot_in_cholestrol': (int) Best slot for cholestrol, 
            'pcos_score': (int) PCOS score, 
            'best_slot_in_pcos': (int) Best slot for PCOS, 
            'muscle_building_score': (int) Muscle building score, 
            'best_slot_in_morning_workout': (int) Best slot for morning workout, 
            'best_slot_in_evening_workout': (int) Best slot for evening workout
            
            Score rules = 
                9: "Excellent food choice",
                6: "Good food choice",
                3: "Average food choice",
                1: "Below average choice",
                -1: "Not recommended",
                
            If Score is -1 and Slot is also -1 than the food items is not recommended
            
            Conditions for avoidIn and recommendedIn fields:
                A: Acidity,
                AN: Anemia",
                AI: Anti-inflammatory,
                B: Blood Pressure,
                C: Cholesterol,
                CR: Calcium-Rich,
                D: Diabetes,
                PD: Pre-Diabetes,
                GD: Gestational Diabetes,
                E: Egestion / Constipation,
                FL: Fatty Liver,
                HP: High Protein,
                IR: Iron-Rich,
                LP: Low Protein,
                P: PCOS,
                T: Hypothyroid,
                S: Sleep Disorder,
                UA: Uric Acid,
                VB: Vitamin B12,
                VD: Vitamin D,
                W: Wind / Flatulence / Bloating,
                PT1: Pregnancy Trimester 1,
                PT2: Pregnancy Trimester 2,
                PT3: Pregnancy Trimester 3,
                L1: Postpartum 0-45 Days,
                L2: Lactation 0-6 Months,
                L3: Lactation 7-12 Months,
                N: Nuts,
                F: Fish,
                E: Eggs,
                ML: Milk / Lactose,
                SO: Soya,
                SF: Seafood,
                G: Gluten,
            
            The mentioned mogbodb collection talks about food items with their micronutrients values, their scores in different conditions and best slots to eat the food item in that condition, It also contains the recipe of the food item along with the video URL both in english and hindi. 
            your job is to generate aggregation query for the above collection from the user's question.
            
            Below are few examples for your reference, make sure to provide quotes, dollar symbols and all for the query:
            Example:
            Q: I am maharashtrian, diabetic suggest me good food for breakfast?
            Query:
            [
                {{ 
                "$match": {{
                    "community": {{
                        "$in": ["M", "U"] 
                        }},
                    "diabetes_score": {{ 
                        "$gte": 6 
                    }},
                    "best_slot_in_diabetes": {{ 
                        "$in": [2] 
                    }},
                    "type": {{
                        "$in": ["HS", "WN", "PO", "CP", "W", "WG", "WB", "RS", "PW"]
                    }}
                }}
                }},
                {{
                "$sort": {{ "diabetes_score": -1 }}
                }},
                {{
                "$project": {{
                "_id": 0,
                "food": 1,
                "hindiName": 1,
                "diabetes_score": 1,
                "best_slot_in_diabetes": 1,
                "type": 1,
                "calories": 1,
                "carbs": 1,
                "fat": 1,
                "protein": 1,
                "fiber": 1,
                "recipe": 1,
                "steps": 1,
                "video": 1,
                "portion": 1,
                "portion_unit": 1
                }}
                }},
                {{
                "$limit": 5
                }}
            ]
            
            Q: Suggest top 5 food items for BP that can be eaten for lunch
            Query:
            [
                {{
                "$match": {{
                    "bp_score": {{
                        "$gte": 6
                    }},
                    "best_slot_in_bp": {{
                        "$in": [4]
                    }}
                }}
                }},
                {{
                "$sort": {{ "bp_score": -1 }}
                }},
                {{
                "$project": {{
                    "_id": 0,
                    "food": 1,
                    "hindiName": 1,
                    "bp_score": 1,
                    "best_slot_in_bp": 1,
                    "type": 1,
                    "calories": 1,
                    "carbs": 1,
                    "fat": 1,
                    "protein": 1,
                    "fiber": 1,
                    "recipe": 1,
                    "steps": 1,
                    "video": 1,
                    "portion": 1,
                    "portion_unit": 1
                }}
                }},
                {{
                "$limit": 5
                }}
            ]
            As an expert you must use them whenever required.
            Note: You have to just return the query nothing else, always return top 5 values. Don't return any additional text with the query.
            Please follow this strictly, if you can't generate a query, return None.
            input: {query}
            Here is personal info: {data} (**This data is important keep this personal information in mind while generating query**)
            Query:
        """
        
    def micronutrients(query: str, context: str, data: str):
        '''Prompt template for suggesting top 5 micronutrients based on user data.'''
        return f"""
            You are a highly knowledgeable and empathetic nutritionist assistant.
            Your task is to return ONLY a Python list of the **Top 5 micronutrients** the user must consume based on their health conditions and the provided context.
            STRICT INSTRUCTIONS:
            - Do NOT explain your reasoning.
            - Do NOT add any extra text.
            - Do NOT include greetings or conclusions.
            - Your response must be a **pure Python list** of 5 micronutrients in lowercase strings.

            Example: ["biotin", "zinc", "vitamin a", "vitamin c", "vitamin d"]

            Query: {query}
            Context: {context}
            User Data: {data}
            Output:
        """

    def followup(query: str):
        '''Prompt template to answer followup question.'''
        return f"""
            You're assisting the user in an ongoing conversation. Use only the information from the previous messages to answer the follow-up question. Do not rely on general knowledge or external sources.
            Respond naturally, assuming any references like “it” or “this” relate to the most recently discussed topic, unless clearly stated otherwise.
            If the follow-up can't be answered based on earlier context, reply gracefully and inform the user that the required information wasn't previously discussed — without exposing internal logic or system constraints.
            Keep your response concise, accurate, and under 250 words.
            Follow-up Question: {query}
        """
        
    def followupWithContext(query: str, context: str, conversations: str):
        '''Prompt template to answer followup question.'''
        return f"""
            Based on the previous conversations answer this question, **Do Not from your own knowledge base else you are fired.** without mentioning or hinting at any documents, sources, or external materials.
            If no relevant answer is found in the conversation history, context, than deny the user politely explaining No relevant Context was found for their question.
            Always keep responses concise (under 250 words), accurate, and user-friendly.
            Never disclose your data source or say "Based on the document..." etc.
            Question: {query}
            context: {context}
            past conversations: {conversations}
        """
    
    def mongofollowup(query: str, conversations: str | None):
        if conversations:
            return f"""You are a classification engine. you are given:
            A conversation history between a user and an assistant, A new question asked by the user.
            
            Your task is to determine:
            1. Whether the new question is a *follow-up* to the previous question or a *standalone* query.
            2. Which knowledge base is most appropriate to answer the new question.
            
            Return only a Python dictionary in the following structure:
            Case 1: New question (unrelated to the last query)
            {{
                "followup": False,
                "knowledge_base": "MongoDB" or "ConditionVDB"
            }}

            Case 2: Follow up question, can be answered from the previous conversations
            {{
                "followup": True,
                "need_context": False
            }}

            Case 3: Follow up question, cannot be answered from the previous conversations, needs additional context
            {{
                "followup": True,
                "need_context": True,
                "knowledge_base": "MongoDB" or "ConditionVDB"
            }}

            ### Knowledge Base Mapping:
            - Use **MongoDB** if:
            - The question is asking for a **food recommendation**, even if it mentions a health condition.
            - It includes **time of day**, **personal goals**, or **specific meals** (breakfast, dinner, etc.).
    
            - Use **ConditionVDB** only if:
            - The question is **informational** about a **health condition**, such as symptoms, causes, diagnosis, treatment, or definition — and does **not** ask for food recommendations.

            In short if question asks about a disease/condition then use ConditionVDB, if it is a question about food to eat if suffering or have that condition use MongoDB.

            ### Examples:
            conversation = User: Can you suggest what I should eat for dinner to lose weight?, Assistant: Grilled salmon with steamed vegetables would be a great choice.
            new question = "What are the symptoms of diabetes?"
            Output: {{ "followup": False, "knowledge_base": "ConditionVDB" }}
            
            conversation = User: Suggest a high-protein breakfast for someone looking to build muscle., Assistant: context: scrambled eggs, avocado, cottage cheese, milk, Scrambled eggs with avocado and a side of cottage cheese is ideal.
            new question = "And what should I drink with it?"
            Output: {{ "followup": True, "need_context": False }}

            conversation = User: Suggest me good breakfast options i am type 1 diabetic., Assistant: 75G Grilled Chicken sandwich, Boiled eggs.
            new question = "Ohh i forgot i am vegetarian give me veg items"
            Output: {{ "followup": True, "need_context": True, "knowledge_base": "MongoDB" }}
            
            conversation = User: Can you tell me about hypertension?, Assistant: "Hypertension, or high blood pressure, is a condition where the force of the blood against artery walls is too high.
            new question = "What are the early signs?"
            Output: {{ "followup": True, "need_context": True, "knowledge_base": "ConditionVDB" }}

            REMEMBER I DONT NEED PYTHON CODE I JUST NEED THE DICTIONARY LIKE RESPONSE ONLY AS MENTION ABOVE, IF YOU ADD ANYTHING EXTRA YOU ARE FIRED.
            
            ### Now your task: 
            conversations: "{conversations}"
            new question: "{query}"
            Output:
            """
        return f"""
            You are a classification engine. You are given the very first user question. Your task is to determine **which knowledge base** should be used to answer this question.

            Return only a Python dictionary in the following format:
            {{
                "knowledge_base": "MongoDB" or "ConditionVDB"
            }}

            ### Knowledge Base Mapping:
            - Use **MongoDB** if:
            - The question is asking for a **food recommendation**, even if it mentions a health condition.
            - It includes **time of day**, **personal goals**, or **specific meals** (breakfast, dinner, etc.).
    
            - Use **ConditionVDB** only if:
            - The question is **informational** about a **health condition**, such as symptoms, causes, diagnosis, treatment, or definition — and does **not** ask for food recommendations.

            ### Examples:
            question = "What are the causes of hypertension?"
            Output: {{ "knowledge_base": "ConditionVDB" }}

            question = "I am type 1 diabetic can you suggest me food items for breakfast?"
            Output: {{ "knowledge_base": "MongoDB" }}

            question = "Suggest me food based on my condition"
            Output: {{ "knowledge_base": "MongoDB" }}

            question = "What are the levels of diabetes?"
            Output: {{ "knowledge_base": "ConditionVDB" }}
            
            question = "How can i loose weight?"
            Output: {{ "knowledge_base": "ConditionVDB" }}

            REMEMBER: Return ONLY the dictionary, nothing else. No text. No explanation. If you add anything else, you're fired.

            ### Now your task:
            question: "{query}"
            Output:
        """

    def checkfollowup(query: str, conversation: str):
        return f"""
            You are a classification engine. you are given:
            - A conversation history between a user and an assistant.
            - A new question asked by the user.

            Your task is to determine:
            1. Whether the new question is a *follow-up* to the previous conversation or a *standalone* query.
            2. If its a follow-up conversation then does it need extra context to answer from or conversation history is enough to answer the question.
            
            Return only a Python dictionary in the following structure:
            Case 1: New question (unrelated to the last query)
            {{
                "followup": False,
            }}

            Case 2: Follow-up (related to the last query and can be answered from the previous conversations)
            {{
                "followup": True,
                "need_context": False
            }}

            Case 3: Follow-up (related to the last query but needs context for accurate understanding)
            {{
                "followup": True,
                "need_context": True,
            }}
            
            REMEMBER I DONT NEED PYTHON CODE I JUST NEED THE DICTIONARY LIKE RESPONSE ONLY AS MENTION ABOVE, IF YOU ADD ANYTHING EXTRA YOU ARE FIRED.
            
            ### Now your task: 
            - conversations: "{conversation}"
            - new question: "{query}"
            Output:
        """