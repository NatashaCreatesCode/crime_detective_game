import json
import os
import random
import sys
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


def slow_print(text, delay=0.025):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def clear_screen():
    print("\n" * 2)


def ask_choice(prompt, options):
    print(prompt)
    for index, option in enumerate(options, start=1):
        print(f"  {index}. {option}")
    while True:
        try:
            choice = int(input("Choose: ").strip())
            if 1 <= choice <= len(options):
                return choice
            print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")


def make_player():
    player = {
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
    return player


def save_game(player):
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f, indent=2)


def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return None


def choose_name():
    name = input("Enter your character name: ").strip()
    if not name:
        return "Shadow"
    return name


def random_clue():
    return random.choice(CLUES)


def create_case():
    suspect = random.choice(SUSPECTS)
    crime = random.choice(CRIME_TYPES)
    return suspect, crime


def show_stats(player):
    print("\n--- Character Stats ---")
    print(f"Name: {player['name']}")
    print(f"Side: {player['side']}")
    print(f"Cash: ${player['cash']}")
    print(f"Health: {player['health']}")
    print(f"Skill: {player['skill']}")
    print(f"Reputation: {player['reputation']}")
    print(f"Suspicion: {player['suspicion']}")
    print(f"District: {player['district']}")
    if player['side'] == "criminal":
        print(f"Alias: {player['alias']}")
    else:
        print(f"Agency: {player['agency']}")


# --------------------------------------------------
# LAW ENFORCEMENT MODE
# --------------------------------------------------

def law_game(player):
    clear_screen()
    slow_print("You have chosen to defend the city.")
    slow_print("A dangerous crime is underway. Your mission is to catch the criminal.")
    slow_print("Find the suspect, the crime, and the motive.")

    player["agency"] = AGENCIES[ask_choice("Choose your agency:", AGENCIES) - 1]
    player["side"] = "law"
    player["mission"] = "Investigate the city crime"

    suspect, crime = create_case()
    correct_suspect = suspect["name"]
    correct_crime = crime
    correct_motive = suspect["motive"]

    suspicion_score = 0
    for turn in range(1, 6):
        clear_screen()
        show_stats(player)
        slow_print(f"\n--- Investigation Turn {turn}/5 ---")

        actions = [
            "Interview a suspect",
            "Inspect the crime scene",
            "Review financial records",
            "Check security footage",
            "Question a witness",
            "Analyze digital evidence",
            "Send an informant",
        ]

        action = actions[ask_choice("Choose your move:", actions) - 1]

        if action == "Interview a suspect":
            other = random.choice(SUSPECTS)
            slow_print(f"You interview {other['name']}, a {other['role']}.")
            slow_print(f"They say: '{other['alibi']}'")
            if other["name"] == correct_suspect:
                slow_print("This suspect looks unusually nervous and inconsistent.")
                suspicion_score += 2
            else:
                slow_print("This suspect seems credible but not strongly connected.")
                suspicion_score += 1

        elif action == "Inspect the crime scene":
            slow_print("You examine the scene in detail.")
            clue = random_clue()
            slow_print(f"Found clue: {clue}")
            if random.randint(1, 2) == 1:
                slow_print("This clue points toward the main suspect.")
                suspicion_score += 2
            else:
                slow_print("The clue helps, but it is not enough alone.")
                suspicion_score += 1

        elif action == "Review financial records":
            slow_print("You audit records and find suspicious money movement.")
            suspicion_score += 2

        elif action == "Check security footage":
            slow_print("You review the security feed and spot someone with a distinctive glove.")
            suspicion_score += 2

        elif action == "Question a witness":
            slow_print("You question a witness.")
            slow_print("The witness says: 'I heard someone say this was about money and revenge.'")
            suspicion_score += 2

        elif action == "Analyze digital evidence":
            slow_print("You inspect logs and digital traces.")
            slow_print("A fake identity and altered records appear in the suspect's activity.")
            suspicion_score += 2

        elif action == "Send an informant":
            slow_print("You send an informant to gather more information.")
            slow_print("The informant reports a hostile reaction when the suspect is questioned.")
            suspicion_score += 2

        print(f"Current evidence score: {suspicion_score}/12")
        save_game(player)
        input("Press Enter to continue...")

    clear_screen()
    slow_print("The case is ready for final judgment.")
    suspect_names = [s["name"] for s in SUSPECTS]
    selected_suspect = suspect_names[ask_choice("Who is the criminal?", suspect_names) - 1]

    selected_crime = CRIMES[ask_choice("What crime was committed?", CRIME_TYPES) - 1]

    motive_choices = [
        "Money",
        "Revenge",
        "Power",
        "Blackmail",
        "Debt",
        "Jealousy",
        "Control",
    ]
    selected_motive = motive_choices[ask_choice("What was the motive?", motive_choices) - 1]

    print()
    slow_print("Final verdict:")

    if (
        selected_suspect == correct_suspect
        and selected_crime == correct_crime
        and selected_motive.lower() in correct_motive.lower()
    ):
        slow_print("Case solved! The city is safe.")
        slow_print(f"Criminal: {correct_suspect}")
        slow_print(f"Crime: {correct_crime}")
        slow_print(f"Motive: {correct_motive}")
        slow_print(f"Method: {suspect['method']}")
        player["reputation"] += 10
        player["cash"] += 200
        slow_print("You earned a promotion and a reward bonus.")
    else:
        slow_print("You were unable to solve the case.")
        slow_print(f"Correct suspect: {correct_suspect}")
        slow_print(f"Correct crime: {correct_crime}")
        slow_print(f"Correct motive: {correct_motive}")
        slow_print(f"Method: {suspect['method']}")
        slow_print("The criminal escaped for now.")

    save_game(player)
    input("Press Enter to return to the main menu...")


