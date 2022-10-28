#type compare
'''
compares types are returns strengths/weaknesses

strong - does 2x damage to ___
weak - does little damage to ___
invulnerable - does no damage to ___
vulnerable - takes 2x damage from ___

'''
#'type': {'strong': [], 'weak': [], 'invulnerable': ''}


def stats_get(types): #combine all stats together (if more than 1 type) and return aggregate dictionary

    pokemon_chart = {
    'normal': {'strong': [], 'weak': ['rock', 'steel'], 'invulnerable': ['ghost'], 'vulnerable': ['fight']},
    
    'fire': {'strong': ['grass', 'ice', 'bug', 'steel'], 'weak': ['fire','water','rock','dragon'], 'invulnerable': [], 'vulnerable': ['water','ground','rock']},
    
    'water': {'strong': ['fire', 'ground', 'rock'], 'weak': ['water','grass','dragon'], 'invulnerable': [], 'vulnerable': ['grass', 'electric']},
    
    'grass': {'strong': ['water','ground','rock'], 'weak': ['fire','grass','flying','bug','poison','bug','dragon','steel'], 'invulnerable': [], 'vulnerable': ['fire','ice','poison','flying','bug']},
    
    'electric': {'strong': ['water','flying'], 'weak': ['grass','electric','dragon'], 'invulnerable': ['ground'], 'vulnerable': ['ground']},
    
    'ice': {'strong': ['grass','ground','flying','dragon'], 'weak': ['fire','water','ice','steel'], 'invulnerable': [], 'vulnerable': ['fire','fighting','ice','steel']},
    
    'fighting': {'strong': ['normal','ice','rock','dark','steel'], 'weak': ['poison','flying','psychic','bug','fairy'], 'invulnerable': ['ghost'], 'vulnerable': ['flying','psychic','fairy']},
    
    'poison': {'strong': ['grass','fairy'], 'weak': ['poison','ground','rock','ghost'], 'invulnerable': ['steel'], 'vulnerable': ['ground','psychic']},
    
    'ground': {'strong': ['fire','electric','poison','rock','steel'], 'weak': ['grass','bug'], 'invulnerable': ['flying'], 'vulnerable': ['water','grass','ice']},
    
    'flying': {'strong': ['grass','fighting','bug'], 'weak': ['electric','rock','steel'], 'invulnerable': [], 'vulnerable': ['electric','ice','rock']},
    
    'psychic': {'strong': ['fighting','poison'], 'weak': ['psychic','steel'], 'invulnerable': ['dark'], 'vulnerable': ['bug','ghost','dark']},
    
    'bug': {'strong': ['grass','psychic','dark'], 'weak': ['fire','fighting','poison','flying','ghost','steel','fairy'], 'invulnerable': [], 'vulnerable': ['flying','rock','fire']},
    
    'rock': {'strong': ['fire','ice','flying','bug'], 'weak': ['fighting','ground','steel'], 'invulnerable': [], 'vulnerable': ['water','grass','fighting','ground','steel']},
    
    'ghost': {'strong': ['psychic','ghost'], 'weak': ['normal','dark'], 'invulnerable': ['normal'], 'vulnerable': ['ghost','dark']},
    
    'dragon': {'strong': ['dragon'], 'weak': ['steel'], 'invulnerable': ['fairy'], 'vulnerable': ['ice','dragon','fairy']},
    
    'dark': {'strong': ['psychic','ghost'], 'weak': ['fighting','dark','fairy'], 'invulnerable': [], 'vulnerable': ['ice','bug','fairy']},
    
    'steel': {'strong': ['ice','rock','fairy'], 'weak': ['fire','water','electric','steel'], 'invulnerable': [], 'vulnerable': ['fire','fighting','ground']},
    
    'fairy': {'strong': ['fighting','dragon','dark'], 'weak': ['fire','poison','steel'], 'invulnerable': [], 'vulnerable': ['poison','steel']}
    }

    agg = {'strong': [], 'weak': [], 'invulnerable': [], 'vulnerable': []}
    
    for ptypes in types:
        for cat in pokemon_chart[ptypes]:
            for stat in pokemon_chart[ptypes][cat]:
                agg[cat].append(stat)

    return(agg)



    
































