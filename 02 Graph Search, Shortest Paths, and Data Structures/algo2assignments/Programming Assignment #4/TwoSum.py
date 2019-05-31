from bisect import bisect_left, bisect_right

def read_txt(path):
    array = []
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            num = int(line.rstrip())
            array.append(num)
    return array

def TwoSum(array, lower=-10000, upper=10000):
    """
    Find the number of distinct sums in the array.
    """

    array = sorted(array)
    numbers = set()
    for x in array:
        i = bisect_left(array, -10000 - x)
        j = bisect_right(array, 10000 - x)

        ## -10000 <= x + y <= 10000
        for y in array[i:j]:
            if x != y:
                numbers.add(x + y)

    return numbers

if __name__ == "__main__":
    array = read_txt("algo1-programming_prob-2sum.txt")
    numbers = TwoSum(array)
    print(len(numbers))
    ## outputs: 427