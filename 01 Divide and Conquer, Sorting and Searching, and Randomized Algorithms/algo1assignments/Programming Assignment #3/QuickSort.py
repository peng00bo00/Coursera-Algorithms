def read_txt(path):
    array = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            array.append(int(line.rstrip()))
    return array

def QuickSort1(array, l, r):
    """
    Sort a given array with quick sort. The pivot element is fixed as the first element.

    Params:
        array: an array to be sorted;
        l: the left index;
        r: the right index.

    Return:
        num: number of counts.
    """

    if l >= r:
        return 0
    else:
        num = r - l
        ## the first element is the pivot element
        i = l
        for j in range(l+1, r+1):
            if array[j] < array[l]:
                i += 1
                array[i], array[j] = array[j], array[i]

        ## exchange the pivot and array[i]
        array[l], array[i] = array[i], array[l]

        left_num = QuickSort1(array, l, i-1)
        right_num = QuickSort1(array, i+1, r)

        num = num + left_num + right_num

        return num

def QuickSort2(array, l, r):
    """
    Sort a given array with quick sort. The pivot element is fixed as the last element.

    Params:
        array: an array to be sorted;
        l: the left index;
        r: the right index.

    Return:
        num: number of counts.
    """

    if l >= r:
        return 0
    else:
        ## Exchange the first and the last element so that the original last element is the pivot.
        array[l], array[r] = array[r], array[l]
        
        num = r - l
        ## the first element is the pivot element
        i = l
        for j in range(l+1, r+1):
            if array[j] < array[l]:
                i += 1
                array[i], array[j] = array[j], array[i]

        ## exchange the pivot and array[i]
        array[l], array[i] = array[i], array[l]

        left_num = QuickSort2(array, l, i-1)
        right_num = QuickSort2(array, i+1, r)

        num = num + left_num + right_num

        return num

def QuickSort3(array, l, r):
    """
    Sort a given array with quick sort. The pivot element is selected according to the "median-of-three" rule.

    Params:
        array: an array to be sorted;
        l: the left index;
        r: the right index.

    Return:
        num: number of counts.
    """

    if l >= r:
        return 0
    else:
        mid = (l + r) // 2
        
        median = l
        if (array[l] <= array[mid] <= array[r]) or (array[r] <= array[mid] <= array[l]):
            median = mid
        elif (array[l] <= array[r] <= array[mid]) or (array[mid] <= array[r] <= array[l]):
            median = r
        
        array[l], array[median] = array[median], array[l]

        num = r - l
        ## the first element is the pivot element
        i = l
        for j in range(l+1, r+1):
            if array[j] < array[l]:
                i += 1
                array[i], array[j] = array[j], array[i]

        ## exchange the pivot and array[i]
        array[l], array[i] = array[i], array[l]

        left_num = QuickSort3(array, l, i-1)
        right_num = QuickSort3(array, i+1, r)

        num = num + left_num + right_num

        return num

if __name__ == "__main__":
    array = read_txt("QuickSort.txt")    
    num = QuickSort1(array, 0, len(array)-1)
    #output: 162085

    array = read_txt("QuickSort.txt")
    num = QuickSort2(array, 0, len(array)-1)
    #output: 164123

    array = read_txt("QuickSort.txt")
    num = QuickSort3(array, 0, len(array)-1)
    #output: 138382