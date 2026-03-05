import tkinter as tk
from tkinter import messagebox


class CohenSutherlandClipping:
    def __init__(self, root):
        self.root = root
        self.root.title("Cohen-Sutherland 直线裁剪")

        # 裁剪窗口参数（左下(xmin, ymin)，右上(xmax, ymax)）
        self.xmin, self.ymin = 200, 150
        self.xmax, self.ymax = 600, 450

        # 线段端点存储
        self.points = []
        self.clipped_line = None

        # 创建画布
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)  # 绑定鼠标点击事件

        # 绘制裁剪窗口和提示文字
        self.draw_window_and_tips()

    # 区域码定义（4位二进制，bit0=左，bit1=右，bit2=下，bit3=上）
    def compute_out_code(self, x, y):
        code = 0b0000  # 初始在窗口内
        if x < self.xmin:
            code |= 0b0001  # 左边界外
        elif x > self.xmax:
            code |= 0b0010  # 右边界外
        if y < self.ymin:
            code |= 0b0100  # 下边界外
        elif y > self.ymax:
            code |= 0b1000  # 上边界外
        return code

    # Cohen-Sutherland 裁剪核心算法
    def clip_line(self, x0, y0, x1, y1):
        code0 = self.compute_out_code(x0, y0)
        code1 = self.compute_out_code(x1, y1)

        while True:
            # 情况1：线段完全在窗口内
            if (code0 | code1) == 0:
                return (x0, y0, x1, y1)
            # 情况2：线段完全在窗口外
            elif (code0 & code1) != 0:
                return None
            # 情况3：线段部分在窗口内，计算交点
            else:
                x, y = 0, 0
                # 取窗口外的端点计算交点
                code_out = code0 if code0 != 0 else code1

                # 计算交点（根据区域码判断穿越的边界）
                if code_out & 0b1000:  # 上边界 (y = ymax)
                    t = (self.ymax - y0) / (y1 - y0) if (y1 - y0) != 0 else 0
                    x = x0 + t * (x1 - x0)
                    y = self.ymax
                elif code_out & 0b0100:  # 下边界 (y = ymin)
                    t = (self.ymin - y0) / (y1 - y0) if (y1 - y0) != 0 else 0
                    x = x0 + t * (x1 - x0)
                    y = self.ymin
                elif code_out & 0b0010:  # 右边界 (x = xmax)
                    t = (self.xmax - x0) / (x1 - x0) if (x1 - x0) != 0 else 0
                    y = y0 + t * (y1 - y0)
                    x = self.xmax
                elif code_out & 0b0001:  # 左边界 (x = xmin)
                    t = (self.xmin - x0) / (x1 - x0) if (x1 - x0) != 0 else 0
                    y = y0 + t * (y1 - y0)
                    x = self.xmin

                # 更新端点和区域码
                if code_out == code0:
                    x0, y0 = x, y
                    code0 = self.compute_out_code(x0, y0)
                else:
                    x1, y1 = x, y
                    code1 = self.compute_out_code(x1, y1)

    # 绘制裁剪窗口和提示信息
    def draw_window_and_tips(self):
        # 绘制裁剪窗口（绿色虚线）
        self.canvas.create_rectangle(
            self.xmin, self.ymin, self.xmax, self.ymax,
            outline="green", dash=(5, 2), width=2
        )
        # 绘制提示文字
        self.canvas.create_text(
            400, 30, text="Cohen-Sutherland 直线裁剪",
            font=("SimHei", 14, "bold"), fill="black"
        )
        self.canvas.create_text(
            400, 60, text="点击鼠标左键选择线段端点（2个点）",
            font=("SimHei", 10), fill="gray"
        )
        self.canvas.create_text(
            400, 80, text="红色：原始线段 | 蓝色：裁剪后线段 | 选完2点后点击重置",
            font=("SimHei", 10), fill="gray"
        )

    # 鼠标点击事件处理
    def on_click(self, event):
        # 收集2个端点
        if len(self.points) < 2:
            self.points.append((event.x, event.y))
            # 画端点标记
            self.canvas.create_oval(
                event.x - 3, event.y - 3, event.x + 3, event.y + 3,
                fill="black", outline=""
            )
            # 收集完2个点后裁剪
            if len(self.points) == 2:
                x0, y0 = self.points[0]
                x1, y1 = self.points[1]
                # 绘制原始线段（红色）
                self.canvas.create_line(x0, y0, x1, y1, fill="red", width=1)
                # 裁剪并绘制结果（蓝色）
                self.clipped_line = self.clip_line(x0, y0, x1, y1)
                if self.clipped_line:
                    cx0, cy0, cx1, cy1 = self.clipped_line
                    self.canvas.create_line(cx0, cy0, cx1, cy1, fill="blue", width=2)
        else:
            # 重置：清空画布重新开始
            self.canvas.delete("all")
            self.points = []
            self.clipped_line = None
            self.draw_window_and_tips()


if __name__ == "__main__":
    root = tk.Tk()
    app = CohenSutherlandClipping(root)
    root.mainloop()