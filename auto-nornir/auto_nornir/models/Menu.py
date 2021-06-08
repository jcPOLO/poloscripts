import os
import sys
from auto_nornir.helpers import is_int
import logging
from auto_nornir.helpers import configure_logging
from typing import List

logger = logging.getLogger(__name__)


class Menu(object):

    configure_logging(logger)

    def __init__(self) -> None:
        # TODO: Charge the options from device methods available
        self.choices = {
            "1": "get_config",
            "2": "get_facts",
        }
        # TODO: Create a class with buttons
        self.buttons = {
            "a": self.apply,
            "z": self.clear,
            "w": self.save,
            "e": self.exit,
        }
        self.final_choices = []

    @staticmethod
    def display_menu() -> None:
        os.system('clear')
        print("""
        Select the number one by one. When finished, press 'a' to run:

        1. Get facts 
        2. Get config
        3. 

        -------------------------------------------------------------------------------

        a. Apply      z. Clear selections     w. Save config.
        
        e. Exit

        """)

    def display_final_choices(self) -> None:
        logger.info(f'Options selected: {self.final_choices}\n')

    def run(self, msg='') -> callable:

        self.display_menu()
        logger.info(msg)

        if self.final_choices:
            self.display_final_choices()
        while True:
            choice = input("Enter an option: ")
            selection = self.validate_selection(choice)
            if isinstance(selection, int):
                selection = self.choices.get(str(selection))
                if selection not in self.final_choices:
                    self.final_choices.append(selection)
                    self.display_menu()
                    self.display_final_choices()
            elif choice in self.choices.keys():
                return self.choices.get(selection)()
            else:
                logger.error("{0} is not a valid choice".format(choice))

    # TODO: all
    def apply(self) -> List:
        if self.final_choices:
            try:
                logger.info(f"applied: -> {self.final_choices} <-")
                return self.final_choices
            except exit():
                raise logger.error('---------------- Error ----------------')
        else:
            logger.error("{0} choices selected are not valid".format(self.final_choices))

    def clear(self) -> None:
        self.final_choices = []
        self.run()
        logger.info(f'Selected tasks cleared.\n')

    def save(self) -> None:
        self.final_choices = []
        result = input('Are you sure you want to execute a write config? [y]')
        if result.lower().strip() not in ["yes", "y", "1", "ok", ""]:
            self.display_menu()
        else:
            logger.info(f'Applying write config...\n')

    def exit(self) -> None:
        self.final_choices = []
        logger.info(f'Bye!\n')
        sys.exit()

    def validate_selection(self, choice) -> int or str:
        if is_int(choice):
            if int(choice) < (len(self.choices) - 3):
                return int(choice)
        else:
            return choice

