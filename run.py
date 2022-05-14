import os
path = os.path.dirname(__file__)
virtual = path + "\\venv"
if not os.path.exists(virtual):
    print("首次运行需要配置虚拟环境，请稍等片刻~")
    os.mkdir(virtual)
    os.system("python -m venv venv")
    os.system(".\\venv\Scripts\\activate && pip install -r requirements.txt && cls && python control.py")
else:
    print("已存在")
    os.system(".\\venv\Scripts\\activate && pip install -r requirements.txt && cls && python control.py")

