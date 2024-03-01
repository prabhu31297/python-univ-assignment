from collections import defaultdict, namedtuple
import os
import re
from real_estate.helper_functions import calculate_stats
from real_estate.helper_functions.context_manager import CustomContextManager

class RealEstate:
    def __init__(self, file_name: str, location: str):
        self.properties_dict = defaultdict(lambda: defaultdict(list))
        self.load_data(file_name, location)

    def load_data(self, file_name, location):
        try:
            with CustomContextManager(location):
                with open(file_name, 'r') as file:
                    # Read the first line of the file
                    first_line = next(file).strip()
                    # Create Property namedtuple
                    column_names = first_line.split(',')  # Assuming tab-separated values
                    Property = self._create_container(first_line)

                    # Process remaining lines
                    for line in file:
                        property_data = line.strip().split(',')  # Assuming tab-separated values
                        if len(property_data) == len(column_names):
                            property_obj = Property(*property_data)
                            state_or_territory = property_obj.state
                            if state_or_territory in self.properties_dict['US States']:
                                self.properties_dict['US States'][state_or_territory].append(property_obj)
                            else:
                                self.properties_dict['Territories'][state_or_territory].append(property_obj)
        except FileNotFoundError:
            print("File not found.")
            while True:
                file_name = input("Please enter a valid file name or 'q' to quit: ")
                if file_name.lower() == 'q':
                    exit()
                if os.path.isfile(file_name):
                    break

    def _create_container(self, first_line):
        field_names = first_line.split(',')
        # Remove any non-alphanumeric characters from field names and convert to valid identifiers
        field_names = [re.sub(r'\W+', '_', name) for name in field_names]
        # Create and return the namedtuple
        Property = namedtuple('Property', field_names)
        return Property

    def compute_stats(self, func_name, *args, **kwargs):
        # Call the function directly instead of using globals()
        if func_name in ['priciest', 'cheapest','best_deal','dirt_cheap','budget_friendly']:
            return getattr(calculate_stats, func_name)
        else:
            return getattr(calculate_stats, func_name)(*args, **kwargs)


