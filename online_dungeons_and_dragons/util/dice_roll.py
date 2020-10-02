from random import randint

def validate_dice_roll(character, num_dice, dice_type, modifier):
    error = None
    if not character:
        error = 'Please enter a valid character name.'
    elif not num_dice or not num_dice.isdigit():
        error = 'Please enter a valid number of dice.'
    elif not dice_type or not dice_type.isdigit():
        error = 'Please enter a valid dice type.'
    elif not modifier or not modifier.lstrip('-').isdigit():
        error = 'Please enter a valid modifier.'

    return error

def generate_dice_roll_message(character, num_dice, dice_type, modifier):
    modifier_str = ''
    if modifier >= 0:
        modifier_str = '+{}'.format(modifier)
    else:
        modifier_str = '{}'.format(modifier)

    msg = '{} rolled {}d{}. Modifier: {}.'.format(character, num_dice, dice_type, modifier_str)
    
    rolls = roll_dice(num_dice, dice_type)
    total = sum(rolls)
    mod_total = total + modifier

    msg += ' Rolls: {}. Total: {}{} = {}.'.format(rolls, total, modifier_str, mod_total)

    return msg

def roll_dice(n, dice_type):
    rolls = []
    for roll in range(n):
        rolls.append(randint(1, dice_type))
    
    return rolls