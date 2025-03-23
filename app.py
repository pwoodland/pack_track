##############################################################################
# PackTrack 0.00
# An attempt to automate repetitive QC admin tasks involved 
# at the mill's weld shop
##############################################################################

# got the read packs gui function to pull and display the pack info from the databse
# next I want to update the create pack function to open a set of fields to collect info 
# and submit to database


from datetime import date
from tkinter import *
from tkinter import ttk
# from qc_forms import Form, VTForm
# from packs import Pack
from pymongo import MongoClient, ReturnDocument
import pymongo


# GUI init
root = Tk()
root.title("PackTrack")
mainframe = ttk.Frame(root, width=1200, height=800, padding=5)
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
buttons = ttk.Frame(mainframe, padding=(5,0))
buttons.grid(column=0, row=0, sticky=(N, W))
content = ttk.Frame(mainframe, borderwidth=2, relief="raised", padding=3)
content.grid(column=1, row=0, sticky=(N, S, E, W))

PACK_NUMBER_COL = 0
REVISION_COL = 1
FAB_WO_COL = 2
INSTALL_WO_COL = 3
WO_DESC_COL = 4
UNIT_NO_COL = 5
AREA_NO_COL = 6
AREA_DESC_COL = 7

# database connection
MONGODB_URI = "mongodb+srv://admin:monkeybutt@cluster0.peilo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGODB_URI)
database = client["pack_track"]
collection = database["packs"]


# Database CRUDs #
# CREATE
# Making sure we don't skip or duplicate pack #s
def get_next_pack_number(col):
    """Check the pack id in the packs table and return the next number"""

    # # Get the latest pack number

    # must use sort parameter if using find_one as .sort() method is only available to a cursor instance
    last_pack = col.find_one({}, {"_id": 0, "pack_number": 1}, sort={"pack_number": pymongo.DESCENDING})
    # last_pack = cur.execute("""SELECT pack_id FROM packs ORDER BY pack_id DESC""").fetchone()

    # Get the last two digits of the year
    new_pack_prefix = str(date.today().year).removeprefix('20')
    new_pack_suffix = ''
    prefix_to_remove = new_pack_prefix + '-'
    last_pack_stripped = last_pack['pack_number'].removeprefix(prefix_to_remove)

    # Find the padding to keep it 3 digits
    if int(last_pack_stripped) < 99:
        new_pack_padding = '0'
        if int(last_pack_stripped) < 9:
            new_pack_padding += '0'       
            # Add the string together with next in line #
        new_pack_suffix = new_pack_padding + str(int(last_pack_stripped) + 1)
    else:
        new_pack_suffix = new_pack_padding + str(int(last_pack_stripped) + 1)
    
    next_pack_number = new_pack_prefix + '-' + new_pack_suffix
    return next_pack_number

# Now to actually add it in the database
# def add_new_pack_number(col):
#     """ This function will add the new pack number to the database"""

#     print("Adding pack number: ", get_next_pack_number(col))
#     col.insert_one({"pack_number" : get_next_pack_number(col)})  

def add_new_pack_number_gui(col):
    """ This function will add the new pack number to the database"""

    print("Adding pack number: ", get_next_pack_number(col))
    col.insert_one({"pack_number" : get_next_pack_number(col)})  


# READ
def list_packs(col):
    """ Find all packs in the database and print them out """

    results = col.find({}, {"_id": 0, "func_location": 0, "func_location_description": 0, "op_short_text": 0, 
                                   "planner_group": 0, "plant_area": 0, "sort_field": 0}
                                   ).sort("pack_number", pymongo.ASCENDING)
    for pack in results:
        print(pack)

