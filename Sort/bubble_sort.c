#include <stdio.h>
#include <stdlib.h>

int* read_data_from_file(const char* filename, int* size) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("Failed to open file %s\n", filename);
        return NULL;
    }
    
    int count = 0;
    int temp;
    while (fscanf(file, "%d", &temp) == 1) {
        count++;
    }
    rewind(file);
    
    int* arr = (int*)malloc(count * sizeof(int));
    if (!arr) {
        printf("Memory allocation failed\n");
        fclose(file);
        return NULL;
    }
    
    for (int i = 0; i < count; i++) {
        fscanf(file, "%d", &arr[i]);
    }
    
    fclose(file);
    *size = count;
    return arr;
}

long long bubble_sort(int* arr, int size) {
    long long comparisons = 0;
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            comparisons++;
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    return comparisons;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <test_data_file>\n", argv[0]);
        return 1;
    }
    
    int size;
    int* arr = read_data_from_file(argv[1], &size);
    if (!arr) {
        return 1;
    }
    
    long long comparisons = bubble_sort(arr, size);
    
    printf("Bubble Sort\n");
    printf("Data size: %d\n", size);
    printf("Comparison operations: %lld\n", comparisons);
    
    free(arr);
    return 0;
}
