##############################################################################
# PackTrack 0.00
# An attempt to automate repetitive QC admin tasks involved 
# at the mill's weld shop
##############################################################################

from qc_forms import Form, VTForm
from packs import Pack

# Sample info
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

sample_pack.update_stage()