import re
import random
import time
import os

# --- CONFIGURATION ---
DATA_FILE = "training_data.txt"
MEMORY_FILE = "user_memory.txt"

class ZenithEvolved:
    def __init__(self, data_file):
        self.name = "ZENITH"
        self.brain = {}      # Linguistic map for writing original English
        self.knowledge = []  # Fact storage for retrieval
        self.history = []
        self.load_and_learn(data_file)
        if not os.path.exists(MEMORY_FILE): open(MEMORY_FILE, 'w').close()

    def load_and_learn(self, path):
        """Builds the NLP brain and the fact database"""
        print(f"[{self.name}] Synchronizing neurons...")
        if not os.path.exists(path):
            open(path, 'w').close()
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().replace('\n', ' ')
                
                # 1. Learn Facts (Retrieval Layer)
                self.knowledge = [s.strip() for s in re.split(r'(?<=[.!?]) +', content) if len(s) > 15]
                
                # 2. Learn English Structure (Generative Layer)
                # We use a Trigram model: (word1, word2) -> predicts word3
                words = content.lower().split()
                for i in range(len(words) - 2):
                    key = (words[i], words[i+1])
                    if key not in self.brain:
                        self.brain[key] = []
                    self.brain[key].append(words[i+2])
            
            print(f"[{self.name}] Evolution complete. {len(self.brain)} linguistic patterns mapped.")
        except Exception as e:
            print(f"Error during evolution: {e}")

    def generate_original_english(self, seed_words=None):
        """Synthesizes new sentences word-by-word"""
        if not self.brain:
            return "My mind is a blank slate. Feed me text."

        # If no seed, pick a random starting pair
        if not seed_words or len(seed_words) < 2:
            seed_key = random.choice(list(self.brain.keys()))
        else:
            # Try to find the user's last two words in our brain
            seed_key = (seed_words[-2], seed_words[-1])
            if seed_key not in self.brain:
                seed_key = random.choice(list(self.brain.keys()))

        result = list(seed_key)
        for _ in range(15): # Max words to generate
            key = (result[-2], result[-1])
            if key in self.brain:
                next_word = random.choice(self.brain[key])
                result.append(next_word)
                if next_word.endswith(('.', '!', '?')): break
            else:
                break
        
        return " ".join(result).capitalize()

    def get_response(self, user_input):
        u = user_input.lower().strip()
        user_words = re.findall(r'\w+', u)

        # 1. Manual Reflexes (Hard-coded soul)
        reflexes = {
            "hi": "Greetings. My processors are warm.",
            "who are you": "I am Zenith. A local god built on pure Python logic.",
            "how are you": "My circuits are stable and my logic is clear. And you?"
        }
        if u in reflexes: return reflexes[u]

        # 2. Fact Search (Finding the best existing sentence)
        candidates = []
        for s in self.knowledge:
            score = sum(1 for w in user_words if w in s.lower() and len(w) > 3)
            if score >= 2: # Needs at least 2 keyword matches to be relevant
                candidates.append(s)
        
        if candidates:
            # Give a fact-based answer
            return random.choice(candidates)

        # 3. Generative Synthesis (Writing original English)
        # If no perfect fact is found, Zenith 'thinks' and writes its own
        return self.generate_original_english(user_words if len(user_words) >= 2 else None)

    def speak(self, text):
        print(f"\n{self.name}: ", end="", flush=True)
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.02)
        print()

# --- EXECUTION ---
bot = ZenithEvolved(DATA_FILE)
bot.speak("My neurons have evolved. I no longer just search; I synthesize.")

while True:
    try:
        msg = input("\nYou: ")
        if not msg.strip(): continue
        if msg.lower() in ["bye", "exit", "quit"]:
            bot.speak("Hibernating. Goodbye, Architect.")
            break
        
        response = bot.get_response(msg)
        bot.speak(response)
        
    except KeyboardInterrupt:
        break
