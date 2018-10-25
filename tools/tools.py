from tools.api.freshservice import *


def getListContacts():
    contactos = []
    for i in getAllContact():
        if i['user']['active'] and not(i['user']['deleted']):
            contactos.append( (i['user']['id'], i['user']['name']) )
    print('[INFO]: load ' + str(contactos.__len__()) + ' contacts')
    return tuple(contactos)


def getSubListRequesterTicket():
    groupTickets = []
    for requester in getListContacts():
        tickets = []
        requesterTickets = getAllTicketsOfContact(requester[0])
        if requesterTickets:
            for ticket in requesterTickets:
                tickets.append( (ticket['id'], ticket['subject']) )
            if tickets:
                groupTickets.append( (requester[1], tuple(tickets)) )
            print('[INFO]: load ' + str(tickets.__len__()) + ' tickets for ' + requester[1])
    return tuple(groupTickets)


def getLastSubListRequesterTicket():
    tickets = getLast30SistemasTickets()
    contacts = getDictContacts()
    groupTickets = {}
    out = []
    if tickets and contacts:
        for tckt in tickets:
            nameContact = contacts.get(tckt['requester_id'])

            if nameContact and groupTickets.get(nameContact):
                groupTickets[nameContact].append((tckt['id'], '#INC-' + str(tckt['display_id']) + ': ' + tckt['subject']))
            elif nameContact:
                groupTickets[nameContact] = [ (tckt['id'], '#INC-' + str(tckt['display_id']) + ': ' + tckt['subject']) ]

        keys = list(groupTickets)
        keys.sort()
        for key in keys:
            out.append( (key, tuple(groupTickets[key])) )
    return out
