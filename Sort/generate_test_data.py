import random
import os

def generate_test_data(sizes, directory='test_data'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for size in sizes:
        filename = os.path.join(directory, f'test_data_{size}.txt')
        data = [random.randint(0, 1000000) for _ in range(size)]
        
        with open(filename, 'w') as f:
            for num in data:
                f.write(f'{num}\n')
        
        print(f'Generated {filename} with {size} numbers')

if __name__ == '__main__':
    sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
    generate_test_data(sizes)
