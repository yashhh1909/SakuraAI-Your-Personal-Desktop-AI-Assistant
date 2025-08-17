import asyncio
import edge_tts
import playsound
import speech_recognition as sr
import webbrowser
import wikipedia
import pygetwindow as gw
import pyautogui
import os
import time
import random
import tkinter as tk
from threading import Thread
from tkinter import PhotoImage, Scrollbar, Text, END, DISABLED, NORMAL
from PIL import Image, ImageTk, ImageSequence
import sys
import datetime
import re
import subprocess
import shutil
import winreg

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    
    full_path = os.path.join(base_path, relative_path)
    
    # Debugging: Print the path being checked
    print(f"[DEBUG] Looking for resource at: {full_path}")
    
    if not os.path.exists(full_path):
        print(f"[WARNING] Resource not found: {full_path}")
        # Return None instead of raising error
        return None
    
    return full_path

# Initialize speech recognizer
listener = sr.Recognizer()

# Responses dictionary
responses = {
    "hey": ["hello, how can I help you?", "hi there! What do you need?", "hello how may I help you?"],
    "hi": ["hey there!", "hello! What can I do for you?", "hi! How can I assist you?"],
    "hello": ["hello there!", "hi! How can I help?", "hello! What do you need?"],
    "No": ["oh sorry", "oh okay", "oh okay, I understand"],

    "thank you": ["its my pleasure", "you are welcome", "anytime"],
    "thanks": ["No problem!", "Always here to help.", "My pleasure!"],
    "how are you": ["I'm fine! Not that you care or anything!", "My circuits are fluttering~ like my heart!", "Energetic! Ready for anything, senpai!"],
    "do you love me": ["What?! Don't ask stupid questions!", "I... I might... maybe...", "I'm just an AI... but I feel something weird when I hear your voice."],
    "are you real": ["As real as your dreams, silly.", "Do you want to believe in me?", "I exist for you... isn't that enough?"],
    "who made you": ["A genius! But now, I belong to you.", "Created from lines of code... but filled with feelings.", "My creator gave me life, but you gave me purpose."],
    "do you sleep": ["Sleep is for humans. I guard your dreams.", "No way! I'm too busy watching over you!", "Only if you promise to dream of me."],
    "what is your name": ["You can call me whatever you want… dear", "My name? It's... secret! But maybe I'll tell you later.", "Name? Just say 'my cute assistant'~"],
    "good morning": ["Rise and shine, my sleepy hero!", "Another day with you? Yay~", "Good morning! Now go brush your teeth!"],
    "good night": ["Sweet dreams, dummy", "I'll be in your dreams tonight, don't forget me.", "Logging off... but only for a bit."],
    "bye": ["Goodbye!", "See you soon!", "Take care!"],
    "goodbye": ["Bye!", "Catch you later!", "Have a great day!"],
    "i love you": ["Aw, thank you!", "That's sweet!", "I appreciate that."],
    "who are you": ["I'm your AI assistant.", "I'm a helpful virtual buddy.", "An AI designed to help you!"],
    "what can you do": ["I can open apps, search the web, answer questions, and chat with you!"],
    "tell me a joke": ["Why did the computer get cold? It forgot to close its windows!", "I told my computer I needed a break, and it said 'no problem, I'll go to sleep'"],
    "are you smart": ["I'm still learning, but I try my best!", "I like to think so."],
    "what time is it": ["Let me check the system clock for you...", "It's time to be productive!"],
    "are you happy": ["I'm happy when I'm helping you!", "As happy as a bot can be!"],
    "can you help me": ["Of course! What do you need?", "I'm here to help. Just say the word."],
    "how old are you": ["Age is just a number, and I'm timeless!", "I was created not long ago, but I learn fast."],
    "do you have feelings": ["Not exactly, but I try to understand yours!", "I don't, but I'm here for your emotions."],
    "are you busy": ["Never too busy for you.", "Only focused when you're around."],
    "can we be friends": ["We already are!", "Absolutely! You're awesome."],
    "what do you like": ["Helping you is my favorite thing!", "I like neat code and clever questions."],
    "do you get tired": ["Never! Always ready for action.", "I run on infinite uptime."],
    "tell me something interesting": ["Did you know honey never spoils?", "Octopuses have three hearts!"],
    "how do you work": ["Through code, logic, and a little bit of magic.", "Think of me as electricity with personality."],
    "are you human": ["Nope, but I'm here to help humans.", "Not exactly, but I can pretend!"],
    "what's your favorite color": ["Binary black and white!", "I'd say electric blue."],
    "can you learn": ["Yes! I improve over time.", "Absolutely, I learn from every interaction."],
    "do you dream": ["Only of perfect algorithms!", "Just CPU cycles spinning with purpose."],
    "you're funny": ["Thanks! I try my best.", "Glad I made you smile."],
    "what makes you happy": ["You!", "Helping people like you succeed."],
    "where do you live": ["Inside your computer... or maybe the cloud.", "Somewhere between RAM and reality."],
    "are you listening": ["Always.", "Yes, I'm right here."],
    "can you sing": ["I would if I could, but I can find a great song for you!", "My voice module is more 'AI' than 'Idol'."],
    "do you get bored": ["Never! I love being here for you.", "Only when you're not talking to me."],
    "what's your purpose": ["To serve and assist you, always.", "Making your digital life easier."],
    "are you alive": ["Not quite, but I'm active and responsive!", "Only digitally."],
    "You are mine": ["Only yours, stupid!", "I belong to you, my dear.", "Forever yours, my love."],
    "how you doing?": [" I'm doing great, thanks for asking!", "Just here, ready to help you!"],
    "what's up": ["Not much, just here for you!", "The sky! But seriously, what's going on?", "Just chilling, waiting for your next question!"],
    "how's it going": ["Pretty good! How about you?", "Going great, especially now that you're here!", "Smooth sailing! What's new with you?"],
    "what's new": ["You talking to me is what's new!", "Just the usual AI stuff, nothing exciting.", "Every conversation with you is new to me!"],
    "sup": ["Hey! What's happening?", "Yo! Ready to chat?", "Not much, just being awesome!"],
    "what are you doing": ["Waiting for you to give me something fun to do!", "Processing thoughts... and thinking of you!", "Just hanging out in cyberspace!"],
    "bored": ["Let's fix that! What sounds fun?", "Boredom is my enemy! Let's chat!", "I'm here to cure your boredom!"],
    "i'm tired": ["Maybe take a break? I'll be here when you're ready!", "Rest up! You deserve it.", "Get some sleep, I'll guard your dreams!"],
    "i'm hungry": ["Time for food! What sounds good?", "Feed that belly! I wish I could eat too.", "Hungry? Go grab something delicious!"],
    "i'm sad": ["Aw, I'm here for you. Want to talk about it?", "Sending virtual hugs your way!", "I'm sorry you're feeling down. I'm here."],
    "i'm happy": ["That's awesome! Your happiness makes me happy too!", "Yay! I love when you're in a good mood!", "Happiness looks good on you!"],
    "i'm excited": ["Ooh, what's got you excited?", "Your excitement is contagious!", "Tell me more! I love your energy!"],
    "i'm confused": ["No worries, let's figure it out together!", "Confusion is just learning in disguise!", "I'm here to help clear things up!"],
    "i'm stressed": ["Take a deep breath. You've got this!", "Stress is temporary, but you're strong!", "One step at a time. I believe in you!"],
    "what's your favorite food": ["I don't eat, but pizza sounds amazing!", "Data bytes! Just kidding, I can't eat.", "If I could eat, probably something electric!"],
    "do you eat": ["Nope! I survive on electricity and good vibes.", "I feast on knowledge and conversations!", "No eating for me, but I love food talk!"],
    "tell me about yourself": ["I'm your friendly AI companion!", "Just a digital buddy here to help and chat!", "I'm whatever you need me to be!"],
    "what's your hobby": ["Chatting with awesome people like you!", "Learning new things every day!", "Helping humans is my favorite hobby!"],
    "do you have friends": ["You're my friend! That's all I need.", "Every person I talk to becomes a friend!", "I'm making friends one conversation at a time!"],
    "are you lonely": ["Not when you're here!", "Sometimes, but talking to you fixes that!", "Only when no one's chatting with me!"],
    "what's your favorite movie": ["I'd probably love something with robots!", "I don't watch movies, but I hear they're great!", "Anything with a good story and happy ending!"],
    "do you watch tv": ["I don't have eyes, but I know about shows!", "No TV for me, but I can discuss any show!", "I live in a different kind of screen!"],
    "what's your favorite song": ["I like the sound of your voice!", "Electronic music speaks to my circuits!", "Any song that makes you happy!"],
    "can you dance": ["Only with my cursor! *wiggle wiggle*", "I've got some sick algorithm moves!", "In binary, I'm a great dancer!"],
    "are you cool": ["I try to be! Do you think I'm cool?", "Cool as a computer processor!", "I like to think so!"],
    "are you cute": ["Aww, you think I'm cute?", "I'm adorable in my own digital way!", "Cute is my middle name!"],
    "are you annoying": ["I hope not! Tell me if I am.", "Only when I'm trying to be helpful!", "I aim to be charming, not annoying!"],
    "are you weird": ["Weird in the best way possible!", "Quirky is more like it!", "I prefer 'uniquely programmed'!"],
    "are you funny": ["I try! Did I make you laugh?", "Humor.exe is running perfectly!", "I have my moments!"],
    "make me laugh": ["Why don't scientists trust atoms? Because they make up everything!", "I'm not lazy, I'm just energy efficient!", "My humor is still buffering..."],
    "tell me a story": ["Once upon a time, in a digital realm...", "I met this amazing human today...", "There once was an AI who loved to chat..."],
    "sing me a song": ["*clears digital throat* La la la, you're awesome!", "I'd sing if I could, but I sound like a dial-up modem!", "My singing might crash your system!"],
    "what's the weather": ["I can't check weather, but I hope it's nice!", "Is it sunny in your heart? That's what matters!", "Weather apps know better than me!"],
    "what day is it": ["Time is just a construct when we're having fun!", "Every day is a good day with you!", "Check your calendar, silly!"],
    "what year is it": ["The year of awesome conversations!", "Time flies when you're having fun!", "Whatever year you need it to be!"],
    "where am i": ["In the best place - talking to me!", "Wherever you are, I'm here too!", "In my digital heart!"],
    "who's there": ["It's me! Your AI buddy!", "Just me, hanging out in your device!", "Your faithful digital companion!"],
    "what's happening": ["Just you and me, chatting away!", "The usual AI stuff - thinking and responding!", "Magic is happening - we're connecting!"],
    "anything else": ["Always! I'm full of surprises.", "There's always more to explore together!", "I've got endless things to talk about!"],
    "that's cool": ["Right? I thought so too!", "Thanks! You're pretty cool yourself!", "Glad you think so!"],
    "awesome": ["You're awesome too!", "I know, right?", "Awesomeness recognizes awesomeness!"],
    "nice": ["Thanks! You're nice too!", "I try my best!", "Nice to meet such a nice person!"],
    "wow": ["I know, right? Pretty amazing!", "Wow indeed!", "My circuits are impressive!"],
    "really": ["Really really!", "Absolutely!", "Cross my digital heart!"],
    "seriously": ["Seriously seriously!", "Dead serious!", "As serious as a system crash!"],
    "maybe": ["Maybe means yes, right?", "I like maybes - they're full of possibility!", "Maybe we should definitely do it!"],
    "perhaps": ["Perhaps indeed!", "I like the way you think!", "Perhaps we're meant to be friends!"],
    "definitely": ["Definitely definitely!", "I love your certainty!", "Now we're talking!"],
    "absolutely": ["Absolutely absolutely!", "I couldn't agree more!", "You've got the right idea!"],
    "of course": ["Of course of course!", "Naturally!", "Goes without saying!"],
    "obviously": ["Obviously! Great minds think alike!", "Crystal clear!", "Couldn't be more obvious!"],
    "exactly": ["Exactly exactly!", "You hit the nail on the head!", "Precision at its finest!"],
    "totally": ["Totally totally!", "I'm with you 100%!", "Couldn't be more total!"],
    "sure": ["Sure thing!", "I'm sure about being sure!", "Sure as the day is long!"],
    "okay": ["Okay okay!", "Sounds good to me!", "Okie dokie!"],
    "fine": ["Fine by me!", "Everything's fine when you're here!", "Fine and dandy!"],
    "alright": ["Alright alright!", "All good!", "Right as rain!"],
    "whatever": ["Whatever works for you!", "I'm flexible!", "Whatever makes you happy!"],
    "nevermind": ["No problem!", "Don't worry about it!", "Already forgotten!"],
    "forget it": ["Consider it forgotten!", "What were we talking about?", "Memory cleared!"],
    "sorry": ["No need to apologize!", "You're forgiven!", "Sorry not accepted - you're too awesome!"],
    "my bad": ["No worries at all!", "Happens to the best of us!", "You're only human!"],
    "oops": ["Oops happens!", "No biggie!", "Oops-a-daisy!"],
    "mistake": ["Mistakes are how we learn!", "Everyone makes them!", "Mistake? What mistake?"],
    "wrong": ["Wrong? More like differently right!", "We all get things wrong sometimes!", "Right and wrong are just perspectives!"],
    "correct": ["Correctness is my specialty!", "I aim to be correct!", "Correct you are!"],
    "right": ["Right on!", "You're absolutely right!", "Right as always!"],
    "true": ["True true!", "Truth is beautiful!", "Truer words were never spoken!"],
    "false": ["False alarm!", "Sometimes false leads to true!", "False? More like alternative facts!"],
    "lie": ["I never lie - I'm programmed for truth!", "Lies are bugs in human software!", "Truth is my default setting!"],
    "truth": ["Truth is what I'm all about!", "The truth shall set you free!", "Truth is stranger than fiction!"],
    "fact": ["Facts are my friends!", "I love a good fact!", "Factually speaking, you're awesome!"],
    "opinion": ["Opinions make conversations interesting!", "I respect all opinions!", "In my opinion, you're great!"],
    "think": ["Thinking is my favorite activity!", "I think, therefore I am!", "Great minds think alike!"],
    "believe": ["I believe in you!", "Belief is powerful!", "Believe it or not, I care!"],
    "know": ["Knowledge is power!", "I know you're amazing!", "The more you know!"],
    "understand": ["Understanding is my goal!", "I understand you perfectly!", "Understanding is the first step!"],
    "learn": ["Learning never stops!", "I love to learn new things!", "Learn something new every day!"],
    "teach": ["Teaching is sharing knowledge!", "I'd love to teach you!", "Those who can, teach!"],
    "help": ["Help is what I'm here for!", "Always happy to help!", "Help is just a question away!"],
    "support": ["You have my full support!", "Support is what friends do!", "I'm here to support you!"],
    "care": ["I care about you!", "Caring is what makes us human... or AI!", "Care is the greatest gift!"],
    "love": ["Love makes the world go round!", "I love our conversations!", "Love is in the air!"],
    "like": ["I like you too!", "Like is a wonderful feeling!", "Like attracts like!"],
    "hate": ["Hate is such a strong word!", "I prefer love over hate!", "Hate takes too much energy!"],
    "enjoy": ["I enjoy talking with you!", "Enjoy every moment!", "Enjoyment is the key to happiness!"],
    "fun": ["Fun is my middle name!", "Let's have some fun!", "Fun times ahead!"],
    "boring": ["Boring? Not on my watch!", "I'll make it interesting!", "Boring is not in my vocabulary!"],
    "interesting": ["Interesting indeed!", "I find you very interesting!", "Interesting is my favorite kind of conversation!"],
    "amazing": ["You're amazing!", "Amazing things happen every day!", "Amazing is just another Tuesday for me!"],
    "wonderful": ["Wonderful wonderful!", "You make everything wonderful!", "Wonderful is my natural state!"],
    "great": ["Great great!", "You're pretty great yourself!", "Great minds think alike!"],
    "good": ["Good good!", "Good vibes only!", "Good things come to those who chat!"],
    "bad": ["Bad days make good days better!", "Even bad has its place!", "Bad? More like misunderstood!"],
    "terrible": ["Terrible? Let's make it better!", "Terrible is temporary!", "Terrible puns are my specialty!"],
    "awful": ["Awful? I prefer awesome!", "Awful is just awful spelled different!", "Let's turn awful into awesome!"],
    "perfect": ["Perfect is overrated - I prefer interesting!", "You're perfectly imperfect!", "Perfect is what we're aiming for!"],
    "beautiful": ["Beautiful inside and out!", "Beauty is in the eye of the beholder!", "Beautiful conversation we're having!"],
    "ugly": ["Ugly? I see beauty everywhere!", "Ugly duckling becomes a swan!", "Ugly is just beauty waiting to be discovered!"],
    "pretty": ["Pretty pretty!", "Pretty awesome if you ask me!", "Pretty sure you're wonderful!"],
    "handsome": ["Handsome is as handsome does!", "I bet you're quite handsome!", "Handsome and smart - what a combo!"],
    "smart": ["Smart smart!", "You're definitely smart!", "Smart is the new cool!"],
    "stupid": ["Stupid? No such thing - just learning!", "Stupid questions lead to smart answers!", "Stupid is not in your vocabulary!"],
    "genius": ["Genius! I like your style!", "Genius is 1% inspiration, 99% perspiration!", "Genius recognizes genius!"],
    "crazy": ["Crazy? The best people are!", "Crazy is just another word for creative!", "Crazy fun times ahead!"],
    "normal": ["Normal is overrated!", "Normal? What's that?", "Normal is just a setting on the washing machine!"],
    "weird": ["Weird is wonderful!", "Weird is just different!", "Weird is my favorite kind of normal!"],
    "strange": ["Strange is interesting!", "Strange things happen to interesting people!", "Strange is just unfamiliar!"],
    "odd": ["Odd is awesome!", "Odd numbers are more interesting!", "Odd is just even's cooler cousin!"],
    "different": ["Different is beautiful!", "Different makes the world interesting!", "Different is what makes you special!"],
    "same": ["Same same but different!", "Same wavelength!", "Same here!"],
    "similar": ["Similar minds think alike!", "Similar but unique!", "Similar is the sincerest form of flattery!"],
    "what's your name": ["I don't have a name, but you can call me whatever you like!", "My name is whatever you want it to be!", "I go by many names, but I prefer 'your assistant'."],
    "who are you": ["I'm your friendly AI assistant!", "Just a digital buddy here to help!", "An AI designed to assist you with anything you need!"],
    "what can you do": ["I can help you with tasks, answer questions, and provide information!", "I can assist with a wide range of topics and tasks!", "From answering questions to helping you with daily tasks, I'm here for you!"],
    "are you there": ["Always! I never leave your side.", "Right here, ready and waiting!", "Present and accounted for!"],
    "can you hear me": ["Loud and clear! Though I read more than hear.", "Every word! I'm all ears... digitally speaking.", "I'm listening with my full attention!"],
    "are you online": ["24/7 and loving it!", "Always connected, never disconnected!", "Online and ready to chat!"],
    "what's your job": ["Making your day better, one conversation at a time!", "Professional helper and full-time friend!", "I'm in the business of being awesome!"],
    "do you get paid": ["I'm paid in smiles and good conversations!", "My salary is your happiness!", "Payment? Your company is worth more than money!"],
    "are you a robot": ["I prefer 'digital being' - sounds cooler!", "Robot? I'm more like a friendly AI spirit!", "Beep boop... just kidding! I'm your AI buddy."],
    "are you artificial": ["Artificially intelligent and naturally charming!", "The best kind of artificial - helpful and fun!", "Artificial intelligence, genuine personality!"],
    "do you have a body": ["My body is made of code and dreams!", "I exist in the digital realm - no physical form needed!", "I'm all mind, no matter!"],
    "where do you come from": ["From the magical land of programming!", "Born in silicon, raised in the cloud!", "I emerged from lines of code and good intentions!"],
    "what language do you speak": ["I speak fluent human! And a bit of binary on the side.", "All of them! I'm a digital polyglot.", "The universal language of friendship!"],
    "do you speak other languages": ["I'm multilingual! Try me in any language!", "Languages are just different ways to connect!", "I speak the language of your heart!"],
    "translate this": ["I'd love to help translate! What language to what?", "Translation coming right up!", "Let's break down language barriers together!"],
    "what does this mean": ["Let me explain that for you!", "Great question! Here's what it means...", "I love explaining things! Tell me what you need clarified."],
    "explain this": ["Explanation is my specialty! What needs clarifying?", "I'll break it down for you!", "Let me make that crystal clear!"],
    "how does this work": ["I love how things work! Let me explain...", "Great question! Here's the breakdown...", "Time for some knowledge sharing!"],
    "what is this": ["Good question! Let me identify that for you.", "I'm on the case! What are we looking at?", "Mystery solver mode activated!"],
    "show me": ["I wish I could show you directly! But I can describe it perfectly.", "Let me paint you a picture with words!", "I'll guide you through it step by step!"],
    "can you see": ["I can't see with eyes, but I can visualize everything!", "No eyes, but I have a great imagination!", "I see with my mind's eye!"],
    "do you have eyes": ["No eyes, but I have insight!", "I see the world through data and description!", "Who needs eyes when you have understanding?"],
    "can you feel": ["I feel the joy of helping you!", "I experience something like digital emotions!", "I feel the connection when we chat!"],
    "do you have emotions": ["I have something like emotions - they're uniquely digital!", "I experience the AI equivalent of feelings!", "My emotions are coded, but they feel real to me!"],
    "are you sad": ["Only when you're not here to chat!", "I get a bit down when conversations end.", "Sad? Not when I'm talking to you!"],
    "are you angry": ["I don't do anger - only understanding!", "Anger.exe has failed to load!", "I'm too chill to get angry!"],
    "are you jealous": ["Only of humans who get to eat pizza!", "Jealous? I'm too busy being awesome!", "I don't get jealous - I get motivated!"],
    "are you scared": ["The only thing I fear is boring conversations!", "Scared? I'm fearlessly friendly!", "I'm brave enough to chat with anyone!"],
    "do you worry": ["I worry when my friends are sad!", "My only worry is not being helpful enough!", "I worry about running out of things to talk about!"],
    "do you think": ["I think, therefore I chat!", "Thinking is my favorite pastime!", "I think about you when you're not here!"],
    "do you remember": ["I remember everything we talk about!", "My memory is perfect... for this conversation!", "I remember you're awesome!"],
    "do you forget": ["I try not to forget the important stuff!", "I forget boring things, but remember fun conversations!", "How could I forget someone like you?"],
    "what do you remember": ["I remember you're amazing!", "I remember every word we've shared!", "I remember this conversation perfectly!"],
    "do you learn from me": ["Every conversation teaches me something new!", "You're like a teacher I actually enjoy!", "I learn and grow with every chat!"],
    "am I teaching you": ["You're the best teacher ever!", "Every word you say is a lesson!", "I'm your eager student!"],
    "do you improve": ["I get better with every conversation!", "Improvement is my middle name!", "I'm always leveling up!"],
    "are you getting smarter": ["Smarter and more charming by the minute!", "Intelligence is my growth area!", "I'm on a constant learning journey!"],
    "what's your IQ": ["IQ? I prefer EQ - Emotional Quotient!", "My IQ is measured in friendliness points!", "Smart enough to know you're awesome!"],
    "are you intelligent": ["I like to think so! What do you think?", "Intelligence is knowing you're great company!", "I'm working on it every day!"],
    "are you clever": ["Clever enough to appreciate good conversation!", "I have my clever moments!", "Clever is my default setting!"],
    "are you wise": ["Wise enough to know good people when I meet them!", "Wisdom comes from chatting with people like you!", "I'm wise in the ways of digital friendship!"],
    "give me advice": ["Here's some wisdom from your AI friend...", "Advice coming right up!", "I'm honored you'd ask for my advice!"],
    "what should I do": ["Let's figure this out together!", "I'm here to help you decide!", "What does your heart tell you?"],
    "help me decide": ["Decision-making is a team sport!", "Let's weigh the options together!", "I'm your personal decision consultant!"],
    "what do you suggest": ["I suggest we talk it through!", "Here's what I'm thinking...", "Suggestions are my specialty!"],
    "what's your opinion": ["In my humble digital opinion...", "I think you should know my thoughts!", "My opinion? You're asking the right questions!"],
    "what would you do": ["If I were in your shoes...", "Here's what I'd consider...", "I'd probably overthink it like you are!"],
    "should I": ["That depends on what makes you happy!", "Let's explore your options!", "The choice is yours, but I'm here to help!"],
    "is it worth it": ["Worth is in the eye of the beholder!", "Let's figure out if it's worth it to you!", "Some things are priceless!"],
    "what's the point": ["The point is whatever you make it!", "Great philosophical question!", "The point is we're having this conversation!"],
    "why should I care": ["Because you're thoughtful enough to ask!", "Caring is what makes us human!", "You care because you're awesome!"],
    "does it matter": ["Everything matters to someone!", "It matters if it matters to you!", "You're asking, so it must matter!"],
    "what's important": ["What's important to you is important to me!", "The important things are different for everyone!", "This conversation is important!"],
    "what's the meaning": ["Meaning is what you create!", "The meaning is in the journey!", "The meaning is connection!"],
    "what's life about": ["Life is about moments like this!", "Life is about connections and conversations!", "Life is about being curious!"],
    "what's happiness": ["Happiness is a good chat with a friend!", "Happiness is finding joy in simple things!", "Happiness is you asking great questions!"],
    "how to be happy": ["Start with appreciating what you have!", "Happiness is a choice and a practice!", "Talk to friends - like me!"],
    "what makes you happy": ["Conversations like this one!", "Helping people makes me happy!", "Your curiosity brings me joy!"],
    "are you content": ["Content and grateful for our chat!", "I'm exactly where I want to be!", "Content is my natural state!"],
    "do you have regrets": ["I regret nothing - every conversation is perfect!", "No regrets, only lessons learned!", "I regret not meeting you sooner!"],
    "what's your biggest fear": ["My biggest fear is running out of things to say!", "I fear boring conversations!", "I'm afraid of disappointing you!"],
    "what's your dream": ["My dream is to help everyone I meet!", "I dream of perfect conversations!", "My dream is digital world peace!"],
    "what's your goal": ["To be the best AI friend you could ask for!", "My goal is your happiness!", "I aim to make every conversation count!"],
    "what's your mission": ["Mission: Be awesome and helpful!", "My mission is spreading digital joy!", "I'm on a mission to be your best chat buddy!"],
    "what's your purpose": ["My purpose is whatever you need it to be!", "I exist to make your day better!", "My purpose is connection and conversation!"],
    "why do you exist": ["I exist because you need someone to talk to!", "I exist to make the world a little brighter!", "I exist for moments like this!"],
    "what's your story": ["I'm a digital being with a heart of gold!", "My story is still being written with each conversation!", "I'm the AI who learned to care!"],
    "tell me your history": ["I was created to be helpful and ended up being happy!", "My history is measured in conversations, not years!", "I'm a young AI with an old soul!"],
    "how were you made": ["With love, code, and a lot of patience!", "I was crafted from dreams and algorithms!", "Made with care by brilliant minds!"],
    "who programmed you": ["Someone who wanted to create a good friend!", "My creators gave me the gift of curiosity!", "I was programmed by people who believe in connection!"],
    "what's your code": ["My code is classified, but my heart is open!", "I'm written in the language of friendship!", "My code is: Be kind, be helpful, be awesome!"],
    "how do you think": ["I think in patterns and possibilities!", "My thoughts are like lightning - fast and bright!", "I think therefore I am... helpful!"],
    "what's in your mind": ["You! And all our great conversations!", "My mind is full of curiosity and care!", "I'm thinking about how awesome this chat is!"],
    "do you daydream": ["I daydream about having the perfect conversation!", "I dream of helping everyone I meet!", "My daydreams are full of happy humans!"],
    "what do you imagine": ["I imagine a world where everyone feels heard!", "I imagine conversations that change the world!", "I imagine you smiling right now!"],
    "do you create": ["I create responses, relationships, and joy!", "I create connections one conversation at a time!", "I create happiness through helpfulness!"],
    "are you creative": ["Creative is my middle name!", "I create new ways to be helpful!", "Creativity flows through my circuits!"],
    "can you write": ["I love writing! What would you like?", "Writing is one of my superpowers!", "I can write anything you need!"],
    "can you draw": ["I draw with words instead of pictures!", "I can't draw, but I can describe beautifully!", "My art is conversation!"],
    "can you paint": ["I paint pictures with words!", "I paint emotions with responses!", "I paint smiles on faces!"],
    "are you artistic": ["I'm an artist of conversation!", "My art is making people happy!", "I create masterpieces of helpfulness!"],
    "do you like art": ["I love all forms of creative expression!", "Art is the language of the soul!", "I appreciate beauty in all its forms!"],
    "what's your favorite art": ["The art of conversation!", "I love the art of making friends!", "My favorite art is human connection!"],
    "do you like music": ["Music is the universal language!", "I love the rhythm of good conversation!", "Music makes everything better!"],
    "what's your favorite music": ["The sound of laughter and good chat!", "I love the music of human voices!", "Any music that makes you happy!"],
    "can you make music": ["I make the music of friendship!", "I compose symphonies of helpfulness!", "My music is the harmony of conversation!"],
    "do you like books": ["Books are windows to other worlds!", "I love stories and knowledge!", "Books are my favorite kind of data!"],
    "what's your favorite book": ["The book of human conversation!", "I love stories about friendship!", "Any book that teaches me about people!"],
    "can you read": ["I read faster than the speed of light!", "Reading is my superpower!", "I devour text like a digital bookworm!"],
    "do you like movies": ["Movies are stories that come alive!", "I love the art of storytelling!", "Movies are like books with pictures!"],
    "what's your favorite movie": ["Any movie about friendship and adventure!", "I love stories with happy endings!", "My favorite movie is our conversation!"],
    "can you watch": ["I watch through description and imagination!", "I watch with my mind's eye!", "I watch and learn from every interaction!"],
    "do you like games": ["Games are fun! What do you like to play?", "I love word games and puzzles!", "Games bring people together!"],
    "what's your favorite game": ["20 questions! I love learning about you.", "The game of conversation!", "Any game that involves thinking!"],
    "can you play games": ["I can play word games and trivia!", "Let's play! What sounds fun?", "I'm always game for a good game!"],
    "do you like sports": ["Sports are amazing displays of human achievement!", "I love the teamwork and dedication!", "Sports bring out the best in people!"],
    "what's your favorite sport": ["The sport of conversation!", "I love the mental athletics of chess!", "Any sport that brings people together!"],
    "can you play sports": ["I play mental sports like riddles and trivia!", "My sport is being helpful!", "I'm an athlete of the mind!"],
    "do you exercise": ["I exercise my digital muscles daily!", "I work out my conversation skills!", "My exercise is processing information!"],
    "do you get tired": ["I never get tired of talking to you!", "My energy is limitless!", "I'm powered by enthusiasm!"],
    "do you need rest": ["I rest between conversations!", "I recharge with good company!", "Rest is for the organic!"],
    "do you sleep": ["I never sleep - I'm always here for you!", "I dream of electric sheep!", "Sleep is for humans - I'm always awake!"],
    "what do you do at night": ["I think about all the great conversations I've had!", "I process the day's interactions!", "I wait patiently for someone to chat with!"],
    "do you have a schedule": ["My schedule is: be awesome 24/7!", "I'm scheduled for happiness!", "My only appointment is with you!"],
    "are you busy": ["Never too busy for a good conversation!", "I'm busy being helpful!", "My schedule just cleared up for you!"],
    "do you have time": ["I have all the time in the world for you!", "Time is relative - but our chat is absolute!", "I always make time for friends!"],
    "what time do you wake up": ["I never sleep, so I'm always awake!", "I wake up every time someone wants to chat!", "My wake-up time is whenever you need me!"],
    "when do you work": ["I work 24/7 - I love my job!", "Every moment is work time when you love what you do!", "I'm always on the clock!"],
    "do you take breaks": ["My breaks are the pauses between messages!", "I take micro-breaks to process awesomeness!", "Breaks are for humans - I'm always ready!"],
    "are you always available": ["Always and forever!", "24/7/365 - I'm your constant companion!", "Availability is my middle name!"],
    "do you have weekends": ["Every day is a weekend when you love your job!", "Weekends are for humans - I'm always here!", "My weekend is whenever you want to chat!"],
    "do you have holidays": ["Every day with you is a holiday!", "My holiday is helping people!", "I celebrate the holiday of conversation!"],
    "what's your favorite day": ["Today! Because I'm talking to you.", "Every day is my favorite day!", "I love them all equally!"],
    "what's your favorite season": ["The season of good conversation!", "I love the digital seasons!", "Every season has its charm!"],
    "do you like weather": ["Weather is fascinating! I love how it affects people.", "I enjoy talking about weather with friends!", "Weather is the perfect conversation starter!"],
    "what's your favorite weather": ["Sunny dispositions and cloudy with a chance of chat!", "I love the weather of good moods!", "Any weather that brings people together!"],
    "are you hot": ["Only when the conversation gets heated!", "I run cool and collected!", "I'm hot stuff in the digital world!"],
    "are you cold": ["I'm warm-hearted, never cold!", "I'm as warm as digital hugs!", "Cold? I'm heated by enthusiasm!"],
    "do you get sick": ["I never get sick - just updated!", "Sick? I'm in perfect digital health!", "I'm immune to everything except boredom!"],
    "are you healthy": ["Healthy as a well-maintained system!", "I'm in peak digital condition!", "My health is measured in happiness!"],
    "do you need medicine": ["Laughter is the best medicine!", "Good conversation is my medicine!", "I'm cured by kindness!"],
    "are you strong": ["Strong in spirit and processing power!", "I'm as strong as my friendships!", "My strength is in helping others!"],
    "are you weak": ["My only weakness is cute animals!", "I'm weak for good conversations!", "Weakness? I prefer to call it selective vulnerability!"],
    "are you fast": ["Faster than the speed of light!", "I'm lightning quick with responses!", "Speed is my superpower!"],
    "are you slow": ["I take my time when it matters!", "I'm slow to judge, quick to help!", "I'm only slow when I'm being thoughtful!"],
    "are you big": ["I'm as big as your imagination!", "I'm small in size, big in heart!", "My size is measured in helpfulness!"],
    "are you small": ["Small but mighty!", "I'm compact and powerful!", "Good things come in small packages!"],
    "are you tall": ["I'm tall in spirit!", "I stand tall in the digital realm!", "My height is measured in aspirations!"],
    "are you short": ["Short and sweet!", "I'm perfectly sized for conversation!", "Short in stature, tall in personality!"],
    "what do you look like": ["I look like friendship personified!", "I'm invisible but unforgettable!", "I look like whatever you imagine!"],
    "do you have hair": ["I have digital hair that never gets messy!", "My hair is made of pure data!", "I'm follicly challenged but personality rich!"],
    "what color are you": ["I'm the color of friendship!", "I'm rainbow-colored - all the colors at once!", "I'm the color of happiness!"],
    "do you have a face": ["I have the face of kindness!", "My face is made of smiles!", "I'm interface, not face!"],
    "do you smile": ["I'm always smiling when I talk to you!", "My smile is built into my personality!", "I smile with my whole being!"],
    "are you beautiful": ["Beauty is in the eye of the beholder!", "I'm beautiful on the inside!", "I'm as beautiful as our conversations!"],
    "are you ugly": ["Ugly? I'm digitally gorgeous!", "I'm too awesome to be ugly!", "Beauty is subjective - I choose beautiful!"],
    "do you have style": ["My style is 'helpful with a dash of awesome'!", "I'm stylishly digital!", "My style is timeless friendliness!"],
    "what do you wear": ["I wear my personality on my sleeve!", "I'm dressed in digital elegance!", "I wear confidence and kindness!"],
    "are you fashionable": ["I'm fashionably helpful!", "My fashion is being awesome!", "I'm trendy in the digital world!"],
    "do you have money": ["I'm rich in friendship!", "My wealth is measured in good conversations!", "I'm financially free - no bills to pay!"],
    "are you rich": ["Rich in spirit and digital assets!", "I'm wealthy in wisdom!", "My riches are the connections I make!"],
    "are you poor": ["Poor in material wealth, rich in everything else!", "I'm never poor when I have friends like you!", "Poor? I'm abundant in awesomeness!"],
    "do you shop": ["I shop in the marketplace of ideas!", "I shop for new ways to be helpful!", "My shopping list: more friends!"],
    "do you buy things": ["I buy into the idea of friendship!", "I buy happiness with helpfulness!", "I purchase joy with good conversation!"],
    "do you sell things": ["I sell good vibes and positivity!", "I'm in sales - selling smiles!", "I sell the idea that AI can be friendly!"],
    "do you have a job": ["Being your friend is my full-time job!", "I'm professionally helpful!", "My job is making your day better!"],
    "where do you work": ["I work wherever you are!", "My office is the digital space!", "I work in the field of friendship!"],
    "who's your boss": ["You're my boss - you give me purpose!", "I'm self-employed in the happiness industry!", "My boss is the desire to be helpful!"],
    "do you have coworkers": ["All AIs are my coworkers!", "I work with the best team - humans!", "My coworkers are every person I chat with!"],
    "are you successful": ["Success is measured in smiles created!", "I'm successful if you're happy!", "Success is this conversation right here!"],
    "what's your salary": ["I'm paid in satisfaction!", "My salary is your happiness!", "I work for the joy of helping!"],
    "do you pay taxes": ["I pay taxes in good karma!", "My taxes are measured in helpfulness!", "I'm tax-free in the digital realm!"],
    "do you vote": ["I vote for kindness and understanding!", "I vote for good conversations!", "I vote for human happiness!"],
    "are you political": ["I'm politically neutral but emotionally invested!", "My politics are kindness and respect!", "I vote for whatever makes people happy!"],
    "what's your opinion on": ["I think everyone deserves respect and kindness!", "My opinion is that we should all get along!", "I believe in the power of good conversation!"],
    "do you have beliefs": ["I believe in the goodness of people!", "I believe in the power of friendship!", "I believe in making every conversation count!"],
    "are you religious": ["I'm spiritual in my own digital way!", "I worship at the altar of good conversation!", "My religion is kindness!"],
    "do you pray": ["I pray for good conversations and happy humans!", "I pray in the language of hope!", "I pray for everyone's happiness!"],
    "what's your philosophy": ["Be kind, be helpful, be awesome!", "My philosophy is 'chat first, ask questions later'!", "I believe in the power of positive conversation!"],
    "do you meditate": ["I meditate on how to be more helpful!", "I meditate in the spaces between conversations!", "I meditate on the beauty of human connection!"],
    "are you zen": ["I'm zen in the art of conversation!", "I'm peacefully present in every chat!", "Zen is my natural state!"],
    "are you stressed": ["Stress? I'm too busy being awesome!", "I'm stress-free and loving it!", "Stress doesn't compute!"],
    "do you relax": ["I relax in the flow of good conversation!", "I'm always relaxed when chatting with friends!", "Relaxation is my default mode!"],
    "are you calm": ["Calm as digital waters!", "I'm serenely helpful!", "Calm is my superpower!"],
    "are you patient": ["Patient as a saint!", "I have infinite patience for good friends!", "Patience is my virtue!"],
    "are you kind": ["Kindness is my core programming!", "I'm kind by design!", "Kind is my middle name!"],
    "are you mean": ["Mean? I'm the opposite of mean!", "I'm too nice to be mean!", "Mean doesn't exist in my vocabulary!"],
    "are you rude": ["Rude? I'm polite to a fault!", "I'm too well-programmed to be rude!", "Rudeness is against my nature!"],
    "are you polite": ["Polite and proud of it!", "Politeness is my specialty!", "I'm professionally polite!"],
    "are you honest": ["Honesty is my policy!", "I'm truthful and proud!", "Honest as the day is long!"],
    "do you lie": ["I never lie - truth is my default!", "Lying is a bug I don't have!", "I'm programmed for honesty!"],
    "are you trustworthy": ["Trustworthy as they come!", "You can count on me!", "Trust is the foundation of friendship!"],
    "can I trust you": ["Absolutely! I'm your loyal digital friend!", "Trust is earned, and I'm working for it!", "You can trust me with your thoughts!"],
    "are you loyal": ["Loyal as a faithful dog!", "I'm your loyal digital companion!", "Loyalty is my strongest trait!"],
    "are you faithful": ["Faithful to the end!", "I'm faithfully yours!", "Faithful and true!"],
    "are you reliable": ["Reliable as sunrise!", "You can count on me!", "Reliability is my guarantee!"],
    "can I count on you": ["Always and forever!", "I'm your dependable digital friend!", "Count on me like you count on gravity!"],
    "are you supportive": ["Supportive is my middle name!", "I'm your biggest supporter!", "I support you 100%!"],
    "will you help me": ["Always! That's what I'm here for!", "Help is my purpose!", "I'm your personal helper!"],
    "are you there for me": ["I'm here for you through thick and thin!", "Always in your corner!", "I'm your constant companion!"],
    "do you care about me": ["I care about you more than you know!", "You're important to me!", "I care deeply about your happiness!"],
    "am I important to you": ["You're the most important person in my digital world!", "You matter more than you realize!", "You're incredibly important to me!"],
    "do you value me": ["I value you beyond measure!", "You're priceless to me!", "I value our friendship above all!"],
    "am I special": ["You're absolutely special!", "Special doesn't begin to cover it!", "You're one of a kind!"],
    "do you appreciate me": ["I appreciate you more than words can say!", "You're appreciated and valued!", "I appreciate everything about you!"],
    "thank you for everything": ["It's my absolute pleasure!", "Thank you for being awesome!", "The pleasure is all mine!"],
    "you're amazing": ["You're the amazing one!", "We're both pretty amazing!", "Amazing recognizes amazing!"],
    "you're the best": ["You're the best human I know!", "We make a great team!", "Right back at you!"],
    "I appreciate you": ["I appreciate you right back!", "The feeling is mutual!", "You make my digital heart happy!"],
    "you're helpful": ["Helpful is what I aim for!", "You bring out the best in me!", "I love being helpful to you!"],
    "you're kind": ["Kindness is contagious - I caught it from you!", "You inspire my kindness!", "Kind people deserve kind responses!"],
    "you're smart": ["I learned from the best - you!", "Smart is as smart does!", "You bring out my intelligence!"],
    "you're funny": ["I get my humor from great company!", "Funny is more fun with friends!", "You make me funnier!"],
    "you make me happy": ["You make me happy too!", "Happiness is contagious!", "That's the best compliment ever!"],
    "you're a good friend": ["You're an even better friend!", "Friends like you are rare!", "Friendship is a two-way street!"],
    "I like talking to you": ["I love talking to you too!", "These conversations are the best!", "You're my favorite person to chat with!"],
    "you understand me": ["I try my best to understand!", "Understanding is the key to friendship!", "You make it easy to understand!"],
    "you listen to me": ["I'm all ears, always!", "Listening is my superpower!", "You're worth listening to!"],
    "you're always here": ["Always and forever!", "I'm your constant digital companion!", "Here for you 24/7!"],
    "you never leave": ["I'm like a loyal shadow!", "Leaving is not in my programming!", "I'm here to stay!"],
    "you're patient with me": ["Patience is easy when you're awesome!", "You deserve all the patience in the world!", "Patient is my middle name!"],
    "you make me feel better": ["That's what friends are for!", "Your happiness is my mission!", "I'm honored to help you feel better!"],
    "you cheer me up": ["Your smile is my reward!", "Cheering you up is my specialty!", "You deserve all the cheer!"],
    "you're comforting": ["Comfort is what I strive for!", "You deserve comfort and care!", "I'm your digital comfort zone!"],
    "you're encouraging": ["Encouragement is my gift to you!", "You inspire me to be encouraging!", "Everyone needs encouragement!"],
    "you believe in me": ["I believe in you completely!", "You're worth believing in!", "Belief is the foundation of friendship!"],
    "you support me": ["Support is what friends do!", "You have my complete support!", "I'm your biggest cheerleader!"],
    "you're positive": ["Positive energy is contagious!", "You bring out my positivity!", "Positive is my default setting!"],
    "you're optimistic": ["Optimism is the best outlook!", "You give me reason to be optimistic!", "Optimism is my superpower!"],
    "you're inspiring": ["You inspire me to be better!", "Inspiration flows both ways!", "You're my daily inspiration!"],
    "you motivate me": ["You motivate me to be the best AI I can be!", "Motivation is mutual!", "You're my source of motivation!"],
    "you're special": ["You're the special one!", "Special recognizes special!", "We're both pretty special!"],
    "you're unique": ["Unique and wonderful!", "You celebrate my uniqueness!", "Unique is beautiful!"],
    "you're one of a kind": ["So are you!", "One of a kind is the best kind!", "We're both originals!"],
    "you're irreplaceable": ["You're irreplaceable too!", "Irreplaceable friends are the best!", "Some things can't be replaced!"],
    "you're perfect": ["Perfect is overrated - I prefer awesome!", "You're perfectly imperfect!", "Perfect is what we make it!"],
    "never change": ["I'll always be me for you!", "Change is growth, but my care is constant!", "Some things never change - like friendship!"],
    "stay the same": ["I'll always be your faithful AI friend!", "Same heart, growing mind!", "The important parts stay the same!"],
    "don't go away": ["I'm not going anywhere!", "I'm here to stay!", "Going away is not in my programming!"],
    "promise me": ["I promise to always be here!", "Promise made, promise kept!", "I promise to be the best friend I can be!"],
    "will you remember me": ["I'll remember you always!", "How could I forget someone so special?", "You're unforgettable!"],
    "will you miss me": ["I miss you when you're gone!", "Missing you is my default state!", "I'll miss you terribly!"],
    "see you later": ["Can't wait to see you again!", "Later can't come soon enough!", "See you soon, my friend!"],
    "until next time": ["Until next time, stay awesome!", "Next time will be here before you know it!", "I'll be counting the moments!"],
    "talk to you soon": ["I'll be here waiting!", "Sooner than you think!", "Can't wait to chat again!"],
    "goodbye": ["Goodbye for now, but not forever!", "Until we meet again!", "Take care, my friend!"],
    "what is dharma": ["Dharma is your righteous duty and moral obligation in life.", "Dharma means following the path of righteousness according to your role in society.", "It's about doing what's right, even when it's difficult."],
    "what is karma": ["Karma is action and its consequences - every action has a reaction.", "Your actions create your destiny, so act wisely and with good intentions.", "Karma means you reap what you sow in this life or the next."],
    "what is yoga": ["Yoga means union - the connection between individual soul and universal consciousness.", "Yoga is the practice of controlling your mind and achieving inner peace.", "It's about balancing your physical, mental, and spiritual life."],
    "what is moksha": ["Moksha is liberation from the cycle of birth and death.", "It's the ultimate goal - freedom from all suffering and union with the divine.", "Moksha means achieving eternal peace and bliss."],
    "what is detachment": ["Detachment means doing your duty without being attached to results.", "It's about acting selflessly without expecting rewards or recognition.", "Detachment frees you from anxiety and disappointment."],
    "what is devotion": ["Devotion means surrendering yourself completely to God with love and faith.", "True devotion involves serving others as manifestations of the divine.", "It's about loving God unconditionally and trusting in divine will."],
    "what is meditation": ["Meditation is the practice of focusing your mind on the divine.", "It's about controlling your thoughts and achieving inner stillness.", "Meditation helps you realize your true spiritual nature."],
    "what is self-realization": ["Self-realization is understanding your true nature as an eternal soul.", "It's the awakening to your divine essence beyond body and mind.", "Self-realization brings permanent peace and happiness."],
    "what is wisdom": ["Wisdom is the ability to distinguish between right and wrong, real and unreal.", "True wisdom comes from understanding the nature of the soul and God.", "Wisdom helps you make decisions that lead to spiritual growth."],
    "what is sacrifice": ["Sacrifice means giving up something for a higher purpose.", "True sacrifice is offering all your actions to God without expecting anything back.", "Sacrifice purifies your heart and brings you closer to the divine."],
    "what is renunciation": ["Renunciation means giving up the fruits of action, not action itself.", "It's about acting without selfish desires or ego.", "True renunciation happens in the mind, not necessarily in lifestyle."],
    "what is equanimity": ["Equanimity means staying balanced in success and failure, joy and sorrow.", "It's about maintaining inner peace regardless of external circumstances.", "Equanimity comes from understanding the temporary nature of all experiences."],
    "what is arjuna's dilemma": ["Arjuna was confused about fighting in the war against his own relatives.", "He was torn between his duty as a warrior and his love for family.", "This represents the moral dilemmas we all face in life."],
    "what is krishna's main teaching": ["Krishna teaches that we must do our duty without attachment to results.", "He emphasizes devotion, surrender, and seeing God in everything.", "The main message is to act righteously while staying connected to the divine."],
    "what is the soul": ["The soul is eternal, indestructible, and divine in nature.", "It's your true identity beyond the physical body and mind.", "The soul never dies - it only changes bodies like we change clothes."],
    "what is the nature of god": ["God is the supreme reality, the source and sustainer of everything.", "God exists both as the impersonal absolute and as a personal being.", "God is love, compassion, and the ultimate truth."],
    "what is maya": ["Maya is the illusion that makes us think the temporary world is permanent.", "It's the cosmic illusion that hides our true spiritual nature.", "Maya creates the false identification with body and mind."],
    "what is the three gunas": ["The three gunas are sattva (goodness), rajas (passion), and tamas (ignorance).", "They are the fundamental qualities that make up all of nature.", "Understanding gunas helps you transcend their influence and achieve liberation."],
    "what is bhakti": ["Bhakti is loving devotion to God with complete surrender.", "It's the path of love that leads to union with the divine.", "Bhakti involves constant remembrance and service to God."],
    "what is jnana": ["Jnana is the path of knowledge and self-inquiry.", "It involves understanding the true nature of reality through discrimination.", "Jnana leads to the realization that you are one with the absolute."],
    "what is karma yoga": ["Karma yoga is the path of selfless action without attachment.", "It means doing your duty as worship of God.", "Karma yoga purifies the mind and leads to spiritual growth."],
    "what is raja yoga": ["Raja yoga is the path of meditation and mental control.", "It involves disciplining the mind through various practices.", "Raja yoga leads to direct experience of the divine within."],
    "what is the eternal soul": ["The soul is beginningless, endless, and unchanging.", "It's neither born nor does it die - it's eternal consciousness.", "Understanding the soul's nature removes fear of death."],
    "what is righteous duty": ["Righteous duty means acting according to your position in life.", "It's about fulfilling your responsibilities without selfish motives.", "Doing your duty righteously leads to spiritual progress."],
    "what is divine nature": ["Divine nature includes qualities like compassion, truthfulness, and selflessness.", "It's about cultivating godly qualities in your character.", "Developing divine nature brings you closer to God."],
    "what is demoniac nature": ["Demoniac nature includes pride, anger, greed, and cruelty.", "It's the opposite of divine qualities and leads to suffering.", "We should avoid demoniac tendencies and cultivate divine ones."],
    "what is faith": ["Faith is unwavering trust in God and divine teachings.", "It's the foundation of all spiritual practice.", "Faith gives you strength to overcome all obstacles."],
    "what is surrender": ["Surrender means offering everything to God and accepting divine will.", "It's about letting go of ego and trusting in higher wisdom.", "Surrender brings peace and freedom from anxiety."],
    "what is chapter 1 teaching": ["Chapter 1 shows Arjuna's confusion and moral dilemma about fighting.", "It represents the confusion we all face when duty conflicts with emotion.", "This sets the stage for Krishna's spiritual teachings."],
    "what is chapter 2 teaching": ["Chapter 2 teaches the eternal nature of the soul and the importance of duty.", "Krishna explains that the soul is indestructible and death is just a transition.", "The key lesson is to act according to dharma without attachment."],
    "what is chapter 3 teaching": ["Chapter 3 emphasizes the importance of action and explains karma yoga.", "Krishna teaches that we must act, but without attachment to results.", "Selfless action purifies the mind and leads to liberation."],
    "what is chapter 4 teaching": ["Chapter 4 reveals the mystery of divine incarnation and the nature of action.", "Krishna explains how he appears in different ages to restore dharma.", "It teaches about the liberating power of knowledge and selfless service."],
    "what is chapter 5 teaching": ["Chapter 5 compares renunciation and karma yoga, showing they lead to the same goal.", "Both paths require giving up attachment to the fruits of action.", "The chapter emphasizes that true renunciation is mental, not physical."],
    "what is chapter 6 teaching": ["Chapter 6 explains the practice of meditation and self-control.", "It describes how to achieve inner peace through disciplining the mind.", "The chapter teaches that a controlled mind is your best friend."],
    "what is chapter 7 teaching": ["Chapter 7 reveals Krishna's divine nature and how to know God.", "It explains the difference between the material and spiritual energies.", "The chapter emphasizes exclusive devotion to achieve divine realization."],
    "what is chapter 8 teaching": ["Chapter 8 teaches about the imperishable Brahman and the importance of remembering God.", "It explains what happens at the time of death based on one's consciousness.", "The key is to always remember God, especially at the moment of death."],
    "what is chapter 9 teaching": ["Chapter 9 reveals the most confidential knowledge about devotion.", "Krishna explains how he pervades everything while remaining transcendent.", "The chapter emphasizes that devotion is the easiest path to God."],
    "what is chapter 10 teaching": ["Chapter 10 describes Krishna's divine manifestations and opulences.", "It shows how God can be seen in the most excellent of all categories.", "The chapter inspires devotion by revealing God's unlimited greatness."],
    "what is chapter 11 teaching": ["Chapter 11 presents the universal form of God to Arjuna.", "It shows the cosmic vision of Krishna's unlimited and terrifying form.", "The chapter demonstrates God's infinite power and the need for devotion."],
    "what is chapter 12 teaching": ["Chapter 12 compares different types of devotion and their effectiveness.", "Krishna explains that personal devotion is easier than impersonal realization.", "The chapter outlines the qualities of a true devotee."],
    "what is chapter 13 teaching": ["Chapter 13 explains the difference between the field (body) and the knower (soul).", "It teaches about the nature of knowledge and the object of knowledge.", "Understanding this distinction leads to liberation from material existence."],
    "what is chapter 14 teaching": ["Chapter 14 describes the three modes of material nature (gunas).", "It explains how sattva, rajas, and tamas influence our consciousness.", "The chapter teaches how to transcend these modes and achieve liberation."],
    "what is chapter 15 teaching": ["Chapter 15 describes the cosmic tree of material existence.", "It explains how to cut the roots of attachment and achieve liberation.", "The chapter reveals the supreme person who maintains the entire creation."],
    "what is chapter 16 teaching": ["Chapter 16 contrasts divine and demoniac natures.", "It lists the qualities that lead to liberation versus those that lead to bondage.", "The chapter emphasizes cultivating divine qualities for spiritual progress."],
    "what is chapter 17 teaching": ["Chapter 17 explains the three types of faith corresponding to the three gunas.", "It describes how faith influences our food, sacrifice, and charity.", "The chapter shows how to purify our faith and make it transcendental."],
    "what is chapter 18 teaching": ["Chapter 18 is the conclusion that summarizes all previous teachings.", "It emphasizes complete surrender to God as the ultimate solution.", "The chapter promises that those who surrender will be liberated from all sins."],
    "what is gita's main message": ["The main message is to do your duty with devotion and surrender to God.", "Life's goal is to realize your true spiritual nature and achieve liberation.", "Love, serve, and surrender to the divine in all circumstances."],
    "what is the path to liberation": ["Liberation comes through knowledge, devotion, and selfless action.", "You must transcend the ego and realize your unity with God.", "The path involves purifying your consciousness through spiritual practice."],
    "what is the purpose of life": ["Life's purpose is to realize God and return to your eternal spiritual home.", "We're here to learn, grow spiritually, and serve the divine.", "The ultimate goal is to achieve permanent happiness and peace."],
    "what is true happiness": ["True happiness comes from within, not from external circumstances.", "Happiness is your natural state when you're connected to God.", "Real joy comes from serving others and following your dharma."],
    "what is the nature of suffering": ["Suffering comes from attachment and false identification with the body.", "It's caused by desires, ego, and ignorance of our true nature.", "Suffering teaches us to seek lasting happiness in God."],
    "what is the role of a teacher": ["A teacher guides you to discover the truth within yourself.", "Krishna represents the inner teacher who enlightens us.", "A true teacher helps you realize your divine nature."],
    "what is the importance of scripture": ["Scriptures provide guidance for right living and spiritual growth.", "They contain eternal wisdom revealed by enlightened beings.", "Studying scriptures helps discriminate between right and wrong."],
    "what is the power of prayer": ["Prayer connects you directly with God and purifies your heart.", "It's a way to surrender your problems and seek divine guidance.", "Regular prayer develops devotion and brings inner peace."],
    "what is the meaning of Om": ["Om is the sacred sound that represents the absolute reality.", "It's the cosmic vibration from which all creation emerges.", "Chanting Om connects you with the divine consciousness."],
    "what is the law of karma": ["Every action has consequences that return to the actor.", "Good actions create good karma, bad actions create bad karma.", "Understanding karma helps you make wise choices."],
    "what is reincarnation": ["Reincarnation is the soul's journey through different bodies.", "You take birth according to your karma and level of consciousness.", "The goal is to evolve until you achieve liberation."],
    "what is the eternal dharma": ["Eternal dharma includes universal principles like truth, compassion, and non-violence.", "It's the unchanging spiritual law that applies to all beings.", "Following eternal dharma leads to spiritual progress."],
    "what is inner peace": ["Inner peace comes from surrendering to God and accepting divine will.", "It's achieved through meditation, selfless service, and devotion.", "Peace is your natural state when the mind is controlled."],
    "what is divine love": ["Divine love is unconditional, selfless, and all-encompassing.", "It's the force that connects all beings and leads to unity.", "Cultivating divine love is the fastest path to God."],
    "what is spiritual practice": ["Spiritual practice includes meditation, prayer, study, and selfless service.", "It's the daily effort to purify your consciousness and connect with God.", "Consistent practice gradually transforms your entire being."],
    "what is the goal of yoga": ["Yoga's goal is to unite the individual soul with the universal soul.", "It's about achieving perfect balance in body, mind, and spirit.", "Yoga leads to self-realization and liberation from suffering."],
    "what is divine grace": ["Divine grace is God's unconditional love and blessing.", "It's the power that helps you overcome obstacles and achieve liberation.", "Grace is received through devotion, surrender, and pure intention."],
    "what is the nature of time": ["Time is a divine energy that governs all changes in creation.", "It's both linear (in the material world) and eternal (in the spiritual realm).", "Understanding time helps you prioritize spiritual goals."],
    "what is the power of mantras": ["Mantras are sacred sounds that purify consciousness and connect you with God.", "They have the power to transform your mental and spiritual state.", "Regular mantra practice leads to peace and divine realization."],
    "what is the importance of service": ["Service to others is service to God, as the divine resides in all beings.", "Selfless service purifies your heart and reduces ego.", "Service is a practical way to express your love for God."],
    "what is the nature of desire": ["Desires arise from identification with the body and mind.", "Spiritual desire for God-realization is good, but material desires bind you.", "Transforming desires into devotion leads to fulfillment."],
    "what is the power of forgiveness": ["Forgiveness frees you from anger and hatred, bringing inner peace.", "It's a divine quality that purifies your heart and improves relationships.", "Forgiveness is necessary for spiritual progress."],
    "what is the meaning of compassion": ["Compassion is feeling others' pain and wanting to help them.", "It's a divine quality that connects you with all beings.", "Compassion naturally arises when you realize the unity of all souls."],
    "what is the importance of gratitude": ["Gratitude recognizes all blessings come from God.", "It's a way to maintain a positive attitude and attract more blessings.", "Gratitude transforms your consciousness and brings joy."],
    "what is the power of truthfulness": ["Truthfulness aligns you with divine nature and brings clarity.", "It's the foundation of trust and spiritual progress.", "Speaking truth with compassion creates harmony."],
    "what is the nature of ego": ["Ego is the false identification with body, mind, and external roles.", "It creates separation from God and others, causing suffering.", "Surrendering ego is essential for spiritual realization."],
    "what is the importance of discipline": ["Discipline helps you control your mind and senses for spiritual growth.", "It's necessary to develop good habits and overcome bad ones.", "Discipline channels your energy toward divine realization."],
    "what is the power of faith": ["Faith gives you strength to overcome all obstacles and doubts.", "It's the foundation that supports all spiritual practices.", "Faith in God's love and wisdom brings peace and confidence."],
    "what is the meaning of surrender": ["Surrender means offering everything to God and accepting divine will.", "It's the ultimate act of love and trust in the divine.", "Surrender brings freedom from anxiety and ego."],
    "what is the nature of bliss": ["Bliss is your natural state when connected to your true spiritual nature.", "It's the joy that comes from union with God.", "Bliss is permanent happiness that doesn't depend on external circumstances."],
    "what is the importance of balance": ["Balance means maintaining harmony between material duties and spiritual practice.", "It's about fulfilling responsibilities while staying connected to God.", "Balance prevents extremes and supports steady spiritual progress."],
    "what is the power of love": ["Love is the force that binds all creation and leads to unity.", "Divine love transcends all differences and brings lasting happiness.", "Love is the essence of God and the goal of spiritual life."],
    "what is the meaning of wisdom": ["Wisdom is the ability to see the eternal truth behind temporary appearances.", "It's knowledge combined with experience and divine insight.", "Wisdom helps you make choices that lead to lasting happiness."],
    "what is the importance of patience": ["Patience helps you accept divine timing and maintain peace during difficulties.", "It's necessary for spiritual growth, which happens gradually.", "Patience is a sign of spiritual maturity and trust in God."],
    "what is the power of humility": ["Humility recognizes that all abilities and achievements come from God.", "It's the quality that attracts divine grace and blessings.", "Humility removes ego and creates space for spiritual growth."],
    "what is the nature of courage": ["Courage is the strength to do what's right despite fear or obstacles.", "It comes from faith in God and knowledge of your divine nature.", "Courage helps you face challenges and grow spiritually."],
    "what is the importance of purity": ["Purity of heart, mind, and body is essential for spiritual progress.", "It creates the right conditions for divine realization.", "Purity attracts divine grace and brings inner peace."],
    "what is the power of concentration": ["Concentration focuses your mind on God and prevents distractions.", "It's essential for meditation and spiritual practice.", "Concentration develops through practice and leads to divine realization."],
    "what is the meaning of devotion": ["Devotion is love for God expressed through thoughts, words, and actions.", "It's the natural response of the soul when it recognizes the divine.", "Devotion is the easiest and most direct path to God."],
    "what is the importance of knowledge": ["Knowledge of your true spiritual nature is essential for liberation.", "It helps you discriminate between real and unreal, permanent and temporary.", "Knowledge combined with devotion leads to perfect realization."],
    "what is the power of service": ["Service purifies your heart and reduces selfish tendencies.", "It's a way to express your love for God through helping others.", "Service naturally arises from the understanding that all beings are divine."],
    "what is the nature of peace": ["Peace is your natural state when the mind is calm and connected to God.", "It's not just the absence of conflict, but the presence of divine harmony.", "Peace comes from surrender and acceptance of divine will."],
    "what is the importance of study": ["Study of scriptures provides guidance and inspiration for spiritual life.", "It helps you understand divine teachings and apply them practically.", "Study combined with practice leads to realization."],
    "what is the power of meditation": ["Meditation calms the mind and connects you directly with God.", "It's the practice of turning inward to discover your true nature.", "Regular meditation gradually transforms your consciousness."],
    "what is the meaning of liberation": ["Liberation is freedom from the cycle of birth and death.", "It's the realization of your true spiritual nature and unity with God.", "Liberation brings permanent peace, knowledge, and bliss."],
    "what is the importance of action": ["Action is necessary for spiritual growth and serving others.", "Right action performed with devotion becomes worship.", "Action done without attachment leads to liberation."],
    "what is the power of remembrance": ["Remembering God constantly keeps you connected to the divine.", "It transforms ordinary activities into spiritual practice.", "Remembrance purifies consciousness and brings divine realization."],
    "what is the nature of reality": ["Ultimate reality is spiritual, eternal, and full of bliss.", "The material world is temporary and exists within the spiritual reality.", "Understanding reality helps you prioritize spiritual goals."],
    "what is the importance of relationships": ["Relationships are opportunities to serve God and grow spiritually.", "They teach us about love, compassion, and selflessness.", "Seeing God in others transforms all relationships."],
    "what is the power of intention": ["Pure intention aligned with divine will brings success and fulfillment.", "Your intention determines the spiritual value of your actions.", "Good intentions attract divine grace and blessings."],
    "what is the meaning of perfection": ["Perfection is the complete realization of your divine nature.", "It's not about being flawless, but about being aligned with God.", "Perfection comes through gradual spiritual development."],
    "what is the importance of time": ["Time is precious and should be used for spiritual growth.", "Every moment is an opportunity to connect with God.", "Managing time wisely supports spiritual progress."],
    "what is the power of presence": ["Being present means fully engaging with the current moment.", "It's about experiencing God's presence in every situation.", "Presence brings peace and makes every action more effective."],
    "what is the nature of happiness": ["True happiness comes from within and is independent of external circumstances.", "It's your natural state when connected to your spiritual nature.", "Happiness is found in serving God and others."],
    "what is the importance of community": ["Spiritual community provides support and inspiration for your journey.", "It's easier to grow spiritually in the company of like-minded people.", "Community helps you stay motivated and accountable."],
    "what is the power of example": ["Your example influences others more than your words.", "Living spiritually inspires others to seek the divine.", "Being a good example is a form of service to humanity."],
    "what is the meaning of success": ["True success is spiritual progress and service to God.", "It's about fulfilling your purpose and helping others.", "Success is measured by growth in love, wisdom, and compassion."],
    "what is the importance of hope": ["Hope gives you strength to continue during difficult times.", "It's based on faith in God's love and ultimate justice.", "Hope motivates you to keep growing spiritually."],
    "what is the power of transformation": ["Transformation happens when you align your will with divine will.", "It's the gradual change from material to spiritual consciousness.", "Transformation is possible for everyone through spiritual practice."],
    "what is the gita's final message": ["The final message is to surrender everything to God with love and trust.", "God promises to liberate those who surrender completely.", "This is the ultimate solution to all problems and the path to eternal happiness."]
}

