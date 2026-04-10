# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def load_results(filename):
    return pd.read_csv(filename)

def plot_four_time(df, save_path):
    algorithms = ['BruteForce', 'Backtracking', 'Greedy', 'DynamicProgramming']
    colors = ['red', 'blue', 'green', 'orange']
    markers = ['o', 's', '^', 'D']
    
    plt.figure(figsize=(12, 8))
    
    for algo, color, marker in zip(algorithms, colors, markers):
        subset = df[(df['Algorithm'] == algo) & (df['TotalValue'] >= 0)]
        if len(subset) > 0:
            plt.plot(subset['Items'], subset['Time(ms)'], 
                    marker=marker, color=color, label=algo, linewidth=2, markersize=8)
    
    plt.xlabel('Number of Items', fontsize=14)
    plt.ylabel('Execution Time (ms)', fontsize=14)
    plt.title('Four Algorithms Execution Time Comparison (Small Scale, Capacity=10000)', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print('Saved four algorithms time plot to {}'.format(save_path))

def plot_four_value(df, save_path):
    algorithms = ['BruteForce', 'Backtracking', 'Greedy', 'DynamicProgramming']
    colors = ['red', 'blue', 'green', 'orange']
    markers = ['o', 's', '^', 'D']
    
    plt.figure(figsize=(12, 8))
    
    for algo, color, marker in zip(algorithms, colors, markers):
        subset = df[(df['Algorithm'] == algo) & (df['TotalValue'] >= 0)]
        if len(subset) > 0:
            plt.plot(subset['Items'], subset['TotalValue'], 
                    marker=marker, color=color, label=algo, linewidth=2, markersize=8)
    
    plt.xlabel('Number of Items', fontsize=14)
    plt.ylabel('Total Value', fontsize=14)
    plt.title('Four Algorithms Solution Value Comparison (Small Scale, Capacity=10000)', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print('Saved four algorithms value plot to {}'.format(save_path))

def plot_four_space(df, save_path):
    algorithms = ['BruteForce', 'Backtracking', 'Greedy', 'DynamicProgramming']
    colors = ['red', 'blue', 'green', 'orange']
    markers = ['o', 's', '^', 'D']
    
    plt.figure(figsize=(12, 8))
    
    for algo, color, marker in zip(algorithms, colors, markers):
        subset = df[(df['Algorithm'] == algo) & (df['TotalValue'] >= 0)]
        if len(subset) > 0:
            plt.plot(subset['Items'], subset['Space(bytes)'], 
                    marker=marker, color=color, label=algo, linewidth=2, markersize=8)
    
    plt.xlabel('Number of Items', fontsize=14)
    plt.ylabel('Space Used (bytes)', fontsize=14)
    plt.title('Four Algorithms Memory Usage Comparison (Small Scale, Capacity=10000)', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print('Saved four algorithms space plot to {}'.format(save_path))

def plot_two_time(df, save_path):
    algorithms = ['Greedy', 'DynamicProgramming']
    colors = ['green', 'orange']
    markers = ['^', 'D']
    
    plt.figure(figsize=(12, 8))
    
    for algo, color, marker in zip(algorithms, colors, markers):
        subset = df[(df['Algorithm'] == algo) & (df['TotalValue'] >= 0)]
        if len(subset) > 0:
            plt.plot(subset['Items'], subset['Time(ms)'], 
                    marker=marker, color=color, label=algo, linewidth=2, markersize=8)
    
    plt.xlabel('Number of Items', fontsize=14)
    plt.ylabel('Execution Time (ms)', fontsize=14)
    plt.title('Greedy vs Dynamic Programming Execution Time Comparison (Large Scale, Capacity=10000)', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print('Saved two algorithms time plot to {}'.format(save_path))

def plot_two_value(df, save_path):
    algorithms = ['Greedy', 'DynamicProgramming']
    colors = ['green', 'orange']
    markers = ['^', 'D']
    
    plt.figure(figsize=(12, 8))
    
    for algo, color, marker in zip(algorithms, colors, markers):
        subset = df[(df['Algorithm'] == algo) & (df['TotalValue'] >= 0)]
        if len(subset) > 0:
            plt.plot(subset['Items'], subset['TotalValue'], 
                    marker=marker, color=color, label=algo, linewidth=2, markersize=8)
    
    plt.xlabel('Number of Items', fontsize=14)
    plt.ylabel('Total Value', fontsize=14)
    plt.title('Greedy vs Dynamic Programming Solution Value Comparison (Large Scale, Capacity=10000)', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print('Saved two algorithms value plot to {}'.format(save_path))

def plot_two_space(df, save_path):
    algorithms = ['Greedy', 'DynamicProgramming']
    colors = ['green', 'orange']
    markers = ['^', 'D']
    
    plt.figure(figsize=(12, 8))
    
    for algo, color, marker in zip(algorithms, colors, markers):
        subset = df[(df['Algorithm'] == algo) & (df['TotalValue'] >= 0)]
        if len(subset) > 0:
            plt.plot(subset['Items'], subset['Space(bytes)'], 
                    marker=marker, color=color, label=algo, linewidth=2, markersize=8)
    
    plt.xlabel('Number of Items', fontsize=14)
    plt.ylabel('Space Used (bytes)', fontsize=14)
    plt.title('Greedy vs Dynamic Programming Memory Usage Comparison (Large Scale, Capacity=10000)', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print('Saved two algorithms space plot to {}'.format(save_path))

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    plots_dir = os.path.join(project_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    four_file = os.path.join(project_dir, "results", "results_four_algorithms.csv")
    two_file = os.path.join(project_dir, "results", "results_two_algorithms.csv")
    
    if not os.path.exists(four_file):
        print('Results file {} not found!'.format(four_file))
        return
    
    if not os.path.exists(two_file):
        print('Results file {} not found!'.format(two_file))
        return
    
    df_four = load_results(four_file)
    df_two = load_results(two_file)
    
    print('Generating six plots...')
    print('-' * 50)
    
    plot_four_time(df_four, os.path.join(plots_dir, 'four_time.png'))
    plot_four_value(df_four, os.path.join(plots_dir, 'four_value.png'))
    plot_four_space(df_four, os.path.join(plots_dir, 'four_space.png'))
    
    plot_two_time(df_two, os.path.join(plots_dir, 'two_time.png'))
    plot_two_value(df_two, os.path.join(plots_dir, 'two_value.png'))
    plot_two_space(df_two, os.path.join(plots_dir, 'two_space.png'))
    
    print('\n' + '='*50)
    print('All six plots generated successfully!')

if __name__ == "__main__":
    main()
