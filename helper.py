from type import UserBody, UserGoals

class Helper:
    # <------------------------- Textualize User Data ------------------------->
    def textualize(data: UserBody | dict):
        if isinstance(data, dict):
            data = UserBody(**data)  # Convert dict to UserBody

        template = f"""User Name: {data.name}
            Age: {data.age}
            State he belongs from: {', '.join(data.community)}
            Food Type Preference: {', '.join(data.foodType)}
            Disease / Conditions he suffers from: {', '.join(data.conditions)}
            Allergetic to: {', '.join(data.allergies) if data.allergies else "No Allergies"}
            """

        if data.goal is not None and isinstance(data.goal, dict):
            goals = UserGoals(**data.goal)
            template += f"""
            Calories Goal: {goals.calories}
            Carbs Goal: {goals.carbs}
            Fat Goal: {goals.fat}
            Protein Goal: {goals.protein}
            """
        return template

    
    # <------------------------- Textualize MongoDB Documents ------------------------->
    def textualizemongo(doc: dict):
        # Food Type Dictionary (Veg, Non-Veg, Eggetarian, Vegan)
        FoodTypeDict = {
            "V":"Vegetarian",
            "NV":"Non-vegetarian",
            "E":"Eggetarian",
            "Ve":"Vegan"
        }
        TypeDict = {
            "F": "Fruits",
            "N": "Nuts / Paans",
            "NS": "Oilseeds / Nut Seeds",
            "NB": "Nut Butters",
            "DY": "Dairy",
            "DK": "Milk / Buttermilk / Chaach",
            "DP": "Paneer / Tofu",
            "Y": "Yogurt / Curd",
            "DB": "Cheese / Butter / Ghee",
            "DD": "Milk Additives",
            "D": "Other Drinks (non-dairy, no milk)",
            "DM": "Beverages / Smoothies / Shakes with Animal Milk",
            "DMK": "Keto Drinks with Milk",
            "DS": "Vegan Beverages / Smoothies with Nut Milk",
            "DSK": "Keto Drink Smoothies",
            "DJ": "Juices",
            "DC": "Caffeinated Beverages (Tea / Coffee)",
            "DO": "Soda / Soft Drinks",
            "DZ": "Drinks with Zero Calories",
            "WC": "Breakfast Cereals / International Cereals (e.g., Corn Flakes)",
            "WM": "International Snack with Milk (e.g., Poha with Curd)",
            "M": "Meal (typically International Plans)",
            "R": "Raita",
            "S": "Side Salad",
            "SA": "Complete Salad / Full Salad (International)",
            "C": "Curries",
            "A": "All Dry Vegetables",
            "SO": "Soups",
            "B": "Chapati / Roti / Rice / Pulao / Biryani / Breads",
            "WP": "Stuffed Chapati / Paranthas / Naan",
            "BN": "Vermicelli",
            "BO": "Noodles",
            "BS": "Pasta / Spaghetti",
            "BB": "Breads",
            "HS": "Healthy Snacks",
            "WN": "Namkeen Snacks",
            "PA": "Papad",
            "PO": "Popcorn",
            "CP": "Chips (all kinds)",
            "W": "Other Snacks",
            "CH": "Chocolates",
            "WI": "Ice Cream / Kulfi",
            "WD": "Indian Sweets / Desserts (Kheer / Barfi) / Dessert Snacks",
            "WT": "Candies",
            "CR": "Cakes / Rolls",
            "WG": "Granola Bars",
            "HN": "Sugary Items (Honey / Jams / Chikki / Sugary Snacks)",
            "WB": "Biscuits / Cookies",
            "RS": "Rusks / Waffy",
            "WA": "Cakes / Pastry / Donut / Jars / Brownie / Muffin / Cupcake",
            "WU": "Burger",
            "WZ": "Pizza",
            "WE": "Tacos / Burritos",
            "WW": "Rolls / Wraps",
            "WH": "Hotdogs",
            "SK": "Ketchups",
            "SE": "Dips / Spreads",
            "XD": "Cooking Sauces",
            "SD": "Chutney / Pickles / Seasoning",
            "XO": "Oils / Fat",
            "XS": "Sugar / Jaggery",
            "XM": "Spices",
            "Z": "Supplements",
            "FI": "Functional Item",
            "IS": "Immunity Boosters (Ghee / Decoction / Oil Pulling)",
            "XP": "Instant Mix / Premix",
            "FF": "Frozen Foods",
            "WR": "Ready to Eat",
            "RW": "Raw Items (Masalas / Tea Leaves / Coffee Powder)",
            "HC": "Raw Pulses and Cereals",
            "HA": "Raw Chicken / Fish / Other Animal Foods",
            "PW": "Post Workout Snacks",
            "WS": "Drinks Smoothie",
            "X": "Miscellaneous Add-ons",
            "Q": "Barbeque",
            "G": "Pancakes / Waffles / Tart",
            "K": "Cheela",
        }
        SlotDict = {
            -1: "As an Alternative",
            0: "When you wake up",
            1: "Before Breakfast",
            2: "Breakfast",
            3: "Mid Morning Snack",
            4: "Lunch",
            5: "Post Lunch",
            6: "Evening Snack",
            7: "Dinner",
            8: "Post Dinner",
        }
        ScoreDict = {
            9: "Excellent food choice",
            6: "Good food choice",
            3: "Average food choice",
            1: "Below average choice",
            -1: "Not recommended",
        }
        CommunityDict = {
            "U":"All States",
            "P":"North India",
            "S":"South India",
            "M":"Maharashtra",
            "G":"Gujarat",
            "B":"Bengali",
        }
        ConditionDict = {
            "A": "Acidity",
            "AN": "Anemia",
            "AI": "Anti-inflammatory",
            "B": "Blood Pressure",
            "C": "Cholesterol",
            "CR": "Calcium-Rich",
            "D": "Diabetes",
            "PD": "Pre-Diabetes",
            "GD": "Gestational Diabetes",
            "E": "Egestion / Constipation",
            "FL": "Fatty Liver",
            "HP": "High Protein",
            "IR": "Iron-Rich",
            "LP": "Low Protein",
            "P": "PCOS",
            "T": "Hypothyroid",
            "S": "Sleep Disorder",
            "UA": "Uric Acid",
            "VB": "Vitamin B12",
            "VD": "Vitamin D",
            "W": "Wind / Flatulence / Bloating",
            "PT1": "Pregnancy Trimester 1",
            "PT2": "Pregnancy Trimester 2",
            "PT3": "Pregnancy Trimester 3",
            "L1": "Postpartum 0-45 Days",
            "L2": "Lactation 0-6 Months",
            "L3": "Lactation 7-12 Months",
            "N": "Nuts",
            "F": "Fish",
            "E": "Eggs",
            "ML": "Milk / Lactose",
            "SO": "Soya",
            "SF": "Seafood",
            "G": "Gluten",
        }
        CountryDict = {
            "IND":"India",
            "IR":"Iran",
            "AUS":"Australia",
            "UK":"United Kingdom",
            "USA":"United States of America",
            "CAN":"Canada",
            "EGY":"Egypt",
            "MAL":"Malaysia",
            "UAE":"United Arab Emirates"
        }
        
        foodName = doc.get("food", "")
        hindiName = doc.get("hindiName", "")
        foodType = doc.get("foodType", None)
        if foodType is not None:
            foodType= FoodTypeDict.get(foodType, None)
        typeFood = doc.get("type", "")
        typeFood = TypeDict[typeFood]
        calories = doc.get("calories", "")
        carbs = doc.get("carbs", "")
        fat = doc.get("fat", "")
        protein = doc.get("protein", "")
        fiber = doc.get("fiber", "")
        recipe = doc.get("recipe", "")
        steps = doc.get("steps", "")
        video = doc.get("video", "")
        portion = doc.get("portion", "")
        portion_unit = doc.get("portion_unit", "")
        avoidIn = doc.get("avoidIn", None)
        if avoidIn is not None:
            avoidIn = ConditionDict.get(avoidIn, None)
        recommendedIn = doc.get("recommendedIn", None)
        if recommendedIn is not None:
            recommendedIn = ConditionDict.get(recommendedIn, None)
        community = doc.get("community", None)
        if community is not None:
            community = [CommunityDict.get(com, "") for com in community]
        possibleSlots = doc.get("possibleSlots", None)
        if possibleSlots is not None:
            possibleSlots = [SlotDict.get(possibleSlot, "") for possibleSlot in possibleSlots]
        country = doc.get("country", None)
        if country is not None:
            country = [CountryDict.get(cntry, "") for cntry in country]
        diabetesScore = doc.get("diabetes_score", None)
        if diabetesScore is not None:
            diabetesScore = ScoreDict.get(diabetesScore, None)
        diabetesBestSlot = doc.get("best_slot_in_diabetes", None)
        if diabetesBestSlot is not None:
            diabetesBestSlot = SlotDict.get(diabetesBestSlot, None)
        bpScore = doc.get("bp_score", None)
        if bpScore is not None:
            bpScore = ScoreDict.get(bpScore, None)
        bpBestSlot = doc.get("best_slot_in_bp", None)
        if bpBestSlot is not None:
            bpBestSlot = SlotDict.get(bpBestSlot, None)
        cholestrolScore = doc.get("cholestrol_score", None)
        if cholestrolScore is not None:
            cholestrolScore = ScoreDict.get(cholestrolScore, None)
        cholestrolBestSlot = doc.get("best_slot_in_cholestrol", None)
        if cholestrolBestSlot is not None:
            cholestrolBestSlot = SlotDict.get(cholestrolBestSlot, None)
        pcosScore = doc.get("pcos_score", None)
        if pcosScore is not None:
            pcosScore = ScoreDict.get(pcosScore, None)
        pcosBestSlot = doc.get("best_slot_in_pcos", None)
        if pcosBestSlot is not None:
            pcosBestSlot = SlotDict.get(pcosBestSlot, None)
        muscleBuildingScore = doc.get("muscle_building_score", None)
        if muscleBuildingScore is not None:
            muscleBuildingScore = ScoreDict.get(muscleBuildingScore, None)
        morningBestSlot = doc.get("best_slot_in_morning_workout", None)
        if morningBestSlot is not None:
            morningBestSlot = SlotDict.get(morningBestSlot, None)
        eveningBestSlot = doc.get("best_slot_in_evening_workout", None)
        if eveningBestSlot is not None:
            eveningBestSlot = SlotDict.get(eveningBestSlot, None)
        
        output = f"""
    foodName: {foodName}
    foodType: {foodType}
    hindiName: {hindiName}
    typeFood: {typeFood}
    calories: {calories}
    carbs: {carbs}
    fat: {fat}
    protein: {protein}
    fiber: {fiber}
    recipe: {recipe}
    steps: {steps}
    video: {video}
    portion: {portion}
    portion_unit: {portion_unit}
    """
        
        if avoidIn:
            output += f"Avoided by people with: {', '.join(avoidIn)}\n"
        if recommendedIn:
            output += f"Recommended for people with: {', '.join(recommendedIn)}\n"
        if community:
            output += f"Consumed in (States): {', '.join(community)}\n"
        if country:
            output += f"Consumed in (Countries): {', '.join(country)}\n"
        if bpScore is not None:
            output += f"Blood Pressure Score: {bpScore}\n"
        if bpBestSlot:
            output += f"Blood Pressure, Best to be taken: {', '.join(bpBestSlot)}\n"
        if diabetesScore is not None:
            output += f"Diabetes Score: {diabetesScore}\n"
        if diabetesBestSlot:
            output += f"Diabetes, Best to be taken: {diabetesBestSlot}\n"
        if cholestrolScore is not None:
            output += f"Cholestrol Score: {cholestrolScore}\n"
        if cholestrolBestSlot:
            output += f"Cholestrol, Best to be taken: {cholestrolBestSlot}\n"
        if pcosScore is not None:
            output += f"PCOS Score: {pcosScore}\n"
        if pcosBestSlot:
            output += f"PCOS, Best to be taken: {pcosBestSlot}\n"
        if muscleBuildingScore is not None:
            output += f"Muscle Building Score: {muscleBuildingScore}\n"
        if morningBestSlot:
            output += f"Morning Workout, Best to be taken: {morningBestSlot}\n"
        if eveningBestSlot:
            output += f"Evening Workout, Best to be taken: {eveningBestSlot}\n"
        if possibleSlots:
            output += f"Normally Consumed during: {', '.join(map(str, possibleSlots))}\n"
        
        return output

