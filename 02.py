import tkinter as tk
from tkinter import ttk, messagebox
import math


class GraphicsDrawingExperiment:
    """图形绘制算法实验平台"""

    def __init__(self, root):
        # 初始化主窗口
        self.root = root
        self.root.title("基本图形生成算法实验")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # 实验参数配置
        self.init_ui()
        self.center_x = self.canvas_width // 2  # 画布中心x坐标（原点）
        self.center_y = self.canvas_height // 2  # 画布中心y坐标（原点）

    def init_ui(self):
        """初始化用户界面"""
        # 1. 顶部说明区域
        header = ttk.Label(
            self.root,
            text="圆与椭圆生成算法实验 —— 中点算法/Bresenham算法",
            font=("SimHei", 12, "bold")
        )
        header.pack(pady=10)

        # 2. 控制面板（参数输入+功能按钮）
        control_frame = ttk.LabelFrame(self.root, text="参数设置")
        control_frame.pack(fill=tk.X, padx=20, pady=5)

        # 2.1 圆参数设置
        circle_frame = ttk.LabelFrame(control_frame, text="圆参数")
        circle_frame.grid(row=0, column=0, padx=10, pady=5)

        ttk.Label(circle_frame, text="半径:").grid(row=0, column=0, padx=5, pady=5)
        self.circle_radius = tk.StringVar(value="100")
        ttk.Entry(circle_frame, textvariable=self.circle_radius, width=8).grid(row=0, column=1, padx=5)

        # 2.2 椭圆参数设置
        ellipse_frame = ttk.LabelFrame(control_frame, text="椭圆参数")
        ellipse_frame.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(ellipse_frame, text="x半轴:").grid(row=0, column=0, padx=5, pady=5)
        self.ellipse_a = tk.StringVar(value="150")
        ttk.Entry(ellipse_frame, textvariable=self.ellipse_a, width=8).grid(row=0, column=1, padx=5)

        ttk.Label(ellipse_frame, text="y半轴:").grid(row=0, column=2, padx=5, pady=5)
        self.ellipse_b = tk.StringVar(value="100")
        ttk.Entry(ellipse_frame, textvariable=self.ellipse_b, width=8).grid(row=0, column=3, padx=5)

        # 2.3 功能按钮
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=0, column=2, padx=10, pady=5)

        ttk.Button(
            btn_frame, text="中点画圆",
            command=self.draw_midpoint_circle
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            btn_frame, text="Bresenham画圆",
            command=self.draw_bresenham_circle
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            btn_frame, text="中点画椭圆",
            command=self.draw_optimized_ellipse
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            btn_frame, text="清空画布",
            command=self.clear_canvas
        ).pack(fill=tk.X, pady=2)

        # 3. 绘图区域
        self.canvas_width = 850
        self.canvas_height = 500
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white",
            bd=2,
            relief=tk.SUNKEN
        )
        self.canvas.pack(padx=20, pady=10)

        # 4. 状态提示区
        self.status = tk.StringVar(value="请选择算法绘制图形")
        ttk.Label(self.root, textvariable=self.status).pack(pady=5)

    def put_pixel(self, x, y, color):
        """绘制像素点"""
        # 转换逻辑：画布左上角(0,0) → 中心(center_x, center_y)为原点，y轴向上为正
        canvas_x = self.center_x + x
        canvas_y = self.center_y - y

        # 边界检查（确保像素在画布内）
        if 0 <= canvas_x < self.canvas_width and 0 <= canvas_y < self.canvas_height:
            self.canvas.create_rectangle(
                canvas_x, canvas_y, canvas_x + 1, canvas_y + 1,
                fill=color, outline=color
            )

    # ------------------------------ 圆绘制算法 ------------------------------
    def circle_symmetry_points(self, x, y, color):
        """八分对称性绘制"""
        sym_points = [
            (x, y), (y, x), (-x, y), (y, -x),
            (x, -y), (-y, x), (-x, -y), (-y, -x)
        ]
        for px, py in sym_points:
            self.put_pixel(px, py, color)

    def draw_midpoint_circle(self):
        """中点画圆算法"""
        try:
            r = int(self.circle_radius.get())
            if r <= 0:
                raise ValueError("半径必须为正整数")
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
            return

        x, y = 0, r
        r_sq = r * r
        # 初始判别式d0 = 1.25 - r
        d = 1.25 - r
        self.circle_symmetry_points(x, y, "red")

        while x <= y:
            x += 1
            if d < 0:
                # 中点在圆内，取右点（d += 2x + 3）
                d += 2 * x + 3
            else:
                # 中点在圆外，取右下点（d += 2(x - y) + 5）
                y -= 1
                d += 2 * (x - y) + 5
            self.circle_symmetry_points(x, y, "red")

        self.status.set(f"已用中点算法绘制圆（半径：{r}）")

    def draw_bresenham_circle(self):
        """Bresenham画圆算法"""
        try:
            r = int(self.circle_radius.get())
            if r <= 0:
                raise ValueError("半径必须为正整数")
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
            return

        x, y = 0, r
        # 初始判别式d = 3 - 2r
        d = 3 - 2 * r
        self.circle_symmetry_points(x, y, "green")

        while x <= y:
            x += 1
            if d < 0:
                # 选择右点（d += 4x + 6）
                d += 4 * x + 6
            else:
                # 选择右下点（d += 4(x - y) + 10）
                y -= 1
                d += 4 * (x - y) + 10
            self.circle_symmetry_points(x, y, "green")

        self.status.set(f"已用Bresenham算法绘制圆（半径：{r}）")

    def ellipse_symmetry_points(self, x, y, color):
        """四分对称性绘制（椭圆对称点处理）"""
        sym_points = [(x, y), (-x, y), (x, -y), (-x, -y)]
        for px, py in sym_points:
            self.put_pixel(px, py, color)

    def draw_optimized_ellipse(self):
        try:
            a = int(self.ellipse_a.get())
            b = int(self.ellipse_b.get())
            if a <= 0 or b <= 0:
                raise ValueError("半轴长必须为正整数")
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
            return

        x, y = 0, b
        a_sq = a ** 2  # a²
        b_sq = b ** 2  # b²

        # 上半段：斜率 ≥ -1
        # 初始判别式d1 = b² - a²b + a²/4
        d1 = b_sq - (a_sq * b) + (a_sq / 4)
        self.ellipse_symmetry_points(x, y, "blue")

        while (b_sq * x) <= (a_sq * y):  # 分段边界条件
            x += 1
            if d1 < 0:
                # 中点在椭圆内，取右点（d1 += b²(2x + 1)）
                d1 += b_sq * (2 * x + 1)
            else:
                # 中点在椭圆外，取右下点（d1 += b²(2x + 1) - a²(2y)）
                y -= 1
                d1 += b_sq * (2 * x + 1) - a_sq * (2 * y)
            self.ellipse_symmetry_points(x, y, "blue")

        # 下半段：斜率 < -1
        # 初始判别式d2 = b²(x+0.5)² + a²(y-1)² - a²b²
        d2 = (b_sq * (x + 0.5) ** 2) + (a_sq * (y - 1) ** 2) - (a_sq * b_sq)
        while y >= 0:
            y -= 1
            if d2 > 0:
                # 中点在椭圆外，取下点（d2 += a²(1 - 2y)）
                d2 += a_sq * (1 - 2 * y)
            else:
                # 中点在椭圆内，取右下点（d2 += b²(2x + 1) + a²(1 - 2y)）
                x += 1
                d2 += b_sq * (2 * x + 1) + a_sq * (1 - 2 * y)
            self.ellipse_symmetry_points(x, y, "blue")

        self.status.set(f"已用中点算法绘制椭圆（x半轴：{a}，y半轴：{b}）")

    def clear_canvas(self):
        """清空画布"""
        self.canvas.delete("all")
        self.status.set("画布已清空，请重新绘制")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsDrawingExperiment(root)
    root.mainloop()