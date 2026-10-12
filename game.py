import random
import sys
import time


# -----------------------------
# Game setup
# -----------------------------

AGENCIES = ["COP", "FBI", "CIA", "CSI"]
CRIMES = [
    "Bank Robbery",
    "Art Theft",
    "Drug Smuggling",
    "Identity Theft",
    "Cyber Hacking",
    "Blackmail",
    "Kidnapping",
    "Money Laundering",
]

SUSPECTS = [
    {
        "name": "Marcus Vale",
        "role": "Former accountant",
        "motive": "He wants revenge after being fired and humiliated.",
        "method": "Used inside knowledge to access the vault.",
        "alibi": "He says he was at the gym, but his card was used later at a hotel.",
        "weakness": "He gets angry when anyone mentions his firing.",
    },
    {
        "name": "Sofia Quinn",
        "role": "Tech specialist",
        "motive": "She needed cash to cover a gambling debt.",
        "method": "Hacked security cameras and bypassed locks.",
        "alibi": "She says she was in a server room all night.",
        "weakness": "She checks her phone constantly when nervous.",
    },
    {
        "name": "Darren Cross",
        "role": "Nightclub owner",
        "motive": "He wanted to destroy a rival gang and steal their shipment.",
        "method": "Used a fake delivery truck to move stolen goods.",
        "alibi": "He claims he hosted a private event, but the cameras were disabled.",
        "weakness": "He brags when he feels safe.",
    },
    {
        "name": "Elena Frost",
        "role": "Luxury broker",
        "motive": "She planned to sell the stolen documents to foreign buyers.",
        "method": "Used forged paperwork to move the evidence.",
        "alibi": "She was at a charity gala, but one photo was altered.",
        "weakness": "She hates being questioned in public.",
    },
]

CLUES = [
    "A black glove was found near the crime scene.",
    "An encrypted USB drive was recovered from a trash bin.",
    "A witness heard the suspect say: 'This is about revenge and money.'",
    "A fake receipt was found in a suspect's coat pocket.",
    "A phone ping placed the suspect near the target location.",
    "The crime shows insider knowledge of the building layout.",
    "A hidden safe house was discovered with stolen goods and a map.",
    "A financial trail links one suspect to recent suspicious transfers.",
]


def slow_print(text, delay=0.025):
    for char in text:
        print(char, end="", flush=True)
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


# -----------------------------
# Law enforcement game
# -----------------------------

def generate_case():
    suspect = random.choice(SUSPECTS)
    crime = random.choice(CRIMES)
    return suspect, crime


def law_game():
    clear_screen()
    slow_print("You have chosen to protect the city.")
    slow_print("A major crime has been committed, and your job is to catch the culprit.")

    agency = AGENCIES[ask_choice("Choose your agency:", AGENCIES) - 1]
    slow_print(f"You are now working with the {agency}.")
    slow_print("The city is counting on you to solve the case.")

    culprit, crime = generate_case()
    correct_suspect = culprit["name"]
    correct_crime = crime
    correct_motive = culprit["motive"]

    suspicion = 0
    max_turns = 5

    for round_number in range(1, max_turns + 1):
        clear_screen()
        slow_print(f"Investigation round {round_number}/{max_turns}")

        action_options = [
            "Interview a suspect",
            "Inspect the crime scene",
            "Review financial records",
            "Check security footage",
            "Question a witness",
            "Analyze digital evidence",
        ]

        action = action_options[ask_choice("What do you investigate next?", action_options) - 1]

        if action == "Interview a suspect":
            suspect = random.choice(SUSPECTS)
            slow_print(f"You interview {suspect['name']}, a {suspect['role']}.")
            slow_print(f"Their statement: '{suspect['alibi']}'")
            if suspect["name"] == correct_suspect:
                slow_print("This suspect seems nervous and inconsistent.")
                suspicion += 2
            else:
                slow_print("This suspect gives a believable answer, but it doesn't match the evidence.")
                suspicion += 1

        elif action == "Inspect the crime scene":
            slow_print("You search the crime scene closely.")
            slow_print(f"You find: {random.choice(CLUES)}")
            if random.randint(1, 2) == 1:
                slow_print("The clue links to the main suspect.")
                suspicion += 2
            else:
                slow_print("The clue is useful but not decisive.")
                suspicion += 1

        elif action == "Review financial records":
            slow_print("You examine recent financial activity.")
            slow_print("You discover suspicious transfers tied to the victim's account.")
            suspicion += 2

        elif action == "Check security footage":
            slow_print("You study camera footage.")
            slow_print("A suspect appears near the scene wearing a dark jacket and a distinctive glove.")
            suspicion += 2

        elif action == "Question a witness":
            slow_print("You interview a witness at the scene.")
            slow_print("The witness says: 'I heard someone say the motive was money and revenge.'")
            suspicion += 2

        elif action == "Analyze digital evidence":
            slow_print("You inspect phones, log files, and digital records.")
            slow_print("One device was used to create fake access records.")
            suspicion += 2

        print()
        slow_print(f"Current case pressure: {suspicion}/10")

    clear_screen()
    slow_print("The case is ready for your final judgment.")

    suspect_names = [suspect["name"] for suspect in SUSPECTS]
    selected_suspect = suspect_names[ask_choice("Who do you think committed the crime?", suspect_names) - 1]

    selected_crime = CRIMES[ask_choice("What crime was committed?", CRIMES) - 1]

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
        slow_print("Case solved! You caught the criminal.")
        slow_print(f"Criminal: {correct_suspect}")
        slow_print(f"Crime: {correct_crime}")
        slow_print(f"Motive: {correct_motive}")
        slow_print(f"Method: {culprit['method']}")
        slow_print("The city is safe, and justice wins.")
    else:
        slow_print("The case is not solved.")
        slow_print("The criminal escaped this time.")
        slow_print(f"Correct suspect: {correct_suspect}")
        slow_print(f"Correct crime: {correct_crime}")
        slow_print(f"Correct motive: {correct_motive}")
        slow_print(f"Method: {culprit['method']}")
        slow_print("You need more evidence and a stronger strategy next time.")


