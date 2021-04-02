import crypto
import binascii

# generates unique id of 4 bytes
def generateID():
    # creates random id
    id = crypto.getrandbits(4)

    # loops through id_list.txt file, where old ids are stored and checks, if
    # the id is unique
    idUnique = False
    while not idUnique:
        # makes string out of generated id
        idHex = binascii.hexlify(id)
        idStr = idHex.decode('utf8')
        idStr = idStr + '\r\n'
        # opens id_list.txt file
        with open('id_list.txt') as usedIds:
            if not idStr in usedIds.read():
                idUnique = True         # if generated id is unique breaks out of loop
            else:
                id = uos.urandom(4)     # generates new id if id is not unique

    # write new unique id to the list
    with open('id_list.txt', 'a') as usedIds:
        usedIds.write(idStr)

    return id
