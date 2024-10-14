def first_fit(item_list, bin_size):
    '''
    First-fit algorithm for the bin packing problem.
    Input:
        item_list (list): list of items to pack
        bin_size (float): capacity of each bin
    
    Output:
        bin_list (list): a list of bins with what's inside of each bin.
    '''
    # Start by opening a bin
    bin_state = [0]

    # Loop over the items
    for item in item_list:
        # Flag that item is not placed yet
        placed = False

        # Loop over the bins
        # for bin in bin_state:
        for i in range(len(bin_state)):

            # Does it fit in the current bin?
            if bin_state[i] + item <= bin_size:
                # Yes, there is space; place the item
                bin_state[i] += item

                # Raise the flag to say it's been placed
                placed = True

                # Stop looking at spaces in later bins
                break
        
        if not placed:
            # Open a new bin
            bin_state.append(0)
            # Put the item in the bin
            bin_state[-1] += item

            # Shorter:
            # bin_state.append(item)
    
    return bin_state


# TODO: debug this function!

# Testing

# size of each item
item_list = [2, 1, 3, 2, 1, 2, 3, 1]

# size of bin
bin_size = 4

# "assert X" does nothing if X is True,
# but raises an error if X is False
print(first_fit(item_list, bin_size))
# assert first_fit(item_list, bin_size) == [4, 4, 4, 3]
