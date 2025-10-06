import argparse
import csv
import random
import time
import os

from insertion_sort import insertionSort
from merge_sort import merge_sort
from quicksort import quickSort
from radix_sort import radix_sort

ALGORITHMS = {
    'insertion': insertionSort,
    'merge': merge_sort,
    'quicksort': quickSort,
    'radix': radix_sort,
}

DEFAULT_TEST_MATRIX = [
    ('random', 1000, ['insertion', 'merge', 'quicksort', 'radix']),
    ('nearly_sorted', 5000, ['insertion', 'merge', 'quicksort']),
    ('reverse', 1000, ['insertion', 'merge', 'quicksort', 'radix']),
    ('duplicates', 20000, ['insertion', 'merge', 'quicksort', 'radix']),
]

PIVOT_STRATEGIES = [
    'median3',
    'first',
]


def generate_dataset(dataset_type, size, seed=None):
    """
    Generate dataset based on type and size.
    
    Args:
        dataset_type: Type of dataset ('random', 'reverse', 'duplicates')
        size: Number of elements
        seed: Random seed for reproducibility
        
    Returns:
        List of integers
    """
    if seed is not None:
        random.seed(seed)
    
    if dataset_type == 'random':
        return [random.randint(-1000, 1000) for _ in range(size)]
    
    elif dataset_type == 'reverse':
        return list(range(size, 0, -1))
    
    elif dataset_type == 'duplicates':
        return [random.randint(0, 99) for _ in range(size)]
    
    elif dataset_type == 'nearly_sorted':
        arr = list(range(size))
        # randomly swap about 5% of the elements to achieve a 'nearly sorted' effect
        num_swaps = size // 20
        for _ in range(num_swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    else:
        raise ValueError(f"Unknown dataset type: {dataset_type}")


def run_sorting_algorithm(algo_name, data, pivot):
    """
    Run a sorting algorithm and collect metrics.
    
    Args:
        algo_name: Name of the algorithm
        data: List to sort (will be copied to preserve original)
        
    Returns:
        Tuple of (time_ms, metrics_dict)
    """
    if algo_name not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algo_name}")
    
    algo_func = ALGORITHMS[algo_name]
    
    # Make a copy to avoid modifying original data
    data_copy = data.copy()
    
    # Time the sorting
    start_time = time.perf_counter()
    if algo_name == 'quicksort':
        if pivot not in PIVOT_STRATEGIES:
            raise ValueError(f"Invalid pivot strategy: {pivot}")
        sorted_data, metrics = algo_func(data_copy, pivot=pivot)
    else: 
        sorted_data, metrics = algo_func(data_copy)
    end_time = time.perf_counter()
    
    # Convert to milliseconds
    time_ms = (end_time - start_time) * 1000
    
    # Verify sorting correctness
    expected = sorted(data)
    if sorted_data != expected:
        print(f"WARNING: {algo_name} did not sort correctly!")
    
    return time_ms, metrics

def build_test_matrix(args):
    """
    Build a test matrix from args.
    - If none of algos/datasets/sizes provided -> return default_matrix.
    - If all three provided -> Cartesian product of datasets x sizes with the provided algos.
    - Otherwise -> filter default_matrix by provided args and shrink per-row algos to requested subset.
    """
    default_test_matrix = DEFAULT_TEST_MATRIX
    algo_list = args.algos.split(',') if args.algos else None
    dataset_list = args.datasets.split(',') if args.datasets else None
    size_list = None
    if args.sizes:
        try:
            size_list = [int(s) for s in args.sizes.split(',')]
        except ValueError:
            raise ValueError("Sizes must be comma-separated integers")

    # None of the three -> default matrix
    if (algo_list is None) and (dataset_list is None) and (size_list is None):
        return default_test_matrix

    # All three provided -> create custom test matrix
    if (algo_list is not None) and (dataset_list is not None) and (size_list is not None):
        custom_matrix = []
        for ds in dataset_list:
            for sz in size_list:
                custom_matrix.append((ds, sz, list(algo_list)))
        return custom_matrix

    # Partial specification -> filter default matrix
    result = []
    for ds, sz, algos in default_test_matrix:
        if dataset_list is not None and ds not in dataset_list:
            continue
        if size_list is not None and sz not in size_list:
            continue
        if algo_list is not None:
            filtered_algos = [a for a in algos if a in algo_list]
        else:
            filtered_algos = list(algos)
        if filtered_algos:
            result.append((ds, sz, filtered_algos))
    return result


def write_csv_header(filepath):
    """
    Write CSV header if file doesn't exist.
    
    Args:
        filepath: Path to CSV file
    """
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['algorithm', 'dataset', 'n', 'comparisons', 'swaps_or_moves', 'ms', 'trial'])


