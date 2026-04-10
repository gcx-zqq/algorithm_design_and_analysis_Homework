# -*- coding: utf-8 -*-
import time
import csv
import os
import random
import pandas as pd

class Item:
    def __init__(self, item_id, weight, value):
        self.id = item_id
        self.weight = weight
        self.value = value

class Result:
    def __init__(self):
        self.selected = []
        self.total_value = 0.0
        self.total_weight = 0
        self.time_ms = 0.0
        self.space_used = 0

def greedy(items, capacity):
    result = Result()
    start_time = time.time()
    
    n = len(items)
    sorted_items = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
    
    remaining = capacity
    for item in sorted_items:
        if item.weight <= remaining:
            result.selected.append(item.id)
            result.total_value += item.value
            result.total_weight += item.weight
            remaining -= item.weight
    
    result.space_used = n * (4 + 8 + 4)
    result.time_ms = (time.time() - start_time) * 1000
    return result

def dynamic_programming(items, capacity):
    result = Result()
    start_time = time.time()
    
    n = len(items)
    dp = [0.0] * (capacity + 1)
    keep = [[False] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for w in range(capacity, items[i].weight - 1, -1):
            if dp[w - items[i].weight] + items[i].value > dp[w]:
                dp[w] = dp[w - items[i].weight] + items[i].value
                keep[i + 1][w] = True
    
    result.total_value = dp[capacity]
    
    w = capacity
    for i in range(n, 0, -1):
        if keep[i][w]:
            result.selected.append(items[i - 1].id)
            w -= items[i - 1].weight
            result.total_weight += items[i - 1].weight
    
    result.space_used = (capacity + 1) * 8 + (n + 1) * (capacity + 1)
    result.time_ms = (time.time() - start_time) * 1000
    return result

def brute_force(items, capacity):
    result = Result()
    start_time = time.time()
    
    n = len(items)
    if n > 20:
        result.total_value = -1
        result.time_ms = (time.time() - start_time) * 1000
        return result
    
    best_value = 0.0
    best_weight = 0
    best_mask = 0
    
    for mask in range(0, 1 << n):
        current_value = 0.0
        current_weight = 0
        
        for i in range(n):
            if mask & (1 << i):
                current_weight += items[i].weight
                current_value += items[i].value
        
        if current_weight <= capacity and current_value > best_value:
            best_value = current_value
            best_weight = current_weight
            best_mask = mask
    
    result.total_value = best_value
    result.total_weight = best_weight
    for i in range(n):
        if best_mask & (1 << i):
            result.selected.append(items[i].id)
    
    result.space_used = n * 4
    result.time_ms = (time.time() - start_time) * 1000
    return result

def backtracking(items, capacity):
    result = Result()
    start_time = time.time()
    
    n = len(items)
    if n > 30:
        result.total_value = -1
        result.time_ms = (time.time() - start_time) * 1000
        return result
    
    sorted_items = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
    
    best_value = [0.0]
    best_weight = [0]
    best_selected = [False] * n
    current_selected = [False] * n
    
    def bound(i, current_weight, current_value):
        bound_val = current_value
        remaining = capacity - current_weight
        
        while i < n and sorted_items[i].weight <= remaining:
            remaining -= sorted_items[i].weight
            bound_val += sorted_items[i].value
            i += 1
        
        if i < n:
            bound_val += remaining * sorted_items[i].value / sorted_items[i].weight
        
        return bound_val
    
    def backtrack(i, current_weight, current_value):
        if current_value > best_value[0]:
            best_value[0] = current_value
            best_weight[0] = current_weight
            for j in range(n):
                best_selected[j] = current_selected[j]
        
        if i >= n:
            return
        
        if bound(i, current_weight, current_value) > best_value[0]:
            if current_weight + sorted_items[i].weight <= capacity:
                current_selected[i] = True
                backtrack(i + 1, current_weight + sorted_items[i].weight, current_value + sorted_items[i].value)
                current_selected[i] = False
            backtrack(i + 1, current_weight, current_value)
    
    backtrack(0, 0, 0.0)
    
    result.total_value = best_value[0]
    result.total_weight = best_weight[0]
    for i in range(n):
        if best_selected[i]:
            result.selected.append(sorted_items[i].id)
    
    result.space_used = n * 3
    result.time_ms = (time.time() - start_time) * 1000
    return result

def read_items_from_csv(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            item_id = int(row[0])
            weight = int(row[1])
            value = float(row[2])
            items.append(Item(item_id, weight, value))
    return items

def print_result(algorithm, result):
    print("========== " + algorithm + " ==========")
    if result.total_value < 0:
        print("Input size too large for this algorithm.")
        return
    print("Total Value: {:.2f}".format(result.total_value))
    print("Total Weight: {}".format(result.total_weight))
    print("Execution Time: {:.4f} ms".format(result.time_ms))
    print("Space Used: {} bytes".format(result.space_used))
    print("Selected Items: {}".format(len(result.selected)))

def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False, encoding='utf-8')

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    results_dir = os.path.join(project_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    
    small_results = []
    small_item_counts = [10, 15, 20]
    small_capacity = 10000
    
    print("="*60)
    print("Testing small-scale data with four algorithms...")
    print("="*60)
    
    for n in small_item_counts:
        csv_filename = os.path.join(project_dir, "data", "knapsack_n{}_c{}.csv".format(n, small_capacity))
        
        print("\n" + "="*60)
        print("Items: {}, Capacity: {}".format(n, small_capacity))
        print("Data file: {}".format(csv_filename))
        
        if not os.path.exists(csv_filename):
            print("Data file not found, skipping...")
            continue
        
        items = read_items_from_csv(csv_filename)
        
        print("\n--- Brute Force ---")
        res_brute = brute_force(items, small_capacity)
        print_result("Brute Force", res_brute)
        small_results.append({
            'Category': 'FourAlgorithms',
            'Algorithm': 'BruteForce',
            'Items': n,
            'Capacity': small_capacity,
            'TotalValue': res_brute.total_value if res_brute.total_value >= 0 else -1,
            'TotalWeight': res_brute.total_weight,
            'Time(ms)': res_brute.time_ms,
            'Space(bytes)': res_brute.space_used,
            'SelectedCount': len(res_brute.selected)
        })
        
        print("\n--- Backtracking ---")
        res_backtrack = backtracking(items, small_capacity)
        print_result("Backtracking", res_backtrack)
        small_results.append({
            'Category': 'FourAlgorithms',
            'Algorithm': 'Backtracking',
            'Items': n,
            'Capacity': small_capacity,
            'TotalValue': res_backtrack.total_value if res_backtrack.total_value >= 0 else -1,
            'TotalWeight': res_backtrack.total_weight,
            'Time(ms)': res_backtrack.time_ms,
            'Space(bytes)': res_backtrack.space_used,
            'SelectedCount': len(res_backtrack.selected)
        })
        
        print("\n--- Greedy ---")
        res_greedy = greedy(items, small_capacity)
        print_result("Greedy", res_greedy)
        small_results.append({
            'Category': 'FourAlgorithms',
            'Algorithm': 'Greedy',
            'Items': n,
            'Capacity': small_capacity,
            'TotalValue': res_greedy.total_value,
            'TotalWeight': res_greedy.total_weight,
            'Time(ms)': res_greedy.time_ms,
            'Space(bytes)': res_greedy.space_used,
            'SelectedCount': len(res_greedy.selected)
        })
        
        print("\n--- Dynamic Programming ---")
        res_dp = dynamic_programming(items, small_capacity)
        print_result("Dynamic Programming", res_dp)
        small_results.append({
            'Category': 'FourAlgorithms',
            'Algorithm': 'DynamicProgramming',
            'Items': n,
            'Capacity': small_capacity,
            'TotalValue': res_dp.total_value,
            'TotalWeight': res_dp.total_weight,
            'Time(ms)': res_dp.time_ms,
            'Space(bytes)': res_dp.space_used,
            'SelectedCount': len(res_dp.selected)
        })
    
    save_results_to_csv(small_results, os.path.join(results_dir, "results_four_algorithms.csv"))
    
    large_results = []
    large_capacity = 10000
    large_item_counts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
    
    print("\n" + "="*60)
    print("Testing large-scale data (Capacity=10000) with greedy and DP...")
    print("="*60)
    
    for n in large_item_counts:
        csv_filename = os.path.join(project_dir, "data", "knapsack_n{}_c{}.csv".format(n, large_capacity))
        
        print("\n" + "="*60)
        print("Items: {}, Capacity: {}".format(n, large_capacity))
        print("Data file: {}".format(csv_filename))
        
        if not os.path.exists(csv_filename):
            print("Data file not found, skipping...")
            continue
        
        items = read_items_from_csv(csv_filename)
        
        print("\n--- Greedy ---")
        res_greedy = greedy(items, large_capacity)
        print_result("Greedy", res_greedy)
        large_results.append({
            'Category': 'TwoAlgorithms',
            'Algorithm': 'Greedy',
            'Items': n,
            'Capacity': large_capacity,
            'TotalValue': res_greedy.total_value,
            'TotalWeight': res_greedy.total_weight,
            'Time(ms)': res_greedy.time_ms,
            'Space(bytes)': res_greedy.space_used,
            'SelectedCount': len(res_greedy.selected)
        })
        
        print("\n--- Dynamic Programming ---")
        res_dp = dynamic_programming(items, large_capacity)
        print_result("Dynamic Programming", res_dp)
        large_results.append({
            'Category': 'TwoAlgorithms',
            'Algorithm': 'DynamicProgramming',
            'Items': n,
            'Capacity': large_capacity,
            'TotalValue': res_dp.total_value,
            'TotalWeight': res_dp.total_weight,
            'Time(ms)': res_dp.time_ms,
            'Space(bytes)': res_dp.space_used,
            'SelectedCount': len(res_dp.selected)
        })
    
    save_results_to_csv(large_results, os.path.join(results_dir, "results_two_algorithms.csv"))
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("  - results/results_four_algorithms.csv")
    print("  - results/results_two_algorithms.csv")

if __name__ == "__main__":
    main()
