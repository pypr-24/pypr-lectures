import numpy as np

def first_fit(item_list, bin_size, method=None):
    '''
    First-fit algorithm for the bin packing problem.
    Input:
        item_list (list): list of items to pack
        bin_size (float): capacity of each bin
        method (str or None):
            None: do nothing
            'increasing': sort items in increasing order of size
            'decreasing': sort items in decreasing order of size
    
    Output:
        bin_list (list): a list of bins with what's inside of each bin.
    '''
    if method is None:
        pass
    elif method == 'increasing':
        item_list = sorted(item_list)
    elif method == 'decreasing':
        item_list = sorted(item_list, reverse=True)
    else:
        raise ValueError('Choose None, "increasing", or "decreasing" for method.')

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


# # Testing

# # size of each item
# item_list = [2, 1, 3, 2, 1, 2, 3, 1]

# # size of bin
# bin_size = 4

# # "assert X" does nothing if X is True,
# # but raises an error if X is False
# print(first_fit(item_list, bin_size, method='increasing'))
# # assert first_fit(item_list, bin_size) == [4, 4, 4, 3]


# Evaluating the different methods

# Set up some simulation parameters
N_sets = 1000
N_items = 50
min_size = 2
max_size = 25
bin_size = 60

# Make the items
items = np.random.randint(min_size, max_size+1, size=(N_items, N_sets))
# print(items)

methods = [None, 'increasing', 'decreasing']

for i in range(N_sets):
    for m in methods:
        bins = first_fit(items[i], bin_size, method=m)
        efficiency = 100 * (sum(bins) / (len(bins) * bin_size))

        # Store efficiency number in some array


# Visualise the results in some way
# (distribution plot, calculating average efficiency...)