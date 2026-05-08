# Project Execution Guide

## Quick Start

This guide explains step-by-step how to run the project and compile the report.

## Step 1: Install Required Package

Before running the code, install the psutil package for memory monitoring:

```bash
pip install psutil
```

## Step 2: Place Dataset Files

Make sure the dataset files are in the project directory:
- chess.dat
- connect.dat

These are the gzip-compressed benchmark datasets.

## Step 3: Run Experiments

Execute the main experiment script:

```bash
python experiment_runner.py
```

This will:
1. Load each dataset
2. Run Apriori algorithm 3 times for each minimum support threshold
3. Run Bitwise Vertical algorithm 3 times for each minimum support threshold
4. Run Optimized Bitwise algorithm 3 times for each minimum support threshold
5. Average the results
6. Calculate speedup ratios
7. Save results to JSON files
8. Display detailed output

The entire process takes approximately 10-20 minutes depending on your system.

## Step 4: Review Results

After execution completes, you will have:
- results_chess.json
- results_connect.json

These contain all metrics for inclusion in your report.

## Step 5: Update Report with Your Results

The Report.tex file contains template sections. You can update the Experimental Results section with your actual data:

1. Run `python results_generator.py` to generate LaTeX table code
2. Copy the generated LaTeX code
3. Paste into the Experimental Results section of Report.tex
4. Replace the sample data with your actual results

## Step 6: Compile Report

Using Overleaf:
1. Create new project
2. Upload Report.tex
3. Click "Recompile"
4. Download PDF

Or using local LaTeX:
```bash
pdflatex Report.tex
```

## Understanding the Output

### Console Output

When you run the experiments, you will see output like:

```
Loading dataset from chess.dat...
Dataset loaded successfully
Transactions: 3196
Unique Items: 752
Avg Transaction Size: 37.20

Running experiments on Chess dataset
Number of runs per configuration: 3
================================================================================

Minimum Support: 0.5 (50%)
--------------------------------------------------------------------------------
  Run 1/3...
  Run 2/3...
  Run 3/3...

Apriori Results:
  Execution Time: 8.3200 seconds
  Memory Used: 187.45 MB
  Frequent Itemsets: 1523
  Candidates Generated: 4581

Bitwise Vertical FIM Results:
  Execution Time: 1.8900 seconds
  Memory Used: 78.32 MB
  Frequent Itemsets: 1523
  Candidates Generated: 4581

Optimized Bitwise Vertical FIM Results:
  Execution Time: 0.5340 seconds
  Memory Used: 72.18 MB
  Frequent Itemsets: 1523
  Candidates Generated: 4581

Speedup (Apriori / Optimized Bitwise): 15.59x
```

This shows performance metrics for one minimum support threshold. The experiment repeats for 0.6, 0.7, 0.8, and 0.9.

### JSON Results Files

Results are saved in JSON format containing:
- Execution time for each algorithm
- Memory consumption
- Number of itemsets found
- Number of candidates generated
- Speedup ratios

Example results_chess.json structure:
```json
{
    "0.5": {
        "apriori": {
            "execution_time": 8.32,
            "memory_used": 187.45,
            "num_itemsets": 1523,
            "num_candidates": 4581
        },
        "bitwise": { ... },
        "bitwise_optimized": { ... },
        "speedup": 15.59
    },
    ...
}
```

## Code Structure Explanation

### apriori.py

Contains three algorithm implementations:

1. **Apriori Class**
   - Classical algorithm from 1994
   - Uses horizontal database representation
   - Generates candidates by joining frequent itemsets
   - Scans database for each candidate level

2. **BitwiseVerticalFIM Class**
   - Contemporary algorithm using vertical bitmaps
   - Converts transactions to bitwise representation
   - Uses AND operations for support counting
   - No database scanning needed

3. **BitwiseVerticalFIMOptimized Class**
   - Extends BitwiseVerticalFIM with optimizations
   - Zero-Skipping: stops AND operations when result is zero
   - Multi-threading: parallelizes candidate evaluation

### experiment_runner.py

Main orchestration script:

- **ExperimentRunner class** handles:
  - Loading datasets
  - Running each algorithm with metrics collection
  - Averaging results over 3 runs
  - Calculating speedup ratios
  - Saving results to JSON

- **main()** function:
  - Defines which datasets to use
  - Defines minimum support thresholds to test
  - Coordinates all experiments
  - Generates output and JSON files

### dataset_loader.py

Utilities for reading datasets:

- **DatasetLoader.load_dataset()** - Opens and parses dataset files
  - Handles gzip compression
  - Returns list of transactions as sets
  
