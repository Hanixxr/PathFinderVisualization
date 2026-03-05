import pygame
import time

from pathFinder import *
from settings import *
from spot import Spot
from button import Button

def make_grid(rows, width):
    """创建网格"""
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    """画出网格线"""
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width, buttons, msg, msg_color, history, current_step, is_playing):
    """核心绘图函数，画出整个界面中的信息"""
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)

    # 侧边栏背景
    pygame.draw.rect(win, SIDEBAR_COLOR, (width, 0, SIDEBAR, width))

    for btn in buttons:
        btn.draw(win)

    # 绘制状态框
    font = pygame.font.SysFont('SimHei', 16)
    status_rect = pygame.Rect(width + 25, 410, 150, 35)
    pygame.draw.rect(win, WHITE, status_rect, border_radius=5)
    pygame.draw.rect(win, msg_color, status_rect, width=2, border_radius=5)
    status_label = font.render(msg, True, msg_color)
    status_label_rect = status_label.get_rect(center=status_rect.center)
    win.blit(status_label, status_label_rect)

    # 绘制进度条
    if history and len(history) > 1:
        bar_x, bar_y, bar_w = width + 20, 485, 160
        # 底色条
        pygame.draw.line(win, PROGRESSBAR_COLOR, (bar_x, bar_y), (bar_x + bar_w, bar_y), 6)
        # 已走进度条
        progress_ratio = current_step / (len(history) - 1)
        pygame.draw.line(win, BLUE, (bar_x, bar_y), (bar_x + int(progress_ratio * bar_w), bar_y), 6)
        # 滑块小圆球
        knob_x = bar_x + int(progress_ratio * bar_w)
        pygame.draw.circle(win, BLUE, (knob_x, bar_y), 8)

        step_font = pygame.font.SysFont('SimHei', 14)
        step_txt = step_font.render(f"步骤: {current_step}/{len(history) - 1}", True, STEP_TEXT_COLOR)
        win.blit(step_txt, (bar_x, bar_y + 15))

    # 在进度条下方或按钮上方增加一个小图标
    if history:
        play_font = pygame.font.SysFont('SimHei', 14)
        status_text = "播放中" if is_playing else "已暂停"
        color = LIGHT_GREEN if is_playing else LIGHT_RED
        play_label = play_font.render(status_text, True, color)
        win.blit(play_label, (width + 20, 460))  # 放在进度条上方一点

    pygame.display.update()

def apply_history_state(grid, state):
    """将历史状态快照中的颜色信息还原到网格节点上"""
    for i, row in enumerate(grid):
        for j, spot in enumerate(row):
            spot.color = state[i][j]

def get_clicked_pos(pos, rows, width):
    """把鼠标点击的像素坐标转换为网格中的行列索引"""
    gap = width // rows
    y, x = pos
    row, col = y // gap, x // gap
    # 确保返回的索引不会超出数组边界
    return min(rows - 1, max(0, row)), min(rows - 1, max(0, col))

def handle_grid_click(pos, grid, rows, width, start, end, sand_mode, is_right_click=False):
    """统一处理网格的点击与拖动逻辑，返回更新后的 (start, end)"""
    row, col = get_clicked_pos(pos, rows, width)
    spot = grid[row][col]

    # 右键：重置
    if is_right_click:
        spot.reset()
        if spot == start: start = None
        if spot == end: end = None

    # 左键：布置网格
    else:
        # 1. 设置起点
        if not start and spot != end:
            start = spot
            start.make_start()
        # 2. 设置终点
        elif not end and spot != start:
            end = spot
            end.make_end()
        # 3. 设置障碍（避开起点和终点）
        elif spot != end and spot != start:
            if sand_mode:
                if not spot.is_barrier():
                    spot.make_sand()
            else:
                spot.make_barrier()
    return start, end

def reset_path(grid):
    """清除探索的路径"""
    for row in grid:
        for spot in row:
            if not (spot.is_barrier() or spot.is_start() or spot.is_end()):
                spot.return_to_base_color()

def run_algorithm(finder_instance, draw_fn, grid, start, end):
    """统一算法执行入口"""
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    # 执行算法并返回结果
    found, history = finder_instance.find_path(draw_fn, grid, start, end)
    return found, history

