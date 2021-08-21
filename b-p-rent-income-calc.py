# from IPython.display import clear_output

import os
clear = lambda: os.system('cls')


def verify_and_convert_amount(text_entered):
    text_entered = text_entered.strip("$ ")
    if text_entered.isnumeric() == True:
        float_text_entered = float(text_entered)
        return float_text_entered
    else:
        print("Only numbers and '$' allowed. Please try again.")
        return "Ask Again"

def take_input(list_names):
    list_values = []
    i = 0
    while i < len(list_names):
        amount = input(f"{list_names[i]}: ")
        amount = verify_and_convert_amount(amount)
        if amount != "Ask Again":
            list_values.append(amount)
            i += 1
    return dict(zip(list_names, list_values))

class PropertyAndExpenses():
    def __init__(self,
                property_price,
                num_rooms,
                property_sqft,
                ):
        self.property_price = property_price
        self.num_rooms = num_rooms
        self.property_sqft = property_sqft

    def get_expense_details(self):
        # standard monthly expenses
        print("\nPlease provide your monthly cost on the following:\n")
        monthly_standard_expense_names = [
                    "\t- Property taxes",
                    "\t- Property insurance",
                    "\t- Electricity",
                    "\t- Water",
                    "\t- Sewer",
                    "\t- Garbage and recycling",
                    "\t- Gas",
                    "\t- Repairs and maintenance",
                    "\t- HOA",
                    "\t- Lawn care",
                    "\t- Snow assistance",
                    "\t- Property manager",
                    "\t- Mortgage payment",
                    ]
        self.monthly_standard_expenses = take_input(
                                        monthly_standard_expense_names,
                                        )
        # savings for rainy day and other large infrequent expenses
        print("\nPlease provide how much you're going to save monthly for these"
              " rainy day / planned expenditures\n")
        monthly_rainy_day_savings_plan_names = [
                    "\t- Vacancy",
                    "\t- Capital expense (also known as major planned upgrades)",
                    "\t- Miscellaneous",
                    ]
        self.monthly_rainy_day_savings_plan = take_input(
                                   monthly_rainy_day_savings_plan_names,
                                   )
        # assert ((standard == 1 and rainy == 0) or (standard == 0 
        # and rainy == 1)), ("This should never happen, but if it does"
        # " then either standard or rainy has been set to a value other"
        # " than 1 or 0 in the calc_monthly_total_expenses method.")
        expenses = [
                    self.monthly_standard_expenses,
                    self.monthly_rainy_day_savings_plan,
                    ]
        return expenses
        # yield self.monthly_rainy_day_savings_plan
        # if standard == 1 and rainy == 0:
        #     yield self.monthly_standard_expenses
        # elif standard == 0 and rainy == 1:
        #     yield self.monthly_rainy_day_savings_plan
        # Note: Could make these Yields instead of returns at some point
        # in the future and handle the AttributeError: 'generator' object
        # has no attribute 'values' that arises when they are Yields.

    def get_income_details(self):
        print("\nPlease provide the following income allocations\n")
        monthly_income_names = [
                  "\t- How much will you receive in total from tenants each each month?",
                  "\t- How much will you make off laundry machines in total"
                  " each month (if applicable)?",
                  "\t- What's the total monthly income from storage unit"
                  " rentals (if applicable)?",
                  "\t- How much other monthly income do you expect from"
                  " the property?",
                  ]
        self.monthly_incomes = take_input(monthly_income_names)
        return self.monthly_incomes


class Owner():
    def __init__(self):
        self.total_investment = 0

    def get_owner_info(self):
        owner_figure_names = [
                            "\t- How much was your down payment on the property?",
                            "\t- Any closing costs? If so, how much?",
                            "\t- How much will you spend improving the property"
                            " after you've purchased it?",
                            ]
        print("\nPlease provide some ownership figures\n")
        owner_figures = take_input(owner_figure_names)
        for value in owner_figures.values():
            self.total_investment += value
        return self.total_investment


class Calculator(PropertyAndExpenses, Owner):
    def __init__(
        self,
        property_price,
        num_rooms,
        property_sqft,
        ):
        # could move the following up into the Calculator __init__
        # monthly_total_expenses,
        # monthly_total_income,
        # monthly_total_cash_flow,
        # cash_on_cash_roi,

        # self.monthly_total_expenses = monthly_total_expenses
        # self.monthly_total_income = monthly_total_income

        # monthly total cash flow = monthly income - monthly expenses
        # self.monthly_total_cash_flow = monthly_total_cash_flow
        
        # cash on cash ROI = annual cash flow / total investment as %
        # self.cash_on_cash_roi = cash_on_cash_roi
        
        # Initialize attributes of the parent classes
        super().__init__(
            property_price,
            num_rooms,
            property_sqft,
            )

    def calc_monthly_total_expenses(self):
        self.monthly_total_standard_expense = 0
        self.monthly_total_rainy_expense = 0
        self.monthly_total_expense = 0

        all_monthly_expenses = PropertyAndExpenses(
            1,
            2,
            3,
            ).get_expense_details()

        for value in all_monthly_expenses[0].values():
            self.monthly_total_standard_expense += value

        for value in all_monthly_expenses[1].values():
            self.monthly_total_rainy_expense += value

        self.monthly_total_expense = \
            self.monthly_total_standard_expense \
          + self.monthly_total_rainy_expense
        
        return self.monthly_total_expense

    def calc_monthly_total_income(self):
        self.monthly_total_income = 0
        for value in PropertyAndExpenses(
            1,
            2,
            3,
            ).get_income_details().values():
            self.monthly_total_income += value
        return self.monthly_total_income

    def calc_monthly_total_cash_flow(self, monthly_total_income, monthly_total_expense):
        """
        monthly income - monthly expenses
        """
        self.monthly_total_cash_flow = \
            monthly_total_income \
          - monthly_total_expense
        return self.monthly_total_cash_flow

    def calc_cash_on_cash_roi(self, monthly_total_cash_flow, total_investment):
        """ annual cash flow / total investment as % """

        annual_cash_flow = monthly_total_cash_flow * 12

        self.cash_on_cash_roi = \
            (annual_cash_flow
            / total_investment) * 100

        return self.cash_on_cash_roi

