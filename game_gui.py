import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import random
import threading
import time

SAVE_FILE = "save_game.json"

AGENCIES = ["COP", "FBI", "CIA", "CSI"]
CRIME_TYPES = [
    "Bank Robbery",
    "Art Theft",
    "Drug Smuggling",
    "Identity Theft",
    "Cyber Hacking",
    "Blackmail",
    "Kidnapping",
    "Money Laundering",
]

CITY_DISTRICTS = [
    "Downtown",
    "Harbor",
    "Old Town",
    "Tech Quarter",
    "Midtown",
    "Industrial Zone",
    "Luxury Row",
    "Riverside",
]

SUSPECTS = [
    {
        "name": "Marcus Vale",
        "role": "Former accountant",
        "motive": "Revenge after being fired and humiliated.",
        "method": "Used inside information and manipulated vault access.",
        "alibi": "He claims he was at the gym, but his card was used at a hotel later.",
        "weakness": "He becomes furious when anyone mentions his dismissal.",
    },
    {
        "name": "Sofia Quinn",
        "role": "Tech specialist",
        "motive": "To pay off a growing gambling debt.",
        "method": "Hacked cameras and used fake credentials to access the target.",
        "alibi": "She says she was in a server room all night.",
        "weakness": "She keeps checking her phone when she is anxious.",
    },
    {
        "name": "Darren Cross",
        "role": "Nightclub owner",
        "motive": "To destroy a rival and steal their product shipment.",
        "method": "Used a fake delivery truck and bribed a clerk.",
        "alibi": "He says he was hosting a private event, but the cameras were disabled.",
        "weakness": "He brags whenever he feels safe.",
    },
    {
        "name": "Elena Frost",
        "role": "Luxury broker",
        "motive": "She planned to sell stolen documents to foreign buyers.",
        "method": "Forged documents and moved evidence through private channels.",
        "alibi": "She was at a charity gala, though one photo appears altered.",
        "weakness": "She hates being questioned in public.",
    },
]

CLUES = [
    "A black glove was left near the scene.",
    "An encrypted USB drive was found in a trash bin.",
    "A witness heard the suspect say: 'This is about revenge and money.'",
    "A fake receipt was found inside a suspect's coat pocket.",
    "A phone ping placed a suspect near the target location.",
    "The crime shows insider knowledge of the building layout.",
    "A hidden safehouse was discovered with stolen goods and a map.",
    "A financial trail shows suspicious transfers before the crime.",
]


def make_player():
    return {
        "name": "",
        "side": "",
        "agency": "",
        "alias": "",
        "cash": 100,
        "health": 100,
        "skill": 50,
        "reputation": 0,
        "suspicion": 0,
        "inventory": [],
        "district": "Downtown",
        "mission": "",
        "status": "alive",
    }


def save_game(player):
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f, indent=2)


def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return None


def random_clue():
    return random.choice(CLUES)


