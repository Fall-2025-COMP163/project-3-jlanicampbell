"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Jelani Campbell

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    valid_char_classes = ["Warrior", "Mage", "Rogue", "Cleric"]

    if character_class not in validate_character_data:
        raise InvalidCharacterClassError(f"{character_class} is not an available class.")
        
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5}, 
        "Mage":    {"health": 80,  "strength": 8,  "magic": 20},
        "Rogue":   {"health": 90,  "strength": 12, "magic": 10},
        "Cleric":  {"health": 100, "strength": 10, "magic": 15}
    }

    stats = base_stats[character_class]

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0, # experience amount begins at 0.
        "gold": 100, # every character starts with 100 gold.
        "inventory": [], # inventory is empty by default, can be added to later.
        "active_quests": [], # no active quests by default.
        "completed_quests": [] # no completed quests by default (no active quests).
    }

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    os.makedirs(save_directory, exist_ok=True)

    # Build the save file path using character's name
    filepath = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filepath, "w") as f:
            for key, value in character.items():
                # If the value is a list (like inventory or quests), join it as comma-separated
                if isinstance(value, list):
                    value = ",".join(value)
                # Write the line as key:value
                f.write(f"{key}:{value}\n")
        return True
    except Exception as e:
        # Could log e here if needed
        return False

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    from custom_exceptions import CharacterDeadError, InvalidSaveDataError

    # Build full file path for the save file
    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    # Check if the file exists
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Save file not found for: {character_name}")

    character = {}

    try:
        with open(filepath, "r") as f:
            for line in f:
                # Skip lines that don't contain a colon (invalid line)
                if ":" not in line:
                    continue

                # Split at the first colon into key and value
                key, value = line.strip().split(":", 1)

                # Strip extra whitespace from key and value
                key = key.strip()
                value = value.strip()

                # Convert comma-separated strings back into lists
                if "," in value:
                    value = value.split(",")
                # Convert numeric strings to integers
                elif value.isdigit():
                    value = int(value)

                # Store in character dictionary
                character[key] = value

    except Exception as e:
        # If any issue occurs while reading or parsing the file, raise an error
        raise InvalidSaveDataError(f"Save data format is invalid for {character_name}: {e}")

    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
      
    if not os.path.exists(save_directory):
        return []
    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]


 # I used ChatGPT for the commands above 
 # They act as a filter for files that end with "_save.txt" only, and keeps the ones that do.

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # builds the filepath system to retrieve information

    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character {character_name} was not found.")
    os.remove(filepath)

    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    if character["health"] == 0:
        raise CharacterDeadError("Character is dead, cannot gain experience.")

# while loop keeps leveling up the character until the experience equals the level * 100
    character["experience"] += xp_amount
    while character["experience"] >= character["level"] * 100:
        level_up_xp = character["level"] * 100
        character["experience"] -= level_up_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        
def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    pass

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    pass

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    pass

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