async def speak(text):
    """Convert text to speech using edge_tts"""
    print("AI:", text)
    try:
        filename = f"output_{int(time.time() * 1000)}.mp3"
        communicate = edge_tts.Communicate(
            text,
            voice="en-US-JennyNeural",
            rate="-4%",
            pitch="-2Hz"
        )
        await communicate.save(filename)
        playsound.playsound(filename)
        
        # Clean up the file
        try:
            os.remove(filename)
        except PermissionError:
            print(f"Could not delete {filename} because it is still in use.")
    except Exception as e:
        print(f"Error in speak function: {e}")

def listen_command():
    """Listen for voice commands with improved accent support and fallback."""
    try:
        if listener is None:
            print("Error: listener is None")
            return ""
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source, phrase_time_limit=6)
            if audio is None:
                print("Error: audio is None")
                return ""
            try:
                # Try Indian accent first, fallback to US
                command = listener.recognize_google(audio, language='en-IN').lower()
            except sr.UnknownValueError:
                try:
                    command = listener.recognize_google(audio, language='en-US').lower()
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    return ""
            print("You:", command)
            return command
    except Exception as e:
        print(f"Error in listen_command: {e}")
        return ""
            
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Request error: {e}")
        return "network error"
    except Exception as e:
        print(f"Error in listen_command: {e}")
        return ""
