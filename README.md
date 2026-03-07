# Pathfinding Algorithm Visualization (A\* / Dijkstra / BFS)

A grid-based pathfinding visualization tool built with **Pygame**.\
It demonstrates three classic algorithms --- **A\***, **Dijkstra**, and
**BFS** --- allowing users to visually compare their exploration
processes and efficiency.

# 1. Environment Setup

## Prerequisites

-   Python 3.8+
-   Pygame library

## Installation

1.  Clone or download this repository to your local machine.
2.  Open a terminal and navigate to the project root directory.
3.  Install the required dependency:

``` bash
pip install pygame
```

# 2. Running the Program

Run the `main` file:

``` bash
python main.py
```

If the interactive window opens successfully, the program is running
correctly.

# 3. Features and Usage

## Mouse Controls

### Left Click

-   First click: Set the **start node** (orange)
-   Second click: Set the **end node** (cyan)
-   Subsequent clicks: Place **obstacles** (black)

When **Sand Mode** is enabled:

-   Subsequent clicks place **sand tiles** (brown)

Holding and dragging the mouse allows continuous placement.

### Right Click

-   Clear cells from the grid
-   Supports click-and-drag for continuous clearing

## Sand Mode

-   **Disabled**: Each grid cell has a default weight of **1**
-   **Enabled**: You can place weighted cells (**sand tiles**, brown)

For simplicity, sand tiles have a **weight of 5**.

## Running Algorithms

After placing the **start node** and **end node**, select an algorithm
to run.

The visualization will display:

-   **Purple** --- Final shortest path
-   **Red** --- Explored nodes
-   **Green** --- Nodes queued for exploration

## Clear Path

After an algorithm finishes:

-   Clicking **Clear Path** removes exploration colors (red and green)
-   The **start node, end node, obstacles, and sand tiles remain
    unchanged**

## Clear Grid

Clears the entire grid and resets it to the initial **white state**.

## Replay Feature

After the algorithm execution is completed:

-   Use the **progress bar** to review each step
-   Supports **pause** and **play**
-   Allows step-by-step replay of the algorithm process

# 4. Algorithms Included

-   **A\*** Search
-   **Dijkstra's Algorithm**
-   **Breadth-First Search (BFS)**

These algorithms can be visually compared through their exploration
patterns and efficiency.

# 5. Technology Stack

-   **Python**
-   **Pygame**

# 6. Project Purpose
This project is designed to help users better understand how classical
pathfinding algorithms work through visualization and interactive
experimentation.

------------------------------------------------------------

# 寻路算法可视化（A* / Dijkstra / BFS）
基于 Pygame 实现的网格寻路算法可视化工具，支持 A*、Dijkstra、BFS 三种算法的路径搜索演示，可直观对比不同算法的探索过程和效率。

## 1. 环境安装
### 前置条件
- Python 3.8+
- Pygame 库

### 安装步骤
1. 克隆/下载本项目到本地；
2. 打开终端，进入项目根目录；
3. 安装依赖：
   ```bash
   pip install pygame
   
## 2. 运行
运行`main`文件，正常弹出交互窗口说明运行成功。

## 3. 功能示例
**鼠标左键**：第一次点击布置起点（橙色），第二次点击布置终点（青色），之后的点击布置障碍（黑色），当沙地模式开启时，之后的点击布置沙地（褐色），支持长按拖动连续布置。

**鼠标右键**：清除网格，支持长按拖动连续清除。

**沙地模式**：关闭时，每个格子的权重默认为1；开启时，可布置带权重的格子（褐色）（简单起见，沙地的权重设置为5）。

**运行算法**：布置好起点和终点后，点击某一算法，会自动运行并给出最短路径（紫色），红色的表示已经探索的格子，绿色的表示准备探索的格子。

**清除路径**：算法运行一次后，点击清除路径按钮，会将探索过程中的染成红色和绿色的格子恢复成原来的颜色，保留起点、终点、障碍和沙地。

**清空网格**：清空全部的网格，恢复成白色。


**回放**：算法执行完成后，可以拖动进度条，进行回溯，查看每一步的结果，以及暂停/播放。
