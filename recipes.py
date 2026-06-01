class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self):
        res = self.name + ": " + str(self._quantity) + " " + self.unit
        return res
    def __repr__(self):
        res = "Ingredient('" + self.name + "', " + str(self._quantity) + ", '" + self.unit + "')"
        return res
    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.unit != other.unit:
            return False
        return True

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients
    def add_ingredient(self, ingredient):
        for i in range(len(self.ingredients)):
            cur = self.ingredients[i]
            if cur == ingredient:
                cur.quantity = cur.quantity + ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if type(ratio) not in (int, float):
            return False
        if ratio <= 0:
            return False
        return True
    def scale(self, ratio):
        new_ings = []
        for ing in self.ingredients:
            new_ing = Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            new_ings.append(new_ing)
        res = Recipe(self.title, new_ings)
        return res
    def __len__(self):
        return len(self.ingredients)
    def __str__(self):
        res = self.title + ":\n"
        for ing in self.ingredients:
            res = res + "- " + str(ing) + "\n"
        return res

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ing in scaled.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title):
        new_items = []
        for item in self._items:
            if item[1] != title:
                new_items.append(item)
        self._items = new_items

    def get_list(self):
        totals = {}
        for item in self._items:
            ing = item[0]
            key = (ing.name, ing.unit)
            if key in totals:
                totals[key] = totals[key] + ing.quantity
            else:
                totals[key] = ing.quantity

        res = []
        for key in totals:
            name = key[0]
            unit = key[1]
            qty = totals[key]
            res.append(Ingredient(name, qty, unit))

        def get_name(ing):
            return ing.name
        res.sort(key=get_name)
        return res

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list
    
class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        scaled = super().scale(ratio)
        res = DietaryRecipe(self.title, self.diet_type, scaled.ingredients)
        return res

    def __str__(self):
        res = "[" + self.diet_type + "] " + super().__str__()
        return res