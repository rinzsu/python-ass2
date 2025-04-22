"""
this program helps the supermarket departments reduce duplication of work and create accurate sales reports. 
program allows 'patches' to be applied to the base price list, so each department can sell the same items at different prices or have things that others don't. 
this program also validates sales records and generates structured reports, identifying both valid and incorrect entries.
"""

def is_valid_sale(price: dict[str,float], item_type: str, item_quantity: int, sale_total: float) -> bool:
  """
  checks if a sale is valid, a valid sale is considered if:
  - the amount is greater than 0
  - the item is listed in the price dictionary
  - the total matches the expected price (rounded to 2 decimal places)
  
  args:
  - price (dict): dictionary with item names and prices
  - item_type (str): name of the item being sold
  - item_quantity (int): how many items were sold
  - sale_total (float): total amount charged for the sale

  returns:
  bool: True if the sale is valid, False otherwise
  """
  return (
    item_quantity > 0 and # check if quantity is 0 then it's not a sale
    item_type in price and # check if item name exist in our catalog
    round(price[item_type], 2) == round((sale_total / item_quantity), 2) # check if price in catalog match with actual price
  )

def flag_invalid_sales(price: dict[str,float], sales: list) -> list:
  """
  finds and returns any sales that aren't valid

  args:
  - price (dict): a dictionary with the name and price of the item
  - sales (list): a list of sales, where each sale is [item_name, quantity, total]

  returns:
  - list: a list of sales that failed the validity check.
  """
  invalid_sales = []
  for sale in sales:
    item_type, item_quantity, sale_total = sale
    if item_quantity == 0:
      if item_type in price:
        continue
    if not is_valid_sale(price, item_type, item_quantity, sale_total):
      invalid_sales.append(sale)
  return invalid_sales

def flag_valid_sales(sales: list, invalid_sales: list) -> list:
  """
  gets valid sales by removing the sales that are marked invalid

  args:
  - sales(list): all recorded sales
  - invalid_sales(list): sales found to be invalid

  returns:
  - list: sales that passed the check
  """
  return [item for item in sales if item not in invalid_sales]

def generate_sales_report(price: dict[str,float], sales: list) -> dict[str,tuple]:
  """
  create a sales report for each item using valid and invalid sales data
  for each item, the report includes:
  - number of units sold
  - valid sales amount
  - average revenue per valid sale
  - invalid sales amount

  args:
  - price (dict): a dictionary with item names and prices
  - sales (list): a list of all sales records

  returns:
  - dict: a dictionary where each key is an item name and its values are a summary of its sales
  """
  sale_report = {}
  fix_price = {k: float(v) for k, v in price.items()}
  price = fix_price

  invalid_sales = flag_invalid_sales(price, sales)
  valid_sales = flag_valid_sales(sales, invalid_sales)

  all_keys = set(price.keys())
  all_keys.update([item[0] for item in sales])

  for key in all_keys:
    sale_report[key] = (0, 0, 0.0, 0)

  for sale in invalid_sales:
    item_type, item_quantity, sale_total = sale
    sr_unit, sr_sale_count, sr_avg, sr_err = sale_report[item_type]
    sale_report[item_type] = (sr_unit, sr_sale_count + 1, sr_avg, sr_err + 1)

  store_revenue = {}
  store_count = {}

  for sale in valid_sales:
    item_type, item_quantity, sale_total = sale
    sr_unit, sr_sale_count, sr_avg, sr_err = sale_report[item_type]
    store_revenue[item_type] = store_revenue.get(item_type, 0.0) + sale_total
    new_sale_unit = sr_unit + item_quantity
    new_sale_count = sr_sale_count + 1
    store_count[item_type] = store_count.get(item_type, 0) + 1
    new_avg = store_revenue[item_type] / store_count[item_type]
    sale_report[item_type] = (new_sale_unit, new_sale_count, new_avg, sr_err)

  return sale_report

def check_dict(obj):
  """
  checks if an object is a non-empty dictionary

  agr:
  - obj (any): the object to check

  returns:
  - bool: True if object is a non-empty dictionary, False otherwise
  """
  return (type(obj) is dict) and len(obj.items()) > 0

