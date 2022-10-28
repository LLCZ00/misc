from ppc_typeCompare import stats_get
from ppc_typeGet import type_get

def info_get(name):
    pokemon_type = type_get(name)
    
    if pokemon_type != 0:
        stats = stats_get(pokemon_type)
        return [name, stats, pokemon_type]
    

    return 0
