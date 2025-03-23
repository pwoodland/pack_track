##############################################################################
# PackTrack 0.00
# An attempt to automate repetitive QC admin tasks involved 
# at the mill's weld shop
##############################################################################

from datetime import date

# from qc_forms import Form, VTForm
# from packs import Pack
from pymongo import MongoClient, ReturnDocument
import pymongo

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
def add_new_pack_number(col):
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

# Main program loop
running = True
while running:
    command = input("What would you like to do? (create / read / update / delete / quit: ")
    if command == "quit":
        running = False
        client.close()
    else:
        match command:
            case "create":
                add_new_pack_number(collection)
            case "read":
                print("Here are all your packs:")
                list_packs(collection)
            case "update":
                update_pack(collection)
            case "delete":
                delete_pack(collection)
            case _:
                print("Sorry that wasn't an option.")
