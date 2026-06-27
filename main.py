# EVOLVING LIFE
# FBLA Intro to Programming 2025-2026
# Made by Prayag Patel

import json
import random
import requests
import os

SAVE_FILE = "saves.json"
MISTRAL_API_KEY = "9K9CUwyGQ8go2Z145m8iTvFwyJSxDzeg"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# ------------- input string checker ------------

def load_filter_list(filename):
    """Reads the filter files and returns a list of lowercase strings."""
    if not os.path.exists(filename):
        # File not loading
        print(f"DEBUG: {filename} NOT FOUND in {os.getcwd()}")
        return []
    try:
        with open(filename, "r") as f:
            # strips and lowercases each line, and ignores empty lines
            data = [line.strip().lower() for line in f if line.strip()]
            return data
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

BANNED_WORDS = load_filter_list("Bad_words.txt")
ALLOWED_BREEDS = load_filter_list("breeds.txt")

# ---------------- utility stuff ----------------

def div():
    #line divider for cleaner menu8s
    print("=" * 50)

# ---------------- main pet / player ----------------

class Pet:
    def __init__(self, name, species):
        #sets us basic pet stats
        self.name = name
        self.species = species

        self.hunger = min(100, max(0, 30))
        self.thirst = min(100, max(0, 30))
        self.energy = min(100, max(0, 70))
        self.hygiene = min(100, max(0, 70))
        self.happiness = min(100, max(0, 50))
        self.health = min(100, max(0, 100))

        self.age_days = 0

        #sets us the skills and point system
        self.skill_points = 0
        self.skills = {
            "Agility": 0,
            "Intelligence": 0,
            "Strength": 0,
            "Charm": 0
        }

        self.traits = []
        self.titles = []

    def mood(self):
        #Used to print out the pet's mood in stat display based on happiness level
        hap = self.happiness
        if hap <= 10:
            return "Ran Away"
        elif hap <= 30:
            return "Sad"
        elif hap <= 40:
            return "Okay"
        elif hap <= 60:
            return "Happy"
        else:
            return "Energetic"


class Player:
    def __init__(self):
        # Sets up the player and initializes basic values and items
        self.day = 1
        self.week = 1

        self.sparks = 100
        self.income = 0
        self.expenses = 0

        self.inventory = {
            "Food": 5,
            "Water": 5,
            "Soap": 2
        }

# --------------- current save tracking -------------

CURRENT_SAVE_SLOT = None

# --------------- AI prompt request -------------

