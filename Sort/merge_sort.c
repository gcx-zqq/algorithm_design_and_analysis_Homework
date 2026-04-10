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

void merge(int* arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    
    int* L = (int*)malloc(n1 * sizeof(int));
    int* R = (int*)malloc(n2 * sizeof(int));
    
    for (int i = 0; i < n1; i++) {
        L[i] = arr[left + i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = arr[mid + 1 + j];
    }
    
    int i = 0, j = 0, k = left;
    
    while (i < n1 && j < n2) {
        comparison_count++;
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }
    
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
    
    free(L);
    free(R);
}

void merge_sort(int* arr, int left, int right) {
    int size = right - left + 1;
    record_subproblem_size(size);
    
    if (left < right) {
        int mid = left + (right - left) / 2;
        merge_sort(arr, left, mid);
        merge_sort(arr, mid + 1, right);
        merge(arr, left, mid, right);
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
    
    merge_sort(arr, 0, size - 1);
    
    printf("Merge Sort\n");
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