def run():
    mo_t_exp = ""
    mo_t_inc = ""
    mo_t_cash_flow = ""
    t_investment = ""
    c_on_c_roi = ""
    print("\nWelcome to the Bigger Pockets calculator!\n")
    while True:
        choice = input("What would you like to do? (To quit type 'q')\n"
            "\t- Calculate my total monthly expenses | type 'expenses'\n"
            "\t- Calculate my total monthly income | type 'income'\n"
            "\t- Calculate my total monthly cash flow | type 'flow'\n"
            "\t- Calculate my total investment | type 'investment'\n"
            "\t- Calculate my Cash on Cash ROI | type 'roi'\n")
        choice = choice.casefold()
        if choice == 'q':
            break
        elif choice == 'expenses':
            clear()
            # clear_output()
            # property_price, num_rooms, property_sqft
            if mo_t_exp == "":
                mo_t_exp = Calculator(1, 2, 3).calc_monthly_total_expenses()
                print(f"\nYour total monthly expense is: ${mo_t_exp:.2f}\n")
            else:
                print(f"\nYour total monthly expense is: ${mo_t_exp:.2f}\n")
        elif choice == 'income':
            clear()
            # clear_output()
            if mo_t_inc == "":
                mo_t_inc = Calculator(1, 2, 3).calc_monthly_total_income()
                print(f"\nYour total monthly income is: ${mo_t_inc:.2f}\n")
            else:
                print(f"\nYour total monthly income is: ${mo_t_inc:.2f}\n")
        elif choice == 'flow':
            clear()
            # clear_output()
            if mo_t_exp != "" and mo_t_inc != "":
                mo_t_cash_flow = mo_t_inc - mo_t_exp
                print(f"\nYour total monthly cash flow is ${mo_t_cash_flow:.2f}\n")
            elif mo_t_exp != "" and mo_t_inc == "":
                print("We need some income figures first!")
                mo_t_inc = Calculator(1, 2, 3).calc_monthly_total_income()
                mo_t_cash_flow = mo_t_inc - mo_t_exp
                print(f"\nYour total monthly cash flow is ${mo_t_cash_flow:.2f}\n")
            elif mo_t_exp == "" and mo_t_inc != "":
                print("We need some expense figures first!")
                mo_t_exp = Calculator(1, 2, 3).calc_monthly_total_expenses()
                mo_t_cash_flow = mo_t_inc - mo_t_exp
                print(f"\nYour total monthly cash flow is ${mo_t_cash_flow:.2f}\n")
            elif mo_t_exp == "" and mo_t_inc == "":
                mo_t_inc = Calculator(1, 2, 3).calc_monthly_total_income()
                mo_t_exp = Calculator(1, 2, 3).calc_monthly_total_expenses()
                mo_t_cash_flow = Calculator(1, 2, 3).calc_monthly_total_cash_flow(mo_t_inc, mo_t_exp)
                print(f"\nYour total monthly cash flow is ${mo_t_cash_flow:.2f}\n")
            else:
                print(f"\nYour total monthly cash flow is ${mo_t_cash_flow:.2f}\n")
        elif choice == 'investment':
            clear()
            # clear_output()
            if t_investment == "":
                t_investment = Owner().get_owner_info()
                print(f"\nYour total upfront investment is: ${t_investment:.2f}\n")
            else:
                print(f"\nYour total upfront investment is: ${t_investment:.2f}\n")
        elif choice == 'roi':
            clear()
            # clear_output()
            if mo_t_exp != "" and mo_t_inc != "":
                mo_t_cash_flow = mo_t_inc - mo_t_exp
            elif mo_t_exp != "" and mo_t_inc == "":
                print("Hey, we'll get there. We need more info first:")
                mo_t_inc = Calculator(1, 2, 3).calc_monthly_total_income()
                mo_t_cash_flow = mo_t_inc - mo_t_exp
            elif mo_t_exp == "" and mo_t_inc != "":
                print("Hey, we'll get there. We need more info first:")
                mo_t_exp = Calculator(1, 2, 3).calc_monthly_total_expenses()
                mo_t_cash_flow = mo_t_inc - mo_t_exp
            elif mo_t_exp == "" and mo_t_inc == "":
                mo_t_inc = Calculator(1, 2, 3).calc_monthly_total_income()
                mo_t_exp = Calculator(1, 2, 3).calc_monthly_total_expenses()
                mo_t_cash_flow = Calculator(1, 2, 3).calc_monthly_total_cash_flow(mo_t_inc, mo_t_exp)
            
            if t_investment == "":
                print("Hey, we'll get there. We need more info first:")
                t_investment = Owner().get_owner_info()
            
            if c_on_c_roi == "":
                c_on_c_roi = Calculator(1, 2, 3).calc_cash_on_cash_roi(mo_t_cash_flow, t_investment)
                print(f"\nYour Cash on Cash Return on Investment is: {c_on_c_roi:.2f}%\n")
            else:
                print(f"\nYour Cash on Cash Return on Investment is: {c_on_c_roi:.2f}%\n")
        else:
            print("Please check your spelling and try again.")

run()