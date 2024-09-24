from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Subcategory:
    name: str
    description: str
    example: str


@dataclass
class Category:
    name: str
    description: str
    example: str
    subcategories: List[Subcategory] = field(default_factory=list)


categories = [
    Category(
        name="Consumables",
        description="Daily expenses, including grocery stores, supermarkets, wholesale clubs, restaurants, "
                    "delivery services etc. The merchant name sometimes contains locations to indicate its cuisine",
        example="Restaurant, Cafeteria, Coffee, Market, Fast Food",
        subcategories=[
            Subcategory(name="Grocery",
                        description="Expenses at grocery stores and supermarkets",
                        example="Trader Joe's, Wholefoods, Costco, Mitsuwa, 99 Ranch"),
            Subcategory(name="Dining",
                        description="Dining and food delivery expenses",
                        example="Jolibee, Uber Eats, Doordash"),
            Subcategory(name="Alcohol",
                        description="Expenses at wineries and alcohol shops",
                        example="Total Wine"),
            Subcategory(name="Household Supplies",
                        description="Household consumable supplies",
                        example="Target")
        ]
    ),

    Category(
        name="Home",
        description="Home related expenditures, including rent, utilities, household essentials"
                    "(not including daily consumables), clothing",
        example="Rent, Utility, Internet, Home, Clothing, Cleaning supplies",
        subcategories=[
            Subcategory(name="Rent",
                        description="Monthly rent payments. The amount of such payments is likely to be higher than"
                                    "other daily purchases",
                        example="Rent"),
            Subcategory(name="Utilities",
                        description="Utility bills",
                        example="Electricity, Water, Garbage, Trash, ATT, Comcast, Verizon, Tmobile"),
            Subcategory(name="Household Essentials",
                        description="Non-daily consumable household items",
                        example="HomeGoods, Daiso, Miniso"),
            Subcategory(name="Clothing",
                        description="Expenses on clothing",
                        example="Zara, Uniqlo, Aritzia")
        ]
    ),

    Category(
        name="Travel",
        description="Traveling expenses, including gas, auto insurance, hotels, flights, rideshares",
        example="Gas station, airlines, auto insurance, ride share app, hotel, Airbnb",
        subcategories=[
            Subcategory(name="Auto",
                        description="Car related expenses, including gas, car insurance, car services, etc",
                        example="Shell, Chevron, BMW, Mercedes"),
            Subcategory(name="Hotel",
                        description="Accommodation expenses",
                        example="Hyatt, Marriott, Hilton, Residence"),
            Subcategory(name="Flight",
                        description="Air travel expenses",
                        example="United Airlines"),
            Subcategory(name="Transportation",
                        description="Expenses on public transit, parking, and rideshare services",
                        example="Lyft, Uber, Transportation, Parking, Transit")
        ]
    ),

    Category(
        name="Entertainment",
        description="Entertainment related expenses, including video game purchases, movies, tickets, ski resorts, etc",
        example="Game, Museum, Resorts, Amusement Park, Shows, Live House",
        subcategories=[
            Subcategory(name="Entertainment",
                        description="Expenses on entertainments",
                        example="AMC, museum, bar, theater")
        ]
    ),

    Category(
        name="Subscription",
        description="Recurring subscription expenses",
        example="Netflix, Spotify, OpenAI",
        subcategories=[
            Subcategory(name="Subscription",
                        description="Expenses on subscriptions",
                        example="Netflix, Spotify, OpenAI")
        ]
    ),

    Category(
        name="Health",
        description="Health related expenses, including doctor appointments, prescription drugs, messages, spa, "
                    "surgeries, and gym passes.",
        example="Spa, Massage, Dental, Hospital",
        subcategories=[
            Subcategory(name="Health",
                        description="Expenses on healthcare.",
                        example="Hospital visit, prescription drugs, surgeries, dental"),
            Subcategory(name="Well-being",
                        description="Expenses on non-medical, general well-beings.",
                        example="Massages, spa, facial")
        ]
    ),

    Category(
        name="Payment",
        description="Payments made towards credit card bills. This category should only contain payments toward"
                    "credit card bills and nothing else",
        example="Credit card payments",
        subcategories=[
            Subcategory(name="Credit Card Payments",
                        description="Payments made towards credit card bills",
                        example="Credit card payments")
        ]
    ),

    Category(
        name="Others",
        description="If you are not certain about a transaction falling into any of the categories, use this.",
        example="",
        subcategories=[
            Subcategory(name="Miscellaneous",
                        description="Miscellaneous expenses",
                        example="Any expense not categorized")
        ]
    )
]


def get_subcategories(category_name: str, categories: List[Category]) -> Optional[List[Subcategory]]:
    for category in categories:
        if category.name == category_name:
            return category.subcategories
    return None


# Pandas schema for transaction logs
log_filename = "full_transaction_logs.csv"

log_schema_types = {
    'ID': 'object',
    'Merchant': 'object',
    'Amount': 'float64',
    'Category': 'object',
    'Subcategory': 'object',
}

log_schema_cols = ['ID', 'Date', 'Year', 'Month', 'Merchant', 'Amount', 'Category', 'Subcategory', 'LogDate']

log_date_cols = {'Date': '%Y-%m-%d',
                 'LogDate': '%Y-%m-%d %H:%M:%S'}
