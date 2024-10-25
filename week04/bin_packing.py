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


def first_fit(item_list, bin_size):
    '''
    首次适应算法用于解决装箱问题。
    输入:
        item_list (list): 要装入箱子的物品列表，每个物品都有一个大小
        bin_size (float): 每个箱子的容量
    
    输出:
        bin_list (list): 包含每个箱子的列表，列表中记录每个箱子的剩余空间
    '''
    # 初始化一个箱子列表，初始箱子为空，容量为0
    bin_state = [0]

    # 遍历物品列表
    for item in item_list:
        # 标志变量，记录物品是否已被放入箱子
        placed = False

        # 遍历已有的箱子，检查物品是否能放入
        for i in range(len(bin_state)):

            # 检查当前物品是否能放入这个箱子
            if bin_state[i] + item <= bin_size:
                # 如果能放下，将物品放入该箱子
                bin_state[i] += item

                # 更新标志变量为True，表示物品已放入箱子
                placed = True
                break  # 放入后跳出循环，不再检查其他箱子
        
        # 如果没有找到合适的箱子，打开一个新箱子
        if not placed:
            # 新箱子初始为0容量
            bin_state.append(0)
            # 将当前物品放入新箱子
            bin_state[-1] += item

    # 返回每个箱子的使用情况（箱子的剩余容量）
    return bin_state


# 测试

# 每个物品的大小
item_list = [2, 1, 3, 2, 1, 2, 3, 1]

# 箱子的容量
bin_size = 4

# 打印结果，验证算法
print(first_fit(item_list, bin_size))  
# 预期结果：[4, 4, 4, 3]
