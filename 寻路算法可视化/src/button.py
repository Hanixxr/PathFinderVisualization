import pygame
from settings import *

# 必须在文件顶部或类外部初始化字体，否则会报错
pygame.font.init()

# 界面中的按钮，pygame没有原生按钮组件
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.current_color = color
        self.font = pygame.font.SysFont('SimHei', 20, bold=False)

    def draw(self, win):
        # 1. 绘制微小的阴影
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(win, SHADOW_COLOR, shadow_rect, border_radius=8)

        # 2. 绘制圆角主矩形
        pygame.draw.rect(win, self.current_color, self.rect, border_radius=8)

        # 3. 绘制亮色边框线
        pygame.draw.rect(win, WHITE, self.rect, width=1, border_radius=8)

        # 4. 渲染文字
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        """判断是否点击，同时也用于逻辑层面的坐标判定"""
        return self.rect.collidepoint(pos)