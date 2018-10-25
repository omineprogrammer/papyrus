## This script requires "requests": http://docs.python-requests.org/
## To install: pip install requests


import requests
import json


def requester(url):
    api_key = "7EkRBuNJuZpypNF3vzJl"
    domain = "colegioalemandsbaq.freshservice.com"
    password = "Ars3n1c033"

    try:
        r = requests.get("https://" + domain + url, auth = (api_key, password))
        if r.status_code == 200:
            return json.loads(r.content)
        elif r.status_code == 404:
            return None
        else:
            print("status_code: " + str(r.status_code))
            return False
    except:
        pass

def getTicket(ticket_id):
    return requester("/helpdesk/tickets/" + str(ticket_id) + ".json")

def getContact(contact_id):
    return requester("/itil/requesters/" + str(contact_id) + ".json")

def getAllContact():
    lst = []
    sw = True
    i = 1
    while sw:
        request = requester('/itil/requesters.json?page=' + str(i))
        if request:
            lst += request
            i += 1
        else:
            sw = False
    return lst

def getAllTicketsOfContact(requester_id):
    return requester("/helpdesk/tickets/filter/requester/" + str(requester_id) + "?format=json")

def getLast30SistemasTickets():
    return requester("/helpdesk/tickets/view/302588?format=json")


def getListContacts():
    contactos = []
    for i in getAllContact():
        # if i['user']['active'] and not(i['user']['deleted']):
            contactos.append( (i['user']['id'], i['user']['name']) )
    return tuple(contactos)

def getDictContacts():
    contactos = {}
    for i in getAllContact():
        # if i['user']['active'] and not(i['user']['deleted']):
            contactos[i['user']['id']] = i['user']['name']
    return contactos