def list_packs_gui(col):
    """ Find all packs in the database and create the table """

    results = col.find({}, {"_id": 0, "func_location": 0, "func_location_description": 0, "op_short_text": 0, 
                                   "planner_group": 0, "plant_area": 0, "sort_field": 0}
                                   ).sort("pack_number", pymongo.ASCENDING)
    # results_as_list = results.to_list()
    # print(results)
    # print(results_as_list)
    i = 0
    for pack in results:
        i += 1
        for k in pack:
            if k == "pack_number":    
                pack_number = pack[k]
                pack_number_value = ttk.Label(content, text=pack_number)
                pack_number_value.grid(column=PACK_NUMBER_COL, row=i)
            elif k == "revision":
                revision = pack[k]
                revision_value = ttk.Label(content, text=revision)
                revision_value.grid(column=REVISION_COL, row=i)
            elif k == "fab_wo_number":
                fab_wo = pack[k]
                fab_wo_value = ttk.Label(content, text=fab_wo)
                fab_wo_value.grid(column=FAB_WO_COL, row=i)
            elif k == "install_wo_number":
                install_wo = pack[k]
                install_wo_value = ttk.Label(content, text=install_wo)
                install_wo_value.grid(column=INSTALL_WO_COL, row=i)
            elif k == "wo_description":
                wo_description = pack[k]
                wo_description_value = ttk.Label(content, text=wo_description)
                wo_description_value.grid(column=WO_DESC_COL, row=i)
            elif k == "unit_no":
                unit_no = pack[k]
                unit_no_value = ttk.Label(content, text=unit_no)
                unit_no_value.grid(column=UNIT_NO_COL, row=i)
            elif k == "plant_area":
                area = pack[k]
                area_value = ttk.Label(content, text=area)
                area_value.grid(column=AREA_NO_COL, row=i)
            elif k == "area_description":
                area_description = pack[k]
                area_description_value = ttk.Label(content, text=area_description)
                area_description_value.grid(column=AREA_DESC_COL, row=i)

# UPDATE

def request_pack(command):
    user_pack = input(f"What pack number do you want to {command}? (YY-XXX): ")
    return user_pack

def update_pack(col):
    """ Ask what pack to update, then what field and value to update """

    requested_pack = request_pack("update")
    pack_to_update = col.find_one({"pack_number": requested_pack}, {"_id":0})
    if pack_to_update != None:
        print(f"Going to update: {pack_to_update}")
        field_to_update = input("What field would you like to update?: ")
        value_to_update = input("What value should it be?: ")
        print(f"Going to update {field_to_update} to {value_to_update}")
        updated_pack = col.find_one_and_update({"pack_number": requested_pack}, {"$set": {field_to_update: value_to_update}}, 
                                               {"_id": 0}, return_document=ReturnDocument.AFTER)
        print("Pack is now:")
        print(updated_pack)
    else:
        print("That might not be in the system...")

# DELETE

def delete_pack(col):
    """ Ask what pack to delete and delete after confirmation """

    requested_pack = request_pack("delete")
    pack_to_delete = col.find_one({"pack_number": requested_pack}, {"_id": 0})
    print("You are about to delete the follwing pack: ")
    print(pack_to_delete)
    confirmation = input("This will delete all of this pack forever. Are you sure you want to delete? Y/N: ").lower()
    if confirmation == "y" or confirmation == "yes":
        col.delete_one({"pack_number": requested_pack})
        print("Deleted")
    else:
        print("Deletion cancelled")

# creating buttons
create_button = ttk.Button(buttons, text="Create Pack", width=10, command=lambda: add_new_pack_number_gui(collection))
create_button.grid()
read_button = ttk.Button(buttons, text="Read Packs", width=10, command=lambda: list_packs_gui(collection))
read_button.grid()
update_button = ttk.Button(buttons, text="Update Pack", width=10)
update_button.grid()
delete_button = ttk.Button(buttons, text="Delete Pack", width=10)
delete_button.grid()

# create main table labels
pack_number_label = ttk.Label(content, text="Pack Number")
pack_number_label.grid(column=0, row=0)
pack_revision_label = ttk.Label(content, text="Revision")
pack_revision_label.grid(column=1, row=0)
fab_wo_label = ttk.Label(content, text="Fab Work Order")
fab_wo_label.grid(column=2, row=0)
install_wo_label = ttk.Label(content, text="Install Work Order")
install_wo_label.grid(column=3, row=0)
wo_description_label = ttk.Label(content, text="Work Order Description")
wo_description_label.grid(column=4, row=0)
unit_no_label = ttk.Label(content, text="Unit #")
unit_no_label.grid(column=5, row=0)
area_code_label = ttk.Label(content, text="Area")
area_code_label.grid(column=6, row=0)
area_description_label = ttk.Label(content, text="Description")
area_description_label.grid(column=7, row=0)



# Main Tkinter loop
root.mainloop()
client.close()
# Main program loop
# running = True
# while running:
#     command = input("What would you like to do? (create / read / update / delete / quit: ")
#     if command == "quit":
#         running = False
#         client.close()
#     else:
#         match command:
#             case "create":
#                 add_new_pack_number(collection)
#             case "read":
#                 print("Here are all your packs:")
#                 list_packs(collection)
#             case "update":
#                 update_pack(collection)
#             case "delete":
#                 delete_pack(collection)
#             case _:
#                 print("Sorry that wasn't an option.")
