class Card():

    def __init__(self, my_value, my_suit):
        self.value = my_value
        self.suit = my_suit
        # Exercise: if my_value > 13, fail with an appropriate error
    

    def __str__(self):
        display_value = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}

        if self.value >= 2 and self.value <= 10:
            return f'{self.value} of {self.suit}'
        else:
            return f'{display_value[self.value]} of {self.suit}'
        
    
    def __eq__(self, other):
        # if self.value == other.value and self.suit == other.suit:
        #     return True
        # else:
        #     return False

        return self.value == other.value and self.suit == other.suit
    

    def __gt__(self, other):
        if (self.suit != 'hearts' and other.suit != 'hearts') \
            or (self.suit == 'hearts' and other.suit == 'hearts'):
            return self.value > other.value
        # elif 'hearts' in [self.suit, other.suit]:
        else:
            return self.suit == 'hearts'
            # if self.suit == 'hearts':
            #     return True
            # else:
            #     return False
        
        # Exercise: make Ace stronger than all the other cards



my_card = Card(12, 'spades')
print(my_card)
my_second_card = Card(10, 'hearts')
assert not (my_card == my_second_card) # should be False
assert my_card == my_card # should be True
assert my_card != my_second_card
assert my_card < my_second_card
# assert my_second_card < my_card

# assert my_second_card <= my_card


print('well done!')

# print(my_card.value)
# print(my_card.suit)
# print(type(my_card))

# import numpy as np
# t = np.zeros((5, 2))
# print(t.shape)

# "dunder" methods (Double UNDERscore)

# my_list = [1, 2, 3]
# sorted(my_list) # this is a function
# my_list.sort()  # this is a method
# sort(my_list) # this won't work
# list.sort(my_list) # same as my_list.sort()



# this_is_snake_case
# thisIsCamelCase
# ThisIsAnotherCase