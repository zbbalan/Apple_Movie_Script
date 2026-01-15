import subprocess
import time
import sys

# ANSI 转义码用于彩色输出
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_GREEN = "\033[92m"
RED = "\033[91m"
ORANGE = "\033[38;5;208m"

def run_script():
    try:
        result = subprocess.run(['/usr/bin/python3', 'Start_MessageMovie.py'], check=True, capture_output=True, text=True)
        print("程序正在运行中...")
    except subprocess.CalledProcessError as e:
        print(f"子进程执行失败: {e}", file=sys.stderr)
        if e.stdout:
            print(f"标准输出: {e.stdout}", file=sys.stderr)
        if e.stderr:
            print(f"错误输出: {e.stderr}", file=sys.stderr)

def main():
    try:
        while True:
            run_script()
            last_i = 0  # 初始化变量以避免未绑定错误
            bar_length = 50  # 定义进度条长度在循环外
            # 创建一个炫酷的脉冲动画进度条
            for i in range(100):
                time.sleep(0.2)  # 减慢进度使动画更明显
                percent = i + 1
                filled_length = int(bar_length * percent // 100)
                
                # 创建绿色系脉冲动画进度条
                bar = ""
                for j in range(bar_length):
                    if j < filled_length:
                        # 创建脉冲效果，模拟发光动画
                        pulse_pos = (j + i) % 6  # 使用循环位置创造脉冲效果
                        if pulse_pos < 2:
                            bar += f"{GREEN}█{RESET}"      # 亮绿色脉冲
                        elif pulse_pos < 4:
                            bar += f"{CYAN}█{RESET}"      # 青色中间层
                        else:
                            bar += f"{BRIGHT_MAGENTA}█{RESET}"  # 洋红色外层
                    else:
                        bar += "░"  # 未填充部分保持默认颜色
                
                # 创建不断变化颜色的百分比
                color_cycle = [GREEN, YELLOW, CYAN, WHITE, BRIGHT_MAGENTA, RED, ORANGE]
                color_index = i % len(color_cycle)
                changing_color = color_cycle[color_index]
                percent_str = f"{changing_color}{percent:3d}%{RESET}"
                
                print(f'\r启动中 [{bar}] {percent_str}', end='', flush=True)
                last_i = i
            
            # 当进度完成时，显示单一颜色的进度条和白色百分比
            completed_bar = f"{BRIGHT_GREEN}" + "█" * bar_length + f"{RESET}"
            completed_percent = f"{WHITE}100%{RESET}"
            print(f'\r启动中 [{completed_bar}] {completed_percent}')
            print(f"任务完成，重置进度... 最后进度：{last_i+1}/100")
    except KeyboardInterrupt:
        print("\n程序已终止")
    except Exception as e:
        print(f"发生未知错误: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
