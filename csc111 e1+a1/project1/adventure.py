"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - _locations: a mapping from location id to Location object.
            This represents all the locations in the game.
        - _items: a list of Item objects, representing all items in the game.
        - current_location_id: the id of the player's current location
        - ongoing: whether the game is still ongoing
        - self.inventory is a list of item names; no duplicates if your logic forbids them

    Representation Invariants:
        - All location IDs are valid and unique.
    """
    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    inventory: list[str]
    score: int
    moves: int
    max_move: int
    max_weight: int
    _item_dict: dict[str, str]

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items, config = self._load_game_data(game_data_file)
        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.inventory = []
        self.score = 0
        self.moves = 0
        self.max_move = 30
        self.max_weight = config.get("max_weight", 1.5)
        self._item_dict = {item.name: item for item in self._items}
        self._sync_items_with_locations()

    def pick_up_item(self, item_nam: str) -> None:
        """Attempt to pick up an item from current location"""
        current_loc1 = self.get_location()
        if item_nam not in current_loc1.items:
            print(f"\nThere's no {item_nam} here to pick up.")
            return

        item = self._item_dict.get(item_nam)
        if not item:
            print(f"\nError: Item {item_nam} not found.")
            return

        current_wei = sum(self._item_dict[name].weight for name in self.inventory)
        new_weight = current_wei + item.weight

        if new_weight > self.max_weight:
            print(f"\nCannot pick up {item_nam}. Max weight {self.max_weight} exceeded!")
            return

        current_wei = new_weight
        current_loc1.items.remove(item_nam)
        self.inventory.append(item_nam)
        print(f"\n*** Picked up: {item_nam} ***")

    def drop_of_item(self, item_na: str) -> None:
        """drop the item selected """
        cur_loc = self.get_location()
        if item_na in self.inventory:
            self.inventory.remove(item_na)
            cur_loc.items.append(item_na)
            print(f"\n*** Dropped off: {item_na} ***")
        else:
            print(f"\nThere's no {item_na} here to drop off.")

    def check_win_condition(self) -> bool:
        """Check if player has collected all required items and returned to dorm"""
        required_items = {"usb drive", "laptop charger", "lucky mug"}
        return (
                self.current_location_id == 9 and all(item in self.inventory for item in required_items)
        )

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file
            config = data.get("config", {})
            # Build Location objects
            locations = {}
            for loc_data in data["locations"]:
                loc_items = loc_data.get("items", [])
                locked = loc_data.get("locked", False)
                required_items = loc_data.get("required_items", [])
                loc = Location(
                    id_num=loc_data["id"],
                    brief_description=loc_data["brief_description"],
                    long_description=loc_data["long_description"],
                    available_commands=loc_data["available_commands"],
                    items=loc_items,
                    visited=False,
                    locked=locked,
                    required_items=required_items
                )
                locations[loc_data["id"]] = loc
        items = []
        if "items" in data:
            for item_data in data["items"]:
                new_item = Item(
                    name=item_data["name"],
                    start_position=item_data["start_position"],
                    target_points=item_data["target_points"],
                    weight=item_data.get("weight", 1.0),
                    description=item_data.get("description", "")
                )
                items.append(new_item)

        # YOUR CODE BELOW

        return locations, items, config

    def _sync_items_with_locations(self) -> None:
        """
        Ensure each Item is also listed in the correct location's items list,
        based on the 'start_position'.
        """
        for it in self._items:
            if it.start_position in self._locations:
                if it.name not in self._locations[it.start_position].items:
                    self._locations[it.start_position].items.append(it.name)

    def get_current_weight(self) -> float:
        """return the current weight the student carries"""
        return sum(self._item_dict[item].weight for item in self.inventory)

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is not None:
            return self._locations[loc_id]
        else:
            return self._locations[self.current_location_id]


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "drop item", "score", "undo", "log", "quit"]
    # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:

        if game.check_win_condition():
            print("\n*** VICTORY! You've returned to your dorm with all required items! ***")
            print("Final inventory:", ", ".join(game.inventory))
            print("Final Steps:", game.moves - 1)
            game.ongoing = False
            continue

        # Show  left
        print(f"\nMoves left: {game.max_move - game.moves}")
        game.moves += 1

        # shows  weights left
        current_weight = game.get_current_weight()
        print(f"Current weight: {current_weight:.1f}/{game.max_weight} kg")

        # Get the current location object
        location = game.get_location()

        # Create a new Event for this location and add it to the log
        current_event = Event(id_num=location.id_num, description=location.long_description)
        game_log.add_event(current_event, choice)

        # Print location description (long on first visit, brief on subsequent visits)
        if not location.visited:
            print(location.long_description)
            location.visited = True
        else:
            print(location.brief_description)

        # If there are items at this location, list them
        if location.items:
            print("\nYou see items here:")
            for item_name in location.items:
                print(f" - {item_name} (use 'pick up {item_name}' to take it)")

        # Show possible actions
        print("\nAvailable actions:")
        print("Global commands:", ", ".join(menu))
        print("Location-specific commands:")
        for cmd in location.available_commands:
            print(f" - {cmd}")

        # Get player input
        choice = input("\nWhat do you do? ").strip().lower()

        # 1) Check if it's a special command (like 'pick up X')
        if choice.lower().startswith("pick up "):
            item_name = choice[8:].strip()
            game.pick_up_item(item_name)
            # After picking up, check if we won
            if game.check_win_condition():
                print("\n*** VICTORY! You've returned to your dorm with all required items! ***")
                print("Final inventory:", ", ".join(game.inventory))
                print("Final Steps:", game.moves)
                game.ongoing = False
            continue
        elif choice.lower().startswith("drop item"):
            undo_ite = choice[10:]
            game.drop_of_item(undo_ite)
        # 2) Check if it's one of the global commands in 'menu'
        elif choice in menu:
            if choice == "look":
                # Reprint long description
                print("\n" + location.long_description)

            elif choice == "inventory":
                if game.inventory:
                    current_weight = game.get_current_weight()
                    print(f"\nInventory ({current_weight:.1f}/{game.max_weight} kg):", ", ".join(game.inventory))
                else:
                    print("\nYour inventory is empty.")

            elif choice == "score":
                # Example: sum up target_points of items in inventory
                total_score = sum(it.target_points for it in game._items if it.name in game.inventory)
                print(f"\nCurrent score: {total_score}")

            elif choice == "undo":
                if game_log.is_empty():
                    print("\nNo actions to undo.")
                    continue
                # Get the command that led to the current last event
                current_last = game_log.last
                # The command is stored in the previous event's next_command
                undo_com = current_last.prev.next_command if current_last.prev else None
                undo_ite = ""
                if undo_com.lower().startswith("pick up"):
                    undo_ite = undo_com[len("pick up "):].strip()
                    game.drop_of_item(undo_ite)
                elif undo_com.lower().startswith("drop item"):
                    undo_ite = undo_com[len("drop item "):].strip()
                    current_loc = game.get_location()
                    if undo_ite in current_loc.items:
                        current_loc.items.remove(undo_ite)
                        game.inventory.append(undo_ite)
                        print(f"\nUndo: Picked up {undo_ite} again.")
                # Remove the last event from the log
                game_log.remove_last_event()
                # If log is not empty after removal, revert to that event's location
                if not game_log.is_empty():
                    game.current_location_id = game_log.last.id_num

            elif choice == "log":
                # Print the entire event log
                game_log.display_events()

            elif choice == "quit":
                print("\nThanks for playing!")
                game.ongoing = False

        # 3) Check if it's a location-specific command (movement, etc.)
        elif choice in location.available_commands:
            new_loc_id = location.available_commands[choice]
            new_location = game.get_location(new_loc_id)

            if new_location.locked:
                required = new_location.required_items
                if all(item in game.inventory for item in required):
                    new_location.locked = False
                    game.current_location_id = new_loc_id
                    print(f"\nUsed {', '.join(required)} to unlock {new_location.brief_description}!")
                else:
                    print(f"\n{new_location.brief_description} is locked. Required items: {', '.join(required)}")
            else:
                game.current_location_id = new_loc_id
                # Check for win condition after moving
                if game.check_win_condition():
                    print("\n*** VICTORY! You've returned to your dorm with all required items! ***")
                    print("Final inventory:", ", ".join(game.inventory))
                    print("Final Steps:", game.moves)
                    game.ongoing = False
                elif game.moves >= game.max_move:
                    print("\nGame Over! It is 4pm now, and your project is due :((")
                    game.ongoing = False

        else:
            print("\nInvalid command. Type 'look' to see available options.")

        # Finally, if we are out of moves, game over
        if game.moves >= game.max_move and game.ongoing:
            print("\nGame Over! You're out of moves!")
            game.ongoing = False
