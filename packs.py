from datetime import date

class Pack:
    """Base class for QC packs"""

    pack_types = ['Main', 'Shop', 'Bolt-in', 'Field Weld', 'Closure', 'SD Field Weld', 'SD Bolt-In', 
                'SD Closure']
    stages = ['Created', 'Scheduled', 'In progress', 'Welded', 'Visualed', 'NDEd', 'Hydrotested', 
              'Installed', 'Signed off', 'Stored']
    required_info = ['Fab WO#', 'Install WO#', ]
    
    def __init__(self, pack_type, stage, shutdown):
        """Initialize the instance variables for a QC pack"""

        self.creation_date = date.today()
        self.pack_type = Pack.pack_types[pack_type]
        self.stage = Pack.stages[stage]
        self.shutdown = shutdown
    
    def update_stage(self):
        """Update pack stage from the list of possible stages"""

        print(f"This pack is currently at stage: {self.stage}")
        print("What would you like to update it to?")
        for i in range(0, len(Pack.stages)):
            print(f"{i} = {Pack.stages[i]}") 
        updated_stage = int(input("Enter stage:"))
        self.stage = Pack.stages[updated_stage]
        print(f"The pack has been updated to: {self.stage}")