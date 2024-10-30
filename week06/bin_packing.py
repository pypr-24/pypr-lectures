import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 15})

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


def generate_random_items(N_sets=1000, N_items=50, min_size=2, max_size=25):
    '''
    Generate N_sets sets of N_items items, with random sizes
    between min_size and max_size (inclusive).
    Returns a Numpy array with shape (N_sets, N_items).
    '''
    items = np.random.randint(min_size, max_size+1, size=(N_sets, N_items))
    return items


def calculate_efficiency(bins, bin_size, metric='pc_filled'):
    '''
    Calculate 2 measures for efficiency of the bin-packing method:
    - the number of bins used,
    - the % of filled spaced across all bins.
    '''
    nb_bins_used = len(bins)

    if metric == 'pc_filled':
        return 100 * (sum(bins) / (nb_bins_used * bin_size))
    elif metric == 'bins_used':
        return nb_bins_used
    else:
        raise ValueError("Choose 'pc_filled' or 'bins_used' for the efficiency metric.")


def evaluate_method(items, method=None, bin_size=60, metric='pc_filled'):
    '''
    Evaluate the efficiency of a particular implementation of
    the first-fit algorithm for the bin-packing problem.

    Runs the first-fit algorithm with a particular 'method',
    to pack each row of 'items' into bins of size 'bin_size'.

    Returns a Numpy vector of length N_sets, containing the
    % of filled space overall for each item set.
    '''
    # Creating a vector to store efficiency data
    N_sets = items.shape[0]
    eff = np.zeros(N_sets)

    # Loop over the sets of items
    for i in range(N_sets):
        # Pack the current set with the designed method
        bins = first_fit(items[i], bin_size, method=method)

        # Store efficiency metric
        eff[i] = calculate_efficiency(bins, bin_size, metric=metric)
    
    # Return the efficiency metric for all sets of items
    return eff


def compare_methods(methods=[None, 'increasing', 'decreasing'], N_sets=1000, N_items=50, min_size=2, max_size=25, bin_size=60):
    '''
    Compares different methods for bin-packing,
    by performing N_sets simulations with N_items
    random items each.
    '''
    # Create the random items
    items = generate_random_items(N_sets, N_items, min_size, max_size)

    # Get efficiency metrics for each method and set of items
    eff_bins_used = np.zeros((len(methods), N_sets))
    eff_pc_filled = np.zeros((len(methods), N_sets))
    for i, m in enumerate(methods):
        eff_bins_used[i] = evaluate_method(items, method=m, bin_size=bin_size, metric='bins_used')
        eff_pc_filled[i] = evaluate_method(items, method=m, bin_size=bin_size, metric='pc_filled')
    
    # Plot the results.
    # (transpose because otherwise boxplot will attempt to
    # draw N_sets different box plots)
    fig, ax = plt.subplots(2, 2, figsize=(12, 10))
    ax[0, 0].boxplot(eff_bins_used.T, labels=[str(m) for m in methods])
    ax[0, 1].boxplot(eff_pc_filled.T, labels=[str(m) for m in methods])

    # Plot the histograms one by one (and with transparency)
    # so they can overlap and we can label them properly
    for i in range(len(methods)):
        ax[1, 0].hist(eff_bins_used[i], alpha=0.5, label=f'{methods[i]}')
        ax[1, 1].hist(eff_pc_filled[i], alpha=0.5, label=f'{methods[i]}')

    # Labelling plots and axes
    ax[0, 0].set(title='Number of boxes used')
    ax[0, 1].set(title='% filled space')

    ax[0, 0].set(ylabel='Boxes used')
    ax[1, 0].set(xlabel='Boxes used', ylabel='Number of item sets')
    ax[1, 1].set(xlabel='% filled space')

    ax[1, 0].legend()
    ax[1, 1].legend()
    plt.show()
