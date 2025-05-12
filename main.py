import json
import os

# Base Product class
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.__price = price
        self.__quantity = quantity

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if price >= 0:
            self.__price = price

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        if quantity >= 0:
            self.__quantity = quantity

    def get_details(self):
        return f"Product: {self.name}, Price: Rs.{self.get_price()}, Quantity: {self.get_quantity()}"

    def to_dict(self):
        return {
            "type": "Product",
            "name": self.name,
            "price": self.get_price(),
            "quantity": self.get_quantity()
        }


class Electronics(Product):
    def __init__(self, name, price, quantity, brand):
        super().__init__(name, price, quantity)
        self.brand = brand

    def get_details(self):
        return f"Electronics - {self.name} by {self.brand}, Rs.{self.get_price()}, Quantity: {self.get_quantity()}"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Electronics"
        data["brand"] = self.brand
        return data


class Clothing(Product):
    def __init__(self, name, price, quantity, size):
        super().__init__(name, price, quantity)
        self.size = size

    def get_details(self):
        return f"Clothing - {self.name} (Size: {self.size}), Rs.{self.get_price()}, Quantity: {self.get_quantity()}"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Clothing"
        data["size"] = self.size
        return data


class FoodItem(Product):
    def __init__(self, name, price, quantity, expiry_date):
        super().__init__(name, price, quantity)
        self.expiry_date = expiry_date

    def get_details(self):
        return f"Food - {self.name}, Rs.{self.get_price()}, Quantity: {self.get_quantity()}, Expires on: {self.expiry_date}"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "FoodItem"
        data["expiry_date"] = self.expiry_date
        return data


# Inventory class to manage products
class Inventory:
    def __init__(self, filename="inventory.json"):
        self.products = []
        self.filename = filename
        self.load_inventory()

    def add_product(self, product):
        self.products.append(product)
        print(f"{product.name} added to inventory.")
        self.save_inventory()

    def remove_product(self, name):
        for product in self.products:
            if product.name.lower() == name.lower():
                self.products.remove(product)
                print(f"{name} removed from inventory.")
                self.save_inventory()
                return
        print(f"{name} not found in inventory.")

    def show_inventory(self):
        if not self.products:
            print("Inventory is empty.")
        else:
            print("\nInventory List:")
            for product in self.products:
                print(product.get_details())
            print()

    def save_inventory(self):
        data = [product.to_dict() for product in self.products]
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def load_inventory(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for item in data:
                    if item["type"] == "Electronics":
                        self.products.append(Electronics(item["name"], item["price"], item["quantity"], item["brand"]))
                    elif item["type"] == "Clothing":
                        self.products.append(Clothing(item["name"], item["price"], item["quantity"], item["size"]))
                    elif item["type"] == "FoodItem":
                        self.products.append(FoodItem(item["name"], item["price"], item["quantity"], item["expiry_date"]))
                    else:
                        self.products.append(Product(item["name"], item["price"], item["quantity"]))


# CLI for user input
def user_menu():
    store = Inventory()

    while True:
        print("\n---- Inventory Management ----")
        print("1. Show Inventory")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Exit")
        choice = input("Select an option (1-4): ")

        if choice == '1':
            store.show_inventory()

        elif choice == '2':
            print("\n-- Add New Product --")
            ptype = input("Enter product type (Electronics / Clothing / FoodItem): ").strip().lower()
            name = input("Name: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))

            if ptype == "electronics":
                brand = input("Brand: ")
                product = Electronics(name, price, quantity, brand)

            elif ptype == "clothing":
                size = input("Size: ")
                product = Clothing(name, price, quantity, size)

            elif ptype == "fooditem":
                expiry_date = input("Expiry Date (YYYY-MM-DD): ")
                product = FoodItem(name, price, quantity, expiry_date)

            else:
                print("Unknown product type! Adding as generic Product.")
                product = Product(name, price, quantity)

            store.add_product(product)

        elif choice == '3':
            name = input("Enter product name to remove: ")
            store.remove_product(name)

        elif choice == '4':
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    user_menu()