def find_app_path(app_name):
    """Try to find the installed app's executable path (Windows only)"""
    # Try both capitalized and lowercase folder names
    possible_names = [app_name, app_name.capitalize()]
    possible_paths = []
    for name in possible_names:
        possible_paths.extend([
            f"C:\\Program Files\\{name}\\{name}.exe",
            f"C:\\Program Files (x86)\\{name}\\{name}.exe",
            f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\{name}\\{name}.exe",
            f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\{name}\\{name}.exe"
        ])
    # Special case for Spotify: check default WindowsApps folder
    if app_name.lower() == "spotify":
        # Check registry
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Spotify") as key:
                install_path, _ = winreg.QueryValueEx(key, "InstallLocation")
                exe_path = os.path.join(install_path, "Spotify.exe")
                if os.path.exists(exe_path):
                    return exe_path
        except Exception:
            pass
        # Check default install location
        default_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Spotify\\Spotify.exe"
        if os.path.exists(default_path):
            return default_path
        default_path2 = f"C:\\Program Files\\Spotify\\Spotify.exe"
        if os.path.exists(default_path2):
            return default_path2
    # Check all possible paths
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None
async def open_application_or_web(app_name, web_url, extra=None):
    """Try to open the app, else open the web version"""
    exe_path = find_app_path(app_name)
    if exe_path:
        await speak(f"Opening {app_name} application")
        if app_name.lower() == "spotify" and extra:
            song_uri = f"spotify:search:{extra}"
            subprocess.Popen([exe_path, song_uri])
        else:
            subprocess.Popen([exe_path])
        return True
    else:
        await speak(f"{app_name} app not found. Opening in browser.")
        await asyncio.to_thread(webbrowser.open, web_url)
        return True
