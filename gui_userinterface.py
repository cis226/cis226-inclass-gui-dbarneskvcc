"""Simple Beverage Management GUI"""

# Third Part Imports
import PySimpleGUI as sg

# First Party Imports
from errors import AlreadyImportedError


class EmployeeListWindow:
    """Simple Beverate List"""

    def __init__(self, beverage_collection, csv_processor, path_to_csv):
        """Constructor"""
        self.beverage_collection = beverage_collection
        self.csv_processor = csv_processor
        self.path_to_csv = path_to_csv

        # Each widget should have a key that uniquely identifies it on the page.
        # This key is used to interact with the widget in code.
        layout = [
            # Text just writes text to the screen
            [sg.Text("Beverage List")],
            # Listbox is great for showing a list of things and allowing
            # selection of a thing from the list. We just use for output.
            [sg.Listbox(["No Beverages"], key="-output-", size=(150, 36))],
            [
                # Renders a Button
                sg.Button("Load CSV", key="-load_csv-"),
                sg.Button("Add New Beverage", key="-open_add_new-"),
                # Renders an Input box. Collects text from user.
                sg.Input("", key="-search_id-"),
                sg.Button("Search", key="-search_button"),
            ],
            [sg.Button("Exit")],
        ]
        self.window = sg.Window("Beverage List", layout)

    def run(self):
        """Start the window"""
        self._run_loop()
        self.window.close()

    def _run_loop(self):
        """Run the Event loop"""
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            # If event is load csv, load the CSV file
            elif event == "-load_csv-":
                self._on_load_csv(event, values)
            # If we want to add a new beverage
            elif event == "-open_add_new-":
                self._on_open_add_new(event, values)

    def _on_load_csv(self, event, values):
        """Handle when Load CSV button is clicked"""
        try:
            self.csv_processor.import_csv(
                self.beverage_collection,
                self.path_to_csv,
            )
            self._update_output(event, values)
            sg.popup_ok("Beverage list has been imported succesfully.")
        except AlreadyImportedError:
            sg.popup_error("The CSV file has already been imported.")
        except FileNotFoundError:
            sg.popup_error("File not found for opening.")
        except EOFError:
            sg.popup_error("The file was unexpectedly empty.")

    def _on_open_add_new(self, event, values):
        """Handle when Open Add New button is clicked"""
        add_window = BeverageAddWindow(self.beverage_collection)
        add_window.run()
        self._update_output(event, values)

    def _update_output(self, event, values):
        """Update the contents of the output Listbox"""
        self.window["-output-"].update(self.beverage_collection.beverages)


class BeverageAddWindow:
    """Simple Beverage Add"""

    def __init__(self, beverage_collection):
        """Constructor"""
        self.beverage_collection = beverage_collection

        layout = [
            [sg.Text("Id"), sg.Input(key="-id-")],
            [sg.Text("Name"), sg.Input(key="-name-")],
            [sg.Text("Pack"), sg.Input(key="-pack-")],
            [sg.Text("Price"), sg.Input(key="-price-")],
            [
                sg.Radio(
                    "Active",
                    "beverage_active_group",
                    key="-beverage_active-",
                    default=True,
                ),
            ],
            [
                sg.Radio(
                    "Inactive",
                    "beverage_active_group",
                    key="-beverage_inactive-",
                ),
            ],
            [
                sg.Button("Add", key="-add_new-"),
                sg.Button("Cancel", key="-cancel-"),
            ],
        ]
        self.window = sg.Window("Beverage Add", layout)

    def run(self):
        """Start the window"""
        self._run_loop()
        self.window.close()

    def _run_loop(self):
        """Run the Event loop"""
        while True:
            event, values = self.window.read()
            # If close window or Cancal clicked, close window.
            if event == sg.WINDOW_CLOSED or event == "-cancel-":
                break
            elif event == "-add_new-":
                success = self._on_add_new(event, values)
                if success:
                    break

    def _on_add_new(self, event, values):
        """Handle when Add button is clicked"""
        try:
            self.beverage_collection.add(
                values["-id-"],
                values["-name-"],
                values["-pack-"],
                float(values["-price-"]),
                values["-beverage_active-"] is True,
            )
            return True
        except ValueError:
            sg.popup_error("That is not a valid Decimal.")
            return False
