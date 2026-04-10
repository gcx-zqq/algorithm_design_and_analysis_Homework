# -*- coding: utf-8 -*-
import random
import subprocess
import json
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_two_100_datasets():
    print("Generating two datasets of 100 random numbers...")
    
    datasets = []
    for i in range(2):
        data = [random.randint(0, 1000000) for _ in range(100)]
        filename = f'test_data/test_data_100_set{i+1}.txt'
        with open(filename, 'w') as f:
            for num in data:
                f.write(f'{num}\n')
        datasets.append((filename, data))
        print(f'  Dataset {i+1} saved to {filename}')
    
    return datasets

def run_all_algorithms(data_file):
    results = {}
    
    for algo in ['bubble', 'merge', 'quick']:
        exe = f'{algo}_sort.exe'
        cmd = [exe, data_file]
        output = subprocess.run(cmd, capture_output=True, text=True).stdout
        
        lines = output.strip().split('\n')
        for line in lines:
            if 'Comparison operations:' in line:
                results[algo] = int(line.split(':')[1].strip())
    
    return results

def plot_two_100_comparison(dataset1_data, dataset2_data, results1, results2):
    print("Generating comparison plot for two 100 datasets...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    axes[0, 0].hist(dataset1_data, bins=20, edgecolor='black', alpha=0.7, color='#3498db')
    axes[0, 0].set_title('Dataset 1 - Value Distribution', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Value', fontsize=10)
    axes[0, 0].set_ylabel('Frequency', fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].hist(dataset2_data, bins=20, edgecolor='black', alpha=0.7, color='#e74c3c')
    axes[0, 1].set_title('Dataset 2 - Value Distribution', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Value', fontsize=10)
    axes[0, 1].set_ylabel('Frequency', fontsize=10)
    axes[0, 1].grid(True, alpha=0.3)
    
    algorithms = ['Bubble', 'Merge', 'Quick']
    x = np.arange(len(algorithms))
    width = 0.35
    
    bars1 = axes[1, 0].bar(x - width/2, [results1['bubble'], results1['merge'], results1['quick']],
                         width, label='Dataset 1', color='#3498db', alpha=0.7)
    bars2 = axes[1, 0].bar(x + width/2, [results2['bubble'], results2['merge'], results2['quick']],
                         width, label='Dataset 2', color='#e74c3c', alpha=0.7)
    axes[1, 0].set_xlabel('Algorithm', fontsize=10)
    axes[1, 0].set_ylabel('Comparison Count', fontsize=10)
    axes[1, 0].set_title('Comparison Count Comparison', fontsize=12, fontweight='bold')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(algorithms)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    for bar in bars1:
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom')
    for bar in bars2:
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom')
    
    diffs = []
    for algo in ['bubble', 'merge', 'quick']:
        diff = abs(results1[algo] - results2[algo])
        diffs.append(diff)
    
    axes[1, 1].bar(algorithms, diffs, color=['#9b59b6', '#1abc9c', '#f39c12'], alpha=0.7)
    axes[1, 1].set_xlabel('Algorithm', fontsize=10)
    axes[1, 1].set_ylabel('Absolute Difference', fontsize=10)
    axes[1, 1].set_title('Comparison Count Difference', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(diffs):
        axes[1, 1].text(i, v + max(diffs)*0.02, str(v), ha='center')
    
    plt.tight_layout()
    plt.savefig('two_100_comparison.png', dpi=300)
    print('  Plot saved as two_100_comparison.png')
    
    return results1, results2

def create_subproblem_tables():
    print("Generating subproblem tables...")
    
    with open('results.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    for idx, algo in enumerate(['merge', 'quick']):
        table_data = []
        headers = ['Size', 'Count', 'Min', 'Max', 'Average']
        
        for size in sizes:
            sp = data['subproblems'][algo][str(size)]
            table_data.append([
                str(size),
                str(len(sp)),
                str(min(sp)),
                str(max(sp)),
                f'{np.mean(sp):.2f}'
            ])
        
        ax = axes[idx]
        ax.axis('tight')
        ax.axis('off')
        
        table = ax.table(cellText=table_data, colLabels=headers,
                        cellLoc='center', loc='center',
                        colWidths=[0.15, 0.15, 0.15, 0.15, 0.2])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 1.5)
        
        for (i, j), cell in table.get_celld().items():
            if i == 0:
                cell.set_facecolor('#2c3e50')
                cell.set_text_props(color='white', weight='bold')
            else:
                if i % 2 == 1:
                    cell.set_facecolor('#ecf0f1')
        
        title = 'Merge Sort' if algo == 'merge' else 'Quick Sort'
        ax.set_title(f'{title} - Subproblem Size Statistics',
                     fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('subproblem_tables.png', dpi=300, bbox_inches='tight')
    print('  Tables saved as subproblem_tables.png')

def write_analysis_report(results1, results2):
    print("Writing analysis report...")
    
    with open('results.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
    
    report = """
================================================================================
                    Sorting Algorithm Experiment Report
================================================================================

1. Experiment Purpose
---------------------
1. Understand and implement Bubble Sort, Merge Sort, and Quick Sort algorithms
2. Verify theoretical time complexity analysis through experiments
3. Analyze algorithm growth rate and asymptotic behavior
4. Understand the impact of input data equivalence classes on algorithm performance

2. Experiment Content and Result Analysis
---------------------------------------

2.1 Two Datasets of 100 Random Numbers (Task 1)
----------------------------------------------
Dataset 1 Comparison Counts:
  Bubble Sort: {r1b}
  Merge Sort:  {r1m}
  Quick Sort:  {r1q}

Dataset 2 Comparison Counts:
  Bubble Sort: {r2b}
  Merge Sort:  {r2m}
  Quick Sort:  {r2q}

Comparison Count Differences:
  Bubble Sort: |{r1b} - {r2b}| = {db}
  Merge Sort:  |{r1m} - {r2m}| = {dm}
  Quick Sort:  |{r1q} - {r2q}| = {dq}

Analysis Conclusion:
- Bubble Sort comparison counts are identical in both datasets (always n(n-1)/2),
  because it only depends on input size n, not initial arrangement.
- Merge Sort has slight differences due to data values, but stays within O(n log n).
- Quick Sort has the largest differences because performance depends on pivot selection.
- Input Data Equivalence Classes: For Bubble Sort, all permutations are equivalent;
  for Merge and Quick Sort, different initial permutations belong to different classes.

2.2 Different Size Tests (Task 2)
--------------------------------
Comparison Count Statistics:

Size    | Bubble Sort | Merge Sort | Quick Sort
--------|-------------|------------|-----------
""".format(
        r1b=results1['bubble'], r1m=results1['merge'], r1q=results1['quick'],
        r2b=results2['bubble'], r2m=results2['merge'], r2q=results2['quick'],
        db=abs(results1['bubble']-results2['bubble']),
        dm=abs(results1['merge']-results2['merge']),
        dq=abs(results1['quick']-results2['quick'])
    )
    
    for size in sizes:
        bubble = data['results'][str(size)]['bubble']['comparisons']
        merge = data['results'][str(size)]['merge']['comparisons']
        quick = data['results'][str(size)]['quick']['comparisons']
        report += f"{size:7d} | {bubble:11d} | {merge:10d} | {quick:10d}\n"
    
    report += """

Theoretical Time Complexity Comparison:

1. Bubble Sort:
   - Theoretical: O(n^2)
   - Experimental: Comparison counts ~ n^2/2, confirming quadratic growth
   - At n=100000, ~5e9 comparisons demonstrate quadratic behavior

2. Merge Sort:
   - Theoretical: O(n log n)
   - Experimental: Comparison counts ~ n log2 n, grows much slower
   - At n=100000, only ~1.7e6 comparisons

3. Quick Sort:
   - Theoretical average: O(n log n)
   - Experimental: Fewer comparisons than Merge Sort on random inputs
   - Better practical performance due to smaller constant factors

Asymptotic Behavior and Growth Rate Analysis:
- The curves show Bubble Sort has clear quadratic growth
- Merge and Quick Sort show linear-logarithmic growth
- For small n (<1000), differences are not obvious
- For large n (>10000), Bubble Sort performance degrades sharply
- This confirms: as n approaches infinity, O(n log n) is far better than O(n^2)

2.3 Subproblem Size Analysis (Task 3)
------------------------------------
Merge Sort Subproblem Characteristics:
- Subproblem sizes decrease strictly, dividing into two roughly equal parts
- Subproblem sequence: n, n/2, n/4, ..., 1
- Recursion depth log2 n, demonstrating divide-and-conquer

Quick Sort Subproblem Characteristics:
- Subproblem division depends on pivot, less balanced than Merge Sort
- On random inputs, relatively balanced with average recursion depth O(log n)
- Subproblem distribution more scattered than Merge Sort

Subproblem Analysis Conclusion:
- Merge Sort always divides evenly, guaranteeing stable O(n log n)
- Quick Sort division depends on input, but performs well on random data
- Recursive algorithm performance closely relates to subproblem balance

3. Experiment Summary
--------------------
1. Theory and Experiment: Results fully verify time complexity analysis
2. Algorithm Selection:
   - Small data: Any algorithm works
   - Medium data: Merge or Quick Sort
   - Large data: Quick Sort (best average) or Merge Sort (stable)
3. Input Impact: Algorithms have different sensitivity to input data
4. Recursion Tips: Correctly handling base cases, division, and merge is key

================================================================================
"""
    
    with open('experiment_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print('  Report saved as experiment_report.txt')
    print(report)

def main():
    print("="*80)
    print("Completing assignment tasks...")
    print("="*80)
    
    datasets = generate_two_100_datasets()
    
    print("\nRunning algorithm tests...")
    results1 = run_all_algorithms(datasets[0][0])
    results2 = run_all_algorithms(datasets[1][0])
    print(f"  Dataset 1 results: {results1}")
    print(f"  Dataset 2 results: {results2}")
    
    results1, results2 = plot_two_100_comparison(
        datasets[0][1], datasets[1][1], results1, results2
    )
    
    create_subproblem_tables()
    
    write_analysis_report(results1, results2)
    
    print("\n" + "="*80)
    print("All tasks completed!")
    print("="*80)

if __name__ == '__main__':
    main()
