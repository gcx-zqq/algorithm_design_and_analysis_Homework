
#include "knapsack.h"

void print_result(Result* res, Item* items) {
    if (res-&gt;total_value &lt; 0) {
        printf("Input size too large for this algorithm.\n");
        return;
    }

    printf("\n========== Result ==========\n");
    printf("Total Value: %.2f\n", res-&gt;total_value);
    printf("Total Weight: %d\n", res-&gt;total_weight);
    printf("Execution Time: %.2f ms\n", res-&gt;time_ms);
    printf("Space Used: %zu bytes\n", res-&gt;space_used);
    printf("Selected Items: %d\n", res-&gt;num_selected);
    printf("Item IDs: ");
    for (int i = 0; i &lt; res-&gt;num_selected &amp;&amp; i &lt; 20; i++) {
        printf("%d ", res-&gt;selected[i]);
    }
    if (res-&gt;num_selected &gt; 20) {
        printf("... (%d total)", res-&gt;num_selected);
    }
    printf("\n");
}

void free_result(Result* res) {
    if (res-&gt;selected) {
        free(res-&gt;selected);
    }
}