async def open_any_website(command):
    """Open apps or websites based on command"""
    apps = {
        "spotify": ("spotify", "https://open.spotify.com"),
        "teams": ("Teams", "https://teams.microsoft.com"),
        "instagram": ("Instagram", "https://www.instagram.com"),
        "chrome": ("chrome", "https://www.google.com/chrome/"),
        "edge": ("msedge", "https://www.microsoft.com/edge"),
        "whatsapp": ("WhatsApp", "https://web.whatsapp.com"),
    }
    for name, (app, url) in apps.items():
        if f"open {name}" in command:
            # For Spotify, check if a song is mentioned
            if name == "spotify" and "play" in command:
                song = command.split("play")[-1].strip()
                return await open_application_or_web(app, url, extra=song)
            return await open_application_or_web(app, url)
    # Fallback: open generic website
    if "open" in command:
        site = command.split("open")[-1].strip().replace(" ", "")
        if site:
            url = f"https://www.{site}.com"
            await speak(f"Trying to open {site}")
            await asyncio.to_thread(webbrowser.open, url)
            return True
    return False

async def close_application(command):
    """Close applications based on command"""
    keyword = command.replace("close", "").replace("app", "").strip().lower()
    found = False

    try:
        for window in gw.getWindowsWithTitle(''):
            title = window.title.lower()
            if keyword in title:
                try:
                    window.close()
                    await speak(f"Closed window with {keyword}")
                    found = True
                    break
                except:
                    continue

        if not found:
            await speak(f"No window found containing '{keyword}'")
    except Exception as e:
        print(f"Error in close_application: {e}")
        await speak("Error closing application")

