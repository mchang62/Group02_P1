Group Project 1: Sorting Algorithm Comparison
by William Wallius, Michael Chang, Andre Forestiere, Benjamin Noh

How to Run
--------------------
Use Default Arguments: 
> python driver.py

Use Custom Arguments: 
> python driver.py --algos merge,quicksort --datasets random,duplicates --sizes 100,500,1000 --trials 10 --seed 123 --out results/experiment1.csv --warmup

Accepts the following arguments:
--algos <algorithms>
    Comma-separated list of algorithms to run
    Options: insertion, merge, quicksort, radix
    Example: --algos merge,quicksort
    Default: runs all algorithms in test matrix

--datasets <types>
    Comma-separated list of dataset types to test
    Options: random, reverse, duplicates
    Example: --datasets random,duplicates
    Default: runs all datasets in test matrix

--sizes <integers>
    Comma-separated list of dataset sizes
    Example: --sizes 100,500,1000
    Default: uses sizes from test matrix (1000 for random/reverse, 20000 for duplicates)

--trials <number>
    Number of trials to run per configuration
    Example: --trials 10
    Default: 5

--seed <number>
    Random seed for reproducible dataset generation
    Example: --seed 123
    Default: 42

--out <filepath>
    Path to output CSV file
    Example: --out my_results/experiment1.csv
    Default: results/runs.csv

--warmup
    Enable warmup run (discarded) before timed trials
    Example: --warmup
    Default: no warmup

Note: When --algos, --datasets, and --sizes are ALL specified together,
the driver runs the full Cartesian product of all combinations.
Otherwise, it filters the default test matrix based on provided arguments.

Default test matrix: 
[
    ('random', 1000, ['insertion', 'merge', 'quicksort', 'radix']),
    ('nearly_sorted', 5000, ['insertion', 'merge', 'quicksort']),
    ('reverse', 1000, ['insertion', 'merge', 'quicksort', 'radix']),
    ('duplicates', 20000, ['insertion', 'merge', 'quicksort', 'radix']),
]


Changelog
--------------------
[10-04]: modified return of radix sort to include metrics of sorting run, only number of moves made during the function execution
