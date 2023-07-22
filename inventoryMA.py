# @ inventoryMA.py
# This is the inventory class for your character

class Inventory:
    
    maxStack = 99
    
    def __init__(self, quantity):
        self.inventory = dict()
        self.INVspace = quantity
        self.numItems = 0
    
    # Inserts a new item into your inventory.
    # If your inventory is full it asks you to select whether to discard the item 
    # or replace an item in your inventory
    def insert(self, item):
        
        # Put new item in inventory if space allows
        if self.numItems < self.INVspace:
            if item in self.inventory:
                self.inventory[item] += 1
            else:
                self.inventory[item] = 1
            self.numItems += 1
        else:
            print("Inventory is full.")
            return None
    
    # Discards a item from your inventory.
    # Or returns that item was not found in your inventory
    def discard(self, item):
        
        # Remove given item from inventory and permamently discard it
        try:
            
            del self.inventory[item]
            self.numItems -= 1
            print(f"Discarded {item} from inventory.")
            
        except:
            print("Item not found in inventory.")
            return None
      
    def getNumItems(self):
        return self.numItems
    
    def getStackSize(self, item):
        return self.inventory[item]
    
    def available_space(self):
        return (self.INVspace - self.getNumItems())
    
    def contains(self, item):
        if item in self.inventory:
            return 'Yes'
        else:
            return 'No'
    