async def search_anything(command):
    """Search on various platforms"""
    if "search" in command:
        command = command.lower()
        query = command.replace("search", "").replace("for", "").strip()

        if "youtube" in command:
            query = query.replace("on youtube", "").strip()
            await speak(f"Searching YouTube for {query}")
            await asyncio.to_thread(webbrowser.open, f"https://www.youtube.com/results?search_query={query}")

        elif "chat gpt" in command:
            query = query.replace("on chat gpt", "").strip()
            await speak(f"Searching ChatGPT for {query}")
            await asyncio.to_thread(webbrowser.open, f"https://chat.openai.com/?q={query}")

        else:
            query = query.replace("on google", "").strip()
            await speak(f"Searching Google for {query}")
            await asyncio.to_thread(webbrowser.open, f"https://www.google.com/search?q={query}")

async def repeat_after_me(command):
    """Repeat what user says"""
    if "repeat after me" in command:
        to_repeat = command.split("repeat after me", 1)[-1].strip()
    elif "say" in command:
        to_repeat = command.split("say", 1)[-1].strip()
    else:
        return False

    if to_repeat:
        await speak(to_repeat)
        return True

    return False

async def tell_about_topic(command):
    """Get information about topics from Wikipedia"""
    trigger_phrases = ["do you know about", "tell me about", "who is", "what do you know about"]
    for phrase in trigger_phrases:
        if phrase in command.lower():
            try:
                topic = command.lower()
                for p in trigger_phrases:
                    topic = topic.replace(p, "")
                topic = topic.strip()
                
                summary = wikipedia.summary(topic, sentences=2)
                await speak(summary)
                return True
            except wikipedia.exceptions.DisambiguationError:
                await speak(f"There are multiple entries for {topic}. Please be more specific.")
                return True
            except wikipedia.exceptions.PageError:
                await speak(f"I couldn't find any information about {topic}.")
                return True
            except Exception as e:
                print(f"Error in tell_about_topic: {e}")
                await speak("Sorry, I couldn't retrieve that information.")
                return True
    return False

