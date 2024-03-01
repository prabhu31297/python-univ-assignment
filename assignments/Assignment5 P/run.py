from real_estate.helper_functions.calculate_stats import priciest, cheapest, best_deal, dirt_cheap, budget_friendly
from real_estate.load_data.load import RealEstate
import pandas as pd

def main():
    file_location = 'real_estate/load_data/data'
    # file_estate = pd.read_csv('real_estate/load_data/data/realtor-data.csv')
    real_estate = RealEstate('realtor-data.csv', file_location)
    print("Data loaded")
    print("Computing stats:")
    print("First 5 Property containers for every State and Territory:")
    for state_or_territory, properties in real_estate.properties_dict['US States'].items():
        print(f"\n'{state_or_territory}': {properties[:10]}")
    for territory, properties in real_estate.properties_dict['Territories'].items():
        print(f"\n'{territory}': {properties[:10]}")

    print("\ncheapest:")
    cheapest_properties = cheapest(real_estate.properties_dict, 'New York')
    for prop in cheapest_properties:
        print(prop)

    print("\npriciest:")
    priciest_properties = priciest(real_estate.properties_dict, 'New York')
    for prop in priciest_properties:
        print(prop)

    print("\ndirt_cheap :")
    dirt_cheap_territory_property = dirt_cheap(real_estate.properties_dict, 'New York')
    print(dirt_cheap_territory_property)

    print("\nbest_deal:")
    best_deal_property = best_deal(real_estate.properties_dict, 'Virgin Islands', 3, 3)
    print(best_deal_property)

    print("\nbudget_friendly:")
    budget_friendly_property = budget_friendly(real_estate.properties_dict, 3, 3, 2500000)
    print(budget_friendly_property)

if __name__ == "__main__":
    main()
