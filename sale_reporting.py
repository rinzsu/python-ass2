"""
this program reads a list of item prices along with the respective sales records. 
processes which sales are valid (correct price, existing item, non-zero quantity),
and constructs a report showing stats like total units sold, how many times each item was sold,
average revenue per sale, and the number of inaccurate sales that are made.
"""

def is_valid_sale(price: dict[str, float], item_type: str, item_quantity: int, sale_total: float) -> bool:
    """
    checks if a sale is valid

    args:
    - item_type (str): item name
    - item_quantity (int): quantity sold
    - sale_total (float): total sale value

    returns:
    - bool: True if the sale is valid, False otherwise
    """
    return (
        item_quantity > 0 and  # check if quantity is 0 then it's not a sale
        item_type in price and  # check if item name exists in our catalog
        round(price[item_type], 2) == round((sale_total / item_quantity), 2)  # check if price in catalog matches actual price
    )


def flag_invalid_sales(price: dict[str, float], sales: list) -> list:
    """
    finds the sales that don’t match the price list

    args:
    - price: price catalog
    - sales: list of sales to check

    return:
    - list of sales that do not match the expected price or item name (skips ones with 0 total)
    """
    invalid_sales = []
    for sale in sales:
        item_type, item_quantity, sale_total = sale

        if not is_valid_sale(price, item_type, item_quantity, sale_total):
            if sale_total == 0:
                continue
            invalid_sales.append(sale)

    return invalid_sales


def flag_valid_sales(sales: list, invalid_sales: list) -> list:
    """
    filter valid sales from the list of all sales by removing sales identified as invalid.

    args:
    - sales (list): Complete list of sales records.
    - invalid sales (list): list of sales records marked as invalid

    returns:
    - list: List of valid sales records (no invalid sales)
    """
    valid_sales = []
    for item in sales:
        if item not in invalid_sales:
            valid_sales.append(item)

    return valid_sales


def generate_sales_report(price: dict[str, float], sales: list) -> dict[str, tuple]:
    """
    puts together a summary of all sales per item

    args:
    - price: price catalog
    - sales: list of all sales

    return:
    - dictionary where each item has a tuple: (units sold, number of sales, avg revenue per sale, number of errors)
    """
    sale_report = {}

    fix_price = {}
    for k, v in price.items():
        fix_price[k] = float(v)

    price = fix_price

    invalid_sales = flag_invalid_sales(price, sales)
    valid_sales = flag_valid_sales(sales, invalid_sales)

    all_keys = set()
    for sale in sales:
        all_keys.add(sale[0])

    for key in price.keys():
        all_keys.add(key)

    for key in all_keys:
        sale_report[key] = (0, 0, 0, 0)

    for sale in invalid_sales:
        item_type, item_quantity, sale_total = sale

        sr_unit, sr_sale_count, sr_avg, sr_err = sale_report[item_type]
        new_sale_count = sr_sale_count + 1
        new_err = sr_err + 1

        sale_report[item_type] = (sr_unit, new_sale_count, sr_avg, new_err)

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


# sample input
price = {
    'car': 7.56,
    'orange': 9.45,
    'apple': 1.89,
    'tangerine': 5.93,
    'laptop': 6.79,
    'item2': 0.39
}

sales = [
    ['Apple', 8, 91.77],        # invalid: 'Apple' ≠ 'apple'
    ['laptop', 5, 33.95],       # valid: 5 * 6.79 = 33.95
    ['laptop', 6, 89.15],       # invalid: 6 * 6.79 = 40.74 ≠ 89.15
    ['tangerne', 8, 15.12],     # invalid: typo in item name
    ['laptop', 9, 61.11],       # valid: 9 * 6.79 = 61.11
    ['lapto', 8, 75.82],        # invalid: 'lapto' not in price
    ['laptop', 3, 20.37],       # valid: 3 * 6.79 = 20.37
    ['tangerine', 3, 0.92],     # invalid: 3 * 5.93 = 17.79
    ['orange', 5, 47.25]        # valid: 5 * 9.45 = 47.25
]


# print the final output
print("SALES REPORT")
report = generate_sales_report(price, sales)
for item, data in sorted(report.items()):
    print(f"{item}: {data}")