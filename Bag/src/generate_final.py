# -*- coding: utf-8 -*-
import csv
import random
import os

def generate_knapsack_data(num_items, capacity, seed=42):
    random.seed(seed)
    data = []
    for i in range(1, num_items + 1):
        weight = random.randint(1, 100)
        value = round(random.uniform(100, 1000), 2)
        data.append((i, weight, value))
    return data

def save_to_csv(data, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ItemID', 'Weight', 'Value'])
        writer.writerows(data)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    small_item_counts = [10, 15, 20]
    small_capacity = 10000
    
    print("Generating small-scale data for four algorithms...")
    for idx, n in enumerate(small_item_counts):
        print(f"  Generating: items={n}, capacity={small_capacity}")
        data = generate_knapsack_data(n, small_capacity, seed=idx + 100)
        filename = f"knapsack_n{n}_c{small_capacity}.csv"
        filepath = os.path.join(data_dir, filename)
        save_to_csv(data, filepath)
    
    large_config = {
        10000: [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000],
        100000: [10000, 20000, 40000, 80000],
        1000000: [160000, 320000]
    }
    
    print("\nGenerating large-scale data for greedy and DP...")
    seed_idx = 200
    for capacity, item_counts in large_config.items():
        for n in item_counts:
            print(f"  Generating: items={n}, capacity={capacity}")
            data = generate_knapsack_data(n, capacity, seed=seed_idx)
            filename = f"knapsack_n{n}_c{capacity}.csv"
            filepath = os.path.join(data_dir, filename)
            save_to_csv(data, filepath)
            seed_idx += 1
    
    print("\nData generation complete!")

if __name__ == "__main__":
    main()
