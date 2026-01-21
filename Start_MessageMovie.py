import os
import sqlite3
import shutil
import logging

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    handlers=[
        logging.FileHandler("app.log"),  # 将日志写入文件
        logging.StreamHandler()  # 将日志输出到控制台
    ]
)

def execute_applescript():
    applescript = """
    tell application "QuickTime Player"
        activate
        new movie recording
        start document 1
        set miniaturized of window 1 to true
        delay 1 -- 延迟10秒以确保录制开始
        tell application "System Events"
            keystroke "q" using {command down, control down} -- 锁屏
        end tell
    end tell
    """
    os.system("osascript -e '{}'".format(applescript))

def get_last_message():
    # 连接到SQLite数据库
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    if not os.path.exists(db_path):
        logging.warning(f"Database does not exist: {db_path}")
        return None
        
    with sqlite3.connect(db_path) as conn:
        # 创建一个游标对象
        cur = conn.cursor()

        # 执行一个SQL查询，获取message表中最后一条数据的ROWID
        cur.execute("SELECT text FROM message ORDER BY ROWID DESC LIMIT 1")

        # 获取查询结果
        result = cur.fetchone()

    return result[0] if result is not None else None

def copy_directory(src_dir, dst_dir):
    # 遍历源目录下的所有目录
    for dirpath, dirnames, filenames in os.walk(src_dir):
        logging.info(f"Checking directories in {dirpath}: {dirnames}")  # 调试信息
        for dirname in dirnames:
            # 如果目录名包含'qtpxcomposition'
            if 'qtpxcomposition' in dirname:
                src_path = os.path.join(dirpath, dirname)
                logging.info(f"Found directory: {src_path}")
                dst_path = os.path.join(dst_dir, dirname)
                logging.info(f"Destination path: {dst_path}")
                
                # 如果目标目录已存在同名的目录，则跳过拷贝操作
                if os.path.exists(dst_path):
                    logging.info(f"Directory {dst_path} already exists. Skipping copy operation.")
                    continue
                
                # 拷贝目录
                try:
                    shutil.copytree(src_path, dst_path)
                    logging.info(f"Successfully copied {src_path} to {dst_path}")
                except Exception as e:
                    logging.error(f"Failed to copy {src_path} to {dst_path}. Error: {e}")

My_Message = get_last_message()

if My_Message and My_Message.lower() == "hello":
    execute_applescript()
elif My_Message and My_Message.lower() == "stop":
    os.system('sh kill_QuickTimePlayer.sh')
    # 源目录和目标目录
    src_dir = os.path.expanduser("~/Library/Containers/com.apple.QuickTimePlayerX/Data/Library/Autosave Information/")
    dst_dir = "./movie/"
    copy_directory(src_dir, dst_dir)
