"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        # Add first event (initial location, no previous command)
        initial_location = self._game.get_location()
        initial_event = Event(initial_location.id_num, initial_location.long_description)
        self._events.add_event(initial_event)

        # Generate the remaining events based on the commands and initial location
        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation, respecting locked rooms and required items."""
        for command in commands:
            # Simulate the command execution
            if command.startswith("pick up "):
                item_name = command[len("pick up "):]
                self._game.pick_up_item(item_name)
            elif command.startswith("drop item "):
                item_name = command[len("drop item "):]
                self._game.drop_of_item(item_name)
            elif command == "inventory":
                pass  # No state change
            elif command == "score":
                pass  # No state change
            else:
                # Movement command
                if command in current_location.available_commands:
                    new_loc_id = current_location.available_commands[command]
                    new_location = self._game.get_location(new_loc_id)

                    # Check if the new location is locked
                    if new_location.locked:
                        required_items = new_location.required_items
                        if all(item in self._game.inventory for item in required_items):
                            # Unlock the location and move
                            new_location.locked = False
                            self._game.current_location_id = new_loc_id
                            current_location = new_location
                            print(f"\nUsed {', '.join(required_items)} to unlock {new_location.brief_description}!")
                        else:
                            # Location is locked, and player doesn't have the required items
                            print(
                                f"\n{new_location.brief_description} is locked. Required items: {', '.join(required_items)}")
                            continue  # Skip this command
                    else:
                        # Location is not locked, move normally
                        self._game.current_location_id = new_loc_id
                        current_location = new_location

                    self._game.moves += 1
                else:
                    print(f"\nInvalid command: {command} at location {current_location.id_num}")
                    continue

            # Log the event
            next_event = Event(current_location.id_num, current_location.long_description, command)
            self._events.add_event(next_event, command)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('project1/game_data.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('game_data.json', 1, ["go east", "go north", "go east"])
        >>> sim.get_id_log()
        [1, 2, 6, 7]
        """
        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""
        current_event = self._events.first
        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)
            current_event = current_event.next


if __name__ == "__main__":
    # Valid winning path test
    win_commands = [
        "go north",
        "pick up usb drive",
        "pick up library card",
        "go south",
        "go east",
        "go down",
        "pick up professor note",
        "go up",
        "go west",
        "go north",
        "go north",
        "pick up laptop charger",
        "go east",
        "pick up lucky mug",
        "go north"
    ]

    win_expected_log = [1, 2, 2, 2, 1, 3, 6, 6, 3, 1, 2, 5, 5, 8, 8, 9]

    win_sim = AdventureGameSimulation('game_data.json', 1, win_commands)
    assert win_sim.get_id_log() == win_expected_log, f"Expected {win_expected_log} got {win_sim.get_id_log()}"

    # Valid losing condition test (exceed max moves)
    lose_commands = ["go north", "go south"] * 16  # 30 commands
    lose_sim = AdventureGameSimulation('game_data.json', 1, lose_commands)
    assert lose_sim._game.moves >= lose_sim._game.max_move, f"Expected ≥{lose_sim._game.max_move} moves, got {lose_sim._game.moves}"

    # Inventory demo
    inventory_demo = [
        "go north",
        "pick up usb drive",
        "inventory",
        "drop item usb drive",
        "inventory",
        "go south",
        "pick up handouts",
        "inventory"
    ]
    print("\nInventory Test:")
    AdventureGameSimulation('game_data.json', 1, inventory_demo).run()

    # Score test
    print("Score Test:")
    score_demo = [
        "go north",  # 2
        "pick up usb drive",  # +10 points
        "score",  # Check score
        "go south",  # 1
        "go east",  # 3
        "pick up professor note",  # +15 points
        "score"  # Total 25
    ]
    AdventureGameSimulation('game_data.json', 1, score_demo).run()
    print("\nScore test completed!\n")

    # Enhancement 1: Weight limit test
    print("Weight Limit Test:")
    enhancement1_demo = [
        "go north",  # 2
        "pick up usb drive",  # 0.2kg
        "pick up library card",  # 0.1kg (total 0.3)
        "go south",  # 1
        "go east",  # 3
        "pick up professor note",  # 0.1kg (total 0.4)
        "pick up philosophy textbook"  # 0.2kg (total 0.6) - under 2kg
    ]
    AdventureGameSimulation('game_data.json', 1, enhancement1_demo).run()
    print("\nWeight limit test completed!\n")

    # Enhancement 2: Locked room test
    print("Locked Room Test:")
    enhancement2_demo = [
        "go north",  # Move to location 2 (Robarts Library Entrance)
        "go north",  # Move to location 5 (Robarts 3rd Floor)
        "go east",  # Attempt to move to location 8 (Robarts Rare Books) - locked
        "go south",  # Move back to location 2 (Robarts Library Entrance)
        "go south",  # Move back to location 1 (Bahen Center Lobby)
        "go east",  # Move to location 3 (Sidney Smith Hall)
        "pick up professor note",  # Pick up the professor note in location 3
        "go west",  # Move back to location 1 (Bahen Center Lobby)
        "go north",  # Move to location 2 (Robarts Library Entrance)
        "pick up library card",  # Pick up the library card in location 2
        "go north",  # Move to location 5 (Robarts 3rd Floor)
        "go east"  # Successfully unlock and move to location 8 (Robarts Rare Books)
    ]
    AdventureGameSimulation('game_data.json', 1, enhancement2_demo).run()
    print("\nLocked room test completed!")