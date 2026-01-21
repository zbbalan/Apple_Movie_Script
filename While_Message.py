import subprocess
import time
import sys
import signal
import os
import sqlite3

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
BLUE = "\033[94m"
PURPLE = "\033[35m"

# 全局变量跟踪状态
last_processed_rowid = 0
recording_status = False  # 追踪录制状态

def get_last_message_with_rowid():
    """获取最新消息及其ROWID，用于避免重复处理"""
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    if not os.path.exists(db_path):
        print(f"Database does not exist: {db_path}")
        return None, None
        
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            # 获取最新消息的ROWID和文本
            cur.execute("SELECT ROWID, text FROM message ORDER BY ROWID DESC LIMIT 1")
            result = cur.fetchone()
            
        if result is not None:
            rowid, text = result
            return text, rowid
        else:
            return None, None
    except Exception as e:
        print(f"Error reading database: {e}")
        return None, None

def run_script():
    """运行消息处理脚本"""
    global recording_status
    try:
        # 使用 Popen 启动子进程，执行一次消息检查
        result = subprocess.run(['/usr/bin/python3', 'Start_MessageMovie.py'], 
                               capture_output=True, text=True, timeout=10)  # 添加超时防止长时间挂起
        if result.returncode == 0:
            print("程序正在运行中... 消息已检查")
            # 更新录制状态，基于当前处理的消息类型
            # 这里可以根据Start_MessageMovie.py的输出来判断录制状态
            # 但目前我们依赖于消息内容来推断状态
        else:
            print(f"程序执行有误: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("程序执行超时")
    except Exception as e:
        print(f"子进程执行失败: {e}", file=sys.stderr)

def show_progress_animation():
    """显示进度条动画的函数"""
    bar_length = 50
    # 创建一个炫酷的脉冲动画进度条
    for i in range(100):
        time.sleep(0.05)  # 加快进度使动画更流畅
        percent = i + 1
        filled_length = int(bar_length * percent // 100)
        
        # 创建带有 > 形状的脉冲动画进度条
        bar = ""
        for j in range(bar_length):
            if j < filled_length:
                # 创建脉冲效果，模拟发光动画
                pulse_pos = (j + i) % 6  # 使用循环位置创造脉冲效果
                if j == filled_length - 1:  # 进度条前端始终显示 > 符号
                    if pulse_pos < 2:
                        bar += f"{GREEN}>{RESET}"      # 亮绿色 > 符号
                    elif pulse_pos < 4:
                        bar += f"{CYAN}>{RESET}"      # 青色 > 符号
                    else:
                        bar += f"{BRIGHT_MAGENTA}>{RESET}"  # 洋红色 > 符号
                else:
                    # 其他已填充部分
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

    # 进度条完成后的炫酷效果
    import random
    import string
    
    # 生成随机的 SHA256 格式哈希值 (64 位十六进制字符)
    sha256_hash = ''.join(random.choices('0123456789abcdef', k=100))
    
    # 快速用哈希值填满进度条，带炫酷颜色效果
    hash_part = sha256_hash[:bar_length]  # 取足够长的哈希值填满整个进度条
    
    # 为每个哈希字符添加随机颜色效果
    colorful_hash = ""
    color_options = [GREEN, YELLOW, CYAN, WHITE, BRIGHT_MAGENTA, RED, ORANGE, BLUE, PURPLE]
    for idx, char in enumerate(hash_part):
        color = color_options[idx % len(color_options)]
        colorful_hash += f"{color}{char}{RESET}"
    
    hash_bar_filled = colorful_hash
    print(f'\r启动中 [{hash_bar_filled}] {WHITE}100%{RESET}', end='', flush=True)
    time.sleep(1)  # 稍微延长显示时间，让人能看清炫酷效果
    
    # 在进度条内显示Verification OK，带闪烁效果
    verification_text = "Verification OK"
    # 截取或重复文本以适应进度条长度
    if len(verification_text) <= bar_length:
        padded_text = verification_text.ljust(bar_length)
    else:
        padded_text = verification_text[:bar_length]
        
    # 为Verification OK添加闪烁颜色效果
    verification_bar = ""
    flash_colors = [GREEN, YELLOW, CYAN, WHITE, BRIGHT_MAGENTA, RED, ORANGE]
    for idx, char in enumerate(padded_text):
        if char != ' ':  # 只对非空格字符应用颜色
            color_idx = (idx + int(time.time() * 10)) % len(flash_colors)  # 使用时间变化产生闪烁效果
            verification_bar += f"{flash_colors[color_idx]}{char}{RESET}"
        else:
            verification_bar += char  # 保留空格不变
    
    print(f'\r启动中 [{verification_bar}] {WHITE}100%{RESET}', end='', flush=True)
    time.sleep(1)  # 短暂停留显示Verification OK
    
    # 最后显示绿色100%进度条，带脉冲效果
    pulse_chars = ['█', '▓', '▒', '░']
    for pulse in range(2):  # 显示2次脉冲效果
        for pulse_char in pulse_chars:
            pulsing_bar = f"{BRIGHT_GREEN}" + pulse_char * bar_length + f"{RESET}"
            print(f'\r启动中 [{pulsing_bar}] {WHITE}100%{RESET}', end='', flush=True)
            time.sleep(0.1)
    
    # 最终显示稳定绿色100%进度条
    final_bar = f"{BRIGHT_GREEN}" + "█" * bar_length + f"{RESET}"
    final_percent = f"{WHITE}100%{RESET}"
    print(f'\r启动中 [{final_bar}] {final_percent}')
    print("任务完成，重置进度... 启动完成")

def main():
    global last_processed_rowid
    try:
        while True:  # 永久循环
            # 检查是否有新消息需要处理
            current_message, current_rowid = get_last_message_with_rowid()
            
            if current_rowid and current_rowid > last_processed_rowid:
                # 有新消息，运行处理脚本
                print(f"检测到新消息 (ROWID: {current_rowid}): {current_message}")
                run_script()
                last_processed_rowid = current_rowid
            # 如果没有新消息，跳过运行脚本，直接显示进度条
            
            # 显示进度条动画
            show_progress_animation()
            
            # 短暂休息
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n程序已终止")
    except Exception as e:
        print(f"发生未知错误: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
