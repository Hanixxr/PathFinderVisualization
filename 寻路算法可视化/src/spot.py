import pygame
from settings import *

# 定义每一个格子的类
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # 计算该格子在屏幕上的实际像素坐标
        # x 对应列(col)，y 对应行(row)
        self.x = row * width
        self.y = col * width
        self.color = WHITE # 初始白色
        self.base_color = WHITE  # 底色，初始白色
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = 1 # 权重默认为1

    def get_pos(self):
        return self.row, self.col

    # --- 状态检查方法 ---
    def is_closed(self):
        return self.color == RED # 已探索

    def is_open(self):
        return self.color == GREEN # 待探索

    def is_barrier(self):
        return self.color == BLACK # 障碍物

    def is_sand(self):
        return self.weight > 1

    def is_start(self):
        return self.color == ORANGE # 起点

    def is_end(self):
        return self.color == TURQUOISE # 终点

    # --- 状态修改方法 ---
    def reset(self):
        """清空网格，恢复默认权重"""
        self.color = WHITE
        self.base_color = WHITE
        self.weight = 1

    def return_to_base_color(self):
        """恢复到底色，不恢复权重"""
        self.color = self.base_color

    def make_start(self):
        self.color = ORANGE
        self.base_color = ORANGE

    def make_barrier(self):
        self.color = BLACK
        self.base_color = BLACK

    def make_sand(self):
        self.weight = 5
        self.color = SAND_COLOR  # 浅褐色
        self.base_color = SAND_COLOR

    def make_end(self):
        self.color = TURQUOISE
        self.base_color = TURQUOISE

    def make_closed(self):
        if not self.is_start() and not self.is_end():
            self.color = RED

    def make_open(self):
        if not self.is_start() and not self.is_end():
            self.color = GREEN

    def make_path(self):
        if not self.is_start() and not self.is_end():
            self.color = PURPLE # 最终路径

    def draw(self, win):
        # 在窗口上画出自己
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        """检查上下左右四个方向，如果不是墙，就加入 neighbors 列表"""
        self.neighbors = []
        directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]
        for direction in directions:
            # 判断边界
            if (0 <= self.row + direction[0] <= self.total_rows - 1
            and 0 <= self.col + direction[1] <= self.total_rows - 1
            and not grid[self.row + direction[0]][self.col + direction[1]].is_barrier()):
                self.neighbors.append(grid[self.row + direction[0]][self.col + direction[1]])