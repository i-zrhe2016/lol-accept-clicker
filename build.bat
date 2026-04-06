@echo off
echo === Build LOL Accept Clicker ===
echo.

pip install pyautogui pillow rapidocr-onnxruntime numpy pyinstaller

echo.
echo Building exe...
pyinstaller --noconfirm --onefile --console --name "lol-accept" --hidden-import=rapidocr_onnxruntime --hidden-import=onnxruntime --collect-all rapidocr_onnxruntime --collect-all onnxruntime accept_clicker.py

echo.
echo Done! Check dist\lol-accept.exe
pause
