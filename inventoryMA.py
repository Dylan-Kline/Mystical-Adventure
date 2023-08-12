# @ inventoryMA.py
# This is the inventory class for the player character

class Inventory:
    
    def __init__(self, quantity):
        self.inventory = dict()
        self.INVspace = quantity
        self.numItems = 0
    
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
    