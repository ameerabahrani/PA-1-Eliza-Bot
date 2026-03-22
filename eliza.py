r"""
eliza.py
Ameera Albahrani
Class: Introduction to NLP

This is a simple implementation of the ELIZA psychotherapist chatbot. 
It is written in python and simulates a conversation by recognizing keywords and patterns in user input, NOT by understanding the meaning of the input.
The goal is to show that a believable conversation can be simulated with simple pattern matching using regex, keyword spotting, and basic transformations.
This code does not store memory or context. Each response is based on the current line of input.
-----------------

This code runs in terminal:
1. Asks the user for their name.
2. Repeatedly accepts user input until the user types "quit", "exit", or "bye".
3. For each user input, it tries to:
    a. Apply simple transformations to turn statements into questions.
    b. Spot keywords related to emotions and respond accordingly.
    c. Uses a generic response if no patterns match.
-----------------
Usage Instructions:

The program runs from the commandline with no arguments:
python eliza.py
*The user can just type responses directly in the terminal after that. The conversation ends when the user types "quit", "exit", or "bye".

-----------------

Example Interaction: 
(1) Broad emotional states
C:\Users\user>python eliza.py
[eliza] Hi, I'm a psychotherapist. What is your name?
=> [user] My name is  Ameera
[eliza] Hi Ameera. How are you feeling today?
=> [Ameera] I miss my friends
[eliza] Ameera, What do you miss about your friends?
=> [Ameera] I miss the companionship
[eliza] Ameera, What do you miss about the companionship?
=> [Ameera] I felt loved, Now i am just lonely
[eliza] Ameera, Do you often feel just lonely?
=> [Ameera] No. I feel angry alot too
[eliza] Ameera, Why do you feel angry alot too?
=> [Ameera] It happens when I dont feel in  control of my surroundings
[eliza] How would you feel once you have that?
=> [Ameera] I think I would finally be happy
[eliza] Ameera, Why do you think you would finally be happy?
=> [Ameera] I dont know
[eliza] Could you elaborate on that?
=> [Ameera] Bye
[eliza] Goodbye, Ameera. Take care.

-----------------
Algorithm: 
1. Greet the user and ask for their name.
3. Extract the name from user input using regex.
4. Enter a loop to accept user input until "quit", "exit", or "bye" is typed.
5. For each user input:
    a. Match and apply transformations to turn statements into questions.
    b. If a transformations matches, reflect pronouns and respond with the transformed question.
    c. If no transformations match, try to spot keywords related to emotions and respond accordingly.
    d. If no keywords match, use a fallback response.
6. End the conversation when the user types "quit", "exit", or "bye".
"""

import re
import random

def pronouns(text):
    #Reflects pronouns in the input text to switch perspectives. These are common pronouns used in therapy.
    #Example: "I want food" -> "you want food", "I miss my friends" -> "you miss your friends"
    reflections = [
        (r"\bi am\b", "you are"),
        (r"\byour\b", "my"),
        (r"\bi\b", "you"),
        (r"\bmy\b", "your"),
        (r"\bme\b", "you"),
        (r"\byou are\b", "I am"),
        (r"\bmyself\b", "yourself"),
    ]

    result = text.lower()
    for pattern, replacement in reflections:
        result = re.sub(pattern, replacement, result)

    return result


#Word spotting : Keywords that show emotion.
#I chose words that are associated with emotional states that are both extreme (desire, control, crave) and colloquial (pissed off, annoyed) for a broader range of emotions. 

WORD_SPOTTING = {
    r"\bangry\b|\bpissed off\b|\bannoyed\b": [
        "Let's talk about what's making you angry",
        "Lets take a deep breath and discuss it.",
        "What is making you feel this way?"
    ],
    r"\bcrave\b|\bcraving\b": [
        "Why do you think you crave that?",
        "Tell me more about your cravings?"
    ],
    r"\bpower\b|\bcontrol\b|\blove\b": [
        "How would you feel once you have that?",
    ],
    r"\bfear\b|\bafraid\b|\bscared\b": [
        "What are you afraid of?",
        "Do these fears trouble you often?",
        "How do you cope with that?",
        "Tell me about these fears?"
    ],
    r"\bsad\b|\bunhappy\b|\bdepressed\b": [
        "I'm sorry you're feeling that way. Can you tell me more about it?",
        "How long have you felt like this?",
        "What would make you feel better?",
        "Lets focus on that."
    ],
    r"\bwant\b|\bdesire\b": [
        "What would that look like?",
        "Why do you want that?"
    ],
}


#Transformation: Simple statement into a question. These are general patterns that can apply to many statements.
#Example: "I want X" = "Why do you want X?"
TRANSFORMATIONS = [
    (r"i feel (.+)", "Why do you feel {}?"),
    (r"i am (.+)", "Do you often feel {}?"),
    (r"i need (.+)", "Why do you need {}?"),
    (r"i miss (.+)", "What do you miss about {}?"),
    (r"i want (.+)", "Why do you want {}?"),
    (r"i think (.+)", "Why do you think {}?"),
]


#Generic responses when no patterns match

GENERIC = [
    "Could you elaborate on that?",
    "I'm not sure I got that.",
    "Could you rephrase that?",
]

def main():

    print("[eliza] Hi, I'm a psychotherapist. What is your name?") #greeting to start
    name_input = input("=> [user] ").strip() 

    # Extract name from input using regex
    match = re.search(r"(?:my name is|i am|it's)\s+(\w+)", name_input, re.IGNORECASE) #common introduction patterns
    name = match.group(1) if match else name_input.split()[0] #default to first word if no match

    # response greeting
    print(f"[eliza] Hi {name}. How are you feeling today?") #start conversation

    while True:
        user_input = input(f"=> [{name}] ").strip() #get the user input

        if user_input.lower() in {"quit", "exit", "bye"}: #exit condition
            print(f"[eliza] Goodbye, {name}. Take care.") 
            break

        lowerCase = user_input.lower() #everything is in lower case to make matching easier

        # 1. Statement transformations
        transformed = False
        for pattern, response_template in TRANSFORMATIONS: #check each transformation pattern
            match = re.search(pattern, lowerCase) #see if it matches
            if match:
                reflected = pronouns(match.group(1)) #reflect pronouns in the matched group, for example "I" to "you". The group(1) is the part that matches the (.+) in the pattern. 
                print(f"[eliza] {name}, " + response_template.format(reflected)) #format the response with the reflected text, for example "Why do you want X?" 
                transformed = True #mark that we found a transformation
                break

        if transformed:
            continue

        # 2. word spotting
        wordSpotted = False

        for pattern, responses in WORD_SPOTTING.items():  #check each keyword pattern
            if re.search(pattern, lowerCase): #check if it matches
                print(f"[eliza] {random.choice(responses)}") #choose a random response from the list
                wordSpotted = True # mark that we found a keyword
                break

        if wordSpotted:
            continue

        # 3. Generic response
        print(f"[eliza] {random.choice(GENERIC)}") #choose a random generic response


# Run
if __name__ == "__main__":
    main()