def append_csv_row(filepath, row_data):
    """
    Append a row to the CSV file.
    
    Args:
        filepath: Path to CSV file
        row_data: Dictionary with keys matching CSV columns
    """
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            row_data['algorithm'],
            row_data['dataset'],
            row_data['n'],
            row_data['comparisons'],
            row_data['swaps_or_moves'],
            row_data['ms'],
            row_data['trial']
        ])


def main():
    """
    Main driver function for running sorting experiments.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run sorting algorithm experiments')
    parser.add_argument('--algos', type=str, help='Comma-separated list of algorithms to run (default: all)')
    parser.add_argument('--pivot', type=str, default='median3', help='Pivot strategy for quicksort (default: median3)')
    parser.add_argument('--datasets', type=str, help='Comma-separated list of datasets (default: all from matrix)')
    parser.add_argument('--sizes', type=str, help='Comma-separated list of sizes (default: from test matrix)')
    parser.add_argument('--trials', type=int, default=5, help='Number of trials per configuration (default: 5)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for dataset generation (default: 42)')
    parser.add_argument('--out', type=str, default='results/runs.csv', help='Output CSV file path')
    parser.add_argument('--warmup', action='store_true', help='Run warmup trial before measurements')
    
    args = parser.parse_args()

    # Create results directory and results csv if they don't exist
    os.makedirs(os.path.dirname(args.out) if os.path.dirname(args.out) else '.', exist_ok=True)
    write_csv_header(args.out)
    
    # Build test matrix according to provided arguments
    try:
        test_matrix = build_test_matrix(args)
    except ValueError as e:
        print(f"Error building test matrix: {e}")
        return

    print("=" * 60)
    print("SORTING ALGORITHM EXPERIMENTS")
    print("=" * 60)
    print(f"Output file: {args.out}")
    print(f"Trials per configuration: {args.trials}")
    print(f"Random seed: {args.seed}")
    print(f"Warmup enabled: {args.warmup}")
    
    # Run experiments based on test matrix
    for dataset_type, size, matrix_algos in test_matrix:
        print(f"\nDataset: {dataset_type}, Size: {size}")
        print("-" * 40)
        
        # Generate dataset once for all algorithms
        try:
            data = generate_dataset(dataset_type, size, args.seed)
        except NotImplementedError as e:
            print(f"  Skipping: {e}")
            continue
        
        # Run each algorithm
        for algo in matrix_algos:
            print(f"  Running {algo}...")
            
            # Warmup run if requested
            if args.warmup:
                try:
                    _, _ = run_sorting_algorithm(algo, data, pivot=args.pivot)
                    print(f"    Warmup complete")
                except Exception as e:
                    print(f"    Warmup failed: {e}")
            
            # Run trials
            for trial in range(1, args.trials + 1):
                try:
                    time_ms, metrics = run_sorting_algorithm(algo, data, pivot=args.pivot)
                    
                    row_data = {
                        'algorithm': algo,
                        'dataset': dataset_type,
                        'n': size,
                        'comparisons': metrics.get('comparisons', 0),
                        'swaps_or_moves': metrics.get('swaps', 0) or metrics.get('moves', 0),
                        'ms': f"{time_ms:.3f}",
                        'trial': trial
                    }
                    
                    append_csv_row(args.out, row_data)
                    
                    print(f"    Trial {trial}: {time_ms:.3f} ms, "
                          f"Comparisons: {row_data.get('comparisons', 0)}, "
                          f"Moves: {row_data.get('swaps_or_moves', 0)}")
                
                except Exception as e:
                    print(f"    Trial {trial} failed: {e}")
    
    print("\n" + "=" * 60)
    print("EXPERIMENTS COMPLETE")
    print(f"Results written to: {args.out}")
    print("=" * 60)
    
    print_summary(args.out)


def print_summary(csv_file):
    """
    Print summary statistics from the results CSV.
    
    Args:
        csv_file: Path to the CSV file
    """
    if not os.path.exists(csv_file):
        return
    
    print("\nSUMMARY STATISTICS")
    print("-" * 40)
    
    # Read CSV and compute averages
    results = {}
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['algorithm'], row['dataset'], row['n'])
            if key not in results:
                results[key] = []
            results[key].append(float(row['ms']))
    
    # Print averages
    for (algo, dataset, n), times in sorted(results.items()):
        avg_time = sum(times) / len(times)
        print(f"{algo:12s} | {dataset:15s} | n={n:6s} | "
              f"Avg: {avg_time:8.3f} ms | Trials: {len(times)}")


if __name__ == "__main__":
    main()