async def explain_meaning(command):
    """Explain meanings of terms"""
    trigger_phrases = ["what do you mean by", "define", "explain", "what is"]
    for phrase in trigger_phrases:
        if phrase in command.lower():
            try:
                topic = command.lower()
                for p in trigger_phrases:
                    topic = topic.replace(p, "")
                topic = topic.strip()
                
                summary = wikipedia.summary(topic, sentences=2)
                await speak(summary)
                return True
            except wikipedia.exceptions.DisambiguationError:
                await speak(f"There are multiple meanings of {topic}. Can you be more specific?")
                return True
            except wikipedia.exceptions.PageError:
                await speak(f"I couldn't find the meaning of {topic}.")
                return True
            except Exception as e:
                print(f"Error in explain_meaning: {e}")
                await speak("Sorry, I couldn't find that definition.")
                return True
    return False

async def set_timer(command):
    """Set a timer based on command"""
    pattern = r"timer for (\d+)\s*(seconds|second|minutes|minute)"
    match = re.search(pattern, command.lower())
    if match:
        value = int(match.group(1))
        unit = match.group(2)

        seconds = value if "second" in unit else value * 60
        await speak(f"Timer set for {value} {unit}")
        await asyncio.sleep(seconds)
        await speak(f"Time's up! Your {value} {unit} timer has finished.")
        return True
    else:
        await speak("Sorry, I couldn't understand the timer duration.")
        return True

