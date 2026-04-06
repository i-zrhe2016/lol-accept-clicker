import tkinter as tk
import pyautogui
import time
import sys
import numpy as np
from PIL import ImageGrab
from rapidocr_onnxruntime import RapidOCR


class RegionSelector:
    """拉框选择屏幕区域"""

    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.rect = None

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black",
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        label = tk.Label(self.root, text="拖动鼠标选择监控区域，ESC取消",
                         fg="white", bg="black", font=("Arial", 20))
        label.place(relx=0.5, rely=0.1, anchor="center")

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=2
        )

    def on_drag(self, event):
        self.canvas.coords(self.rect,
                           self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.root.destroy()

    def get_region(self):
        self.root.mainloop()
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        if x2 - x1 < 10 or y2 - y1 < 10:
            return None
        return (x1, y1, x2, y2)


# 全局初始化 OCR 引擎（只加载一次模型）
ocr_engine = RapidOCR()


def find_and_click_accept(region):
    """截图识别并点击接受按钮"""
    x1, y1, x2, y2 = region
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img_array = np.array(screenshot)

    result, _ = ocr_engine(img_array)
    if not result:
        print("  未识别到文字")
        return False

    for line in result:
        box, text, confidence = line
        print(f"  识别: {text!r} (置信度: {float(confidence):.2f})")
        if "接受" in text or "接" in text:
            # box 是四个角坐标 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            # 取中心点
            cx = int(sum(p[0] for p in box) / 4)
            cy = int(sum(p[1] for p in box) / 4)
            click_x = x1 + cx
            click_y = y1 + cy
            print(f"  >>> 找到「接受」，点击坐标 ({click_x}, {click_y})")
            pyautogui.click(click_x, click_y)
            return True

    return False


def main():
    print("=== LOL 自动接受匹配工具 ===")
    print("正在加载 OCR 引擎...")
    # 预热 OCR
    ocr_engine(np.zeros((10, 10, 3), dtype=np.uint8))
    print("OCR 引擎就绪！")
    print("10秒后开始选择区域...")
    for i in range(10, 0, -1):
        print(f"  {i}秒后启动...")
        time.sleep(1)
    print("请拖动鼠标框选「接受」按钮所在的区域...\n")

    selector = RegionSelector()
    region = selector.get_region()

    if not region:
        print("未选择有效区域，退出。")
        sys.exit(1)

    print(f"监控区域: {region}")
    print("3秒后开始检测，每5秒检测一次，按 Ctrl+C 停止\n")
    time.sleep(3)

    pyautogui.FAILSAFE = True

    while True:
        print(f"[{time.strftime('%H:%M:%S')}] 检测中...")
        try:
            clicked = find_and_click_accept(region)
            if clicked:
                print("  已点击接受，等待10秒后继续监控...")
                time.sleep(10)
            else:
                print("  未检测到「接受」")
        except Exception as e:
            print(f"  错误: {e}")
        time.sleep(5)


if __name__ == "__main__":
    main()
