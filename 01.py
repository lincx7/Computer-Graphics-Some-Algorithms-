import tkinter as tk
from tkinter import ttk, messagebox


class LineDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("直线绘制算法")
        self.root.geometry("850x650")

        # 初始化变量
        self.start = None  # 起点坐标 (x, y)
        self.end = None  # 终点坐标 (x, y)
        self.algorithm = 1  # 1:DDA, 2:Bresenham, 3:中点法

        # 创建输入区域（手动输入坐标）
        input_frame = ttk.LabelFrame(root, text="手动输入坐标", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # 起点输入
        ttk.Label(input_frame, text="起点 X:").grid(row=0, column=0, padx=5, pady=5)
        self.start_x = ttk.Entry(input_frame, width=8)
        self.start_x.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Y:").grid(row=0, column=2, padx=5, pady=5)
        self.start_y = ttk.Entry(input_frame, width=8)
        self.start_y.grid(row=0, column=3, padx=5, pady=5)

        # 终点输入
        ttk.Label(input_frame, text="终点 X:").grid(row=0, column=4, padx=5, pady=5)
        self.end_x = ttk.Entry(input_frame, width=8)
        self.end_x.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(input_frame, text="Y:").grid(row=0, column=6, padx=5, pady=5)
        self.end_y = ttk.Entry(input_frame, width=8)
        self.end_y.grid(row=0, column=7, padx=5, pady=5)

        # 确认输入按钮
        self.confirm_btn = ttk.Button(input_frame, text="确认坐标", command=self.confirm_coords)
        self.confirm_btn.grid(row=0, column=8, padx=10, pady=5)

        # 创建画布
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 创建信息显示区域
        info_frame = ttk.LabelFrame(root, text="信息", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.alg_label = ttk.Label(info_frame, text="当前算法：DDA(红)")
        self.alg_label.pack(side=tk.LEFT, padx=10)

        self.coord_label = ttk.Label(info_frame, text="坐标：请选择或输入起点和终点")
        self.coord_label.pack(side=tk.LEFT, padx=10)

        self.help_label = ttk.Label(info_frame,
                                    text="操作：左键选点 | 1/2/3切换算法 | R重置 | Q退出 | 输入坐标后点确认")
        self.help_label.pack(side=tk.LEFT, padx=10)

        # 绑定事件
        self.canvas.bind("<Button-1>", self.on_click)  # 鼠标左键点击
        self.root.bind("<Key>", self.on_key_press)  # 键盘按键

    def confirm_coords(self):
        """处理手动输入的坐标，验证并绘制直线"""
        try:
            # 获取输入值并转换为整数
            x0 = int(self.start_x.get()) if self.start_x.get() else None
            y0 = int(self.start_y.get()) if self.start_y.get() else None
            x1 = int(self.end_x.get()) if self.end_x.get() else None
            y1 = int(self.end_y.get()) if self.end_y.get() else None

            # 验证坐标有效性（必须同时输入起点和终点）
            if not (x0 is not None and y0 is not None and x1 is not None and y1 is not None):
                messagebox.showerror("输入错误", "请完整输入起点和终点的X、Y坐标！")
                return

            # 验证坐标范围（不超过画布大小）
            canvas_width = self.canvas.winfo_width() or 800
            canvas_height = self.canvas.winfo_height() or 600
            if not (0 <= x0 < canvas_width and 0 <= y0 < canvas_height and
                    0 <= x1 < canvas_width and 0 <= y1 < canvas_height):
                messagebox.showerror("范围错误", f"坐标需在0-{canvas_width}（X）和0-{canvas_height}（Y）之间！")
                return

            # 更新坐标并绘制直线
            self.start = (x0, y0)
            self.end = (x1, y1)
            self.draw_line()
            self.update_info()

        except ValueError:
            messagebox.showerror("格式错误", "坐标必须是整数！")

    def on_click(self, event):
        """鼠标点击选择坐标（同时清空输入框，避免冲突）"""
        if not self.start:
            self.start = (event.x, event.y)
            self.end = None
            # 同步显示到输入框
            self.start_x.delete(0, tk.END)
            self.start_x.insert(0, str(event.x))
            self.start_y.delete(0, tk.END)
            self.start_y.insert(0, str(event.y))
        else:
            self.end = (event.x, event.y)
            # 同步显示到输入框
            self.end_x.delete(0, tk.END)
            self.end_x.insert(0, str(event.x))
            self.end_y.delete(0, tk.END)
            self.end_y.insert(0, str(event.y))
        self.draw_line()
        self.update_info()

    def on_key_press(self, event):
        """键盘事件：切换算法/重置/退出"""
        key = event.keysym.lower()
        if key in ['1', '2', '3']:
            self.algorithm = int(key)
            alg_names = ["DDA(红)", "Bresenham(绿)", "中点法(蓝)"]
            self.alg_label.config(text=f"当前算法：{alg_names[self.algorithm - 1]}")
            if self.start and self.end:
                self.draw_line()
        elif key == 'r':
            # 重置：清空画布、坐标、输入框
            self.canvas.delete("all")
            self.start = None
            self.end = None
            self.start_x.delete(0, tk.END)
            self.start_y.delete(0, tk.END)
            self.end_x.delete(0, tk.END)
            self.end_y.delete(0, tk.END)
            self.update_info()
        elif key == 'q':
            self.root.quit()

    def update_info(self):
        """更新坐标显示信息"""
        if self.start and self.end:
            info = f"起点：{self.start} | 终点：{self.end}"
        elif self.start:
            info = f"起点：{self.start} | 请选择或输入终点"
        else:
            info = "请选择或输入起点和终点"
        self.coord_label.config(text=info)

    def draw_pixel(self, x, y, color):
        """绘制单个像素（1x1矩形）"""
        self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)

    def dda_line(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy)) or 1
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x0, y0
        for _ in range(int(steps) + 1):
            self.draw_pixel(int(x + 0.5), int(y + 0.5), "red")  # 优化浮点数精度
            x += x_inc
            y += y_inc

    def bresenham_line(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x1 > x0 else -1
        sy = 1 if y1 > y0 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            self.draw_pixel(x, y, "green")
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def midpoint_line(self, x0, y0, x1, y1):
        a = y0 - y1
        b = x1 - x0
        x, y = x0, y0
        self.draw_pixel(x, y, "blue")
        step_x = 1 if b > 0 else -1
        step_y = 1 if a < 0 else -1
        if b < 0:
            b = -b
        if a > 0:
            a = -a
        d = a + (b // 2)
        while x != x1 or y != y1:
            if d < 0:
                y += step_y
                d += a + b
            else:
                d += a
            x += step_x
            self.draw_pixel(x, y, "blue")

    def draw_line(self):
        """根据当前算法绘制直线"""
        if not (self.start and self.end):
            return
        self.canvas.delete("all")  # 清空旧内容
        x0, y0 = self.start
        x1, y1 = self.end
        if self.algorithm == 1:
            self.dda_line(x0, y0, x1, y1)
        elif self.algorithm == 2:
            self.bresenham_line(x0, y0, x1, y1)
        else:
            self.midpoint_line(x0, y0, x1, y1)
        # 标记端点
        self.canvas.create_oval(x0 - 3, y0 - 3, x0 + 3, y0 + 3, fill="white")
        self.canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="white")


if __name__ == "__main__":
    root = tk.Tk()
    # 确保中文显示正常
    root.option_add("*Font", "SimHei 9")
    app = LineDrawer(root)
    root.mainloop()