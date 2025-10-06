import time, random
def insertionSort(numbers):
    """
    Sorts a list of integers using the insertion sort algorithm.

    Args:
        numbers (list[int]): The list of integers to sort.
    Returns:
        tuple: A tuple containing the sorted list and a metrics dictionary.
            - sorted list (list[int])
            - metrics (dict): Dictionary with performance metrics
                - 'comparisons': Number of comparisons made during sorting
                - 'moves': Number of element moves during sorting
    """

    moves, comparisons = 0,0
    if len(numbers) <= 1:
        return numbers, {'comparisons': comparisons, 'moves': moves}
    for i in range (1, len(numbers)):
        key = numbers[i]
        j = i - 1
        comparisons += 1
        while j >= 0 and numbers[j] > key:
            moves += 1
            comparisons += 1
            numbers[j+1] = numbers[j]
            j -= 1
        numbers[j+1] = key
        moves += 1
        comparisons += 1
    return numbers, {'comparisons': comparisons, 'moves': moves}

randList = [random.randint(1,100) for _ in range (100)]
startTime = time.time()
insertionSort(randList)
print("Time to sort : ", insertionSort(randList), " ", time.time()- startTime, "seconds")

