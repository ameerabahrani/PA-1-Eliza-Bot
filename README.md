# PA-1---Eliza-Bot-
A Python implementation of the ELIZA psychotherapist chatbot. ELIZA simulates conversation by spotting keywords and patterns in user input using regex — it doesn't actually understand anything. The point is to show that you can fake a pretty convincing conversation with just pattern matching and some simple transformations.
No memory, no context. Every response is based only on whatever the user just typed.

Running it
bashpython eliza.py
No arguments needed. Just type in the terminal. To exit, type quit, exit, or bye.

Example
[eliza] Hi, I'm a psychotherapist. What is your name?
=> [user] My name is Ameera
[eliza] Hi Ameera. How are you feeling today?
=> [Ameera] I miss my friends
[eliza] Ameera, What do you miss about your friends?
=> [Ameera] I felt loved, Now i am just lonely
[eliza] Ameera, Do you often feel just lonely?
=> [Ameera] No. I feel angry alot too
[eliza] Ameera, Why do you feel angry alot too?
=> [Ameera] It happens when I dont feel in control of my surroundings
[eliza] How would you feel once you have that?
=> [Ameera] I dont know
[eliza] Could you elaborate on that?
=> [Ameera] Bye
[eliza] Goodbye, Ameera. Take care.

How it works

Asks for the user's name, extracts it with regex.
Loops until the user quits.
Each input goes through:

Transformation rules that flip statements into questions and reflect pronouns
Keyword spotting for emotion-related words
A fallback response if nothing matches