# 5. 主程序入口
def main(win, width):
    grid = make_grid(ROWS, width)
    start, end = None, None     # 起点和终点
    run = True                  # 程序运行标识
    sand_mode = False           # 沙地模式

    status_msg, status_color = READY, DARK_GREY # 状态信息

    history = []                  # 记录历史路径
    current_step = 0              # 当前运行到的步骤

    confirm_clear = False         # 确认清空网格
    is_dragging = False           # 进度条拖动状态
    is_playing = False            # 是否正在自动播放
    last_play_time = time.time()  # 记录上一次播放的时间戳

    btn_x = width + 20
    buttons = [
        Button(btn_x, 50, 160, 45, "A* 算法", BLUE),
        Button(btn_x, 110, 160, 45, "Dijkstra算法", LIGHT_GREEN),
        Button(btn_x, 170, 160, 45, "BFS 算法", LIGHT_PURPLE),
        Button(btn_x, 230, 160, 45, "沙地模式: 关", SAND_MODE_COLOR),
        Button(btn_x, 290, 160, 45, "清除路径", YELLOW),
        Button(btn_x, 350, 160, 45, "清空网格", LIGHT_RED),
        Button(btn_x, 520, 75, 35, "上一步", SHADOW_COLOR),
        Button(btn_x + 85, 520, 75, 35, "下一步", SHADOW_COLOR),
        Button(btn_x, 560, 160, 35, "播放 / 暂停", PAUSE_COLOR)
    ]

    while run:
        # --- 自动播放逻辑 ---
        if is_playing and history:
            current_time = time.time()
            if current_time - last_play_time > PLAY_SPEED:
                if current_step < len(history) - 1:
                    current_step += 1
                    apply_history_state(grid, history[current_step])
                    last_play_time = current_time
                else:
                    is_playing = False  # 播放到最后一步自动停止

        draw(win, grid, ROWS, width, buttons, status_msg, status_color, history, current_step, is_playing)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            pos = pygame.mouse.get_pos()

            # --- 鼠标按下事件 ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    # 1. 优先处理侧边栏区域 (点击了右侧界面)
                    if pos[0] >= width:
                        # 如果点击的不是清空按钮，就重置清空状态
                        if not buttons[5].is_clicked(pos):
                            confirm_clear = False
                            buttons[5].text = "清空网格"
                            buttons[5].current_color = LIGHT_RED

                        # 进度条交互判定 (判定范围包含进度条及其上下感应区)
                        if history:
                            bar_x, bar_y, bar_w = width + 20, 485, 160
                            if bar_x <= pos[0] <= bar_x + bar_w and bar_y - 15 <= pos[1] <= bar_y + 15:
                                is_dragging = True
                                is_playing = False  # 手动拖动时停止自动播放
                                rel_x = max(0, min(pos[0] - bar_x, bar_w))
                                current_step = int((rel_x / bar_w) * (len(history) - 1))
                                apply_history_state(grid, history[current_step])
                                continue  # 处理完进度条直接跳过后续按钮判定

                        # 按钮交互判定
                        if (buttons[0].is_clicked(pos) or buttons[1].is_clicked(pos) or buttons[2].is_clicked(pos)) and start and end:
                            if buttons[0].is_clicked(pos):
                                path_finder = AStar()
                            elif buttons[1].is_clicked(pos):
                                path_finder = Dijkstra()
                            else:
                                path_finder = BFS()

                            # 执行封装好的算法调用函数
                            found, history = run_algorithm(
                                path_finder,
                                lambda: draw(win, grid, ROWS, width, buttons, status_msg, status_color, history, len(history), is_playing),
                                grid, start, end
                            )

                            current_step = len(history) - 1
                            status_msg, status_color = (SUCCESS, LIGHT_GREEN) if found else (INVALID, LIGHT_RED)

                        elif buttons[3].is_clicked(pos):
                            sand_mode = not sand_mode
                            buttons[3].text = "沙地模式: 开" if sand_mode else "沙地模式: 关"
                            buttons[3].current_color = SAND_COLOR if sand_mode else SAND_MODE_COLOR

                        elif buttons[4].is_clicked(pos):  # 清除路径
                            reset_path(grid)
                            history, current_step = [], 0
                            is_playing = False
                            status_msg, status_color = CLEAR, DARK_GREY

                        elif buttons[5].is_clicked(pos):  # 清空全部
                            if not confirm_clear:
                                confirm_clear = True
                                buttons[5].text = "确认清空吗？"
                                buttons[5].current_color = LIGHT_RED
                            else:
                                start, end = None, None
                                history, current_step = [], 0
                                is_playing = False
                                grid = make_grid(ROWS, width)
                                status_msg, status_color = READY, DARK_GREY

                                confirm_clear = False
                                buttons[5].text = "清空网格"
                                buttons[5].current_color = LIGHT_RED

                        elif (buttons[6].is_clicked(pos) or buttons[7].is_clicked(pos)) and history:  # [6]-上一步 / [7]-下一步
                            is_playing = False
                            current_step = max(0, current_step - 1) if buttons[6].is_clicked(pos) else min(len(history) - 1, current_step + 1)
                            apply_history_state(grid, history[current_step])

                        elif buttons[8].is_clicked(pos) and history:  # 播放/暂停
                            is_playing = not is_playing
                            last_play_time = time.time()  # 重置计时防止跳帧

                    # 2. 处理网格区域 (点击了左侧地图)
                    elif not is_dragging:
                        start, end = handle_grid_click(pos, grid, ROWS, width, start, end, sand_mode)

                elif event.button == 3:  # 右键按下 (原地删除)
                    if pos[0] < width:
                        start, end = handle_grid_click(pos, grid, ROWS, width, start, end, sand_mode, is_right_click=True)

            # --- 鼠标抬起事件 ---
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False

            # --- 鼠标移动事件 ---
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                # 拖动进度条逻辑
                if is_dragging and history:
                    bar_x, bar_w = width + 20, 160
                    rel_x = max(0, min(pos[0] - bar_x, bar_w))
                    current_step = int((rel_x / bar_w) * (len(history) - 1))
                    apply_history_state(grid, history[current_step])

                # 网格拖动绘图 (按下左键且在网格内)
                elif pos[0] < width:
                    if pygame.mouse.get_pressed()[0]:  # 按住左键拖动
                        start, end = handle_grid_click(pos, grid, ROWS, width, start, end, sand_mode)
                    elif pygame.mouse.get_pressed()[2]:  # 按住右键拖动
                        start, end = handle_grid_click(pos, grid, ROWS, width, start, end, sand_mode, is_right_click=True)

    pygame.quit()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH + SIDEBAR, WIDTH))
    pygame.display.set_caption("寻路算法可视化")
    main(WIN, WIDTH)