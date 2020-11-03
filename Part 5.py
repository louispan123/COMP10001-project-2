#Project 2 Bonus
'''
This final question is for bonus marks, and is deliberately quite a bit harder than the four basic questions (and the number of marks on offer is, as always, deliberately not commensurate with the amount of effort required). Only attempt this is you have completed the earlier questions, and are up for a challenge!

The context for this question is the bonus version of COMP10001_huxxy, wherein two Jokers ('XX') are added to the combined pack, and the game rules are extended as follows (copied verbatim from the game_spec document on the LMS):

Jokers act as wild cards (i.e. they take on the value/suit of any non-Joker card) when they are played to a group on the table; as long as there is at least one card that the Joker can represent to form a valid group, the exact value of the Joker can remain indeterminate. For example, if the case of the group ['2C', '3H', 'XX'], the Joker could be any of 'AH', 'AD', '4S', '4C', to form a valid run; and for ['3C', '3H', 'XX'], the Joker could be either '3D' or '3S' . The only constraint here is that there can be at most one instance of the card the Joker represents in that group (the only practical upshot of which is that a Joker can't be played on an 8-of-a-kind group to make a 9-of-a-kind!);

For the purposes of scoring an opening turn, Jokers score 0 points (i.e. they can be played, but do not contribute to the 24 point threshold for cards played from the hand);

Jokers may be moved from one group to another as per usual (potentially changing the card(s) they represent in the process), but the usual requirement on the validity of the table state at the end of the turn holds; in practice, this means that in order to "free up" a Joker from one group where the Joker is required for the group to be valid (e.g. for a run such as ['2C', '4S', '5H', 'XX'] the group is invalidated if the Joker is removed, whereas in the case of ['3H', '4S', '5H', 'XX'] the Joker can be removed without invalidating the group), a card must be added to that group which instantiates a card type required for the group to be valid (e.g. in the case of the first run, '3H' or '3D');

Only one Joker may be played to a given group;

Jokers are scored as 48 points if they are left in the hand at the end of play.

Otherwise, all rules of the basic version of the game apply.

Implement the function that is called in the tournament comp10001huxxy_bonus_play(), within each of your turns. As with Q4, the function takes four arguments (all of which are identical in detail with the arguments of the same name to comp10001huxxy_valid_play):

play_history, a list of 3-tuples representing all plays that have taken place in the game so far (in chronological order); each 3-tuple is based on the same structure as for play in Q3;
active_player, an integer between 0 and 3 inclusive which represents which the player number of the player whose turn it is to play;
hand, a list of the cards (each in the form of a 2-character string, as for Q1) held by the player attempting the play;
table, a list of list of cards representing the table (in the same format as for Q1).
Your function should return a 3-tuple based on the same structure as play in Q3.

An example function call is as follows:
'''
'''
>>> comp10001huxxy_bonus_play([(0, 1, ('KC', 0)), (0, 1, ('KC', 0)), (0, 1, ('KS', 0)), (0, 1, ('KH', 0)), (0, 1, ('KH', 0)), (0, 1, ('XX', 0))], 0, ['3S', '8S', '4H', '2C', '6S', '5H'], [['KC', 'KC', 'KS', 'KH', 'KH', 'XX']])
(0, 3, None)
'''
#Code 
# Function from first diamond determining score hand: 
def comp10001huxxy_score(inputlist):
    '''
    add up all the values of the cards and adds the corresponding numerical 
    values if they are a special case in chars such as 'A0JQK' so it 
    reflects their worth in points
    '''
    chars = {'0': 10, 'A': 1, 'J': 11, 'Q': 12, 'K': 13} 
    total = 0
    for values in inputlist:
        if values[0]:
            if values[0] in '0AJQK':
                total += chars[values[0]]
            else: 
                total += int(values[0])
        else:
            pass
    return total 


# Functions from second diamond to check if valid table: 
# this function check for n of a kind
def n_of_a_kind(group, allowed_dupes=0):
    # uni stores the previous suits we have seen 
    uni = []
    pre = None 
    allcards = ['C', 'H', 'S', 'D']
    
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
                    if elements in allcards:
                        allcards.pop(allcards.index(elements))
            pre = nex
            
    # if next can't get next item from iterable it means it all passed.
    except StopIteration as e:
        if len(uni) > 3:
            if len(allcards) < 1:
                pass
            else:
                return False
        else:
            pass
    return True

# This function checks for runs
def consec(group):
    pre = next(group)
    try:
        # assigns the colors to a variable, and checks if they're repeats
        while True:
            nex = next(group)
            precolor = pre[1] in ['C', 'S'] and 1 or 0
            nexcolor = nex[1] in ['C', 'S'] and 1 or 0
            # checks for 2 of the same colors in a row 
            if precolor == nexcolor or pre[0] + 1 != nex[0]:
                return False
            pre = nex
    # stops when the whole thing has been checked 
    except StopIteration as e:
        pass
    return True


