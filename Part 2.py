# Valid Table
'''
Write a function comp10001huxxy_valid_table() which takes a single argument:

groups, a list of lists of cards (each a 2-element string, where the first letter is the card value and the second letter is the card suit, e.g. '3H' for the 3 of Hearts), where each list of cards represents a single group on the table, and the combined list of lists represents the combined groups played to the table.
Your function should return a bool, which evaluates whether the table state is valid or not. Recall from the rules of the game that the table is valid if all groups are valid, where a group can take one of the following two forms:

an N-of-a-kind (i.e. three or more cards of the same value), noting that in the case of a 3-of-a-kind, each card must have a unique suit (e.g. ['2S', '2S', '2C'] is not a valid 3-of-a-kind, as the Two of Spades has been played twice), and if there are 4 or more cards, all suits must be present.

a run (i.e. a group of 3 or more cards, starting from the lowest-valued card, and ending with the highest-valued card, forming a continuous sequence in terms of value, and alternating in colour; note that the specific ordering of cards in the list is not significant, i.e. ['2C', '3D', '4S'] and ['4S', '2C', '3D'] both make up the same run.

Example function calls are as follows:
'''
'''
>>> comp10001huxxy_valid_table([])
True
>>> comp10001huxxy_valid_table([['AC']])
False
>>> comp10001huxxy_valid_table([['AC', '2S']])  # run too short
False
>>> comp10001huxxy_valid_table([['AC', '2S', '3H']]) # run doesn't alternate in colour
False
>>> comp10001huxxy_valid_table([['AC', '2S', '4H']]) # values not adjacent
False
>>> comp10001huxxy_valid_table([['AC', '2H', '3S']])
True
>>> comp10001huxxy_valid_table([['3C', 'AS', '2H']]) # test unsorted run
True
>>> comp10001huxxy_valid_table([['0C', 'JH', 'QS', 'KH', '9D']])
True
>>> comp10001huxxy_valid_table([['2C', '2H']]) # n-of-kind too short
False
>>> comp10001huxxy_valid_table([['2C', '2H', '2C']]) # same suit twice for 3-of-kind
False
>>> comp10001huxxy_valid_table([['2C', '2H', '2S', '2C']]) # same suit twice for 4-of-kind
False
>>> comp10001huxxy_valid_table([['2C', '2H', '2S']])
True
>>> comp10001huxxy_valid_table([['2C', '2H', '2S', '2D']])
True
>>> comp10001huxxy_valid_table([['2C', '2H', '2S', '2D', '2S']])
True
>>> comp10001huxxy_valid_table([['2C', '2H', '2S', '2D', '2S'], ['0D', '9C', '8H']])
True
'''
#Code
def n_of_a_kind(group, allowed_dupes=0):
    '''Takes in a list_iterator called groups and a value allowed_dupes which
    signify if duplicate cards are allowed. This function will go through 
    each of the cards in the list, and if all cards are the same type, with
    different suits then it will return True, otherwise it will return False
    '''
    # uni stores the previous suits we have seen 
    uni = []
    pre = None 
    all_cards = ['C', 'H', 'S', 'D']
    
    # constantly checks next item in iterable
    try:
        while True:
            nex = next(group)
            # checking if we have seen the suit before by adding suits to list
            if pre and nex[0] != pre[0]:
                return False
            if (nex[1] in uni):
                if allowed_dupes > 0:
                    allowed_dupes -= 1
                else:
                    return False
            uni.append(nex[1])
            
            # check if n of a kind of 4 or more in length has all suits
            if len(uni) >= 4:
                for elements in uni:
                    if elements in all_cards:
                        all_cards.pop(all_cards.index(elements))
            pre = nex
            
    # if next can't get next item from iterable it means it all passed.
    except StopIteration as e:
        if len(uni) > 3:
            if len(all_cards) < 1:
                pass
            else:
                return False
        else:
            pass
    return True


def consec(group):
    '''Takes in a list_iterator called group and tries to find consecutive
    cards in it by comparing the suit of the card, and checking for 
    alterations between suits, it returns True if it doesn't detect any
    consecutive cards are of different types, otherwise if a abnormality 
    is detected it returns False
    '''
    pre = next(group)
    try:
        # assigns the colors to a variable, and checks if they're repeats
        while True:
            nex = next(group)
            pre_color = pre[1] in ['C', 'S'] and 1 or 0
            nex_color = nex[1] in ['C', 'S'] and 1 or 0
            # checks for 2 of the same colors in a row 
            if pre_color == nex_color or pre[0] + 1 != nex[0]:
                return False
            pre = nex
    # stops when the whole thing has been checked 
    except StopIteration as e:
        pass
    return True


def comp10001huxxy_valid_table(groups):
    '''Accepts a list of lists of lists called groups, goes through each group
    and checks if groups is of valid length and also transforms each card
    into a list format [card value, suit] to run them through n_of_a_kind
    and consec, returns a true or false value at the end signifying if any
    group within groups is invalid. 
    '''
    min_run_length = 3
    
    # assigns the non numericals to their corresponding numbers
    assign = {
        'A': '1',
        '0': '10',
        'J': '11',
        'Q': '12',
        'K': '13'
    }
    
    # storage for split values
    converted = []
    
    # returns 0 if empty input
    if len(groups) == 0:
        return True
    
    for g, group in enumerate(groups):
        # test for too short
        if len(group) < min_run_length:
            return False
        
        # replaces numbers with numericals
        new_group = []
        for i, card in enumerate(group):
            value, suit = card[0], card[1]
            spl = [int(value in assign and assign[value] or value), suit]
            new_group.append(spl)
        # sorts them in order depending on first value 
        new_group = sorted(new_group, key=lambda c: c[0])
        converted.append(new_group)
    
    # stores results from each group check
    results = []
    for group in converted:
        #  checks if it is a valid n of a kind or row
        if n_of_a_kind(iter(group), len(group) - 4) or consec(iter(group)):
            results.append(True)
            break
        results.append(False)
           
    # returns the overall result, from all the tests for all existing groups
    return all(results)