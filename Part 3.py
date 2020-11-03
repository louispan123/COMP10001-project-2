#Valid Play
'''
Write a function comp10001huxxy_valid_play() which takes five arguments:

play, a 3-tuple representing the play that is being attempted; see below for details;
play_history, a list of 3-tuples representing all plays that have taken place in the game so far (in chronological order); each 3-tuple is based on the same structure as for play;
active_player, an integer between 0 and 3 inclusive which represents the player number of the player whose turn it is to play;
hand, a list of the cards (each in the form of a 2-character string, as for Q1) held by the player attempting the play;
table, a list of list of cards representing the table (in the same format as for Q2).
Your function should return a Boolean indicating whether the play is valid or not given the current game state (i.e. the combination of the plays made to date, the content of the player's hand, and the groups on the table). In this, you only need to validate the state of the table (using comp10001huxxy_valid_table from Q2, which you are provided with a reference implementation of) if the play ends the player's turn and they have played to the table. Note that play_history, hand, and table all represent the respective states prior to the proposed play being made (e.g. play_history will not contain play).

The composition of the 3-tuple used to represent each play is (player_turn, play_type, play_details), where player_turn is an integer (between 0 and 3 inclusive) indicating which player is attempting to play, and play_type and play_details are structured as follows, based on the play type:

pick up a card from stock (and thereby end the turn): play_type = 0, play_details = None;
play a card from the hand to the table: play_type = 1, play_details = (card, to_group) where card is the card from the hand that is to be played, and to_group is the (zero-offset) index of group in table to play to; in the instance that the card is to start a new group, to_group should be set to the one more than the index of the last group on the table (i.e. if there are three groups, the last group will be index 2, so 3 would represent that the card is to be used to start a new group);
play a card from one group on the table to another: play_type = 2, play_details = (card, from_group, to_group) where card is the card to be played from the group, from_group is the (zero-offset) index of the group in table to play card from, and to_group is the index of the group in table to play card to (and, similarly to above, a value of one more than the index of the last group indicates that a new group is to be formed)
end the turn, after playing from the hand or play between groups on the table: play_type = 3, play_details = None.
Note that picking up a card (play_type = 0) implicitly ends the turn, whereas if plays are made from the hand/between groups on the table, an explicit "end of turn" play (play_type = 3) must be used to confirm that the player is ending their turn.

Example function calls are as follows:
'''
'''
>>> comp10001huxxy_valid_play((0, 0, None), [], 0, ['3S', 'KC', '8C', '3S', '8S', 'KH', '4H', '2C', '6S', '5H', '8C', 'KD'], [])
True
>>> comp10001huxxy_valid_play((0, 1, ('KC', 0)), [], 0, ['3S', 'KC', '8C', '3S', '8S', 'KH', '4H', '2C', '6S', '5H', '8C', 'KD'], [])
True
>>> comp10001huxxy_valid_play((0, 1, ('KC', 1)), [], 0, ['3S', 'KC', '8C', '3S', '8S', 'KH', '4H', '2C', '6S', '5H', '8C', 'KD'], [])
False  # invalid group no.
>>> comp10001huxxy_valid_play((0, 1, ('AC', 0)), [], 0, ['3S', 'KC', '8C', '3S', '8S', 'KH', '4H', '2C', '6S', '5H', '8C', 'KD'], [])
False  # can't play card you don't hold
>>> comp10001huxxy_valid_play((0, 1, ('KH', 0)), [(0, 1, ('KC', 0))], 0, ['3S', '8C', '3S', '8S', 'KH', '4H', '2C', '6S', '5H', '8C', 'KD'], [['KC']])
True
>>> comp10001huxxy_valid_play((0, 1, ('KD', 0)), [(0, 1, ('KC', 0)), (0, 1, ('KH', 0))], 0, ['3S', '8C', '3S', '8S', '4H', '2C', '6S', '5H', '8C', 'KD'], [['KC', 'KH']])
True
>>> comp10001huxxy_valid_play((0, 2, ('KS', 1, 0)), [(0, 1, ('KC', 0)), (0, 1, ('KH', 0))], 0, ['3S', '8C', '3S', '8S', '4H', '2C', '6S', '5H', '8C', 'KD'], [['KC', 'KH']])
False  # group/card don't exist
>>> comp10001huxxy_valid_play((0, 3, None), [(0, 1, ('KC', 0)), (0, 1, ('KH', 0)), (0, 1, ('KD', 0))], 0, ['3S', '8C', '3S', '8S', '4H', '2C', '6S', '5H', '8C'], [['KC', 'KH', 'KD']])
True
>>> comp10001huxxy_valid_play((0, 3, None), [], 0, ['3S', 'KC', '8C', '3S', '8S', 'KH', '4H', '2C', '6S', '5H', '8C', 'KD'], [])
False  # attempt to end turn without any plays to table
>>> comp10001huxxy_valid_play((0, 3, None), [(0, 1, ('KC', 0)), (0, 1, ('KH', 0))], 0, ['3S', '8C', '3S', '8S', '4H', '2C', '6S', '5H', '8C', 'KD'], [['KC', 'KH']])
False  # table state not valid
>>> comp10001huxxy_valid_play((0, 3, None), [(0, 1, ('AC', 0)), (0, 1, ('AH', 0)), (0, 1, ('AD', 0))], 0, ['3S', '8C', '3S', '8S', '4H', '2C', '6S', '5H', '8C'], [['AC', 'AH', 'AD']])
False  # insufficient points for opening turn
>>> comp10001huxxy_valid_play((0, 1, ('KS', 0)), [(0, 1, ('KC', 0)), (0, 1, ('KH', 0)), (0, 1, ('KD', 0)), (0, 3, None), (1, 0, None), (2, 0, None), (3, 0, None), (0, 0, None), (1, 0, None), (2, 0, None), (3, 0, None)], 0, ['3S', '8C', '3S', '8S', '4H', '2C', '6S', '5H', '8C', 'KS'], [['KC', 'KH', 'KD']])
True
>>> comp10001huxxy_valid_play((0, 3, None), [(0, 1, ('KC', 0)), (0, 1, ('KH', 0)), (0, 1, ('KD', 0)), (0, 3, None), (1, 0, None), (2, 0, None), (3, 0, None), (0, 0, None), (1, 0, None), (2, 0, None), (3, 0, None), (0, 1, ('KS', 0))], 0, ['3S', '8C', '3S', '8S', '4H', '2C', '6S', '5H', '8C'], [['KC', 'KH', 'KD', 'KS']])
True
>>> comp10001huxxy_valid_play((1, 0, None), [], 0, ['3S', 'KC', '8C', '3S', '8S', 'KH', '4H', '2C', '6S', '5H', '8C', 'KD'], [])
False  # wrong player
'''
#Code
# DO NOT DELETE/EDIT THIS LINE OF CODE, AS IT IS USED TO PROVIDE ACCESS TO
# THE FUNCTIONS FROM THE PREVIOUS QUESTION
from hidden import comp10001huxxy_valid_table

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

