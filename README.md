# 算法设计与分析实验作业

本项目包含排序问题和0-1背包问题的不同求解算法实现与性能分析。

## 目录结构

```
SuanFaSheJiYuFenXi_Homework/
├── Sort/                    # 排序算法实验
├── Bag/                     # 0-1背包问题实验
└── README.md                # 本说明文件
```

## Sort - 排序算法实验

### 实现算法
1. **冒泡排序 (Bubble Sort)**
   - 时间复杂度: O(n?)
   - 比较次数固定为 n(n-1)/2，与输入数据无关

2. **归并排序 (Merge Sort)**
   - 时间复杂度: O(n log n)
   - 稳定排序，分治策略

3. **快速排序 (Quick Sort)**
   - 平均时间复杂度: O(n log n)
   - 最坏时间复杂度: O(n?)
   - 实际性能优秀

### 实验内容
- 不同数据集的比较次数对比
- 不同规模数据的性能测试
- 子问题规模分析

### 主要文件
- `bubble_sort.c` - 冒泡排序实现
- `merge_sort.c` - 归并排序实现
- `quick_sort.c` - 快速排序实现
- `experiment_report.txt` - 实验报告

## Bag - 0-1背包问题实验

### 实现算法
1. **蛮力法 (Brute Force)**
   - 时间复杂度: O(2?)
   - 仅适用于 n ≤ 20 的小规模问题

2. **动态规划法 (Dynamic Programming)**
   - 时间复杂度: O(n×C)，C为背包容量
   - 空间复杂度: O(n×C)
   - 能得到全局最优解

3. **贪心法 (Greedy)**
   - 时间复杂度: O(n log n)
   - 不能保证得到最优解，但速度最快

4. **回溯法 (Backtracking)**
   - 时间复杂度: O(2?)，通过剪枝通常比蛮力法快
   - 适用于 n ≤ 30 的中等规模问题

### 主要文件
- `src/brute_force.c` - 蛮力法C实现
- `src/dynamic_programming.c` - 动态规划C实现
- `src/greedy.c` - 贪心法C实现
- `src/backtracking.c` - 回溯法C实现
- `data/` - 测试数据
- `results/` - 测试结果
- `plots/` - 性能对比图表

---

## 上传GitHub步骤

### 1. 初始化Git仓库
在项目目录下打开终端，执行：
```bash
git init
```

### 2. 配置用户信息（首次使用Git需要）
```bash
git config user.name "你的用户名"
git config user.email "你的邮箱"
```

### 3. 添加文件到暂存区
```bash
git add .
```

### 4. 提交文件
```bash
git commit -m "Initial commit: 排序算法和0-1背包问题实验"
```

### 5. 在GitHub上创建新仓库
1. 访问 https://github.com 并登录
2. 点击右上角的 "+" → "New repository"
3. 填写仓库名称（例如：SuanFaSheJiYuFenXi_Homework）
4. 选择 Public 或 Private
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 6. 关联远程仓库并推送
```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

### 7. 后续更新（如果有修改）
```bash
git add .
git commit -m "更新说明"
git push
```
