#main for the Pokemon Power Checker
'''
Calls from typeCompare and typeGet, prints pokemon:
name
type
strengths
weaknesses
invulnerabilities
vulnerabiliteis
'''
from ppc_typeGet import type_get
from ppc_typeCompare import stats_get

def print_format(name, p_stats, p_types): #prints stats n such in a pretty way
    print("Name: {}".format(name))
    print("Type(s): {}\n".format(', '.join(p_types)))
    
    print("Does x2 damage to: ")
    if len(p_stats['strong']) == 0:
        print("None\n")
    else:
        for s in p_stats['strong']:
            print(s)
        print()
        
    print("Does little damage to: ")
    for s in p_stats['weak']:
        print(s)
    print()
        
    print("Does no damage to: ")
    if len(p_stats['invulnerable']) == 0:
        print("None\n")
    else:
        for s in p_stats['invulnerable']:
            print(s)
        print()
        
    print("Takes 2x damage from: ")
    for s in p_stats['vulnerable']:
        print(s)
    print()

    input()
        


if __name__ == '__main__':
    while True:
        pokemon_name = input("Enter Pokemon Name: ")

        pokemon_type = type_get(pokemon_name)

        if type(pokemon_type == list):
            stats = stats_get(pokemon_type)

            print_format(pokemon_name, stats, pokemon_type)
            continue

        else:
            print(pokemon_type)
            continue