def comp10001huxxy_valid_play(play, play_history, active_player, hand, table):
    '''Accepts a tuple called play, a list of tuples called play_history,
    a integer; active_player, a list called hand and a list of lists called 
    table. Firstly the function looks over the common errors of a invalid 
    table such as checking if correct player is starting their turn, then
    it goes on to find the play type and runs seperate tests using the 
    details in hand, play and table. If it appears to be invalid in any of the
    checks, it will return False, otherwise it will return True
    '''
    player_turn = play[0]
    play_type = play[1]
    play_details = play[2]
    
    # checks if correct player is starting off 
    if player_turn != 0 and len(play_history) == 0:
        return False 
    
    # checks if it's just picking up a card
    if play_type == 0:
        return True 
    
    # checking placing card onto table
    if play_type == 1:
        card = play_details[0]
        to_group = play_details[1]
        # checking if card is in hand and if group exists
        if card not in hand or to_group > len(table):
            return False       
        return True 
    
    # checking swapping cards in between groups 
    if play_type == 2:
        card = play_details[0]
        from_group = play_details[1]
        to_group = play_details[2]
        # Checking if the groups exist 
        if to_group > (len(table) - 1) or from_group > (len(table) - 1):
            return False
        # checking if card exists in hand 
        elif card not in hand: 
            return False 
        return True 
    
    # checks for valid end of turn 
    if play_type == 3:
        # checking if the table is valid 
        if not comp10001huxxy_valid_table(table):
            return False
        # check if a play has been made: 
        if len(play_history) < 1:
            return False
        # checks for opening turn by checking if 24 points have been played:
        first_move = True
        played_points = 0
        for plays in play_history:
            # prevents adding plays which are None Type
            if plays[2]:
                if plays[0] == active_player:
                    # adds up values for all previously played cards
                    played_points += comp10001huxxy_score([plays[2][0]])
                    if played_points > 24:
                        first_move = False
        # checks if there are sufficient points for opening turn
        if first_move:
            # counts total points of play
            total_pts = 0
            for groups in table:
                total_pts += comp10001huxxy_score(groups)
            if total_pts < 24:
                return False
        return True
            
        
        
           
            
            
     

    
    