#pokemon power checker
'''
retrieves type information from api based on name, returns types
'''
import requests

def type_get(name):

    response = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
    status = response.status_code
    types_to_send = []
    
    if status == 200:#get type
        types = response.json()['types']
        for t in types:#appends any types to a list to be passed on to typeCompare
            types_to_send.append(t['type']['name'])
        
    else:#handle errors
        if status == 404:
            return "pokemon not found"
            
        else:
            return "error. status code: {}".format(status)
            
    return types_to_send