# -----------------------------
# Criminal game
# -----------------------------

def criminal_game():
    clear_screen()
    slow_print("You have chosen the criminal path.")
    slow_print("Your goal is to commit the crime and avoid being caught.")

    crime = CRIMES[ask_choice("Choose the crime you want to commit:", CRIMES) - 1]
    alias = input("Choose your criminal alias: ").strip() or "Ghost"

    slow_print(f"Alias accepted: {alias}")
    slow_print(f"You are planning a {crime}.")
    slow_print("The police are watching. Stay hidden and keep your story straight.")

    suspicion = 0
    max_rounds = 5

    for round_number in range(1, max_rounds + 1):
        clear_screen()
        slow_print(f"Operation round {round_number}/{max_rounds}")

        actions = [
            "Destroy evidence",
            "Forge an alibi",
            "Bribe a witness",
            "Use a fake identity",
            "Move stolen goods",
            "Hide in a safe house",
            "Use a hacker to delete traces",
            "Create a decoy location",
        ]

        action = actions[ask_choice("Choose your move:", actions) - 1]

        if action == "Destroy evidence":
            slow_print("You destroy files, receipts, and records.")
            suspicion += 2
        elif action == "Forge an alibi":
            slow_print("You build a fake story and create fake schedules.")
            suspicion += 1
        elif action == "Bribe a witness":
            slow_print("You pay someone to keep quiet.")
            suspicion += 3
        elif action == "Use a fake identity":
            slow_print("You switch to a false identity and alter your appearance.")
            suspicion += 1
        elif action == "Move stolen goods":
            slow_print("You move the stolen items to a safer location.")
            suspicion += 2
        elif action == "Hide in a safe house":
            slow_print("You stay away from public places and cut contact.")
            suspicion += 1
        elif action == "Use a hacker to delete traces":
            slow_print("You bring in a hacker to erase digital evidence.")
            suspicion += 3
        elif action == "Create a decoy location":
            slow_print("You set up a fake location to mislead the investigators.")
            suspicion += 2

        event = random.randint(1, 5)
        if event == 1:
            slow_print("A surveillance team is nearby. You must stay calm.")
            suspicion += 2
        elif event == 2:
            slow_print("A witness noticed a suspicious detail about your disguise.")
            suspicion += 1
        elif event == 3:
            slow_print("One of your contacts starts panicking and talks too much.")
            suspicion += 2
        elif event == 4:
            slow_print("The police notice suspicious money transfers.")
            suspicion += 2
        elif event == 5:
            slow_print("No major trouble yet. Keep moving.")

        print(f"Current suspicion level: {suspicion}/20")

        if suspicion >= 18:
            slow_print("The law is closing in on you.")
            slow_print("You have been identified by the authorities.")
            break

    clear_screen()
    if suspicion >= 18:
        slow_print("You were caught.")
        slow_print("The investigators found out who you are and what you did.")
        slow_print("The city wins this round.")
    else:
        slow_print("The investigation failed to catch you.")
        slow_print(f"Alias: {alias}")
        slow_print(f"Crime: {crime}")
        slow_print("You escaped without being discovered.")
        slow_print("You win as the criminal mastermind.")


# -----------------------------
# Main menu
# -----------------------------

def main_menu():
    clear_screen()
    slow_print("Welcome to the game: City of Shadows")
    slow_print("Choose your side.")
    slow_print("You can either play as a criminal or as a law enforcement agent.")

    menu_options = [
        "Play as a criminal",
        "Play as a law agent",
        "Exit",
    ]

    choice = menu_options[ask_choice("Main menu:", menu_options) - 1]

    if choice == "Play as a criminal":
        criminal_game()
    elif choice == "Play as a law agent":
        law_game()
    else:
        slow_print("Goodbye.")
        sys.exit(0)


if __name__ == "__main__":
    main_menu()
