# qc_forms are where the classes for all the forms live
from datetime import date

class Form:
    """Base class for all QC forms"""

    def __init__(self, header):
        """Initialize the base class with suppled info"""
        self.header = header
        self.creation_date = date.today()
    
    def update(self):
        """Update form with current data"""
        self.latest_date = date.today()

class VTForm(Form):
    """Class for VT/WQC report"""

    def __init__(self, welds, header):
        """Initialize the VT form with its parent init as well"""
        super().__init__(header)
        self.welds = welds

    def print_welds(self):
        """Print out the list of welds for the VT form"""
        for weld in self.welds:
            print(f"Weld #{weld}: JT-{weld}")