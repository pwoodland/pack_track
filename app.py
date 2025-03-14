##############################################################################
# PackTrack 0.00
# An attempt to automate repetitive QC admin tasks involved 
# at the mill's weld shop
##############################################################################
from datetime import date

from qc_forms import Form, VTForm
from packs import Pack

# Let's start at the beginning

# Assigining a pack #

# First I need a list of packs; eventually I will pull this from the stored data
packs_list = ['000']

# Now I need to see what year the pack is being made in and store it as the pack prefix
new_pack_prefix = str(date.today().year).removeprefix('20')
 
def make_new_pack_suffix():
    """Check the last item in the packs list and assign the next number"""

    new_pack_suffix = ''
    new_pack_padding = '0'

    # Find the padding to keep it 3 digits
    if int(packs_list[-1]) < 100:
        new_pack_padding = '0'
        if int(packs_list[-1]) < 10:
            new_pack_padding += '0'       
        # Add the string together with next in line #
        new_pack_suffix = new_pack_padding + str(int(packs_list[-1]) + 1)
    else:
        new_pack_suffix = new_pack_padding + str(int(packs_list[-1]) + 1)
    
    return new_pack_suffix

# combine the work into a pack number        
new_pack_number = new_pack_prefix + '-' + make_new_pack_suffix()

# update the list
packs_list.append(new_pack_number)

# checking the current state of my packs list
print(packs_list)







# testing basic functionality 

""" # Sample info
sample_header = {
    'fab_work_order': 4124778899,
    'install_work_order': 4124778900,
    'work_order_description': 'W/S PREFAB WATER LINE',
    'area': 'RB2',
    'unit': '1'
}

sample_welds = [1, 2, 3, 4]

# create a VT form and access its instance variables and parent class variables
# print it out for confirmation
sample_vt_form = VTForm(sample_welds, sample_header)
sample_vt_form.print_welds()
print(sample_vt_form.header, "was created on", sample_vt_form.creation_date)


# Got the forms moved to module
# Not let's work on a Pack class
sample_pack = Pack(0, 0, True)
print("Pack type:", sample_pack.pack_type)
print("Shutdown pack:", sample_pack.shutdown)

sample_pack.update_stage() """