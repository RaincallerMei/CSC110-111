"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - id_num: Integer id of this event's location
    - description: Long description of this event's location
    - next_command: String command which leads this event to the next event, None if this is the last game event
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    """

    # NOTES:
    # This is proj1_event_logger (separate from the ex1 file). In this file, you may add new attributes/methods,
    # or modify the names or types of provided attributes/methods, as needed for your game.
    # If you want to create a special type of Event for your game that requires a different
    # set of attributes, you can create new classes using inheritance, as well.

    id_num: int
    description: str
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        -first:the first event in the linked list,or None if the list is empty.
        -last:the last event in the linked list,or None if the list is empty
    Representation Invariants:
        - If 'first' is None, then 'last' must also be None (the list is empty).
        - If 'first' is not None, then 'last' is not None (the list is non-empty).
        - If the list is non-empty:
            - 'first.prev' is None (no event precedes the first).
            - 'last.next' is None (no event follows the last).
            - By following 'next' links starting at 'first', you can reach 'last'.
            - By following 'prev' links starting at 'last', you can reach 'first'.
    """
    first: Optional[Event]
    last: Optional[Event]

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.first = None
        self.last = None

    def display_events(self) -> None:
        """Display all events in chronological order."""
        curr = self.first
        while curr:
            print(f"Location: {curr.id_num}, Command: {curr.next_command}")
            curr = curr.next

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""

        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        # Hint: You should update the previous node's <next_command> as needed
        if self.is_empty():
            # This is the first event in the list
            self.first = event
            self.last = event
            event.prev = None
            event.next = None
            self.first.next_command = command
        else:
            # Link from the current last to this new event

            self.last.next = event
            self.last.next_command = command  # The command that led from the old last event to 'event'
            event.prev = self.last
            event.next = None
            self.last = event

    def remove_last_event(self) -> None:
        """Remove the last event from this event list.
        If the list is empty, do nothing."""

        # Hint: The <next_command> and <next> attributes for the new last event should be updated as needed
        if self.is_empty():
            return
            # If there is only one event in the list
        else:
            if self.first == self.last:
                self.first = None
                self.last = None
            # Move last pointer back
            new_last = self.last.prev
            # Clear out references for the old last
            self.last.prev = None
            # The new last event won't lead anywhere
            if new_last is not None:
                new_last.next = None
                new_last.next_command = None
            self.last = new_last

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""
        ids = []
        curr = self.first
        while curr:
            ids.append(curr.id_num)
            curr = curr.next
        return ids
    # Note: You may add other methods to this class as needed


if __name__ == "__main__":
    # pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
