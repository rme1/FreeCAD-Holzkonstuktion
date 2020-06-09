class merzi (Workbench): 
   MenuText = "Merzi"
   def Initialize(self):
       import merzi_BalkenBauen # py Skript
       commandslist = ["MerziLinie","makeKugellager","makeBalken"]
       self.appendToolbar("Merzi",commandslist)
       
Gui.addWorkbench(merzi())