def patch_item_price(price, patch):
  """
  updates the price from the original list with the new value

  args:
  - price(dict): The original list of item prices
  - patch(dict): The new price to update or add  

  returns:
  - dict: the updated list with the new price included
  """
  if check_dict(patch):
    for k1, v1 in patch.items():
      if check_dict(v1):
        for k2, v2 in v1.items():
          price[k2] = v2
      else:
        price[k1] = v1
  return price

def generate_sales_reports(price, patch, sales):
  """
  creates a complete sales report for each department,
  the report updates prices based on department rules and includes:
  - all item stats
  - invalid sales

  args:
  - price(dict): original price
  - patch(dict): price update for each department
  - sales(list): sales data with department info

  returns:
  - list: one entry per department as a tuple:
    (department name, report data, invalid sales)
  """
  all_dep_name = sorted(list(set([x[0] for x in sales])))

  all_dep_sales = {}

  for dep in all_dep_name:
    dep_price = dict(price)

    if dep in patch:
      dep_price = patch_item_price(dep_price, patch[dep])

    dep_sales = [ [x[1], x[2], x[3]] for x in sales if x[0] == dep]
    all_dep_sales[dep] = {
      "report": generate_sales_report(dep_price, dep_sales),
      "invalid": flag_invalid_sales(dep_price, dep_sales)
    }

  final_sales = []

  for k, v in all_dep_sales.items():
    final_sales.append((k, v["report"], v["invalid"]))

  return final_sales

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
  """
  main function to simulate the robot's action:
  - runs a sales report for different store departments
  - sets the specific updates for prices and department
  - validates sales and filters out invalid ones
  - generates and prints reports for each department
  """
  price = {
    'apple': 8.91,
    'item2': 9.54,
    'orange': 5.9,
    'laptop': 2.91,
    'car': 3.57,
    'item1': 6.28,
    'item3': 0.79
  }

  patch = {
    'evilDepartmnet': {
      'car': 5.13
    }
  }

  sales = [
    ['dep4', 'aple', 5, 29.5],
    ['dep1', 'lapto', 0, 0.0],
    ['evilDepartmnet', 'car', 9, 32.129999999999995],
    ['dep4', 'ornge', 10, 40.81],
    ['dep4', 'apple', 10, 89.1],
    ['evilDepartmnet', 'car', 5, 17.849999999999998],
    ['dep1', 'apple', 4, 35.64],
    ['evilDepartmnet', 'item2', 4, 38.16]
  ]

  expected = [
    (
      'dep4',
      {
        'aple': (0, 1, 0, 1),
        'ornge': (0, 1, 0, 1),
        'apple': (10, 1, 89.1, 0),
        'item2': (0, 0, 0, 0),
        'orange': (0, 0, 0, 0),
        'laptop': (0, 0, 0, 0),
        'car': (0, 0, 0, 0),
        'item1': (0, 0, 0, 0),
        'item3': (0, 0, 0, 0)
      },
      [
        ['aple', 5, 29.5],
        ['ornge', 10, 40.81]
      ]
    ),
    (
      'dep1',
      {
        'lapto': (0, 1, 0, 1),
        'apple': (4, 1, 35.64, 0),
        'item2': (0, 0, 0, 0),
        'orange': (0, 0, 0, 0),
        'laptop': (0, 0, 0, 0),
        'car': (0, 0, 0, 0),
        'item1': (0, 0, 0, 0),
        'item3': (0, 0, 0, 0)
      },
      [
        ['lapto', 0, 0.0]
      ]
    ),
    (
      'evilDepartmnet',
      {
        'car': (0, 2, 0, 2),
        'item2': (4, 1, 38.16, 0),
        'apple': (0, 0, 0, 0),
        'orange': (0, 0, 0, 0),
        'laptop': (0, 0, 0, 0),
        'item1': (0, 0, 0, 0),
        'item3': (0, 0, 0, 0)
      },
      [
        ['car', 9, 32.129999999999995],
        ['car', 5, 17.849999999999998]
      ]
    )
  ]

  # generate complete sales reports for each department
  final_report = generate_sales_reports(price, patch, sales)

  # retrieve the department name, sales report, and list of invalid sales
  for dep in final_report:
    dep_name = dep[0]
    sales_report = dep[1]
    invalid_sales = dep[2]

    # print all sales information
    print("Sales Report:")
    for item_name in sales_report:
      values = sales_report[item_name]
      print(item_name, ":", values)

    # print sales that were flagged as invalid
    print("Invalid Sales:")
    for invalid in invalid_sales:
      print(invalid)
    print() 