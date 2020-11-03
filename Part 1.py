#Score Hand
'''
Write a function comp10001huxxy_score() which takes a single argument:

cards, a list of cards held by a player, each in the format of a 2-letter string
Your function should return a non-negative integer indicating the score for the combined cards, based on the value of each card ('A' = 1, '2' = 2, ..., 'K' = 13).

Example function calls are as follows:
'''
'''
>>> comp10001huxxy_score([])
0
>>> comp10001huxxy_score(['AC'])
1
>>> comp10001huxxy_score(['4C', '2H', 'KS'])
19
'''
#Code
def comp10001huxxy_score(input_list):
    '''Accepts a list of strings (cards) as input and returns the 
    total number of points all the cards in the list add up to as a 
    integer
    '''
    chars = {'0': 10, 'A': 1, 'J': 11, 'Q': 12, 'K': 13} 
    total = 0
    for values in input_list:
        # checks if the card exists 
        if values[0]:
            # checks if card doesn't properly represent its points value 
            if values[0] in '0AJQK':
                total += chars[values[0]]
            else: 
                total += int(values[0])
        else:
            pass
    return total 