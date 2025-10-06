import time, random

def merge_sort(numbers, metricsList={'comparisons': 0, 'moves': 0}):
	"""
	Sorts a list using a merge sort algorithm.
	
	Args: 
        numbers (list[int]): The list of integers to sort.
        metricsList (dict): A dictionary to accumulate performance metrics.
    Returns:
        tuple: A tuple containing the sorted list and a metrics dictionary.
            - sorted list (list[int])
            - metrics (dict): Dictionary with performance metrics
                - 'comparisons': Number of comparisons made during sorting
                - 'moves': Number of element moves during sorting
	"""
	sortedList = numbers
	
	if len(numbers) > 1:
		pivot_index = len(numbers)//2
		left = numbers[:pivot_index]
		right = numbers[pivot_index:]

		left_sorted, left_metrics = merge_sort(left, metricsList)
		right_sorted, right_metrics = merge_sort(right, metricsList)

		sortedList, metricsList = merge(left_sorted, right_sorted)
		metricsList['comparisons'] += left_metrics['comparisons'] + right_metrics['comparisons']
		metricsList['moves'] += left_metrics['moves'] + right_metrics['moves']
	
	return sortedList, metricsList

def merge(left, right):
	r = l = 0
	sortedList = []
	comparisons = 0
	moves = 0

	while l < len(left) and r < len(right):
		if left[l] > right[r]:
			sortedList.append(right[r])
			moves += 1
			r += 1
		else:
			sortedList.append(left[l])
			moves += 1
			l += 1
		
		comparisons += 1
	sortedList.extend(right[r:])
	sortedList.extend(left[l:])
	moves += abs((r-len(right)))+abs((l-len(left)))
	return sortedList, {'comparisons': comparisons, 'moves': moves}


t = time.time()
metrics = merge_sort([2,6,1,4,3,8])[1]
metrics['elapsed seconds'] = time.time() - t
print(metrics)


t = time.time()
metrics = merge_sort([random.randint(1,100) for _ in range(200000)])[1]
metrics['elapsed seconds'] = time.time() - t
print(metrics)
