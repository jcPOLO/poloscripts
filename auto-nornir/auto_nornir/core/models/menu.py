import os
import sys
from auto_nornir.core.helpers import configure_logging, is_int
from auto_nornir.core.models.platform import PlatformBase
from auto_nornir.core.models.template import Template
import logging
from typing import List

logger = logging.getLogger(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = dir_path+'/../templates/ios/'


class Menu(object):

    configure_logging(logger)
    method_list = [method for method in dir(PlatformBase) if method.startswith('__') is False]
    templates = os.listdir(TEMPLATES_DIR)

    def __init__(self) -> None:

        # TODO: Redo this madness (but working)
        self.getters = {
            i: self.method_list[i] for i in range(0, len(self.method_list))
        }
        self.templates = {
            i+len(self.method_list): self.templates[i] for i in range(0, len(self.templates))
        }
        self.choices = self.getters.copy()
        self.choices.update(self.templates)

        # TODO: Create a class with buttons
        self.buttons = {
            "a": self.apply,
            "z": self.clear,
            "w": self.save,
            "e": self.exit,
        }
        self.final_choices = []

    def display_menu(self) -> None:
        os.system('clear')
        print("""
        Select the number one by one. When finished, press 'a' to run:
        """)
        for k, v in self.getters.items():
            print("        {}. {}".format(k, v))
        print("""
        ---------------------------------- DANGER -------------------------------------
        """)
        for k, v in self.templates.items():
            print("        {}. {}".format(k, v))
        print("""
        -------------------------------------------------------------------------------

        a. Apply      z. Clear selections     w. Save config.
        
        e. Exit

        """)
        print(dir_path)

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
                selection = self.choices.get(selection)
                if selection not in self.final_choices:
                    self.final_choices.append(selection)
                    self.display_menu()
                    self.display_final_choices()
            elif choice in self.buttons.keys():
                return self.buttons.get(selection)()
            else:
                logger.error("{0} is not a valid choice".format(choice))

    # TODO: all
    def apply(self) -> List:
        if self.final_choices:
            if any('.j2' in s for s in self.final_choices):
                all_templates = [s for s in self.final_choices if ".j2" in s]
                logger.info("creating jinja2 final template")
                t = Template(all_templates)
                t.create_final_template()
            logger.info(f"applied: -> {self.final_choices} <-")
            return self.final_choices
        else:
            logger.error("{0} choices selected are not valid".format(self.final_choices))

    def clear(self) -> None:
        self.final_choices = []
        self.run()
        logger.info(f'Selected tasks cleared.\n')

    def save(self) -> List:
        self.final_choices = []
        result = input('Are you sure you want to execute a write config? [y]')
        if result.lower().strip() not in ["yes", "y", "1", "ok", ""]:
            self.display_menu()
        else:
            logger.info(f'Applying write config...\n')
            self.final_choices = ['save_config']
            return self.final_choices

    def exit(self) -> None:
        self.final_choices = []
        logger.info(f'Bye!\n')
        sys.exit()

    def validate_selection(self, choice) -> int or str:
        if is_int(choice):
            if int(choice) < (len(self.choices) + 1):
                return int(choice)
        else:
            return choice