- **DatasetLoader.get_dataset_info()** - Provides statistics
  - Transaction count
  - Unique items
  - Average transaction size

## Metrics Explanation

### Execution Time
The wall-clock time in seconds for the complete algorithm to run. This is the most important metric for comparing algorithm performance.

### Memory Used
Peak RAM consumption in MB. This shows memory efficiency of each approach. Apriori typically uses more memory for candidate storage.

### Frequent Itemsets
Total number of frequent itemsets discovered. Should be identical for all algorithms since they find the same patterns. If different, it indicates a bug.

### Candidates Generated
Number of candidate itemsets evaluated. Should also be identical for all algorithms. Different values would indicate correctness issues.

### Speedup Ratio
How many times faster is the optimized algorithm compared to Apriori. Calculated as:
Speedup = Apriori Time / Optimized Bitwise Time

Higher speedup = better performance improvement.

## Defensive Viva Topics

Be prepared to explain:

1. **Why Apriori Fails on Dense Data**
   - Dense datasets have many frequent items
   - Join operation creates exponential candidates
   - Example: 1000 frequent items creates C(1000,2) = 500,000 pairs
   - Database scanning becomes bottleneck

2. **How Bitwise Vertical Works**
   - Convert transactions to item vertical lists
   - Each item has bitmap of transactions containing it
   - Support = count of 1-bits in AND result
   - Bitwise AND is CPU primitive, very fast

3. **Zero-Skipping Optimization**
   - When AND of two bitmaps = 0, no remaining items can be frequent
   - Skip remaining AND operations
   - Early termination saves CPU cycles
   - Most effective on sparse candidates

4. **Multi-threading Optimization**
   - Candidates are independent (no dependencies)
   - Can evaluate multiple candidates in parallel
   - Use Python threading with thread pool
   - Speedup ~= number of cores used

5. **Memory Efficiency**
   - Apriori stores full candidate lists
   - Bitwise uses bitmaps: 1 bit per item per transaction
   - Example: 1000 items, 10000 transactions = 1.25 MB per level
   - Apriori requires more memory for candidate trees

6. **Time Complexity Analysis**
   - Apriori: O(2^n * |D|) worst case
   - Bitwise: O(p * |c|) per level
   - n = items, D = transactions, p = candidates, c = candidate size

## Troubleshooting

### Dataset Loading Error
"Dataset file not found: chess.dat"
- Check that chess.dat and connect.dat are in the correct directory
- File path should be: d:/GIKI/SEMESTER 06/Design and Analysis of Algorithm/DA Prj/

### Module Import Error
"ModuleNotFoundError: No module named 'psutil'"
- Install psutil: `pip install psutil`

### Results Not Generated
If results files don't appear:
- Check that datasets loaded successfully (first output line)
- Try running with just one dataset first
- Check available disk space for JSON output

### Unexpected Execution Times
- First run may be slower (Python bytecode compilation)
- Background processes can affect timing
- Multiple runs are averaged to reduce variance
- Results should be consistent across runs

## Tips for Success

1. **Run Experiments Early**
   - Takes 10-20 minutes, do not leave for last minute
   - Have results before writing discussion

2. **Save Console Output**
   - Copy console output to document
   - Include sample results in report appendix

3. **Understand the Code**
   - Each team member should understand all algorithms
   - Be ready to explain any function in viva

4. **Practice Viva Explanations**
   - Prepare 2-3 minute explanations for:
     - How each algorithm works
     - Why optimizations help
     - What results mean
   - Practice with team members

5. **Check Results Correctness**
   - All algorithms should find same itemsets
   - Candidate counts should match
   - Speedup should be positive (optimized faster than Apriori)

## Team Responsibility

- **Mohammad Ali (2023326)**: Focus on Apriori implementation and analysis
- **Rafay Akram (2023491)**: Focus on Bitwise Vertical implementation
- **Abdullah Waheed (2023048)**: Focus on optimizations and experiments

All members must understand:
- How to run the code
- Results interpretation
- Theoretical complexity analysis
- Optimization justification

## Final Checklist

Before submission:
- [ ] Code runs successfully
- [ ] Results files generated
- [ ] Report.tex compiles without errors
- [ ] All sections completed
- [ ] Actual experimental data included in report
- [ ] References in IEEE format
- [ ] All team members understand entire project
- [ ] Print and bind hard copy
- [ ] Submit PDF to Google Classroom
- [ ] Submit code via repository link

## Contact Information

For questions about implementation, refer to:
- README.md: Project overview
- Code comments: Implementation details
- Report.tex: Theory and methodology
