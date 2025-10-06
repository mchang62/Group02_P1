def radix_sort(numbers):
    """
    Sorts a list of integers using LSD (Least Significant Digit) radix sort.
    Handles both positive and negative integers.
    
    Args:
        numbers: List of integers to be sorted
        
    Returns:
        tuple: A tuple containing the sorted list and a metrics dictionary.
            - sorted list (list[int])
            - metrics (dict): Dictionary with performance metrics
                - 'comparisons': Number of comparisons made during sorting
                - 'moves': Number of element moves during sorting
    """
    # Early exit for edge cases
    if not numbers:
        return []
    if len(numbers) == 1:
        return numbers.copy()
    
    move_count = 0
    
    # Input Validation
    if not all(isinstance(num, int) for num in numbers):
        raise ValueError("All elements must be integers")
    
    # Create a copy to preserve original list
    numbers = numbers.copy()
    
    # Initialize buckets (0-9 for base-10)
    buckets = {digit: [] for digit in range(10)}
    
    max_digits = get_max_digits(numbers)
    
    # Process each digit position (LSD - starting from ones place)
    place = 1
    for digit_position in range(max_digits):
        # Reset buckets
        for key in buckets:
            buckets[key] = []
        
        for num in numbers:
            digit = get_abs_digit(num, place)
            buckets[digit].append(num)
            move_count += 1
        
        i = 0
        for key in range(10):
            for num in buckets[key]:
                numbers[i] = num
                i += 1
        
        place *= 10
    
    # Handle negatives by sorting to beginning and reversing
    negatives = [num for num in numbers if num < 0]
    positives = [num for num in numbers if num >= 0]

    negatives.reverse()
    result = []
    for neg in negatives:
        result.append(neg)
        move_count += 1
    for pos in positives:
        result.append(pos)
        move_count += 1
    
    metrics = {
        'moves': move_count,
    }
    
    return result, metrics


def get_max_digits(numbers):
    """
    Finds the maximum number of base-10 digits in the list.
    
    Args:
        numbers: List of integers
        
    Returns:
        Integer representing maximum digit count
    """
    if not numbers:
        return 0
    
    max_val = max(abs(num) for num in numbers)
    
    if max_val == 0:
        return 1
    
    digit_count = 0
    while max_val > 0:
        digit_count += 1
        max_val //= 10
    
    return digit_count


def get_abs_digit(num, place):
    """
    Returns the absolute value of digit at specified place value of num.
    Example: num = -173, place = 10 (tens) → 7
    
    Args:
        num: Integer to extract digit from
        place: Place value (1 for ones, 10 for tens, 100 for hundreds, etc.)
        
    Returns:
        Single digit (0-9) at the specified place
    """
    return (abs(num) // place) % 10
