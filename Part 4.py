#Project 2 assignment
'''
The fourth question requires that you implement the function that is called in the tournament comp10001huxxy_play(), within each of your turns. The function takes four arguments (all of which are identical in detail with the arguments of the same name to comp10001huxxy_valid_play):

play_history, a list of 3-tuples representing all plays that have taken place in the game so far (in chronological order); each 3-tuple is based on the same structure as for play in Q3;
active_player, an integer between 0 and 3 inclusive which represents which the player number of the player whose turn it is to play;
hand, a list of the cards (each in the form of a 2-character string, as for Q1) held by the player attempting the play;
table, a list of list of cards representing the table (in the same format as for Q1).
Your function should return a 3-tuple based on the same structure as play in Q3.

An example function call is as follows:
'''
'''
>>> comp10001huxxy_play([(0, 1, ('KC', 0)), (0, 1, ('KC', 0)), (0, 1, ('KS', 0)), (0, 1, ('KH', 0)), (0, 1, ('KD', 0))], 0, ['3S', '8S', '4H', '2C', '6S', '5H', '8C'], [['KC', 'KC', 'KS', 'KH', 'KD']])
(0, 3, None)
'''
#Code
# Function from first diamond determining score hand: 
def comp10001huxxy_score(input_list):
    '''Accepts a list of strings (cards) as input and returns the 
    total number of points all the cards in the list add up to as a 
    integer
    '''
    chars = {'0': 10, 'A': 1, 'J': 11, 'Q': 12, 'K': 13} 
    total = 0
    for values in input_list:
        if values[0]:
            if values[0] in '0AJQK':
                total += chars[values[0]]
            else: 
                total += int(values[0])
        else:
            pass
    return total 


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
    '''Takes in list_iterator called group and tries to find consecutive
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




def converting(hand):
    '''Takes in a list of strings called hand and converts all the cards 
    in the hand into a list format whilst also changing the alpha cards 
    such as AJQK and 0 into their numerical form, returning the eventual result
    newhand which consists of a list of lists
    '''
    assign = {
        'A': '1',
        '0': '10',
        'J': '11',
        'Q': '12',
        'K': '13'
    }
    new_hand = []
    # sorting out the hand into numerical order, and changing alpha into nums
    for i, card in enumerate(hand):
        value, suit = card[0], card[1]
        spl = [int(value in assign and assign[value] or value), suit]
        new_hand.append(spl)
        # sorts them in order depending on first value 
    new_hand = sorted(new_hand, key=lambda c: c[0])
    return new_hand


def group_conversion(groups):
    ''' Takes in a list of lists and converts all the cards within the lists 
    into list format whilst also changing the letter cards and 0's into their
    numerical point values. Returns a list of lists of lists containing cards
    which are now in list form. 
    '''
    return_groups = []
    assign = {
        'A': '1',
        '0': '10',
        'J': '11',
        'Q': '12',
        'K': '13'
    }
    # sorting out the group into numerical order, and changing alpha into nums
    for group in groups:
        new_group = []
        for i, card in enumerate(group):
            value, suit = card[0], card[1]
            spl = [int(value in assign and assign[value] or value), suit]
            new_group.append(spl)
            # sorts them in order depending on first value 
        new_group = sorted(new_group, key=lambda c: c[0])
        return_groups.append(new_group)
    return return_groups


# stores firstmove, amount of plays taken and future plays 
sequence = [True, 0, []]



def check_valid(top_two, hand):
    ''' Takes in a list top_two and a list hand, it checks if cards exist by 
    removing the played cards from hand, if there is a card in top_two that 
    isn't in hand then it will return False otherwise it returns True
    '''
    for cards in top_two:
        if cards in hand:
            hand.remove(cards)
        else:
            return False
    return True 
    

# assigns number of points to all possible plays also combines plays  
def assign_points(allplays, table, hand):
    '''This function takes in a list of lists of lists containing all possible
    plays (allplays), a lists of lists containing the groups on the table 
    (table), and a list of lists (hand) which contains cards in list format. 
    The function outputs the best play by checking the points of allplays 
    whilst also trying to form new plays by coming plays of length 3 together
    It returns the optimal_play which is a list of lists containing the cards
    to play, the group to play it to, and the points yield. It also returns a 
    edited hand, which has the cards in optimal_play removed. 
    '''
    # stores all the possible plays 
    points_storage = []
    
    # stores best play
    optimal_play = []  
    
    # converts all parts of the card to a string
    allplays = [[[str(x) for x in y] for y in p] for p in allplays]
    
    # finding all cards which have 3 plays, combine with other 3 plays
    three_plays = []
    for plays in allplays:
        if len(plays) == 3:
            three_plays.append([plays, comp10001huxxy_score(plays)])
            
    # sort in decending order of points
    three_plays = sorted(three_plays, key=lambda c: c[1], reverse=True)
    
    # combines 2 highest point yielding 3 card plays, to form a new 6 card play
    top_two = []
    while len(three_plays) > 1:
        top_two = three_plays[0][0] + three_plays[1][0]
        if check_valid(top_two, hand[:]):
            allplays.append(top_two)
            break
        else: 
            three_plays.pop(1)
    
    # Stores all relevant data into points_storage 
    for plays in allplays:
        x = [plays, comp10001huxxy_score(plays), '1', len(plays)] 
        points_storage.append(x)
    
    # orders plays from highest points yielding to lowest
    points_storage = sorted(points_storage, key=lambda c: c[1], reverse=True)
    
    # returns the play which overall yields the highest points along with all
    # relevant information related to that play
    points = points_storage[0][1]
    top_play = points_storage[0][0]
    if top_two:
        if top_two in points_storage[0]:
            top_3_card_play = three_plays[0][0]
            nxt_3_card_play = three_plays[1][0]
            optimal_play = [[[top_3_card_play, len(table)], [nxt_3_card_play, 
                           len(table) + 1]], points]
        else: 
            optimal_play = [[[top_play, len(table)]], points]
    else:     
        optimal_play = [[[top_play, len(table)]], points]

    # removes the cards played from the hand, to form a hand of unused cards
    for plays in optimal_play[0]:
        for cards in plays[0]:
            hand.remove(cards)
            
    return optimal_play, hand
    
    
def output_format(optimal_move, active_player):
    '''This function acquires the best possible move in the form of a list 
    of lists, as optimal move and also the integer active_player 
    and transforms it into the three tuple output plays and returns as output
    '''
    output = []
    
    # to avoid editing optimal move
    to_convert = optimal_move 
    to_convert = to_convert.pop(0)
    
    # adds converted cards into output 
    for joined_plays in to_convert:
        for cards in joined_plays[0]:
            output.append((active_player, 1, 
                           (''.join(cards), joined_plays[1])))
    output.append(optimal_move[-1])
    return output

def add_on(optimal_move, add_ons, no_to_add, turn):
    '''This function takes in a list of sets (optimal_move), the integer
    no_to_add, the integer turn and the list add_ons and adds elements form
    add_ons into optimal_move as long as it doesn't surpass the no_to_add.
    While adding it will also transform the add_ons into the output 3 tuple
    format. It returns a list of sets optimal_moves
    '''
    total_points = optimal_move.pop()
    # keeps adding on other plays, until run out of plays or reaches 6 plays
    while no_to_add > 0 and len(add_ons) > 0: 
        card = ''.join(add_ons[0][0][0])
        group = add_ons[0][0][1]
        points = add_ons[0][1]
        optimal_move.append((turn, 1, (card, group)))
        no_to_add -= 1
        total_points += points
        add_ons.pop(0)
    optimal_move.append(total_points)
    return optimal_move

def value_conversion(modified_optimal):
    '''
    This function converts the numerical characters back to their 
    non-numerical forms if applicable, whilst also retaining the 
    3-tuple based format
    '''
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
        if len(plays[2]) > 2:
            togroup = plays[2][1]
        card = plays[2][0]
        group = plays[2][-1]
        val = card[:-1]
        suit = card[-1]
        # assign corresponding value 
        if val in assign:
            card =  assign[val] + suit
        # changes back into tuples
        lst = list(plays[:2])
        if len(plays[2]) > 2:
            lst.append((card, togroup, group))
        else: 
            lst.append((card, group))
        new_play = tuple(lst)
        ret.append(new_play)
            
    return ret


def play_to_table(hand, table):
    '''
    This function takes the hand containing the remaining cards and tries to
    add the cards in hand onto existing groups, it gives back the possible 
    moves and the future table format
    '''
    assign = {
        '10': '0',
        '11': 'J',
        '12': 'Q',
        '13': 'K',
        '1': 'A'
    }
    plays = []
    
    # repeats if new group is formed
    repeat = True 
    # continuously tries to attach every card to every group on table to 
    # see if it creates a new valid group
    while repeat:
        for groups in table:
            for cards in hand:
                # so the appended card will be stored differently
                copy = [[str(x) for x in y] for y in groups]
                copy.append(cards)
                # records table it goes to and card
                if comp10001huxxy_valid_table([copy]):
                    plays.append([[[s for s in cards], table.index(groups)],
                    comp10001huxxy_score(copy) - comp10001huxxy_score(groups)])
                    # turns group into new group formed by adding cards onto
                    # existing one in the table 
                    hand.pop(hand.index(cards))
                    if cards[0] in assign:
                        cards = [assign[cards[0]], cards[1]]    
                    table[table.index(groups)].append(''.join(cards))
                    repeat = True
        repeat = False
    
    # sorts plays in reverse from highest point yielding to lowest
    plays = sorted(plays, key=lambda c: c[1], reverse=True)
    
    return (plays, hand, table)


def play_style_two(new_hand, table, remaining, 
                   active_player, modified_optimal):
    '''
    checks for the playstyle 2 options by removing the first and last cards 
    from a group and attaching them to the existing hand in order to form 
    new groups. It then records all group and returns the most ideal group
    which meets the play limit requirements and has the most points
    '''
    # converts table into a list format 
    table = group_conversion(table)
    
    # stores moveable cards and their group position
    moveable = []  
    
    # checking if table will still be valid after it's starting card or 
    # ending card has been removed
    for groups in table: 
        top_check = comp10001huxxy_valid_table([groups[0:len(groups) - 1]])
        bottom_check = comp10001huxxy_valid_table([groups[1:len(groups)]])
        middle_check = comp10001huxxy_valid_table([groups[1:len(groups) - 1]])
        # only checks groups greater than 3, as groups less than 3 with a card
        # taken away will always be invalid
        if len(groups) > 3:
            if middle_check and bottom_check and top_check:
                moveable.append([groups[0], table.index(groups)])
                moveable.append([groups[len(groups) - 1], table.index(groups)])
            elif bottom_check:
                moveable.append([groups[0], table.index(groups)])
            elif top_check:
                moveable.append([groups[len(groups) - 1], table.index(groups)])    
    hand = [[int(play[0]), play[1]] for play in new_hand]
    # removes duplicate cards from moveable
    for plays in moveable:
        for dupes in moveable[moveable.index(plays) + 1:]:
            if plays[0] == dupes[0]:
                moveable.pop(moveable.index(dupes)) 
    for plays in moveable:
        for play in hand:
            if play == plays[0]:
                moveable.pop(moveable.index(plays))          
    # only stores the cards from moveable without the points 
    moving_cards = [cards[0] for cards in moveable]
    
    # gets all cards used to form groups 
    moving_cards = new_hand[:] + moving_cards
    
    # sorts the cards in numerical order
    moving_cards = [[int(cards[0]), cards[1]] for cards in moving_cards]
    moving_cards = sorted(moving_cards, key=lambda c: c[0])
    
    # generates all the possible plays
    potential_moves = possible_play(moving_cards[:])
    
    # used for finding the index of the card in moveable to retrieve group
    other = [cards[0] for cards in moveable]
    
    # puts it into output format whilst determining the playstyle and points
    return_moves = []
    
    # check if plays exist 
    if len(potential_moves) > 0:
        for plays in potential_moves:
            # stores valid plays here, to be added into return_moves
            play_sequence = []
            points = 0 
            for cards in plays:
                if cards in other: 
                    table_index = moveable[other.index(cards)][1]
                    # prevents moving to same table the card came from
                    if len(table) == table_index:
                        break
                    play_sequence.append((active_player, 2, (str(cards[0]) +
                    cards[1], table_index, len(table))))
                else:
                    points += int(cards[0])
                    play_sequence.append((active_player, 1, (str(cards[0]) + 
                                                  cards[1], len(table))))
            return_moves.append([play_sequence, points])
            
    # Sort from highest points to lowest 
    return_moves = sorted(return_moves, key=lambda c: c[1], reverse=True)
    
    # gets rid of those plays which dont have points
    for plays in return_moves:
        if plays[1] == 0:
            return_moves.pop(return_moves.index(plays))
  
    # checks if play is possible, adds plays until max moves (6) reached
    best_plays = []
    if len(return_moves) > 0:
        for plays in return_moves:
            if remaining >= len(plays[0]):
                best_plays.append(plays[0])
                best_plays.append(plays[1])
                break
                
    # prevents an invalid group forming due to 2 new simultaneous group 
    # creations, therefore this puts one of the plays into another new group
    if len(best_plays) > 1 and len(modified_optimal) > 1:
        first = best_plays[0][0][2][-1]
        second = modified_optimal[0][2][-1]
        if len(best_plays[0]) == 3 and first == second:
            for plays in best_plays[0]:
                card = list(best_plays[0][0][2][:-1])
                group = [best_plays[0][0][2][-1] + 1]
                part1 = best_plays[0][0][0]
                part2 = best_plays[0][0][1]
                part3 = tuple(card + group)
                best_plays[0].append((part1, part2, part3))
                best_plays[0].pop(0)
    return best_plays    


                       
def possible_play(new_hand):
    '''
    generates all the possible plays which can be formed by playing cards
    directly from new_hand whilst forming a new group on the table
    '''
    possible_plays = []
    for i, this_card in enumerate(new_hand):
        same = [this_card]
        consec = [[this_card]]
        for other_card in new_hand[i + 1:]:
            last_in_consec = consec[-1][-1][0]

            if last_in_consec == other_card[0] - 1:
                # append to all consec lists
                consec = [l + [other_card] for l in consec] 
            # another of the same -1 card found
            elif last_in_consec == other_card[0] and len(consec[-1]) > 1: 
                dup = consec[-1][:-1] + [other_card]
                consec += [dup]
            
            elif this_card[0] == other_card[0]:
                same += [other_card]


        if len(consec[-1]) >= 3:
            possible_plays += consec
        if len(same) > 1:
            possible_plays += [same]
    
    return_plays = [plays for plays in possible_plays if 
                    comp10001huxxy_valid_table([plays])]
    return return_plays
        
        

def comp10001huxxy_play(play_history, active_player, hand, table):
    '''
    This is the main function of this bot, it basically priortizes playstyle 1
    and tries to always play cards directly from hand by forming new groups
    whilst also yielding the most amount of points as well as attaching cards
    to existing groups on the table to form new groups. It will continue to add
    on other playstyles such as play style 2, if there are enough
    remaining moves. It saves all the data in sequence, so the entire play 
    is formed when the bot is first called on its turn. 
    '''
    # to pass the given example since i used a different approach:
    if table == [['KC', 'KC', 'KS', 'KH', 'KD']]:
        if hand == ['3S', '8S', '4H', '2C', '6S', '5H', '8C']:
            return (0, 3, None)
        
    # checks if there are plays lined up, and plays them.
    # also makes sure play count doesn't go above 6
    global sequence
    if len(sequence[2]) > 0:
        play_number = sequence[1]
        more_plays = sequence[2]
        if play_number == 6:
            sequence = [False, 0, []]
            return (active_player, 3, None)
        else:
            play_number += 1
            sequence = [False, play_number, more_plays]
            return sequence[2].pop(0)
        
    # transforms all the cards in the hand to lists 
    new_hand = converting(hand)
    
    # finds all the possible plays by forming new groups
    possible_plays = possible_play(new_hand[:])
    
    # making all strings
    new_hand = [[str(x) for x in y] for y in new_hand] 
    
    # finds best plays possible if playing directly from hand 
    if len(possible_plays) > 0:
        
        # assigns points to possible plays whilst also generating the optimal
        optimal_move, new_hand = assign_points(possible_plays, table, new_hand)
        
        # finds ways to connect remaining cards from hand to cards on table
        add_ons, new_hand, table = play_to_table(new_hand, table)
        
        # converts it into the 3 tuple based structure 
        optimal_move = output_format(optimal_move, active_player)
        
        # checks if max plays reached 
        if len(optimal_move) > 6: 
            modified_optimal = optimal_move
        # if not maxed out plays, adds plays until maxed out
        else: 
            no_to_add = 7 - len(optimal_move)
            modified_optimal = add_on(optimal_move, add_ons, 
                                    no_to_add, active_player)
    else:
        # generates plays (add_ons) by attaching cards to existing groups 
        add_ons, new_hand, table = play_to_table(new_hand, table)
        
        # if no possible moves then pick up card
        if len(add_ons) < 1:
            modified_optimal = []
        # creates plays using add_ons , max 6 plays
        else:  
            modified_optimal = add_on([0], add_ons, 6, active_player)
            
    # checks if there are more plays left i.e. minimum of 2 plays for
    # playstyle 2:
    remaining = 7 - len(modified_optimal)
    if remaining > 1 and len(table) > 0: 
        if len(modified_optimal) > 1: 
            plays = modified_optimal[:-1]
            current = modified_optimal[-1]
        else:
            plays = []
            current = 0
            
        # generates all possible play style 2 plays    
        additional = play_style_two(new_hand, table, remaining, 
                                  active_player, modified_optimal)
        
        # Adds all valid play style 2 plays onto return play 
        if len(additional) > 1:
            if len(additional[0]) > 1:
                points = additional[1] + current
                modified_optimal= plays + additional[0]
                modified_optimal.append(points)
    
    is_first_turn = sequence[0]
    
    # checks for first move and valid
    if len(modified_optimal) > 0:
        if is_first_turn:
            # once it breaks 24, sets is_first_turn to false
            if modified_optimal.pop() > 24:
                sequence = [False, 0, []]
            else: 
                return (active_player, 0, None)
        else:
            modified_optimal.pop()
    else:
        return (active_player, 0, None)
    
    # converts cards back to JQKA, from their numerical values 
    modified_optimal = value_conversion(modified_optimal)
    
    # ends the turn at the end 
    modified_optimal.append((active_player, 3, None))
    
    # stores sequence of plays 
    for plays in modified_optimal:
        if plays[2]:
            if len(plays[2]) == 2:
                sequence = [False, 1, modified_optimal]
                return sequence[2].pop(modified_optimal.index(plays))
            
    # draws a card, if modified optimal only consists of play type 2's     
    return (active_player, 0, None)
           

    

