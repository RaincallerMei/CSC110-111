"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass, field


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        -id_num: Unique integer ID for this location
        -brief_description: A short text describing this location (shown on subsequent visits)
        -long_description: A longer text describing this location (shown on first visit)
        -available_commands: A dict mapping command strings (e.g., "go east") to either
                            another location ID (int) or some special action (None or str)
        -items: A list of item names that can be found at this location
        -visited: Whether the player has visited this location before
    Representation Invariants:
        - self.id_num is a unique integer >= 1 (within the entire game).
        - self.brief_description and self.long_description are non-empty strings.
        - self.available_commands is a dict mapping (non-empty) string keys
          to either an integer (location ID) or None/special action.
        - self.items is a list of item names (strings); no duplicates within the same list.
        - self.visited is a boolean indicating if the player has visited this location.

    """
    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int | None]
    items: list[str]
    visited: bool = False
    locked: bool = False
    required_items: list[str] = field(default_factory=list)

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, id_num, brief_description, long_description, available_commands, items,
                 visited=False, locked=False, required_items=field(default_factory=list)) -> None:
        """Initialize a new location.

        """
        self.id_num = id_num
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited
        self.locked = locked
        self.required_items = required_items


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        -name: Name of the item (e.g., "toonie")
        -start_position: The location ID where this item initially resides
        -target_position: Possibly a location ID related to an action or scoring
        -target_points: Points gained if item is used or brought to certain location

    Representation Invariants:
        - self.name is a non-empty string (unique item identifier in the game).
        - self.start_position is a valid Location ID in the game (or 0/-1 if unplaced).
        - self.target_position is a valid Location ID if used in scoring or puzzle logic.
        - self.target_points >= 0 (non-negative; if scoring is used in your game).

    """
    name: str
    start_position: int
    target_points: int
    weight: float = 0.0
    description: str = ''

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
