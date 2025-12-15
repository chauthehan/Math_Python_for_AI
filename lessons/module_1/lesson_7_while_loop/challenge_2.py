# Challenge 2: Adventure Game Chatbot [OPTIONAL]
# This is a complex challenge - take your time!

print("Bot: Welcome to the Adventure Game!")
print("Bot: What's your name, adventurer?")
player_name = input("You: ").strip().title()

print(f"\nBot: Hello {player_name}! Your adventure begins...")

# Initialize game variables
score = 0
current_room = "entrance"
inventory = []

# Track which items have been collected (so they don't appear again)
items_collected = []

# Main game loop
while True:
    # Display current status
    print(f"\nBot: Score: {score} | Items: {inventory}")
    print()
    
    # ENTRANCE HALL
    if current_room == "entrance":
        print("=== ENTRANCE HALL ===")
        print("Bot: You are in a grand entrance hall.")
        
        if "KEY" not in items_collected:
            print("Bot: You see a shiny KEY on the floor.")
        
        print("Bot: Doors lead to: library, garden")
        
        command = input("Bot: What do you want to do? (go [room] / take [item] / inventory / quit)\nYou: ").lower().strip()
        
        if command == "quit":
            break
        elif command == "inventory":
            print(f"Bot: You are carrying: {inventory}")
        elif command.startswith("go"):
            if "library" in command:
                current_room = "library"
            elif "garden" in command:
                current_room = "garden"
            else:
                print("Bot: You can't go there from here!")
        elif command.startswith("take"):
            if "key" in command and "KEY" not in items_collected:
                inventory.append("KEY")
                items_collected.append("KEY")
                score = score + 10
                print("Bot: You picked up the KEY! (+10 points)")
            else:
                print("Bot: There's nothing here to take!")
        else:
            print("Bot: I don't understand that command.")
    
    # LIBRARY
    elif current_room == "library":
        print("=== LIBRARY ===")
        print("Bot: You are in a dusty library filled with ancient books.")
        
        if "BOOK" not in items_collected:
            print("Bot: You see a magical BOOK on the shelf.")
        
        if "KEY" in inventory:
            print("Bot: Doors lead to: entrance, secret (you have the KEY!)")
        else:
            print("Bot: Doors lead to: entrance, secret (requires KEY)")
        
        command = input("Bot: What do you want to do? (go [room] / take [item] / inventory / quit)\nYou: ").lower().strip()
        
        if command == "quit":
            break
        elif command == "inventory":
            print(f"Bot: You are carrying: {inventory}")
        elif command.startswith("go"):
            if "entrance" in command:
                current_room = "entrance"
            elif "secret" in command:
                if "KEY" in inventory:
                    print("Bot: You use your KEY to unlock the secret room!")
                    current_room = "secret"
                else:
                    print("Bot: The secret room is locked! You need a KEY.")
            else:
                print("Bot: You can't go there from here!")
        elif command.startswith("take"):
            if "book" in command and "BOOK" not in items_collected:
                inventory.append("BOOK")
                items_collected.append("BOOK")
                score = score + 15
                print("Bot: You picked up the BOOK! (+15 points)")
            else:
                print("Bot: There's nothing here to take!")
        else:
            print("Bot: I don't understand that command.")
    
    # GARDEN
    elif current_room == "garden":
        print("=== GARDEN ===")
        print("Bot: You are in a beautiful garden with colorful flowers.")
        
        if "FLOWER" not in items_collected:
            print("Bot: You see a rare FLOWER blooming.")
        
        print("Bot: Doors lead to: entrance")
        
        command = input("Bot: What do you want to do? (go [room] / take [item] / inventory / quit)\nYou: ").lower().strip()
        
        if command == "quit":
            break
        elif command == "inventory":
            print(f"Bot: You are carrying: {inventory}")
        elif command.startswith("go"):
            if "entrance" in command:
                current_room = "entrance"
            else:
                print("Bot: You can't go there from here!")
        elif command.startswith("take"):
            if "flower" in command and "FLOWER" not in items_collected:
                inventory.append("FLOWER")
                items_collected.append("FLOWER")
                score = score + 5
                print("Bot: You picked up the FLOWER! (+5 points)")
            else:
                print("Bot: There's nothing here to take!")
        else:
            print("Bot: I don't understand that command.")
    
    # SECRET ROOM
    elif current_room == "secret":
        print("=== SECRET ROOM ===")
        print("Bot: You found the SECRET ROOM! A TREASURE chest glows before you!")
        
        if "TREASURE" not in items_collected:
            print("Bot: You see a precious TREASURE in the chest.")
        
        print("Bot: Doors lead to: library")
        
        command = input("Bot: What do you want to do? (go [room] / take [item] / inventory / quit)\nYou: ").lower().strip()
        
        if command == "quit":
            break
        elif command == "inventory":
            print(f"Bot: You are carrying: {inventory}")
        elif command.startswith("go"):
            if "library" in command:
                current_room = "library"
            else:
                print("Bot: You can't go there from here!")
        elif command.startswith("take"):
            if "treasure" in command and "TREASURE" not in items_collected:
                inventory.append("TREASURE")
                items_collected.append("TREASURE")
                score = score + 50
                print("Bot: You picked up the TREASURE! (+50 points)")
            else:
                print("Bot: There's nothing here to take!")
        else:
            print("Bot: I don't understand that command.")

# Game over
print(f"\nBot: Thanks for playing, {player_name}!")
print(f"Bot: Final Score: {score}")
print(f"Bot: Items Collected: {inventory}")

if len(inventory) == 4:
    print("Bot: You found all 4 items! Perfect score!")
elif len(inventory) >= 2:
    print("Bot: Great job exploring!")
else:
    print("Bot: Come back and explore more next time!")