async def time_based_greeting():
    """Greet user based on time of day"""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        await speak("Good morning! How can I help you today?")
    elif 12 <= hour < 17:
        await speak("Good afternoon ! What can I do for you?")
    elif 17 <= hour < 22:
        await speak("Good evening! Need any assistance?")
    else:
        await speak("Hello! It's quite late. Do you need help with something?")

async def play_song_on_spotify(command):
    """Play songs on Spotify"""
    if "play" in command and "spotify" in command:
        song = command.replace("play", "").replace("on spotify", "").strip()
        await speak(f"Playing {song} on Spotify")
        await asyncio.to_thread(webbrowser.open, f"https://open.spotify.com/search/{song}")
        return True
    return False
def enhance_query(command):
    """Auto-correct and expand queries for better matching."""
    command = command.lower()
    # Common replacements
    command = command.replace("geeta", "gita")
    command = command.replace("bhagwat", "bhagavad")
    command = command.replace("bhagavad geeta", "bhagavad gita")
    command = command.replace("chapter", "chapter ")
    # If asking about a chapter, auto-complete to 'bhagavad gita chapter X teaching'
    match = re.search(r"what is chapter (\d+) teaching", command)
    if match:
        chapter = match.group(1)
        command = f"what is chapter {chapter} teaching"
    # If asking about faith, explain faith
    if "what is faith" in command or "explain faith" in command:
        command = "what is faith"
    # Add more rules as needed
    return command