# --------------------------------------------------
# CRIMINAL MODE
# --------------------------------------------------

def criminal_game(player):
    clear_screen()
    slow_print("You have chosen the criminal path.")
    slow_print("Your goal: commit the crime, hide your role, and avoid being caught.")
    player["side"] = "criminal"

    alias = input("Choose your criminal alias: ").strip() or "Ghost"
    player["alias"] = alias
    player["mission"] = "Pull off a major crime"

    district = CITY_DISTRICTS[ask_choice("Choose your district for the job:", CITY_DISTRICTS) - 1]
    player["district"] = district

    crime = CRIME_TYPES[ask_choice("Choose the crime you want to commit:", CRIME_TYPES) - 1]
    player["cash"] += 50

    suspicion = 0
    health = 100
    rounds = 0
    target_summary = f"You are planning a {crime} in {district}."

    while rounds < 6:
        clear_screen()
        show_stats(player)
        slow_print(f"\n{target_summary}")
        slow_print(f"--- Criminal Turn {rounds + 1}/6 ---")

        actions = [
            "Destroy evidence",
            "Forge an alibi",
            "Bribe a witness",
            "Use a fake identity",
            "Move stolen goods",
            "Hide in a safe house",
            "Use a hacker",
            "Scout the area",
        ]

        action = actions[ask_choice("Choose your move:", actions) - 1]

        if action == "Destroy evidence":
            slow_print("You destroy receipts, files, and records.")
            suspicion += 2
            player["cash"] += 15
        elif action == "Forge an alibi":
            slow_print("You build a fake story and manipulate witness statements.")
            suspicion += 1
            player["cash"] += 10
        elif action == "Bribe a witness":
            slow_print("You pay a witness to stay quiet.")
            suspicion += 3
            player["cash"] -= 30
        elif action == "Use a fake identity":
            slow_print("You switch to a false identity and alter your appearance.")
            suspicion += 1
            player["cash"] += 5
        elif action == "Move stolen goods":
            slow_print("You move the stolen goods to a safer place.")
            suspicion += 2
            player["cash"] += 20
        elif action == "Hide in a safe house":
            slow_print("You hole up in a safe house and avoid public attention.")
            suspicion += 1
            player["health"] += 5
        elif action == "Use a hacker":
            slow_print("You use a hacker to erase digital traces.")
            suspicion += 3
            player["cash"] -= 25
        elif action == "Scout the area":
            slow_print("You observe patrol routes and weak points.")
            suspicion += 1
            player["skill"] += 5

        event = random.randint(1, 5)
        if event == 1:
            slow_print("A surveillance team is nearby. You stay calm and keep moving.")
            suspicion += 2
        elif event == 2:
            slow_print("A witness noticed a suspicious detail about your disguise.")
            suspicion += 1
        elif event == 3:
            slow_print("One of your contacts panics and talks too much.")
            suspicion += 2
        elif event == 4:
            slow_print("The police notice suspicious financial transfers.")
            suspicion += 2
        elif event == 5:
            slow_print("No problem yet. Keep the pressure low.")

        player["suspicion"] = suspicion
        player["health"] = max(0, min(100, player["health"] - random.randint(0, 6)))
        player["skill"] = max(0, min(100, player["skill"]))

        if player["health"] <= 0:
            slow_print("You were seriously injured and your escape route collapsed.")
            player["status"] = "dead"
            break

        if suspicion >= 18:
            slow_print("The investigation is closing in. You are in danger.")
            slow_print("The authorities are starting to recognize your pattern.")

        if suspicion >= 22:
            slow_print("The police have identified you.")
            player["status"] = "caught"
            break

        slow_print(f"Current suspicion: {suspicion}/22")
        save_game(player)
        input("Press Enter to continue...")
        rounds += 1

    clear_screen()
    if player["status"] == "caught":
        slow_print("You were caught.")
        slow_print("The investigators found out who you are and what you did.")
        slow_print("The city wins this time.")
    elif player["status"] == "dead":
        slow_print("You were injured badly and your criminal run ended.")
        slow_print("You did not survive the night.")
    else:
        slow_print("Mission successful.")
        slow_print(f"Alias: {alias}")
        slow_print(f"Crime: {crime}")
        slow_print("You executed the plan, stayed hidden, and escaped the investigators.")
        slow_print("You win as the criminal mastermind.")
        player["reputation"] += 12
        player["cash"] += 150

    save_game(player)
    input("Press Enter to return to the main menu...")