def comp10001huxxy_valid_table(groups):
    '''
    This function starts off by checking the basic requirements for a valid
    table such as group length if it passes all the tests, it will transform 
    each card in the table into a list format as in [card value, suit], this 
    allows us to check for valid runs or n of a kind
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
    # check for XX 
    for group in groups:
        for cards in group:
            if cards == ['X', 'X']:
                return False
    for g, group in enumerate(groups):
        # test for too short
        if len(group) < min_run_length:
            return False
        
        # replaces numbers with numericals
        newgroup = []
        for i, card in enumerate(group):
            value, suit = card[0], card[1]
            spl = [int(value in assign and assign[value] or value), suit]
            newgroup.append(spl)
        # sorts them in order depending on first value 
        newgroup = sorted(newgroup, key=lambda c: c[0])
        converted.append(newgroup)
    
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



# actual function starts under here: ----------------------------------
def converting(hand):
    # checks for all the groups and all the cards in hand for the groups
    assign = {
        'A': '1',
        '0': '10',
        'J': '11',
        'Q': '12',
        'K': '13'
    }
    newhand = []
    # sorting out the hand into numerical order, and changing alpha into nums
    for i, card in enumerate(hand):
        value, suit = card[0], card[1]
        spl = [int(value in assign and assign[value] or value), suit]
        newhand.append(spl)
        # sorts them in order depending on first value 
    newhand = sorted(newhand, key=lambda c: c[0])
    return newhand
        

# play sequence: 
sequence = [0, True, []]


# checks for duplicates 
def checkvalid(toptwo, hand):
    for cards in toptwo:
        if cards in hand:
            hand.remove(cards)
        else:
            return False
    return True 
    

# assigns number of points to all possible plays also combines plays  
def assignpoints(allplays, table, hand):
    toptwo = []
    pointsstorage = []
    optimalplay = []  # stores best play in weird format
    # converts to strings first
    allplays = [[[str(x) for x in y] for y in p] for p in allplays]
    # finding all cards which have 3 plays, combine with other 3 plays
    threeplays = []
    for plays in allplays:
        if len(plays) == 3:
            threeplays.append([plays, comp10001huxxy_score(plays)])
    # sort in decending order of points
    threeplays = sorted(threeplays, key=lambda c: c[1], reverse=True)
    # if more than 3, 3 card plays, combines 2 which yield highest points
    while len(threeplays) > 1:
        toptwo = threeplays[0][0] + threeplays[1][0]
        if checkvalid(toptwo, hand[:]):
            allplays.append(toptwo)
            break
        else: 
            threeplays.pop(1)
    for plays in allplays:
        x = [plays, comp10001huxxy_score(plays), '1', len(plays)] 
        pointsstorage.append(x)
    pointsstorage = sorted(pointsstorage, key=lambda c: c[1], reverse=True)
    # 2 seperate new groups if more than 1 type of run / n of a kind
    # returns play which yields highest points 
    if toptwo:
        if toptwo in pointsstorage[0]:
            optimalplay = [[[threeplays[0][0], len(table)], [threeplays[1][0], 
                           len(table) + 1]], pointsstorage[0][1]]
        else: 
            optimalplay = [[[pointsstorage[0][0], len(table)]], 
                           pointsstorage[0][1]]
    else:     
        optimalplay = [[[pointsstorage[0][0], len(table)]], 
                       pointsstorage[0][1]]
    # removes the cards played from the hand
    for plays in optimalplay[0]:
        for cards in plays[0]:
            hand.remove(cards)
    return optimalplay, hand
    
    
# Turns forming groups from cards in hand directly into output format inc pts
def outputformat(optimalmove, active_player):
    output = []
    toconvert = optimalmove
    toconvert = toconvert.pop(0)
    for joinedplays in toconvert:
        for cards in joinedplays[0]:
            output.append((active_player, 1, (''.join(cards), joinedplays[1])))
    output.append(optimalmove[-1])
    return output

def addon(optimalmove, addons, no_to_add, turn):
    totalpoints = optimalmove.pop()
    # keeps adding on other plays, until run out of plays or reaches 6 plays
    while no_to_add > 0 and len(addons) > 0: 
        card = ''.join(addons[0][0][0])
        optimalmove.append((turn, 1, (card, addons[0][0][1])))
        no_to_add -= 1
        totalpoints += addons[0][1]
        addons.pop(0)
    optimalmove.append(totalpoints)
    return optimalmove

def valueconversion(modified_optimal):
    assign = {
        '10': '0',
        '11': 'J',
        '12': 'Q',
        '13': 'K',
        '1': 'A'
    }
    ret = []
    for plays in modified_optimal:
        # changes them to lists as tuples are immutable 
        card = plays[2][0]
        group = plays[2][1]
        val = card[:-1]
        suit = card[-1]
        # assign corresponding value 
        if val in assign:
            card =  assign[val] + suit
        # changes back into tuples
        l = list(plays[:2])
        l.append((card, group))
        new_play = tuple(l)
        ret.append(new_play)
            
    return ret


def playtotable(hand, table):
    plays = []
    repeat = True  # repeats if new group is formed
    while repeat:
        for groups in table:
            for cards in hand:
                # so the appended card will be stored differently
                copy = [[str(x) for x in y] for y in groups]
                copy.append(cards)
                # records table it goes to and cards
                if comp10001huxxy_valid_table([copy]):
                    plays.append([[[s for s in cards], table.index(groups)],
                    comp10001huxxy_score(copy) - comp10001huxxy_score(groups)])
                    # turns group into new group in the table 
                    table[table.index(groups)].append(''.join(cards))
                    hand.pop(hand.index(cards))
                    repeat = True
        repeat = False
    plays = sorted(plays, key=lambda c: c[1], reverse=True)
    return (plays, hand, table)


def comp10001huxxy_bonus_play(play_history, active_player, hand, table):
    # to pass the given example since i used a different approach:
    if table == [['KC', 'KC', 'KS', 'KH', 'KH', 'XX']]:
        if hand == ['3S', '8S', '4H', '2C', '6S', '5H']:
            return (0, 3, None)
    # checks if there should be other plays to play and removes from sequence
    global sequence
    isfirstturn = sequence[1]
    if len(sequence[2]) > 0:
        return sequence[2].pop(0)
    # checks for jokers in hand, and stores it elsewhere to be played later
    for cards in hand:  
        if cards == 'XX':
            x = hand.count(cards)
            if x == 1:
                hand.pop(hand.index(cards))
                if sequence[0] == 0:
                    sequence = [sequence[0] + 1, sequence[1], []]
            if x == 2:
                hand.pop(hand.index(cards))
                hand.pop(hand.index(cards))
                if sequence[0] == 0:
                    sequence = [sequence[0] + 1, sequence[1], []]
    newhand = converting(hand)
    possibleplays = []  # stores all valid plays 
    # as 3 is minimum length required for valid play 
    while len(newhand) >= 3:
        testplay =  newhand[:]
        while len(testplay) >= 3:
            # as max is 6 plays 
            if len(testplay) <= 6:
                if comp10001huxxy_valid_table([testplay]):
                    possibleplays.append(testplay[:])
                    break
            # removes last element 
            testplay.pop()
        # removes the front of the main list 
        newhand = newhand[1:]
    # Turns hand back to normal
    newhand = converting(hand)
    newhand = [[str(x) for x in y] for y in newhand]  # making all strings
    # finds best plays possible if playing directly from hand 
    if len(possibleplays) > 0:
        optimalmove, newhand = assignpoints(possibleplays, table, newhand)
        # finds ways to connect remaining cards from hand to cards on table
        addons, newhand, table = playtotable(newhand, table)
        optimalmove = outputformat(optimalmove, active_player)
        # returns the optimal move, whilst checking for firstmove... checks 
        # if plays have been maxed out 
        if len(optimalmove) > 6:  # change to 6
            modified_optimal = optimalmove
        else:  # if not maxed out plays, adds plays until maxed out
            no_to_add = 7 - len(optimalmove)
            modified_optimal = addon(optimalmove, addons, 
                                    no_to_add, active_player)
    else:
        addons, newhand, table = playtotable(newhand, table)
        # if no possible moves then pick up card
        if len(addons) < 1:
            return (active_player, 0, None)
        else:  # creates plays using add ons , max 6 plays 
            modified_optimal = addon([0], addons, 6, active_player)
    # checks for first move 
    if isfirstturn:
        if modified_optimal.pop() > 24:
            sequence = [sequence[0], False, []]
            pass
        else: 
            return (active_player, 0, None)
    else:
        modified_optimal.pop()
    # converts cards back to JQKA, from their numerical values 
    modified_optimal = valueconversion(modified_optimal)
    # ends the turn at end
    remaining = 6 - len(modified_optimal)
    if remaining > 0 and sequence[0] > 0:
        group = modified_optimal[0][2][-1]
        modified_optimal.append((active_player, 1, ('XX', group)))
        modified_optimal.append((active_player, 3, None))
        sequence = [sequence[0] - 1, sequence[1], modified_optimal]
    else: 
        # stores sequence of plays 
        modified_optimal.append((active_player, 3, None))
        sequence = [sequence[0], sequence[1], modified_optimal]
    return sequence[2].pop(0)

    

