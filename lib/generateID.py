import uos
import binascii

def generateID():
    id = uos.urandom(4)

    idUnique = False
    while not idUnique:
        idHex = binascii.hexlify(id)
        idStr = idHex.decode('utf8')
        idStr = idStr + '\r\n'

        with open('id_list.txt') as usedIds:
            if not idStr in usedIds.read():
                idUnique = True
            else:
                id = uos.urandom(4)

    idHex = binascii.hexlify(id)
    idStr = idHex.decode('utf8')
    idStr = idStr + '\r\n'

    with open('id_list.txt', 'a') as usedIds:
        usedIds.write(idStr)

    return id
