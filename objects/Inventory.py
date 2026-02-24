import config.constant as C

class Inventory:
    def __init__(self):
        self.slots = [(None, 0)] * 6  # (item, quantity)

    def add_item(self, item, quantity=1):
        for i in range(len(self.slots)):
            if self.slots[i][0] is None:
                self.slots[i] = (item, quantity)
                return True
            elif self.slots[i][0] == item:
                self.slots[i] = (item, self.slots[i][1] + quantity)
                return True
        return False  # Inventory full
    
    # def remove_item(self, item, quantity=1):
    #     for i in range(len(self.slots)):
    #         if self.slots[i][0] == item:
    #             if self.slots[i][1] >= quantity:
    #                 self.slots[i] = (item, self.slots[i][1] - quantity)
    #                 if self.slots[i][1] == 0:
    #                     self.slots[i] = (None, 0)
    #                 return True
    #             else:
    #                 return False  # Not enough quantity to remove
    #     return False  # Item not found
    
    def use_item(self, index, sprite):
        item, quantity = self.slots[index]
        if item is not None and quantity > 0:
            if "heal" in C.ITEM_JSON[item]['effects'] and getattr(sprite, 'health_remaining', None):
                sprite.health_remaining = min(sprite.health_remaining + C.ITEM_JSON[item]['effects']['heal'], sprite.health_start)
            self.slots[index] = (item, quantity - 1)
            if self.slots[index][1] == 0:
                self.slots[index] = (None, 0)
    
    def get_inventory(self):
        return self.slots