def ask_mistral(prompt):
    """
    Sends a prompt to Mistral and returns the assistant's reply as text.
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "mistral-small-latest",  # or another available model
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are helping a player understand how to play a text-based "
                    "virtual pet game called EVOLVING LIFE. Be clear and short."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.3,
    }

    try:
        resp = requests.post(MISTRAL_API_URL, headers=headers, json=data, timeout=15)
        resp.raise_for_status()
        j = resp.json()
        # Basic extraction of the first message text
        raw = j["choices"][0]["message"]["content"].strip()
        return '\n'.join(line.strip() for line in raw.split('\n') if line.strip())
    except Exception as e:
        return f"Sorry, I could not reach the AI right now. Error: {e}"


# ---------------- saving / loading ----------------

def load_saves_info():
    #loads your save file info into the program if it exists
    try:
        with open(SAVE_FILE, "r") as s:
            return json.load(s)
    except:
        #if no save file exists, then 4 empty slots get created
        return {"slot1": None, "slot2": None, "slot3": None, "slot4": None}

def write_saves_info(saves):
    #writes all the updated save data into the json file
    with open(SAVE_FILE, "w") as f:
        json.dump(saves, f, indent=4)

def pet_to_dict(p):
    return p.__dict__

def player_to_dict(pl):
    return pl.__dict__

def autosave_if_possible(pet, player):
    #checks to see if a save slot is connected and if it is then it will auto save
    if CURRENT_SAVE_SLOT is not None:
        save_game(CURRENT_SAVE_SLOT, pet, player, True)

def save_game(slot, pet, player, autosaver=False):
    saves = load_saves_info()

    # checks to see if the slot already has data and that the game isn't autosaving
    if saves.get(slot) is not None and not autosaver:
        pet_name = saves[slot]["pet"].get("name", "Unknown")
        day = saves[slot]["player"].get("day", "Unknown")
        print(f"WARNING: {slot.upper()} already has '{pet_name}' (Day {day})")
        confirm = input(f"Overwrite this save? (y/n): ").strip().lower()
        #if the user doesn't want to override the save then the saving process stops
        if confirm != "y":
            print("Save cancelled.")
            return False

    # If the program gets to this point then it will save the current game info into the specified slot
    saves[slot] = {"pet": pet_to_dict(pet), "player": player_to_dict(player)}
    write_saves_info(saves)
    print("Game saved to", slot.upper())
    return True


def clear_save(slot):
    #used in the loading menu to clear slots and make space for new saves
    saves = load_saves_info()
    if saves.get(slot) is None:
        print("That slot is already empty.")
        return
    confirm = input(f"Are you sure you want to clear {slot.upper()}? (y/n) ").strip().lower()
    if confirm == "y":
        saves[slot] = None
        write_saves_info(saves)
        print(slot.upper(), "cleared.")
    else:
        print("Clear cancelled.")

def load_game(slot):
    #after a slot has been confirmed to load from, the game will update the pet and player objects with the save data
    saves = load_saves_info()

    data = saves.get(slot)
    if not data:
        print("That slot is empty.")
        return None, None

    p = data["pet"]
    pet = Pet(p["name"], p["species"])
    pet.__dict__.update(p)

    pl = data["player"]
    player = Player()
    player.__dict__.update(pl)

    print("Loaded", slot.upper())
    return pet, player

def display_slots():
    #used to show the user the current save slots that are in use and the data inside them
    saves = load_saves_info()
    for i, key in enumerate(["slot1", "slot2", "slot3", "slot4"], start=1):
        info = saves.get(key)
        if info is None:
            print(f"{i}) {key} - EMPTY")
        else:
            pet_name = info["pet"].get("name", "Unknown")
            day = info["player"].get("day", "Unknown")
            print(f"{i}) {key} - {pet_name} | Day: {day}")


def save_load_menu(pet=None, player=None):
    #will display all the slots in the main menu and also gives the option to clear slots
    global CURRENT_SAVE_SLOT
    while True:
        div()
        print("SAVE / LOAD MENU")
        div()
        display_slots()
        print("5) Clear a slot")
        print("6) Cancel")
        choice = input("> ").strip()

        slots = {
            "1": "slot1",
            "2": "slot2",
            "3": "slot3",
            "4": "slot4"
        }

        if choice in slots:
            if pet is not None:  # SAVE MODE
                saved = save_game(slots[choice], pet, player)
                if saved:  # Only set slot if save succeeded
                    CURRENT_SAVE_SLOT = slots[choice]
            else:  # LOAD MODE
                pet, player = load_game(slots[choice])
                CURRENT_SAVE_SLOT = slots[choice]
                if pet is not None:
                    CURRENT_SAVE_SLOT = slots[choice]
            return pet, player  # Exit menu after save/load

        elif choice == "5":
            div()
            print("Which slot do you want to clear?")
            display_slots()
            sub = input("> ").strip()
            if sub in slots:
                clear_save(slots[sub])
            else:
                print("Not a valid slot.")
        elif choice == "6":
            return pet, player
        else:
            print("?? not a menu option")

# ---------------- displays ----------------

def show_status(pet, player):
    #displays all the stats while the game is being played
    div()
    print("Day", player.day, "| Week", player.week)
    print("Sparks:", player.sparks)
    print("Total expenses:", player.expenses)
    div()
    print(f"{pet.name} the {pet.species}")
    print("Mood:", pet.mood())
    print("Hunger:", pet.hunger, "| Thirst:", pet.thirst)
    print("Energy:", pet.energy, "| Hygiene:", pet.hygiene)
    print("Happiness:", pet.happiness, "| Health:", pet.health)
    print("Skill Points:", pet.skill_points)
    print("Skills:", pet.skills)
    div()

def show_end_stats(pet, player):
    #after the pet dies or runs away the game displays a final summary of the game
    print("")
    div()
    print("GAME SUMMARY")
    div()
    print(f"Pet: {pet.name} the {pet.species}")
    print(f"Final Day Reached: {player.day}")
    print(f"Final Health: {pet.health}")
    print(f"Final Happiness: {pet.happiness}")
    print(f"Total Sparks Remaining: {player.sparks}")
    print(f"Total Expenses: {player.expenses}")

    print("\nSkills Unlocked:")
    for skill, lvl in pet.skills.items():
        print(f"- {skill}: Level {lvl}")

    div()

def how_to_play_display():
    while True:
        print("Options:")
        print("1) Basic Tips")
        print("2) AI Q&A")
        print("3) Go back to home screen")
        choice = input("> ").strip().lower()

        if choice == "1":
            print("HOW TO PLAY")
            div()
            print("- Use your actions to keep your pet's stats in check")
            print("- Sparks are the in-game currency used to buy items")
            print("- If you run out of items buy them from the store")
            print("- Use skill points to upgrade your pets skills and have better event outcomes")
            print("- Make sure your pet doesn't reach a happiness or health below 10 or its game over")
            div()
        elif choice == "2":
            user_q = input("\nWhat would you like to know? \n> ")
            if user_q.strip() == "":
                print("Please type a question.")
                continue
            full_prompt = f"""
            The player asked: "{user_q}"

            Context: EVOLVING LIFE is a console-based pet game where you take care of a pet and
            manage the cost of caring for it using sparks (the in-game money). The whole game is
            controlled by entering numbers that correspond to actions based on a list of possible 
            actions.

            The goal is to keep your pet happy, healthy, and not go broke on sparks.
            pet has several important stats:
            
            Saving: There are 4 slots that can be accessed in your main screen when you are playing the game
            - 4 slots
            - Will only override if confirmed to override
            
            - Hunger: how hungry your pet is (high hunger is bad).
            - Thirst: how thirsty your pet is (high thirst is bad).
            - Energy: how tired your pet is (low energy is bad).
            - Hygiene: how clean your pet is (low hygiene is bad).
            - Happiness: how happy your pet is (low happiness can make them sad or leave).
            - Health: overall health (if this gets too low, things go badly).
            - Skill Points: points you can spend in the Skill Tree.
            
            Your player stats:
            
            - Day and Week: track how long you've been playing.
            - Sparks: your money.
            - Income: how much you've earned like through your weekly allowance.
            - Expenses: how much you've spent on your pet.
            
            During the main game loop you will see a menu like this:

            1. Feed
            2. Water
            3. Clean
            4. Play
            5. Inventory
            6. Skill Tree
            7. Store
            8. Save
            9. Next Day
            10. Health Check
            0. Quit
            
            Inventory:
            
            - Food: used to feed your pet.
            - Water: used to give your pet a drink.
            - Soap: used to clean your pet.
            
            There isn't a real way to win but you can think of winning as:
            
            - Keeping your pet alive, healthy, and happy for many days.
            - Managing sparks so you don't go broke.
            - Growing your pet's skills and watching its stats change over time.
            
            However you can lose if your pet's Happiness gets so low that it runs away or
            if its health goes too low and it dies.
            
            ---------------- Most Important Tips ----------------
            
            - Don't ignore Hunger and Thirst. High values can slowly damage Health.
            - Keep an eye on Hygiene; dirty pets are not happy or healthy.
            - Use Rest when Energy is low so your pet doesn't get completely drained.
            - Spend Skill Points whenever you have them so your pet feels like it is improving.
            - Try not to burn through sparks too fast. Think before you buy everything.
            - Use Health Check and the vet when Health drops too low.
            - Remember to save your game to a slot so you can load it later.
            
            If you balance care and money, your pet will stay around longer, be happier,
            and you will get the most out of EVOLVING LIFE.
            ===========================================================
            
            Response Guideline
            - Always respond in simple language
            - Give practical examples if needed: "If your pet has high hunger, use option 1 (Feed) twice."
            - Mention skill benefits briefly if relevant: "Upgrade Strength to make hunger grow slower."
            - keep response short
            """
            answer = ask_mistral(full_prompt)
            div()
            print("Answer:")
            print(answer)
            input("\nPress Enter to continue")
        elif choice == "3":
            return
        else:
            print("Not a valid option.")


# ---------------- actions ----------------

def feed(pet, player):
    if player.inventory.get("Food", 0) <= 0:
        print("No food left.")
        return
    player.inventory["Food"] -= 1
    pet.hunger = max(0, pet.hunger - 20)
    pet.happiness = min(100, pet.happiness + 5)
    print(f"You fed {pet.name}.")
    autosave_if_possible(pet, player)


def give_water(pet, player):
    if player.inventory.get("Water", 0) <= 0:
        print("No water left.")
        return
    player.inventory["Water"] -= 1
    pet.thirst = max(0, pet.thirst - 20)
    print(f"{pet.name} drank water.")
    autosave_if_possible(pet, player)

def clean(pet, player):
    if player.inventory.get("Soap", 0) <= 0:
        print("No soap left.")
        return
    player.inventory["Soap"] -= 1
    pet.hygiene = min(100, pet.hygiene + 30)
    pet.happiness = min(100, pet.happiness + 5)
    print(f"{pet.name} is cleaner now.")
    autosave_if_possible(pet, player)


def play(pet):
    if pet.energy <= 0:
        print(f"{pet.name} is too tired to play!")
        return
    pet.energy = max(0, pet.energy - random.randint(15,30))
    pet.hunger = min(100, pet.hunger + random.randint(2,7))
    pet.happiness = min(100, pet.happiness + random.randint(8,12))
    print(f"You and {pet.name} played together.")


def inventory(player):
    #Displays how much of each item the user currently has
    div()
    print("INVENTORY")
    print("Food:", player.inventory.get("Food", 0))
    print("Water:", player.inventory.get("Water", 0))
    print("Soap:", player.inventory.get("Soap", 0))
    print()
    input("Hit Enter to continue >")
    div()

def health_check(pet, player):
    #Checks to see if the pet needs a vet visit by lookng at their health stats
    div()
    print("HEALTH CHECK")
    print("Current health:", pet.health)
    if pet.health >= 80:
        print(f"{pet.name} looks healthy and strong.")
    elif pet.health >= 50:
        print(f"{pet.name} is okay but could be better.")
    else:
        print(f"{pet.name} is not doing well. Maybe visit the vet?")

    print("1. Visit vet (costs 25 sparks)")
    print("2. Back")
    choice = input("> ").strip()
    if choice == "1":
        if player.sparks >= 25:
            player.sparks -= 25
            player.expenses += 25
            pet.health = min(100, pet.health + 40)
            pet.happiness += 5
            print("You took your pet to the vet. Health improved.")
            autosave_if_possible(pet, player)
        else:
            print("Not enough sparks for a vet visit.")
    else:
        print("You decided not to visit the vet right now.")

# ---------------- skill tree ----------------

def skill_tree(pet):
    while True:
        div()
        print("SKILL TREE")
        print("Skill Points Available:", pet.skill_points)
        i = 1
        for skill in pet.skills:
            level = pet.skills[skill]
            cost = level + 1
            print(str(i) + ".", skill, "- Level", level, "(Cost:", cost, "points)")
            i += 1
        print("5. Exit")
        choice = input("> ").strip()

        if choice in ["1", "2", "3", "4"]:
            idx = int(choice) - 1
            skill_name = list(pet.skills.keys())[idx]
            current_level = pet.skills[skill_name]
            cost = current_level + 1
            if pet.skill_points >= cost:
                pet.skill_points -= cost
                pet.skills[skill_name] += 1
                print(skill_name, "increased to level", pet.skills[skill_name], "(-", cost, "points)")
            else:
                print("Not enough skill points. You need", cost, "points.")
        elif choice == "5":
            break
        else:
            print("Not a valid option.")



# ---------------- store ----------------

def store(player):
    while True:
        div()
        print("STORE")
        print("1. Food (10 sparks)")
        print("2. Water (5 sparks)")
        print("3. Soap (8 sparks)")
        print("4. Exit")
        c = input("> ").strip()

        if c == "1":
            if player.sparks >= 10:
                player.inventory["Food"] += 1
                player.sparks -= 10
                player.expenses += 10
                print("Bought food.")
            else:
                print("Not enough sparks.")
        elif c == "2":
            if player.sparks >= 5:
                player.inventory["Water"] += 1
                player.sparks -= 5
                player.expenses += 5
                print("Bought water.")
            else:
                print("Not enough sparks.")
        elif c == "3":
            if player.sparks >= 8:
                player.inventory["Soap"] += 1
                player.sparks -= 8
                player.expenses += 8
                print("Bought soap.")
            else:
                print("Not enough sparks.")
        elif c == "4":
            break
        else:
            print("Invalid choice.")

# ---------------- day progression ----------------

def random_event(pet,player):
    #Allows for random events to occur each day that can be both positive and negative
    events = [
        (f"{pet.name} found something shiny.", 5),
        (f"{pet.name} tripped while playing.", -5),
        ("A calm peaceful day.", 0),
        (f"{pet.name} learned faster today.", 10),
        ("Random health checkup at the vet.", 0),
        (f"{pet.name} felt a bit sick today.", -8),
    ]
    roll = random.random()

    if roll < 0.50:
        e = events[2]  # Calm peaceful day
    elif roll < 0.60:
        e = events[0]  # Found something shiny
    elif roll < 0.70:
        e = events[1]  # Tripped while playing
    elif roll < 0.80:
        e = events[3]  # Learned faster today
    elif roll < 0.90:
        e = events[5]  # Felt a bit sick
    else:
        e = events[4]  # Random health checkup

    txt, effect = e[0], e[1]
    print("Event:", txt)

    # skill effects on different events
    agility = pet.skills["Agility"]
    intelligence = pet.skills["Intelligence"]
    strength = pet.skills["Strength"]
    charm = pet.skills["Charm"]

    if txt == f"{pet.name} tripped while playing.":
        if agility >= 5:
            print("High Agility saved them! No harm done.")
        else:
            pet.health = max(0, pet.health - random.randint(3, 8))

    elif txt == f"{pet.name} learned faster today.":
        effect += intelligence  # Smart pets gain more happiness
        print(f"Intelligence bonus: +{intelligence} extra happiness!")

    elif txt == "Random health checkup at the vet.":
        if random.random() < 0.5:
            print(f"The vet said {pet.name} is fine. No charge.")
        else:
            if strength >= 5:
                print(f"{pet.name} is strong! He fought off his sickness.")
            else:
                c = input(f"Oh No! {pet.name} is sick. Pay 25 for treatment? (y/n): ").lower()
                if c == "y" and player.sparks<25:
                    print("Not enough sparks.")
                elif c == "y":
                    player.sparks -= 25
                    player.expenses += 25
                    pet.happiness = min(100, pet.happiness + 10)
                    pet.health = min(100, pet.health + 40)
                else:
                    pet.health = max(15, pet.health - 40)

    elif txt == f"{pet.name} felt a bit sick today.":
        if charm >= 3:
            print(f"{pet.name} cheered up despite feeling sick!")
            pet.health = max(15, pet.health - random.randint(2, 8))
        else:
            pet.health = max(15, pet.health - random.randint(5, 15))
        pet.happiness = max(0, pet.happiness + effect)

    else:
        # Apply base effect with skill multipliers
        final_effect = effect + (charm // 4)  # Charm boosts positive events
        pet.happiness = max(0, min(100, pet.happiness + final_effect))

        if final_effect < 0:
            pet.health = max(0, pet.health - random.randint(3, 8))
        elif final_effect > 0:
            pet.health = min(100, pet.health + random.randint(1, 4))


def end_day(pet, player):

    #adds skill points each day based on pets happiness level
    h = pet.happiness
    if h <= 30:
        gained = 0
    elif h <= 40:
        gained = 1
    elif h <= 60:
        gained = 2
    else:
        gained = 3

    pet.skill_points += gained

    #checks to see if the player gets weekly allowance
    if player.day % 7 == 0:
        player.sparks += 20
        player.week += 1
        player.income += 20
        print("Weekly bonus: +20 sparks!")

    # Care check
    if pet.hunger > 70 or pet.thirst > 70 or pet.hygiene < 30:
        pet.health = max(0, pet.health - random.randint(5, 15))

    # Skill resistance
    strength = pet.skills["Strength"]
    charm = pet.skills["Charm"]
    agility = pet.skills["Agility"]
    intelligence = pet.skills["Intelligence"]

    #Decays pet stats after each day by a random amount to keep game interesting
    pet.hunger = min(100, max(0, pet.hunger + max(3, random.randint(5, 10) - strength)))
    pet.thirst = min(100, max(0, pet.thirst + max(3, random.randint(5, 10) - strength)))
    pet.hygiene = min(100, max(0, pet.hygiene - max(5, random.randint(7, 15) - charm)))
    pet.happiness = min(100, max(0, pet.happiness - max(1, random.randint(2, 10) - agility)))
    pet.energy = min(100, max(0, 90 + (intelligence // 3)))
    pet.health = min(100, max(0, pet.health))

    print("End of day", player.day)
    print("Sparks now:", player.sparks, "| Total expenses:", player.expenses)
    input("Hit Enter to continue >")

    player.day += 1


    #Checks to see if the pet is still able to play and if not then displays end of game summary
    saves = load_saves_info()

    if pet.happiness <= 10 or pet.health <= 0:

        if CURRENT_SAVE_SLOT is not None and CURRENT_SAVE_SLOT in saves:
            saves[CURRENT_SAVE_SLOT] = None
            write_saves_info(saves)

        if pet.health <= 0:
            print("\nYour pet got too sick and died!\nPlease try to care for you pet better next time.")
        else:
            print("\nYour pet ran away from a lack of care!\nPlease try to care for you pet better next time.")

        show_end_stats(pet, player)
        return False
    autosave_if_possible(pet, player)
    return True



# ---------------- game loop ----------------

def game_loop(pet, player):
    global CURRENT_SAVE_SLOT
    run = True
    first_day = True
    while run:
        #This ensures that an event isn't triggered as soon as the user starts the game
        if first_day:
            print()
            print("Starting Day", player.day)
            input("Hit Enter to continue >")
            first_day = False

        show_status(pet, player)

        #Displays all the users options each day
        print("1. Feed")
        print("2. Water")
        print("3. Clean")
        print("4. Play")
        print("5. Inventory")
        print("6. Skill Tree")
        print("7. Store")
        print("8. Save")
        print("9. Next Day")
        print("10. Health Check")
        print("0. Quit")

        choice = input("> ").strip()

        if choice == "1":
            feed(pet, player)
        elif choice == "2":
            give_water(pet, player)
        elif choice == "3":
            clean(pet, player)
        elif choice == "4":
            play(pet)
        elif choice == "5":
            inventory(player)
        elif choice == "6":
            skill_tree(pet)
        elif choice == "7":
            store(player)
        elif choice == "8":
            save_load_menu(pet, player)
        elif choice == "9":
            still_alive = end_day(pet, player)
            if not still_alive:
                run = False
            else:
                print()
                print("Starting Day", player.day)
                input("Hit Enter to continue >")
                print()
                random_event(pet, player)
                input("\nContinue> ")
        elif choice == "10":
            health_check(pet, player)
        elif choice == "0":
            print("\nThanks for playing1!")

            # If the user is playing on an unsaved new game then they are asked if they want to save
            if CURRENT_SAVE_SLOT is None:
                print("You haven't saved this game yet.")
                save_anyway = input("Save before quitting? (y/n): ").strip().lower()
                if save_anyway == "y":
                    div()
                    print("SAVE YOUR NEW GAME")
                    div()
                    pet, player = save_load_menu(pet, player)  # Opens save menu
                    print("Game saved! Goodbye!")
                else:
                    print("Goodbye!")
            else:
                # If the user already has a save slot then the game will auto save when they quit
                print(f"Final auto-save to {CURRENT_SAVE_SLOT.upper()}...")
                saves = load_saves_info()
                saves[CURRENT_SAVE_SLOT] = {"pet": pet_to_dict(pet), "player": player_to_dict(player)}
                write_saves_info(saves)
                print("All progress saved. Thanks for playing!")

            break
        else:
            print("?? not a menu option")

# ---------------- entry point ----------------

def main():
    global CURRENT_SAVE_SLOT
    print("WELCOME TO EVOLVING LIFE")
    print("1. New Game")
    print("2. Load Game")
    print("3. How to Play")
    menu_choice = input("> ")

    if menu_choice == "2":
        pet, player = save_load_menu()
        if not pet:
            print("No game loaded.")
            return
    elif menu_choice == "3":
        continue_choice = how_to_play_display()

        #if user chose to continue playing then it will go back to home screen
        if continue_choice == "y":
            print("\n\n\n\n")
            main()
        else:
            print("\nNow that you know how to play. Please try the game sometime.\nThank you for visiting!")
            return
    else:
        while True:
            #if user chooses to start a new game then they will be onboarded
            pet_name = input("Name your pet: ").strip()
            # Bad word check for name
            if any(word in pet_name.lower() for word in BANNED_WORDS):
                print("Error: That name contains inappropriate language.")
                continue

            pet_species = input("Pet species/breed: ").strip()
            # Breed filter check
            if ALLOWED_BREEDS and pet_species.lower() not in ALLOWED_BREEDS:
                print(f"Error: '{pet_species}' is not a recognized breed.")
                if len(ALLOWED_BREEDS) > 0:
                    print(f"Try: {ALLOWED_BREEDS[0].title()}, {ALLOWED_BREEDS[39].title()}...")
                continue

            print(f"You chose '{pet_name}' the '{pet_species}'.")
            ok = input("Is this okay? (y/n) ").strip().lower()
            if ok == "y":
                break
            else:
                print("")
        pet = Pet(pet_name, pet_species)
        player = Player()
        CURRENT_SAVE_SLOT = None

    game_loop(pet, player)

if __name__ == "__main__":
    main()