# --------------------------------------------------
# MAIN MENU
# --------------------------------------------------

def main_menu():
    print("""
    ██████╗██╗██████╗  █████╗ ████████╗███████╗██╗     ██╗ ██████╗ ███████╗
    ██╔════╝██║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║     ██║██╔═══██╗██╔════╝
    ██║     ██║██████╔╝███████║   ██║   █████╗  ██║     ██║██║   ██║█████╗  
    ██║     ██║██╔══██╗██╔══██║   ██║   ██╔══╝  ██║     ██║██║   ██║██╔══╝  
    ╚██████╗██║██║  ██║██║  ██║   ██║   ███████╗███████╗██║╚██████╔╝███████╗
    ╚═════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝╚═╝ ╚═════╝ ╚══════╝
    """)
    print("Welcome to City of Shadows")
    print("Choose your path in a city filled with secrets, danger, and ambition.")

    if os.path.exists(SAVE_FILE):
        saved = load_game()
        if saved:
            choice = ask_choice("Main menu:", ["New Game", "Load Saved Game", "Exit"])
            if choice == 1:
                player = make_player()
                player["name"] = choose_name()
                return player
            elif choice == 2:
                return saved
            else:
                print("Goodbye.")
                sys.exit(0)

    choice = ask_choice("Main menu:", ["New Game", "Exit"])
    if choice == 1:
        player = make_player()
        player["name"] = choose_name()
        return player
    print("Goodbye.")
    sys.exit(0)


def game_loop():
    while True:
        player = main_menu()
        if player["name"] == "":
            player["name"] = "Shadow"

        if "side" in player and player["side"]:
            if player["side"] == "criminal":
                criminal_game(player)
            elif player["side"] == "law":
                law_game(player)
            else:
                role_choice = ask_choice("Choose your role:", ["Criminal", "Law Agent"])
                if role_choice == 1:
                    criminal_game(player)
                else:
                    law_game(player)
        else:
            role_choice = ask_choice("Choose your role:", ["Criminal", "Law Agent"])
            if role_choice == 1:
                criminal_game(player)
            else:
                law_game(player)

        save_game(player)


if __name__ == "__main__":
    game_loop()
