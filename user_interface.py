"""User Interface module"""

# System imports.
import os


class UserInterface:
    """UserInterface class"""

    MAX_MENU_CHOICES = 5

    # region public methods

    def display_welcome_greeting(self):
        """Display Welcome Greeting."""
        # change_color(Style.CYAN)
        Style.CYAN
        print("Welcome to the beverage program")
        Style.RESET

    def display_menu_and_get_response(self):
        """Display Menu and get response."""

        # Display menu and prompt
        self._display_menu()
        self._display_main_prompt()

        # Get the selection they enter
        selection = self._get_selection()

        # While the response is not valid.
        while not self._verify_selection_valid(selection):
            # Display error message.
            self._display_error_message()
            # Display prompt again.
            self._display_main_prompt()
            # Get selection again.
            selection = self._get_selection()

        # Return the selection casted to an int
        return int(selection)

    def get_search_query(self):
        """Get the search query from the user."""
        print()
        print("What would you like to search for?")
        self._display_prompt()
        return input()

    def get_new_item_information(self):
        """Get new Item information from the user."""
        return (
            self._get_str_field("Id"),
            self._get_str_field("Name"),
            self._get_str_field("Pack"),
            self._get_decimal_field("Price"),
            self._get_bool_field("Active"),
        )

    def display_import_success(self):
        """Display import success."""
        print()
        Style.GREEN
        print("Beverage list has been imported successfully.")
        Style.RESET

    def display_import_error(self):
        """Display import error."""
        print()
        Style.RED
        print("There was an error importing the CSV file.")
        Style.RESET

    def display_already_imported_error(self):
        """Display already imported error"""
        self.display_import_error()
        Style.RED
        print("The CSV file has already been imported.")
        Style.RESET

    def display_file_not_found_error(self):
        """Display file not found error"""
        self.display_import_error()
        Style.RED
        print("File not found for opening.")
        Style.RESET

    def display_empty_file_error(self):
        """Display empty file error"""
        self.display_import_error()
        Style.RED
        print("The file was unexpectedly empty.")
        Style.RESET

    def display_all_items(self, all_items_output):
        """Display all Items."""
        print()
        Style.GREEN
        print("Printing list")
        print()
        Style.YELLOW
        print(self._get_item_header())
        Style.RESET
        print(all_items_output, end="")
        print(self._get_line_separator())

    def display_all_items_error(self):
        """Display all Items error."""
        print()
        Style.RED
        print("There are no items in the list to print.")
        Style.RESET

    def display_item_found(self, item_information):
        """Display Item found success."""
        print()
        Style.GREEN
        print("Item Found!")
        print()
        Style.YELLOW
        print(self._get_item_header())
        Style.RESET
        print(item_information)
        print(self._get_line_separator())

    def display_item_found_error(self):
        """Display Item found error."""
        print()
        Style.RED
        print("Can not find a item with that id.")
        Style.RESET

    def display_add_beverage_success(self):
        """Display Add Item success."""
        print()
        Style.GREEN
        print("The item was successfully added.")
        Style.RESET

    def display_beverage_already_exists_error(self):
        """Display Item already exists error."""
        print()
        Style.RED
        print("Unable to add. An item with that id already exists.")
        Style.RESET

    # endregion

    # region private methods

    def _display_prompt(self):
        """Display the prompt"""
        print("> ", end="")

    def _display_menu(self):
        """Display the Menu"""
        print()
        print("What would you like to do?")
        print()
        print("1. Load Beverage List From CSV")
        print("2. Print Entire List Of Items")
        print("3. Search For An Item")
        print("4. Add New Item To The List")
        print("5. Exit Program")

    def _display_main_prompt(self):
        """Display the Prompt"""
        print()
        print("Enter Your Choice:")
        self._display_prompt()

    def _display_error_message(self):
        """Display error message."""
        print()
        Style.RED
        print("That is not a valid option. Please make a valid choice")
        Style.RESET

    def _get_line_separator(self):
        """Display a line separator"""
        line_str = "-"
        return f"+{line_str*8}+{line_str*58}+{line_str*17}+{line_str*8}+{line_str*8}+"

    def _get_item_header(self):
        """Display the Item header."""
        id_str = "Id"
        name_str = "Name"
        pack_str = "Pack"
        price_str = "Price"
        active_str = "Active"

        header = f"| {id_str:>6} | {name_str:<56} | {pack_str:<15} | {price_str:>6} | {active_str:<6} |"
        lines = self._get_line_separator()
        return f"{lines}{os.linesep}{header}{os.linesep}{lines}"

    def _get_selection(self):
        """Get the selection from the user."""
        return input()

    def _verify_selection_valid(self, selection):
        """Verify that a selection from the main menu is valid."""

        # Declare a return value variable and init to False
        return_value = False

        try:
            # Parse the selection into a choice var
            choice = int(selection)

            # If the choice is between 0 and the MAX_MENU_CHOICES
            if choice > 0 and choice <= self.MAX_MENU_CHOICES:
                # Set the return value to True
                return_value = True
        # If not a valid int, this exception will get raised.
        except ValueError:
            # Ensure return value is False. Should not need this.
            return_value = False

        # Return the return_value
        return return_value

    def _get_str_field(self, field_name):
        """Get a valid string field from the console."""
        print(f"What is the new Item's {field_name}?")
        self._display_prompt()
        valid = False
        while not valid:
            value = input()
            if value:
                valid = True
            else:
                Style.RED
                print("You must provide a value.")
                Style.RESET
                print()
                print(f"What is the new Item's {field_name}?")
                self._display_prompt()
        return str(value)

    def _get_decimal_field(self, field_name):
        """Get a valid Decimal field from the console."""
        print(f"What is the new Item's {field_name}?")
        self._display_prompt()
        valid = False
        while not valid:
            try:
                value = float(input())
                valid = True
            except ValueError:
                Style.RED
                print("That is not a valid Decimal. Please enter a valid Decimal.")
                Style.RESET
                print()
                print(f"What is the new Item's {field_name}?")
                self._display_prompt()
        return str(value)

    def _get_bool_field(self, fieldname):
        """Get a valid Bool field from the console."""
        print(f"Should the Item be {fieldname}? (y/n)")
        self._display_prompt()
        valid = False
        while not valid:
            user_input = input()
            if user_input.lower() == "y" or user_input.lower() == "n":
                valid = True
                value = user_input.lower() == "y"
            else:
                Style.RED
                print("That is not a valid Entry.")
                Style.RESET
                print()
                print(f"Should the Item be {fieldname}? (y/n)")
                self._display_prompt()

        return str(value)

    # endregion


# Decorator to convert Style class to a Singleton
def singleton(cls):
    return cls()


# Class of different Styles
@singleton
class Style:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

    def __getattribute__(self, name):
        """Override default dunder method"""
        value = super().__getattribute__(name)
        print(value, end="")
        return value
