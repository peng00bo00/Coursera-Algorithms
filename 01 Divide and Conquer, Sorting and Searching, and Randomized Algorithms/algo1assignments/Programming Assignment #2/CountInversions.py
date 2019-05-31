def read_txt(path):
    lst = []
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            lst.append(int(line.rstrip()))
    return lst

def MergeCount(lst):
    """
    Count inversions of a given list with merge sort.
    Return a sorted list and the number of inversions.

    lst: an array
    """

    if len(lst) == 0 or len(lst) == 1:
        return lst, 0
    else:
        mid = len(lst) // 2
        left, right = lst[:mid], lst[mid:]

        ## Split the list to 2 parts and count inversions recursively
        left_sort, left_num = MergeCount(left)
        right_sort, right_num = MergeCount(right)
        num = left_num + right_num

        sort = []
        while left_sort and right_sort:
            if left_sort[0] > right_sort[0]:
                sort.append(right_sort[0])
                right_sort = right_sort[1:]
                ## left_sort[i] > right_sort[0] for any i
                ## There are len(left_sort) inversions
                num += len(left_sort)
            else:
                sort.append(left_sort[0])
                left_sort = left_sort[1:]
        sort = sort + left_sort + right_sort
        return sort, num

if __name__ == "__main__":
    lst = read_txt("IntegerArray.txt")
    sort, num = MergeCount(lst)
    #print(sort)
    print(num)
    #output: 2407905288
