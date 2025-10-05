import random
import time
import sys

def quickSort(a: list[int], pivot: str = "median3") -> tuple[list[int], dict]:
    """
    Sorts a list and counts its internal operations (Internal Instrumentation).
    NOTE: This function does NOT know it is being timed.
    """
    comparisonCount = 0
    moveCount = 0
    listToSort = a[:]
    
    def swapElements(targetList, indexOne, indexTwo):
        nonlocal moveCount
        if indexOne != indexTwo:
            targetList[indexOne], targetList[indexTwo] = targetList[indexTwo], targetList[indexOne]
            moveCount += 3

    def choosePivot(targetList, lowIndex, highIndex):
        nonlocal comparisonCount
        if pivot == "first":
            swapElements(targetList, lowIndex, highIndex)
            return
        if pivot == "median3":
            midIndex = (lowIndex + highIndex) // 2
            if targetList[lowIndex] > targetList[midIndex]:
                comparisonCount += 1
                swapElements(targetList, lowIndex, midIndex)
            if targetList[lowIndex] > targetList[highIndex]:
                comparisonCount += 1
                swapElements(targetList, lowIndex, highIndex)
            if targetList[midIndex] > targetList[highIndex]:
                comparisonCount += 1
                swapElements(targetList, midIndex, highIndex)
            swapElements(targetList, midIndex, highIndex)
            return

    def partitionArray(targetList, lowIndex, highIndex):
        nonlocal comparisonCount
        choosePivot(targetList, lowIndex, highIndex)
        pivotValue = targetList[highIndex]
        i = lowIndex - 1
        for j in range(lowIndex, highIndex):
            comparisonCount += 1
            if targetList[j] <= pivotValue:
                i += 1
                swapElements(targetList, i, j)
        swapElements(targetList, i + 1, highIndex)
        return i + 1

    def quickSortRecursive(targetList, lowIndex, highIndex):
        if lowIndex < highIndex:
            partitionIndex = partitionArray(targetList, lowIndex, highIndex)
            quickSortRecursive(targetList, lowIndex, partitionIndex - 1)
            quickSortRecursive(targetList, partitionIndex + 1, highIndex)

    if listToSort:
        quickSortRecursive(listToSort, 0, len(listToSort) - 1)
        
    # The algorithm's "contract" is to return the sorted list AND its metrics.
    metrics = {'comparisons': comparisonCount, 'moves': moveCount}
    return listToSort, metrics

# Set a higher recursion limit for deep recursion on large datasets
sys.setrecursionlimit(20000)

def main():
    """
    Main driver function to run sanity checks and sorting experiments,
    then print performance results in CSV format.
    """
    # First, run the sanity test on the quickSort function
    # NOTE: The sanity test does not need to be timed.
    if not sanityTest(quickSort):
        print("Sanity Test FAILED. Halting execution.")
        return

    print("Sanity Test Passes. Proceeding to performance analysis.\n")
    
    # --- Configuration for Data Generation ---
    seed_value = 17
    min_val = -100000
    max_val = 100000
    # -----------------------------------------

    arraySizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
    algorithm_name = "quickSort"
    dataset_name = "random"
    trial_number = 1
    
    print("algorithm,dataset,n,trial,comparisons,moves,timeMs")

    for size in arraySizes:
        # 1. Prepare the data for this run
        unsortedList = generateRandom(n=size, lo=min_val, hi=max_val, seed=seed_value)
        
        # 2. Time the sorting operation (External Timing)
        # This is the correct design: the timer wraps the algorithm call.
        startTime = time.perf_counter()
        sortedList, metrics = quickSort(unsortedList, pivot="median3")
        endTime = time.perf_counter()
        
        # 3. Process the results
        elapsedSeconds = endTime - startTime
        elapsed_ms = elapsedSeconds * 1000
        
        moves = metrics['moves']
        comparisons = metrics['comparisons']
        
        csvRow = [
            algorithm_name, dataset_name, size, trial_number,
            comparisons, moves, f"{elapsed_ms:.3f}"
        ]
        
        print(",".join(map(str, csvRow)))

def generateRandom(n: int, lo: int, hi: int, seed: int) -> list[int]:
    """
    Generates a list of n random integers using a specified seed.
    """
    random.seed(seed)
    return [random.randint(lo, hi) for _ in range(n)]

def sanityTest(sort_function):
    # ... (sanityTest implementation remains the same, but I've corrected the call below) ...
    print("--- Running Sanity Tests ---")
    
    test_cases = {
        "Empty list": [], "Single element": [42], "Already-sorted": [10, 20, 30, 40, 50, 60],
        "All-equal": [7, 7, 7, 7, 7], "Negatives present": [-5, 100, -1, 0, 42, -99]
    }
    all_tests_passed = True
    for name, data in test_cases.items():
        sorted_result, _ = sort_function(data)
        expected_result = sorted(data)
        if sorted_result != expected_result:
            all_tests_passed = False
            print(f"[FAIL] Test '{name}' failed!")
        else:
            print(f"[PASS] Test '{name}' succeeded.")
    
    print("\n--- Running Smoke Test (N=50) ---")
    smoke_array = generateRandom(n=50, lo=-1000, hi=1000, seed=17) # Corrected call
    sorted_smoke, smoke_metrics = sort_function(smoke_array)
    counters_increased = smoke_metrics['comparisons'] > 0 and smoke_metrics['moves'] > 0
    is_sorted_correctly = sorted_smoke == sorted(smoke_array)
    if counters_increased and is_sorted_correctly:
        print(f"[PASS] Smoke test succeeded.")
    else:
        all_tests_passed = False
        print(f"[FAIL] Smoke test failed!")
    print("--- Sanity Testing Complete ---")
    return all_tests_passed

if __name__ == "__main__":
    main()