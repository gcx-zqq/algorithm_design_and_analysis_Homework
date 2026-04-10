#include <stdio.h>
#include <stdlib.h>

long long comparison_count = 0;
int* subproblem_sizes = NULL;
int subproblem_count = 0;
int subproblem_capacity = 1000;

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

void record_subproblem_size(int size) {
    if (subproblem_count >= subproblem_capacity) {
        subproblem_capacity *= 2;
        subproblem_sizes = (int*)realloc(subproblem_sizes, subproblem_capacity * sizeof(int));
    }
    subproblem_sizes[subproblem_count++] = size;
}

void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int partition(int* arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        comparison_count++;
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void quick_sort(int* arr, int low, int high) {
    int size = high - low + 1;
    record_subproblem_size(size);
    
    if (low < high) {
        int pi = partition(arr, low, high);
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <test_data_file>\n", argv[0]);
        return 1;
    }
    
    subproblem_sizes = (int*)malloc(subproblem_capacity * sizeof(int));
    
    int size;
    int* arr = read_data_from_file(argv[1], &size);
    if (!arr) {
        free(subproblem_sizes);
        return 1;
    }
    
    comparison_count = 0;
    subproblem_count = 0;
    
    quick_sort(arr, 0, size - 1);
    
    printf("Quick Sort\n");
    printf("Data size: %d\n", size);
    printf("Comparison operations: %lld\n", comparison_count);
    printf("Subproblem sizes:\n");
    for (int i = 0; i < subproblem_count; i++) {
        printf("%d ", subproblem_sizes[i]);
    }
    printf("\n");
    
    free(arr);
    free(subproblem_sizes);
    return 0;
}
