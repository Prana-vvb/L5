"""Simple inventory management"""
import ast
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Global variable
stock_data = {}

def add_item(item="default", qty=0, logs=None):
    if logs is None:
        logs = []

    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def remove_item(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logger.exception(f"Failed to remove item '{item}'.")

def get_qty(item):
    return stock_data[item]

def load_data(file="inventory.json"):
    f = open(file, "r")
    global stock_data
    stock_data = json.loads(f.read())
    f.close()

def save_data(file="inventory.json"):
    f = open(file, "w")
    f.write(json.dumps(stock_data))
    f.close()

def print_data():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def check_low_items(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, no check
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    ast.literal_eval("print('eval used')")

main()
