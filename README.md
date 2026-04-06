# LOL 自动接受匹配

自动识别并点击英雄联盟的「接受」按钮。

## 使用方法

1. 从 [Releases](https://github.com/i-zrhe2016/lol-accept-clicker/releases) 下载最新 `lol-accept.exe`
2. 运行 exe，等待 10 秒倒计时
3. 倒计时结束后，拖动鼠标框选游戏中「接受」按钮所在区域
4. 3 秒后开始自动检测，每 5 秒检测一次
5. 检测到「接受」按钮时自动点击，按 `Ctrl+C` 停止

## 本地运行

```bash
pip install pyautogui pillow rapidocr-onnxruntime numpy
python accept_clicker.py
```

## 本地打包

Windows 上双击运行 `build.bat`，生成的 exe 在 `dist/` 目录下。
