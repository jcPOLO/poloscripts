import os
import sys
from helpers import is_int
import logging


class Menu(object):
    platforms = ['ios']

    def __init__(self) -> None:
        self.choices = {
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

        1. 
        2. 
        3. 

        -------------------------------------------------------------------------------

        a. Apply      z. Clear selections     w. Save config.
        
        e. Exit

        """)

    def display_final_choices(self) -> None:
        logging.info(f'Options selected: {self.final_choices}\n')

    # TODO: Review this method that probable should return None instead
    def run(self, printable='') -> callable:

        self.display_menu()
        logging.info(printable)

        if self.final_choices:
            self.display_final_choices()
        while True:
            choice = input("Enter an option: ")
            template = self.choices.get(choice)

            if is_int(choice):
                choice = int(choice)
            if is_int(choice) and choice < len(Menu.template_files):
                if template not in self.final_choices:
                    self.final_choices.append(template)
                self.display_menu()
                self.display_final_choices()
            elif choice in self.choices.keys():
                return template()
            else:
                logging.error("{0} is not a valid choice".format(choice))

    # TODO: all
    def apply(self) -> str:
        if self.final_choices:
            try:
                logging.info(f"applied: -> {self.final_choices} <-")
                return ''
            except exit():
                raise logging.error('---------------- Error ----------------')
        else:
            logging.error("{0} choices selected are not valid".format(self.final_choices))

    def clear(self) -> None:
        self.final_choices = []
        self.run()
        logging.info(f'Selected templates cleared.\n')

    def save(self) -> None:
        self.final_choices = []
        result = input('Are you sure you want to execute a write config? [y]')
        if result.lower().strip() not in "yes":
            self.display_menu()
        else:
            logging.info(f'Applying write config...\n')
            return result

    def exit(self) -> None:
        self.final_choices = []
        logging.info(f'Bye!\n')
        sys.exit()

