import subprocess
import time
import sys

# ANSI 转义码用于彩色输出
RED = "\033[91m"
RESET = "\033[0m"

def run_script():
    try:
        result = subprocess.run(['/usr/bin/python3', 'Start_MessageMovie.py'], check=True)
        print("程序正在运行中...")
    except subprocess.CalledProcessError as e:
        print(f"{RED}子进程执行失败: {e}{RESET}", file=sys.stderr)

def main():
    try:
        while True:
            run_script()
            for i in range(100):
                time.sleep(0.05)  # 模拟任务进度
                print(f"\r任务进度: {i+1}/100", end='')  # 使用简单的打印语句显示进度
                last_i = i
            print(f"\n任务完成，重置进度... 最后进度：{last_i+1}/100")
    except KeyboardInterrupt:
        print("\n程序已终止")
    except Exception as e:
        print(f"{RED}发生未知错误: {e}{RESET}", file=sys.stderr)

if __name__ == "__main__":
    main()