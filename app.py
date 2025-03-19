##############################################################################
# PackTrack 0.00
# An attempt to automate repetitive QC admin tasks involved 
# at the mill's weld shop
##############################################################################

from datetime import date

from qc_forms import Form, VTForm
from packs import Pack
from pymongo import MongoClient
import pymongo

MONGODB_URI = "mongodb+srv://admin:monkeybutt@cluster0.peilo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGODB_URI)
database = client["pack_track"]

# I currently have a datebase with one table, packs, with 3 columns
# I also have a function that can get the next pack number
# as well as a function that can store the next pack number in the databse

# Next step will be to add fab and install work orders and view the table in a CLI

def get_next_pack_number():
    """Check the pack id in the packs table and return the next number"""

    # # Get the latest pack number
    collection = database["packs"]
    # must use sort parameter if using find_one as .sort() method is only available to a cursor instance
    last_pack = collection.find_one({}, {"_id": 0, "pack_number": 1}, sort={"pack_number": pymongo.DESCENDING})
    # last_pack = cur.execute("""SELECT pack_id FROM packs ORDER BY pack_id DESC""").fetchone()

    # Get the last two digits of the year
    new_pack_prefix = str(date.today().year).removeprefix('20')
    new_pack_suffix = ''
    new_pack_padding = '0'
    prefix_to_remove = new_pack_prefix + '-'
    last_pack_stripped = last_pack['pack_number'].removeprefix(prefix_to_remove)

    # Find the padding to keep it 3 digits
    if int(last_pack_stripped) < 100:
        new_pack_padding = '0'
        if int(last_pack_stripped) < 10:
            new_pack_padding += '0'       
        # Add the string together with next in line #
        new_pack_suffix = new_pack_padding + str(int(last_pack_stripped) + 1)
    else:
        new_pack_suffix = new_pack_padding + str(int(last_pack_stripped) + 1)
    
    next_pack_number = new_pack_prefix + '-' + new_pack_suffix
    return next_pack_number


def add_new_pack_number():
    """ This function will add the new pack number to the database"""

    collection = database["packs"]
    print("Adding pack number: ", get_next_pack_number())
    collection.insert_one(
        {
            "pack_number" : get_next_pack_number()
        }
    )  

add_new_pack_number()
client.close()

##############################################################################
# testing basic functionality 

# # Sample info
# sample_header = {
#     'fab_work_order': 4124778899,
#     'install_work_order': 4124778900,
#     'work_order_description': 'W/S PREFAB WATER LINE',
#     'area': 'RB2',
#     'unit': '1'
# }

# sample_welds = [1, 2, 3, 4]

# # create a VT form and access its instance variables and parent class variables
# # print it out for confirmation
# sample_vt_form = VTForm(sample_welds, sample_header)
# sample_vt_form.print_welds()
# print(sample_vt_form.header, "was created on", sample_vt_form.creation_date)


# # Got the forms moved to module
# # Not let's work on a Pack class
# sample_pack = Pack(0, 0, True)
# print("Pack type:", sample_pack.pack_type)
# print("Shutdown pack:", sample_pack.shutdown)

# sample_pack.update_stage()
