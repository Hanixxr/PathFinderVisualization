from abc import abstractmethod
from collections import deque

import pygame
from queue import PriorityQueue

class PathFinder:
    def __init__(self):
        pass

    @staticmethod
    def reconstruct_path(came_from, current, draw, start):
        """将找到的最短路径显示出来"""
        while current in came_from:
            current = came_from[current]
            if current != start: # 起点不染成紫色
                current.make_path()
            draw()

    @staticmethod
    def capture_state(grid):
        """保存当前网格所有格子的颜色快照"""
        return [[spot.color for spot in row] for row in grid]

    @staticmethod
    def h(p1, p2):
        """启发式函数：计算曼哈顿距离 (L型距离)"""
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    @abstractmethod
    def find_path(self, draw, grid, start, end):
        raise NotImplementedError("子类必须实现find_path方法")

class AStar(PathFinder):
    def __init__(self):
        super().__init__()

    def find_path(self, draw, grid, start, end):
        """A* 算法主体，继承自父类"""
        history = []
        count = 0

        # 优先队列：存储 (F值, 进入顺序, 节点对象)
        open_set = PriorityQueue()
        open_set.put((0, count, start))

        # 记录每个节点的来路（用于最后画路径）
        came_from = {}

        # G值：从起点到当前节点的实际距离 (初始化为无穷大)
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0

        # F值：G值 + H值 (预估总距离)
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())

        # 记录哪些节点在队列中（方便快速查找）
        open_set_hash = {start}

        # 记录初始状态
        history.append(self.capture_state(grid))

        while not open_set.empty():
            # 让用户能中途关掉窗口不卡死
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]  # 取出 F 值最小的节点
            open_set_hash.remove(current)

            if current == end:  # 找到终点！
                self.reconstruct_path(came_from, end, draw, start)
                history.append(self.capture_state(grid))
                end.make_end()
                return True, history  # 返回成功标志和历史记录

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + neighbor.weight

                # 如果发现更近的走法
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()  # 标记为待探索（绿色）

            draw()  # 每处理一个节点，重绘一次屏幕，产生动画效果
            history.append(self.capture_state(grid))  # 保存快照

            if current != start:
                current.make_closed()  # 标记为已探索（红色）

        return False, history  # 没找到路径


class Dijkstra(PathFinder):
    def __init__(self):
        super().__init__()

    def find_path(self, draw, grid, start, end):
        """Dijkstra算法主体，继承自父类。Dijkstra 算法不需要 h(n)，或者说 h(n) 恒等于 0"""
        history = []
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}

        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0

        open_set_hash = {start}

        history.append(self.capture_state(grid))

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end, draw, start)
                history.append(self.capture_state(grid))
                end.make_end()
                return True, history

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + neighbor.weight

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    # Dijkstra 只根据 G 值排序
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((g_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()
            history.append(self.capture_state(grid))

            if current != start:
                current.make_closed()

        return False, history

class BFS(PathFinder):
    def __init__(self):
        super().__init__()

    def find_path(self, draw, grid, start, end):
        """BFS算法主体，继承自父类。Dijkstra使用优先队列存储，而BFS使用队列存储"""
        history = []
        queue = deque([start])
        visited = {start}
        came_from = {}

        history.append(self.capture_state(grid))

        while queue:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = queue.popleft()

            if current == end:
                self.reconstruct_path(came_from, end, draw, start)
                history.append(self.capture_state(grid))
                end.make_end()
                return True, history

            for neighbor in current.neighbors:
                # BFS 不考虑权重，只要没访问过且不是墙
                if neighbor not in visited and not neighbor.is_barrier():
                    came_from[neighbor] = current
                    visited.add(neighbor)
                    queue.append(neighbor)
                    if neighbor != end:
                        neighbor.make_open()

            draw()
            history.append(self.capture_state(grid))

            if current != start:
                current.make_closed()

        return False, history