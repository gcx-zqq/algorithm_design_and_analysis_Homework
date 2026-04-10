
#include "knapsack.h"

typedef struct {
    Item* items;
    int n;
    int capacity;
    double best_value;
    int best_weight;
    int* best_selected;
    int* current_selected;
} BacktrackContext;

double bound(BacktrackContext* ctx, int i, int current_weight, double current_value) {
    double bound_val = current_value;
    int remaining = ctx-&gt;capacity - current_weight;

    while (i &lt; ctx-&gt;n &amp;&amp; ctx-&gt;items[i].weight &lt;= remaining) {
        remaining -= ctx-&gt;items[i].weight;
        bound_val += ctx-&gt;items[i].value;
        i++;
    }

    if (i &lt; ctx-&gt;n) {
        bound_val += (double)remaining * ctx-&gt;items[i].value / ctx-&gt;items[i].weight;
    }

    return bound_val;
}

void backtrack(BacktrackContext* ctx, int i, int current_weight, double current_value) {
    if (current_value &gt; ctx-&gt;best_value) {
        ctx-&gt;best_value = current_value;
        ctx-&gt;best_weight = current_weight;
        for (int j = 0; j &lt; ctx-&gt;n; j++) {
            ctx-&gt;best_selected[j] = ctx-&gt;current_selected[j];
        }
    }

    if (i &gt;= ctx-&gt;n) {
        return;
    }

    if (bound(ctx, i, current_weight, current_value) &gt; ctx-&gt;best_value) {
        if (current_weight + ctx-&gt;items[i].weight &lt;= ctx-&gt;capacity) {
            ctx-&gt;current_selected[i] = 1;
            backtrack(ctx, i + 1, current_weight + ctx-&gt;items[i].weight, current_value + ctx-&gt;items[i].value);
            ctx-&gt;current_selected[i] = 0;
        }
        backtrack(ctx, i + 1, current_weight, current_value);
    }
}

int compare_greedy(const void* a, const void* b) {
    Item* itemA = (Item*)a;
    Item* itemB = (Item*)b;
    double ratioA = itemA-&gt;value / itemA-&gt;weight;
    double ratioB = itemB-&gt;value / itemB-&gt;weight;
    if (ratioB &gt; ratioA) return 1;
    if (ratioB &lt; ratioA) return -1;
    return 0;
}

Result backtracking(Item* items, int n, int capacity) {
    Result res;
    res.selected = (int*)malloc(n * sizeof(int));
    res.num_selected = 0;
    res.total_value = 0;
    res.total_weight = 0;

    clock_t start = clock();

    if (n &gt; 30) {
        res.time_ms = 0;
        res.total_value = -1;
        clock_t end = clock();
        res.time_ms = ((double)(end - start)) * 1000.0 / CLOCKS_PER_SEC;
        res.space_used = sizeof(int) * n;
        return res;
    }

    Item* sorted_items = (Item*)malloc(n * sizeof(Item));
    memcpy(sorted_items, items, n * sizeof(Item));
    qsort(sorted_items, n, sizeof(Item), compare_greedy);

    BacktrackContext ctx;
    ctx.items = sorted_items;
    ctx.n = n;
    ctx.capacity = capacity;
    ctx.best_value = 0;
    ctx.best_weight = 0;
    ctx.best_selected = (int*)calloc(n, sizeof(int));
    ctx.current_selected = (int*)calloc(n, sizeof(int));

    res.space_used = sizeof(int) * n * 3 + n * sizeof(Item);

    backtrack(&amp;ctx, 0, 0, 0);

    res.total_value = ctx.best_value;
    res.total_weight = ctx.best_weight;
    for (int i = 0; i &lt; n; i++) {
        if (ctx.best_selected[i]) {
            res.selected[res.num_selected++] = sorted_items[i].id;
        }
    }

    free(sorted_items);
    free(ctx.best_selected);
    free(ctx.current_selected);

    clock_t end = clock();
    res.time_ms = ((double)(end - start)) * 1000.0 / CLOCKS_PER_SEC;

    return res;
}
