
#include "knapsack.h"

Item* read_items_from_csv(const char* filename, int* n) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("Cannot open file: %s\n", filename);
        return NULL;
    }

    char line[256];
    int count = 0;

    while (fgets(line, sizeof(line), file)) {
        if (count &gt; 0) {
            (*n)++;
        }
        count++;
    }

    rewind(file);

    Item* items = (Item*)malloc(*n * sizeof(Item));
    count = 0;
    int index = 0;

    while (fgets(line, sizeof(line), file)) {
        if (count &gt; 0) {
            int id, weight;
            double value;
            sscanf(line, "%d,%d,%lf", &amp;id, &amp;weight, &amp;value);
            items[index].id = id;
            items[index].weight = weight;
            items[index].value = value;
            index++;
        }
        count++;
    }

    fclose(file);
    return items;
}

void save_result_to_csv(FILE* fp, const char* algorithm, int n, int capacity, Result* res) {
    fprintf(fp, "%s,%d,%d,%.2f,%d,%.2f,%zu,%d\n",
            algorithm, n, capacity,
            res-&gt;total_value &gt;= 0 ? res-&gt;total_value : -1,
            res-&gt;total_weight,
            res-&gt;time_ms,
            res-&gt;space_used,
            res-&gt;num_selected);
}

int main() {
    int item_counts[] = {10, 15, 20, 1000, 2000, 5000, 10000};
    int capacities[] = {10000, 100000};
    int num_item_counts = sizeof(item_counts) / sizeof(item_counts[0]);
    int num_capacities = sizeof(capacities) / sizeof(capacities[0]);

    FILE* result_file = fopen("results/results.csv", "w");
    if (!result_file) {
        printf("Cannot create result file\n");
        return 1;
    }
    fprintf(result_file, "Algorithm,Items,Capacity,TotalValue,TotalWeight,Time(ms),Space(bytes),SelectedCount\n");

    for (int c_idx = 0; c_idx &lt; num_capacities; c_idx++) {
        int capacity = capacities[c_idx];
        for (int n_idx = 0; n_idx &lt; num_item_counts; n_idx++) {
            int n = item_counts[n_idx];
            char csv_filename[256];
            sprintf(csv_filename, "data/knapsack_n%d_c%d.csv", n, capacity);

            printf("\n========================================\n");
            printf("Items: %d, Capacity: %d\n", n, capacity);
            printf("Data file: %s\n", csv_filename);

            int num_items = 0;
            Item* items = read_items_from_csv(csv_filename, &amp;num_items);
            if (!items || num_items != n) {
                printf("Using randomly generated data...\n");
                srand(n * capacity);
                items = (Item*)malloc(n * sizeof(Item));
                for (int i = 0; i &lt; n; i++) {
                    items[i].id = i + 1;
                    items[i].weight = rand() % 100 + 1;
                    items[i].value = 100.0 + (rand() % 90001) / 100.0;
                }
                num_items = n;
            }

            printf("\n--- Brute Force ---\n");
            Result res_brute = brute_force(items, num_items, capacity);
            print_result(&amp;res_brute, items);
            save_result_to_csv(result_file, "BruteForce", n, capacity, &amp;res_brute);
            free_result(&amp;res_brute);

            printf("\n--- Backtracking ---\n");
            Result res_backtrack = backtracking(items, num_items, capacity);
            print_result(&amp;res_backtrack, items);
            save_result_to_csv(result_file, "Backtracking", n, capacity, &amp;res_backtrack);
            free_result(&amp;res_backtrack);

            printf("\n--- Greedy ---\n");
            Result res_greedy = greedy(items, num_items, capacity);
            print_result(&amp;res_greedy, items);
            save_result_to_csv(result_file, "Greedy", n, capacity, &amp;res_greedy);
            free_result(&amp;res_greedy);

            printf("\n--- Dynamic Programming ---\n");
            if ((long long)n * (long long)capacity &lt;= 100000000) {
                Result res_dp = dynamic_programming(items, num_items, capacity);
                print_result(&amp;res_dp, items);
                save_result_to_csv(result_file, "DynamicProgramming", n, capacity, &amp;res_dp);
                free_result(&amp;res_dp);
            } else {
                printf("Size too large, skipping DP\n");
                fprintf(result_file, "DynamicProgramming,%d,%d,-1,0,0,0,0\n", n, capacity);
            }

            free(items);
        }
    }

    fclose(result_file);
    printf("\nAll tests completed! Results saved to results/results.csv\n");

    return 0;
}
