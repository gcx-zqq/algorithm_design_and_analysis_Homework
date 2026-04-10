import subprocess
import os
import json
import matplotlib.pyplot as plt
import numpy as np

def compile_c_program(source_file, output_file):
    cmd = ['gcc', '-o', output_file, source_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'Compilation failed for {source_file}')
        print(result.stderr)
        return False
    print(f'Compiled {source_file} successfully')
    return True

def run_sort_program(program, data_file):
    cmd = [program, data_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def parse_output(output):
    lines = output.strip().split('\n')
    data = {}
    
    for line in lines:
        if 'Data size:' in line:
            data['size'] = int(line.split(':')[1].strip())
        elif 'Comparison operations:' in line:
            data['comparisons'] = int(line.split(':')[1].strip())
        elif 'Subproblem sizes:' in line:
            idx = lines.index(line)
            if idx + 1 < len(lines):
                sizes_line = lines[idx + 1].strip()
                if sizes_line:
                    data['subproblems'] = list(map(int, sizes_line.split()))
    
    return data

def main():
    sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
    programs = {
        'bubble': 'bubble_sort.exe',
        'merge': 'merge_sort.exe',
        'quick': 'quick_sort.exe'
    }
    
    source_files = {
        'bubble': 'bubble_sort.c',
        'merge': 'merge_sort.c',
        'quick': 'quick_sort.c'
    }
    
    for name, src in source_files.items():
        if not compile_c_program(src, programs[name]):
            return
    
    results = {}
    all_subproblems = {'merge': {}, 'quick': {}}
    
    for size in sizes:
        data_file = f'test_data/test_data_{size}.txt'
        print(f'\nTesting size {size}...')
        
        results[size] = {}
        
        for name, prog in programs.items():
            output = run_sort_program(prog, data_file)
            parsed = parse_output(output)
            results[size][name] = parsed
            
            if name in ['merge', 'quick'] and 'subproblems' in parsed:
                all_subproblems[name][size] = parsed['subproblems']
    
    with open('results.json', 'w') as f:
        json.dump({'results': results, 'subproblems': all_subproblems}, f, indent=2)
    
    plot_comparison_chart(results, sizes)
    plot_subproblem_charts(all_subproblems)
    
    print('\nAnalysis complete!')
    print('Results saved to results.json')
    print('Charts saved as comparison_chart.png, merge_subproblems.png, quick_subproblems.png')

def plot_comparison_chart(results, sizes):
    bubble = [results[s]['bubble']['comparisons'] for s in sizes]
    merge = [results[s]['merge']['comparisons'] for s in sizes]
    quick = [results[s]['quick']['comparisons'] for s in sizes]
    
    plt.figure(figsize=(12, 7))
    
    plt.plot(sizes, bubble, marker='o', label='Bubble Sort', linewidth=2, color='#e74c3c')
    plt.plot(sizes, merge, marker='s', label='Merge Sort', linewidth=2, color='#3498db')
    plt.plot(sizes, quick, marker='^', label='Quick Sort', linewidth=2, color='#2ecc71')
    
    plt.xscale('log')
    plt.yscale('log')
    
    plt.xlabel('Data Size', fontsize=12)
    plt.ylabel('Comparison Operations', fontsize=12)
    plt.title('Comparison of Sorting Algorithms - Comparison Operations', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('comparison_chart.png', dpi=300)
    print('Saved comparison_chart.png')

def plot_subproblem_charts(all_subproblems):
    plot_subproblem_single(all_subproblems['merge'], 'Merge Sort', 'merge_subproblems.png')
    plot_subproblem_single(all_subproblems['quick'], 'Quick Sort', 'quick_subproblems.png')

def plot_subproblem_single(subproblems, title, filename):
    sizes = sorted(subproblems.keys())
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    for i, size in enumerate(sizes):
        sp = subproblems[size]
        axes[i].hist(sp, bins=20, edgecolor='black', alpha=0.7)
        axes[i].set_title(f'Size {size}', fontsize=10)
        axes[i].set_xlabel('Subproblem Size', fontsize=8)
        axes[i].set_ylabel('Frequency', fontsize=8)
        axes[i].grid(True, alpha=0.3)
    
    for j in range(len(sizes), len(axes)):
        axes[j].axis('off')
    
    plt.suptitle(f'{title} - Subproblem Sizes Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    plt.savefig(filename, dpi=300)
    print(f'Saved {filename}')

if __name__ == '__main__':
    main()
