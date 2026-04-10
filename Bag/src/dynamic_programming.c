
#include "knapsack.h"

Result dynamic_programming(Item* items, int n, int capacity) {
    Result res;
    res.selected = (int*)malloc(n * sizeof(int));
    res.num_selected = 0;
    res.total_value = 0;
    res.total_weight = 0;

    clock_t start = clock();

    double* dp = (double*)malloc((capacity + 1) * sizeof(double));
    int** keep = (int**)malloc((n + 1) * sizeof(int*));
    for (int i = 0; i &lt;= n; i++) {
        keep[i] = (int*)calloc(capacity + 1, sizeof(int));
    }

    res.space_used = (capacity + 1) * sizeof(double) + (n + 1) * (capacity + 1) * sizeof(int);

    for (int i = 0; i &lt;= capacity; i++) {
        dp[i] = 0;
    }

    for (int i = 0; i &lt; n; i++) {
        for (int w = capacity; w &gt;= items[i].weight; w--) {
            if (dp[w - items[i].weight] + items[i].value &gt; dp[w]) {
                dp[w] = dp[w - items[i].weight] + items[i].value;
                keep[i + 1][w] = 1;
            }
        }
    }

    res.total_value = dp[capacity];

    int w = capacity;
    for (int i = n; i &gt; 0; i--) {
        if (keep[i][w]) {
            res.selected[res.num_selected++] = items[i - 1].id;
            w -= items[i - 1].weight;
            res.total_weight += items[i - 1].weight;
        }
    }

    free(dp);
    for (int i = 0; i &lt;= n; i++) {
        free(keep[i]);
    }
    free(keep);

    clock_t end = clock();
    res.time_ms = ((double)(end - start)) * 1000.0 / CLOCKS_PER_SEC;

    return res;
}