def create_case():
    suspect = random.choice(SUSPECTS)
    crime = random.choice(CRIME_TYPES)
    return suspect, crime


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("City of Shadows - Crime Detective Game")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a1a")
        
        self.player = None
        self.suspect = None
        self.crime = None
        self.suspicion_score = 0
        self.turn = 0
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#1a1a1a")
        self.style.configure("TLabel", background="#1a1a1a", foreground="#00ff00")
        self.style.configure("TButton", background="#333333", foreground="#00ff00")
        self.style.map("TButton", background=[("active", "#555555")])
        
        self.show_main_menu()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(
            frame,
            text="CITY OF SHADOWS",
            font=("Arial", 28, "bold"),
            bg="#1a1a1a",
            fg="#ff0000"
        )
        title.pack(pady=20)
        
        subtitle = ttk.Label(
            frame,
            text="Crime Detective Game - Choose Your Path"
        )
        subtitle.pack(pady=10)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=40)
        
        new_game_btn = ttk.Button(
            button_frame,
            text="New Game",
            command=self.start_new_game,
            width=20
        )
        new_game_btn.pack(pady=10)
        
        if os.path.exists(SAVE_FILE):
            load_game_btn = ttk.Button(
                button_frame,
                text="Load Saved Game",
                command=self.load_saved_game,
                width=20
            )
            load_game_btn.pack(pady=10)
        
        exit_btn = ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,
            width=20
        )
        exit_btn.pack(pady=10)
    
    def start_new_game(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Enter Your Character Name:").pack(pady=10)
        
        name_entry = ttk.Entry(frame, width=30)
        name_entry.pack(pady=10)
        name_entry.focus()
        
        def create_player():
            name = name_entry.get().strip() or "Shadow"
            self.player = make_player()
            self.player["name"] = name
            self.choose_role()
        
        ttk.Button(frame, text="Continue", command=create_player).pack(pady=20)
    
    def load_saved_game(self):
        self.player = load_game()
        if self.player:
            if self.player["side"] == "criminal":
                self.show_criminal_game()
            else:
                self.show_law_game()
        else:
            messagebox.showerror("Error", "No save file found.")
            self.show_main_menu()
    
    def choose_role(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Choose Your Role:", font=("Arial", 16, "bold")).pack(pady=20)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=40)
        
        ttk.Button(
            button_frame,
            text="Criminal",
            command=self.start_criminal_role,
            width=25
        ).pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="Law Agent",
            command=self.start_law_role,
            width=25
        ).pack(pady=10)
    
    def start_criminal_role(self):
        self.player["side"] = "criminal"
        self.show_criminal_setup()
    
    def start_law_role(self):
        self.player["side"] = "law"
        self.show_law_setup()
    
    def show_criminal_setup(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Criminal Setup", font=("Arial", 16, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Choose your criminal alias:").pack(pady=5)
        alias_entry = ttk.Entry(frame, width=30)
        alias_entry.pack(pady=5)
        alias_entry.insert(0, "Ghost")
        
        ttk.Label(frame, text="Choose your district:").pack(pady=5)
        district_var = tk.StringVar(value=CITY_DISTRICTS[0])
        district_dropdown = ttk.Combobox(frame, textvariable=district_var, values=CITY_DISTRICTS, state="readonly")
        district_dropdown.pack(pady=5)
        
        ttk.Label(frame, text="Choose your crime:").pack(pady=5)
        crime_var = tk.StringVar(value=CRIME_TYPES[0])
        crime_dropdown = ttk.Combobox(frame, textvariable=crime_var, values=CRIME_TYPES, state="readonly")
        crime_dropdown.pack(pady=5)
        
        def start():
            alias = alias_entry.get().strip() or "Ghost"
            district = district_var.get()
            crime = crime_var.get()
            
            self.player["alias"] = alias
            self.player["district"] = district
            self.player["mission"] = f"Pull off a {crime}"
            self.player["crime"] = crime
            self.player["cash"] += 50
            
            self.show_criminal_game()
        
        ttk.Button(frame, text="Start Criminal Mission", command=start).pack(pady=30)
    
    def show_law_setup(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Law Agent Setup", font=("Arial", 16, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Choose your agency:").pack(pady=10)
        agency_var = tk.StringVar(value=AGENCIES[0])
        agency_dropdown = ttk.Combobox(frame, textvariable=agency_var, values=AGENCIES, state="readonly")
        agency_dropdown.pack(pady=10)
        
        def start():
            agency = agency_var.get()
            self.player["agency"] = agency
            self.player["mission"] = "Investigate the city crime"
            self.suspect, self.crime = create_case()
            self.suspicion_score = 0
            self.turn = 0
            self.show_law_game()
        
        ttk.Button(frame, text="Start Investigation", command=start).pack(pady=30)
    
    def show_criminal_game(self):
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(main_frame, text="Character Stats")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats_text = f"""
Name: {self.player['name']}  |  Alias: {self.player['alias']}  |  District: {self.player['district']}
Cash: ${self.player['cash']}  |  Health: {self.player['health']}  |  Skill: {self.player['skill']}  |  Reputation: {self.player['reputation']}
Suspicion: {self.player['suspicion']}/22  |  Mission: {self.player['mission']}
        """
        
        stats_label = ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT)
        stats_label.pack(padx=10, pady=10)
        
        # Story frame
        story_frame = ttk.LabelFrame(main_frame, text="Mission Log")
        story_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        story_text = scrolledtext.ScrolledText(story_frame, height=15, width=100, bg="#222222", fg="#00ff00")
        story_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        story_text.config(state=tk.DISABLED)
        self.story_text = story_text
        
        self.add_story("You are planning a crime. Choose your moves carefully to avoid getting caught.")
        
        # Actions frame
        actions_frame = ttk.LabelFrame(main_frame, text="Available Actions")
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        actions = [
            ("Destroy Evidence", lambda: self.criminal_action("Destroy evidence", 2, 15)),
            ("Forge an Alibi", lambda: self.criminal_action("Forge an alibi", 1, 10)),
            ("Bribe a Witness", lambda: self.criminal_action("Bribe a witness", 3, -30)),
            ("Use Fake Identity", lambda: self.criminal_action("Use a fake identity", 1, 5)),
            ("Move Stolen Goods", lambda: self.criminal_action("Move stolen goods", 2, 20)),
            ("Hide in Safe House", lambda: self.criminal_action("Hide in a safe house", 1, 0)),
            ("Hire a Hacker", lambda: self.criminal_action("Use a hacker", 3, -25)),
            ("Scout Area", lambda: self.criminal_action("Scout the area", 1, 0)),
        ]
        
        button_frame = ttk.Frame(actions_frame)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for action_name, command in actions:
            ttk.Button(button_frame, text=action_name, command=command).pack(side=tk.LEFT, padx=5)
    
    def criminal_action(self, action, suspicion_add, cash_add):
        self.player["suspicion"] += suspicion_add
        self.player["cash"] += cash_add
        self.player["health"] = max(0, self.player["health"] - random.randint(0, 6))
        
        self.add_story(f"Action: {action}")
        self.add_story(f"Suspicion increased by {suspicion_add} (Total: {self.player['suspicion']}/22)")
        
        if cash_add != 0:
            self.add_story(f"Cash changed by ${cash_add} (Total: ${self.player['cash']})")
        
        event = random.randint(1, 5)
        if event == 1:
            self.add_story("⚠️ A surveillance team is nearby!")
            self.player["suspicion"] += 2
        elif event == 2:
            self.add_story("⚠️ A witness noticed something suspicious about your disguise.")
            self.player["suspicion"] += 1
        elif event == 3:
            self.add_story("⚠️ One of your contacts panicked and talked too much.")
            self.player["suspicion"] += 2
        elif event == 4:
            self.add_story("⚠️ The police noticed suspicious financial transfers.")
            self.player["suspicion"] += 2
        else:
            self.add_story("✓ No immediate threat detected.")
        
        if self.player["suspicion"] >= 22:
            self.add_story("\n🚔 THE POLICE HAVE IDENTIFIED YOU!")
            self.player["status"] = "caught"
            self.end_criminal_game()
        elif self.player["suspicion"] >= 18:
            self.add_story("\n⚠️ WARNING: The investigation is closing in on you!")
        elif self.player["health"] <= 0:
            self.add_story("\n💀 You were seriously injured. Your escape route collapsed.")
            self.player["status"] = "dead"
            self.end_criminal_game()
        else:
            self.show_criminal_game()
        
        save_game(self.player)
    
    def end_criminal_game(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if self.player["status"] == "caught":
            result_text = "GAME OVER - YOU WERE CAUGHT\nThe authorities identified you and arrested you."
        elif self.player["status"] == "dead":
            result_text = "GAME OVER - YOU DIED\nYou did not survive the night."
        else:
            result_text = f"MISSION SUCCESS!\nYou escaped as {self.player['alias']} and completed the {self.player['crime']}."
            self.player["reputation"] += 12
            self.player["cash"] += 150
        
        ttk.Label(frame, text=result_text, font=("Arial", 14), justify=tk.CENTER).pack(pady=30)
        
        stats = f"""
Final Stats:
Name: {self.player['name']}
Alias: {self.player['alias']}
Cash: ${self.player['cash']}
Reputation: {self.player['reputation']}
Final Suspicion: {self.player['suspicion']}/22
        """
        
        ttk.Label(frame, text=stats, font=("Arial", 11), justify=tk.CENTER).pack(pady=20)
        
        ttk.Button(frame, text="Return to Main Menu", command=self.show_main_menu).pack(pady=20)
        
        save_game(self.player)
    
    def show_law_game(self):
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(main_frame, text="Investigation Stats")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.turn += 1
        stats_text = f"""
Agent: {self.player['name']}  |  Agency: {self.player['agency']}  |  Turn: {self.turn}/5
Evidence Score: {self.suspicion_score}/12
        """
        
        stats_label = ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT)
        stats_label.pack(padx=10, pady=10)
        
        # Story frame
        story_frame = ttk.LabelFrame(main_frame, text="Investigation Log")
        story_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        story_text = scrolledtext.ScrolledText(story_frame, height=12, width=100, bg="#222222", fg="#00ff00")
        story_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        story_text.config(state=tk.DISABLED)
        self.story_text = story_text
        
        if self.turn == 1:
            self.add_story("A major crime has occurred in the city. You must investigate and catch the criminal.")
        
        # Actions frame
        actions_frame = ttk.LabelFrame(main_frame, text="Investigation Actions")
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        actions = [
            ("Interview Suspect", self.interview_suspect),
            ("Inspect Crime Scene", self.inspect_scene),
            ("Review Financial Records", self.review_finances),
            ("Check Security Footage", self.check_footage),
            ("Question Witness", self.question_witness),
            ("Analyze Digital Evidence", self.analyze_digital),
            ("Send Informant", self.send_informant),
        ]
        
        button_frame = ttk.Frame(actions_frame)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for action_name, command in actions:
            ttk.Button(button_frame, text=action_name, command=command).pack(side=tk.LEFT, padx=5)
        
        if self.turn >= 5:
            ttk.Button(button_frame, text="FINAL JUDGMENT", command=self.law_final_judgment, fg="red").pack(side=tk.LEFT, padx=5)
    
    def interview_suspect(self):
        suspect = random.choice(SUSPECTS)
        self.add_story(f"\n📋 You interview {suspect['name']}, a {suspect['role']}.")
        self.add_story(f"Statement: '{suspect['alibi']}'")
        
        if suspect["name"] == self.suspect["name"]:
            self.add_story("⚠️ This suspect appears NERVOUS and INCONSISTENT!")
            self.suspicion_score += 2
        else:
            self.add_story("✓ This suspect seems credible but not strongly connected.")
            self.suspicion_score += 1
        
        self.add_story(f"Evidence Score: {self.suspicion_score}/12")
        self.check_law_game_end()
    
    def inspect_scene(self):
        self.add_story("\n🔍 You examine the crime scene in detail.")
        clue = random_clue()
        self.add_story(f"Found clue: {clue}")
        
        if random.randint(1, 2) == 1:
            self.add_story("✓ This clue points toward the main suspect!")
            self.suspicion_score += 2
        else:
            self.add_story("The clue helps, but it is not definitive.")
            self.suspicion_score += 1
        
        self.add_story(f"Evidence Score: {self.suspicion_score}/12")
        self.check_law_game_end()
    
    def review_finances(self):
        self.add_story("\n💰 You audit financial records and transactions.")
        self.add_story("Found: Suspicious money movements linked to the victim.")
        self.suspicion_score += 2
        self.add_story(f"Evidence Score: {self.suspicion_score}/12")
        self.check_law_game_end()
    
    def check_footage(self):
        self.add_story("\n📹 You review security footage.")
        self.add_story("Spotted: Someone with a distinctive glove near the scene.")
        self.suspicion_score += 2
        self.add_story(f"Evidence Score: {self.suspicion_score}/12")
        self.check_law_game_end()
    
    def question_witness(self):
        self.add_story("\n👤 You question a witness from the scene.")
        self.add_story("Witness says: 'I heard someone mention money and revenge.'")
        self.suspicion_score += 2
        self.add_story(f"Evidence Score: {self.suspicion_score}/12")
        self.check_law_game_end()
    
    def analyze_digital(self):
        self.add_story("\n💻 You inspect digital evidence and logs.")
        self.add_story("Found: Fake identity records and altered access logs.")
        self.suspicion_score += 2
        self.add_story(f"Evidence Score: {self.suspicion_score}/12")
        self.check_law_game_end()
    
    def send_informant(self):
        self.add_story("\n🕵️ You send an informant to gather information.")
        self.add_story("Informant reports: Hostile reaction when suspect is questioned.")
        self.suspicion_score += 2
        self.add_story(f"Evidence Score: {self.suspicion_score}/12")
        self.check_law_game_end()
    
    def check_law_game_end(self):
        if self.turn >= 5:
            self.add_story("\n⏱️ Time for final judgment! Make your case.")
        else:
            self.show_law_game()
    
    def law_final_judgment(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="FINAL JUDGMENT", font=("Arial", 16, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Who is the criminal?").pack(pady=10)
        suspect_var = tk.StringVar(value=SUSPECTS[0]["name"])
        suspect_dropdown = ttk.Combobox(frame, textvariable=suspect_var, values=[s["name"] for s in SUSPECTS], state="readonly")
        suspect_dropdown.pack(pady=10)
        
        ttk.Label(frame, text="What crime was committed?").pack(pady=10)
        crime_var = tk.StringVar(value=CRIME_TYPES[0])
        crime_dropdown = ttk.Combobox(frame, textvariable=crime_var, values=CRIME_TYPES, state="readonly")
        crime_dropdown.pack(pady=10)
        
        ttk.Label(frame, text="What was the motive?").pack(pady=10)
        motive_var = tk.StringVar(value="Money")
        motive_dropdown = ttk.Combobox(frame, textvariable=motive_var, values=["Money", "Revenge", "Power", "Blackmail", "Debt", "Jealousy", "Control"], state="readonly")
        motive_dropdown.pack(pady=10)
        
        def submit_verdict():
            suspect = suspect_var.get()
            crime = crime_var.get()
            motive = motive_var.get()
            
            correct = (
                suspect == self.suspect["name"] and
                crime == self.crime and
                motive.lower() in self.suspect["motive"].lower()
            )
            
            self.show_verdict(correct, suspect, crime, motive)
        
        ttk.Button(frame, text="Submit Verdict", command=submit_verdict).pack(pady=30)
    
    def show_verdict(self, correct, selected_suspect, selected_crime, selected_motive):
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if correct:
            result = "✓ CASE SOLVED!\nYou caught the criminal and solved the case!\nThe city is safe."
            self.player["reputation"] += 10
            self.player["cash"] += 200
        else:
            result = "✗ CASE NOT SOLVED\nYou were unable to catch the criminal.\nThe criminal escaped for now."
        
        ttk.Label(frame, text=result, font=("Arial", 14), justify=tk.CENTER).pack(pady=30)
        
        verdict_text = f"""
Your Verdict:
- Suspect: {selected_suspect}
- Crime: {selected_crime}
- Motive: {selected_motive}

Correct Answer:
- Suspect: {self.suspect["name"]}
- Crime: {self.crime}
- Motive: {self.suspect["motive"]}
- Method: {self.suspect["method"]}

Final Stats:
- Reputation: {self.player['reputation']}
- Cash: ${self.player['cash']}
        """
        
        ttk.Label(frame, text=verdict_text, font=("Arial", 10), justify=tk.LEFT).pack(pady=20)
        
        ttk.Button(frame, text="Return to Main Menu", command=self.show_main_menu).pack(pady=20)
        
        save_game(self.player)
    
    def add_story(self, text):
        self.story_text.config(state=tk.NORMAL)
        self.story_text.insert(tk.END, text + "\n")
        self.story_text.see(tk.END)
        self.story_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GameGUI(root)
    root.mainloop()
