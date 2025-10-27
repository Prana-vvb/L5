"""Simple inventory management"""
import json
import logging
from datetime import datetime
from ast import literal_eval

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class Inventory:
    """Encapsulates all inventory logic and state."""

    def __init__(self, stock_file="inventory.json"):
        """Initialize the inventory, loading data from the file."""
        self.stock_file = stock_file
        self.stock_data = {}
        self.logs = []
        self.load_data()

    def add_item(self, item="default", qty=0):
        """
        Add a specified quantity of an item to the stock.
        Handles type checking for quantity.
        """
        if not isinstance(item, (str, int)):
            logger.warning(f"Item name '{item}' is not a string or int. Skipping.")
            return
        try:
            qty_val = int(qty)
        except (ValueError, TypeError):
            logger.error(f"Invalid quantity '{qty}' for item '{item}'. Must be an integer.")
            return

        if not item:
            return

        self.stock_data[item] = self.stock_data.get(item, 0) + qty_val
        self.logs.append(f"{str(datetime.now())}: Added {qty_val} of {item}")
        logger.info(f"Added {qty_val} of {item}. New total: {self.stock_data[item]}")

    def remove_item(self, item, qty):
        """
        Remove a specified quantity of an item from the stock.
        Handles type checking and removes item if stock reaches zero or less.
        """
        try:
            qty_val = int(qty)
            if qty_val <= 0:
                logger.warning(f"Quantity to remove must be positive: {qty_val}")
                return
        except (ValueError, TypeError):
            logger.error(f"Invalid quantity '{qty}' for item '{item}'. Skipping.")
            return

        try:
            self.stock_data[item] -= qty_val
            logger.info(f"Removed {qty_val} of {item}. New total: {self.stock_data.get(item)}")
            if self.stock_data[item] <= 0:
                del self.stock_data[item]
                logger.info(f"Item '{item}' removed from stock as quantity is zero or less.")
        except KeyError:
            logger.exception(f"Failed to remove item '{item}'. Not in stock.")
        except TypeError:
            logger.error(f"Data error for item '{item}'. Cannot perform subtraction.")

    def get_qty(self, item):
        """Get quantity of a specific item, defaulting to 0."""
        return self.stock_data.get(item, 0)

    def load_data(self):
        """
        Load inventory data from the JSON file.
        Uses 'with open' and handles potential errors.
        """
        try:
            with open(self.stock_file, "r") as f:
                self.stock_data = json.load(f)
                logger.info(f"Successfully loaded data from {self.stock_file}")
        except FileNotFoundError:
            logger.warning(f"{self.stock_file} not found. Starting with empty inventory.")
            self.stock_data = {}
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {self.stock_file}. Starting with empty inventory.")
            self.stock_data = {}

    def save_data(self):
        """
        Save the current inventory data to the JSON file.
        """
        try:
            with open(self.stock_file, "w") as f:
                json.dump(self.stock_data, f, indent=4)
                logger.info(f"Successfully saved data to {self.stock_file}")
        except IOError as e:
            logger.error(f"Failed to save data to {self.stock_file}: {e}")

    def print_data(self):
        """Print a simple inventory report to the console."""
        print("\n--- Items Report ---")
        if not self.stock_data:
            print("Inventory is empty.")
        for i, qty in self.stock_data.items():
            print(f"{i} -> {qty}")
        print("--------------------\n")

    def check_low_items(self, threshold=5):
        """Check for items with quantity below the threshold."""
        result = []
        for i, qty in self.stock_data.items():
            try:
                if int(qty) < threshold:
                    result.append(i)
            except (ValueError, TypeError):
                 logger.warning(f"Item '{i}' has non-numeric quantity '{qty}'. Skipping in low-item check.")
        return result

def main():
    """Main function to demonstrate Inventory class."""
    inventory = Inventory()
    inventory.add_item("apple", 10)
    inventory.add_item("banana", 5)
    inventory.add_item(123, "ten")
    inventory.add_item("grape", "not-a-number")
    inventory.remove_item("apple", 3)
    inventory.remove_item("orange", 1)
    print("Apple stock:", inventory.get_qty("apple"))
    print("Banana stock:", inventory.get_qty("banana"))
    print("Low items:", inventory.check_low_items())
    inventory.print_data()
    inventory.save_data()
    literal_eval("print('eval used')")


if __name__ == "__main__":
    main()
