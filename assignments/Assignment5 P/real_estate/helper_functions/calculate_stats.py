def cheapest(property_dict, state_or_territory: str):
    """
    Function that returns the top 5 cheapest properties for the given State/Territory.

    Args:
        property_dict (dict): Dictionary containing properties organized by states/territories.
        state_or_territory (str): The name of the State or Territory.
        remove duplicates and empty values in prices

    Returns:
        list: The top 5 cheapest properties for the given State/Territory.
    """
    try:
        properties = property_dict['US States'][state_or_territory] + property_dict['Territories'][state_or_territory]
        properties = [prop for prop in properties if prop.price.replace('.', '').isdigit()]
        properties = [prop for prop in properties if float(prop.price) > 0.0]

        # Filter out properties with blank, zero, or empty prices
        properties = [prop for prop in properties if prop.price.strip() != '' and float(prop.price) != 0.0]

        if properties:
            return sorted(properties, key=lambda x: float(x.price))[:5]
        else:
            print(f"No properties found for '{state_or_territory}'.")
    except KeyError:
        print(f"No data found for '{state_or_territory}'")



def priciest(property_dict, state_or_territory):
    """
    Function that returns the Property container for the top 5 priciest properties in the given State/Territory.

     Args:
        property_dict (dict): Dictionary containing properties organized by states/territories.
        state_or_territory (str): The name of the State or Territory.
        removes duplicates and empty values in prices
    """
    try:
        properties = property_dict['US States'][state_or_territory] + property_dict['Territories'][state_or_territory]
        properties = [prop for prop in properties if prop.price.strip() and float(prop.price) > 0.0]
        if properties:
            sorted_properties = sorted(properties, key=lambda x: float(x.price), reverse=True)
            unique_prices = set()
            unique_properties = []
            for prop in sorted_properties:
                if prop.price not in unique_prices:
                    unique_properties.append(prop)
                    unique_prices.add(prop.price)
                if len(unique_properties) == 5:
                    break
            return unique_properties
        else:
            print(f"No properties found for '{state_or_territory}'.")
    except KeyError:
        print(f"No data found for '{state_or_territory}'.")


def dirt_cheap(property_dict, state_or_territory=None):
    """
    Function that returns the Property container of the absolute cheapest property
    in all of the US States and Territories (or in a specific state/territory if specified).

    Args:
        property_dict (dict): Dictionary containing properties organized by states/territories.
        state_or_territory (str, optional): The name of the State or Territory to filter properties.

    Returns:
        Property: The absolute cheapest property.
    """
    try:
        all_properties = []

        # If state_or_territory is provided, filter properties for that specific state/territory
        if state_or_territory:
            properties = property_dict['US States'].get(state_or_territory, []) + property_dict['Territories'].get(state_or_territory, [])
        else:
            # Combine properties from all states and territories
            properties = []
            for state_properties in property_dict['US States'].values():
                properties.extend(state_properties)
            for territory_properties in property_dict['Territories'].values():
                properties.extend(territory_properties)

        # Filter out properties with non-numeric prices and remove properties with blank or 0.0 prices
        all_properties = [prop for prop in properties if prop.price.replace('.', '').isdigit() and float(prop.price) > 0.0]

        if all_properties:
            return min(all_properties, key=lambda x: float(x.price))
        else:
            print("No properties found.")
    except KeyError:
        print("No data found.")


def best_deal(property_dict, state_or_territory: str, num_bedrooms: int, num_bathrooms: int):
    """
    Function that returns the Property container for the property that has the best price per square foot.

    Args:
        property_dict (dict): Dictionary containing properties organized by states/territories.
        state_or_territory (str): The name of the State or Territory.
        num_bedrooms (int): Number of bedrooms.
        num_bathrooms (int): Number of bathrooms.

    Returns:
        Property: The property with the best price per square foot.
    """
    try:
        properties = property_dict.get('US States', {}).get(state_or_territory, []) + \
                     property_dict.get('Territories', {}).get(state_or_territory, [])

        suitable_properties = [prop for prop in properties
                               if prop.bed == str(num_bedrooms) and prop.bath == str(num_bathrooms)]

        suitable_properties = [prop for prop in suitable_properties
                               if float(prop.house_size) > 0 and float(prop.price) > 0]

        if not suitable_properties:
            print(
                f"No properties found for {num_bedrooms} bedrooms and {num_bathrooms} bathrooms in '{state_or_territory}'")
            return None

        # Convert relevant attributes to float
        for prop in suitable_properties:
            prop.price = float(prop.price)
            prop.house_size = float(prop.house_size)

        best_property = min(suitable_properties, key=lambda x: x.price / x.house_size)
        return best_property

    except KeyError:
        print(f"No data found for '{state_or_territory}'")
        return None


def budget_friendly(property_dict, num_bedrooms, num_bathrooms, max_budget):
    """
    Function that returns the Property container for the property that gives you the best bang for
    the buck regardless of the State/Territory.

    Args:
        property_dict (dict): Dictionary containing properties organized by states/territories.
        num_bedrooms (int): Number of bedrooms.
        num_bathrooms (float): Number of bathrooms.
        max_budget (float): Maximum budget.

    Returns:
        Property: The property that gives the best value for the budget.
    """
    try:
        all_properties = []

        # Extract all properties from the dictionary
        for properties in property_dict.values():
            all_properties.extend(properties)

        # Filter out properties with missing or non-numeric prices
        suitable_properties = [
            prop for prop in all_properties
            if hasattr(prop, 'bed') and hasattr(prop, 'bath') and hasattr(prop, 'price')
            and prop.bed == str(num_bedrooms)
            and prop.bath == str(num_bathrooms)
            and isinstance(prop.price, (int, float))
            and float(prop.price) <= max_budget
        ]

        if not suitable_properties:
            print(f"No properties found for {num_bedrooms} bedrooms, {num_bathrooms} bathrooms, and a budget of ${max_budget}.")
            return None

        # Convert relevant attributes to float
        for prop in suitable_properties:
            prop.price = float(prop.price)

        # Find the best property based on price per square footage
        best_property = min(suitable_properties, key=lambda prop: prop.price / float(prop.sqft))
        return best_property

    except KeyError:
        print("KeyError: 'US States' or 'Territories' not found in the property dictionary.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