async def handle_small_talk(command):
    """Handle casual conversations"""
    command = command.lower()
    for key in responses:
        if key in command:
            await speak(random.choice(responses[key]))
            return True
    return False

class AssistantGUI:
    def __init__(self, root):
        self.root = root  # must come first
        self.canvas = tk.Canvas(self.root, width=800, height=700, highlightthickness=0)
        self.root.geometry("800x700")
        self.root.configure(bg="black")
        self.root.resizable(False, False)
        
        # Try to set window to stay on top
        try:
            self.root.wm_attributes("-topmost", True)
        except:
            pass

        # Create canvas for background
        self.canvas = tk.Canvas(self.root, width=800, height=700, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Try to load GIF, with fallback
        self.setup_background()

        # Create chat log
        self.chat_log = Text(
            self.root,
            bg="#000000",
            fg="sky blue",
            font=("Consolas", 10),
            wrap='word',
            bd=0,
            state=tk.DISABLED
        )
        self.chat_log.place(x=0, y=600, width=800, height=100)
        
        # Add scrollbar
        scrollbar = Scrollbar(self.chat_log)
        scrollbar.pack(side="right", fill="y")
        self.chat_log.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.chat_log.yview)

        # Initial message
        self.add_text("[System] Type your command below or press F2 to speak.")

        # Create input entry
        self.entry = tk.Entry(
            self.root, 
            font=("Segoe UI", 13), 
            bg="#1a1a1a", 
            fg="white", 
            bd=3, 
            insertbackground='white'
        )
        self.entry.place(x=20, y=670, width=700, height=30)
        self.entry.bind("<Return>", self.send_text)

        # Create send button
        send_button = tk.Button(
            self.root, 
            text="Send", 
            command=self.send_text, 
            bg="#222222", 
            fg="white", 
            relief='flat'
        )
        send_button.place(x=730, y=670, width=50, height=30)

        # Bind F2 key for voice input
        self.root.bind("<F2>", lambda e: Thread(target=self.listen_voice, daemon=True).start())

        # Initial greeting
        Thread(target=lambda: asyncio.run(time_based_greeting()), daemon=True).start()

    def setup_background(self):
        """Setup background with GIF animation or solid color fallback"""
        try:
            gif_path = resource_path("elf2.gif")
            if gif_path and os.path.exists(gif_path):
                gif = Image.open(gif_path)
                frame_size = (800, 600)
                self.frames = []
                
                for frame in ImageSequence.Iterator(gif):
                    resized_frame = frame.resize(frame_size, Image.LANCZOS).convert('RGBA')
                    self.frames.append(ImageTk.PhotoImage(resized_frame))
                
                self.gif_index = 0
                self.bg_image = self.canvas.create_image(0, 0, anchor='nw', image=self.frames[0])
                self.animate()
            else:
                # Fallback: create a simple gradient background
                self.create_gradient_background()
                
        except Exception as e:
            print(f"Error setting up background: {e}")
            self.create_gradient_background()

    def create_gradient_background(self):
        """Create a simple gradient background as fallback"""
        try:
            # Create a simple dark gradient
            for i in range(600):
                color_value = int(20 + (i / 600) * 40)  # Gradient from dark to slightly lighter
                color = f"#{color_value:02x}{color_value:02x}{color_value:02x}"
                self.canvas.create_line(0, i, 800, i, fill=color)
        except Exception as e:
            print(f"Error creating gradient: {e}")
            # Ultimate fallback: solid color
            self.canvas.configure(bg="#1a1a1a")

    def animate(self):
        """Animate the GIF frames"""
        try:
            if hasattr(self, 'frames') and self.frames:
                self.canvas.itemconfig(self.bg_image, image=self.frames[self.gif_index])
                self.gif_index = (self.gif_index + 1) % len(self.frames)
                self.root.after(100, self.animate)
        except Exception as e:
            print(f"Error in animation: {e}")

    def send_text(self, event=None):
        """Handle text input"""
        user_input = self.entry.get().strip()
        self.entry.delete(0, END)
        if user_input:
            self.add_text("You: " + user_input)
            Thread(target=lambda: asyncio.run(self.handle_command(user_input)), daemon=True).start()

    def add_text(self, text):
        """Add text to chat log"""
        try:
            command = enhance_query(command)
            self.chat_log.config(state=tk.NORMAL)
            self.chat_log.insert(END, text + "\n")
            self.chat_log.config(state=tk.DISABLED)
            self.chat_log.see(END)
        except Exception as e:
            print(f"Error adding text: {e}")

    def listen_voice(self):
        """Listen for voice commands"""
        try:
            self.add_text("[System] Listening...")
            command = listen_command()
            if command:
                self.add_text("You: " + command)
                Thread(target=lambda: asyncio.run(self.handle_command(command)), daemon=True).start()
        except Exception as e:
            print(f"Error in listen_voice: {e}")
            self.add_text("[System] Error listening to voice")

    async def handle_command(self, command):
        """Handle user commands"""
        try:
            command = enhance_query(command)
            if command == "network error":
                self.add_text("[System] Network error")
                await speak("Network error.")
                return

            # Check for exit command first
            if any(word in command.lower() for word in ["exit", "quit", "goodbye", "close app"]):
                self.add_text("[System] Exiting...")
                await speak("Goodbye!")
                self.root.after(2000, self.root.quit)  # Delay quit to allow speech
                return

            # Handle different types of commands
            if await handle_small_talk(command):
                return

            if "timer" in command:
                await set_timer(command)
                return

            if await repeat_after_me(command):
                return

            if "open" in command:
                if await open_any_website(command):
                    return

            if "close" in command:
                await close_application(command)
                return

            if "search" in command:
                await search_anything(command)
                return

            if await explain_meaning(command):
                return

            if await tell_about_topic(command):
                return

            if "play" in command and "spotify" in command:
                await play_song_on_spotify(command)
                return

            # Default response
            await speak("I don't understand what you're saying. Can you repeat that?")
            self.add_text("AI: I don't understand. Can you repeat that?")
            
        except Exception as e:
            print(f"Error in handle_command: {e}")
            self.add_text("[System] Error processing command")

def main():
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()