import tkinter as tk
from tkinter import Canvas


class SeedFillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("四连通非递归种子填充（优化版）")

        # 窗口参数
        self.WIDTH = 800
        self.HEIGHT = 600

        # 创建画布
        self.canvas = Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="white")
        self.canvas.pack()

        # 颜色定义
        self.BOUNDARY_COLOR = "black"
        self.FILL_COLOR = "lightblue"
        self.BG_COLOR = "white"

        # 记录已填充的像素（避免重复处理，提升效率）
        self.filled = set()

        # 绘制五边形（顶点坐标与原C++一致）
        self.poly_points = [400, 100, 300, 250, 350, 400, 450, 400, 500, 250]
        self.draw_polygon(self.poly_points, 5)

        # 种子点
        self.seed_x, self.seed_y = 400, 250

        # 显示填充提示
        self.status_text = self.canvas.create_text(400, 550, text="填充中...", fill="gray", font=("SimHei", 12))

        # 执行填充（用after(0)避免阻塞UI）
        self.root.after(0, self.boundary_fill4_optimized, self.seed_x, self.seed_y)

        # 按任意键关闭
        self.root.bind("<KeyPress>", lambda e: self.root.quit())

    # 绘制多边形（与原逻辑一致）
    def draw_polygon(self, points, n):
        for i in range(n):
            x1 = points[2 * i]
            y1 = points[2 * i + 1]
            x2 = points[2 * ((i + 1) % n)]
            y2 = points[2 * ((i + 1) % n) + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill=self.BOUNDARY_COLOR, width=1)

    # 优化版四连通种子填充：批量填充一行像素
    def boundary_fill4_optimized(self, seed_x, seed_y):
        pixel_stack = [(seed_x, seed_y)]

        while pixel_stack:
            curr_x, curr_y = pixel_stack.pop()

            # 跳过已填充或越界的像素
            if (curr_x, curr_y) in self.filled or not self.in_canvas(curr_x, curr_y):
                continue

            # 向左扫描：找到当前行最左侧可填充的像素
            left_x = curr_x
            while self.is_fillable(left_x, curr_y):
                left_x -= 1
            left_x += 1  # 回到最左侧可填充像素

            # 向右扫描：找到当前行最右侧可填充的像素
            right_x = curr_x
            while self.is_fillable(right_x, curr_y):
                right_x += 1
            right_x -= 1  # 回到最右侧可填充像素

            # 批量填充当前行（从left_x到right_x）：效率核心优化
            self.fill_scanline(left_x, right_x, curr_y)

            # 检查当前行上下两行的相邻像素，将可填充的像素入栈（四连通扩展）
            self.check_and_push_neighbors(left_x, right_x, curr_y - 1, pixel_stack)  # 下一行
            self.check_and_push_neighbors(left_x, right_x, curr_y + 1, pixel_stack)  # 上一行

        # 填充完成，更新提示
        self.canvas.itemconfig(self.status_text, text="填充完成！按任意键关闭")

    # 批量填充一行像素（从x1到x2，y固定）
    def fill_scanline(self, x1, x2, y):
        if x1 > x2:
            x1, x2 = x2, x1  # 确保x1 <= x2
        # 绘制一条水平线段，替代逐个像素绘制（效率提升关键）
        self.canvas.create_line(x1, y, x2, y, fill=self.FILL_COLOR, width=1)
        # 记录已填充的像素（避免重复处理）
        for x in range(x1, x2 + 1):
            self.filled.add((x, y))

    # 检查一行中可填充的像素，压入栈
    def check_and_push_neighbors(self, left_x, right_x, y, stack):
        x = left_x
        while x <= right_x:
            # 找到连续可填充的像素段的起点
            while x <= right_x and not self.is_fillable(x, y):
                x += 1
            if x > right_x:
                break
            # 压入当前可填充段的任意一个像素（后续会扫描整行）
            stack.append((x, y))
            # 跳过当前连续段
            while x <= right_x and self.is_fillable(x, y):
                x += 1

    # 判断像素是否在画布内
    def in_canvas(self, x, y):
        return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT

    # 判断像素是否可填充（核心逻辑：非边界、非已填充、在画布内）
    def is_fillable(self, x, y):
        if not self.in_canvas(x, y) or (x, y) in self.filled:
            return False

        # 检查是否为边界色（检测当前坐标是否与边界线重叠）
        boundary_items = self.canvas.find_overlapping(x, y, x, y)
        for item in boundary_items:
            if self.canvas.itemcget(item, "outline") == self.BOUNDARY_COLOR:
                return False

        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = SeedFillApp(root)
    root.mainloop()