## 用iphone操作你的mac

该技术用到了python3及sqlite数据库与AppleScript

示例为关键字触发任务

如果要使用请修改Applescript

### Start_MessageMovie.py

```sh
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
```

更改sqlite关键字My_Message

更改路径中ZBB为YourMacName

## 重要提示

此项目需要访问macOS的Messages数据库，由于安全和隐私原因，现代macOS系统对此类访问进行了限制。您需要手动授予相应权限。

## 设置步骤

### 1. 授予终端完全磁盘访问权限

1. 打开"系统偏好设置" > "安全性与隐私" > "隐私"标签页
2. 在左侧列表中选择"完全磁盘访问权限"
3. 点击左下角的锁图标并输入密码解锁
4. 点击"+"按钮，前往"/Applications/Utilities/Terminal.app"添加终端应用
5. 或者如果您使用IDE，也需将IDE添加到列表中

### 2. 授予辅助功能权限

1. 打开"系统偏好设置" > "安全性与隐私" > "隐私"标签页
2. 在左侧列表中选择"辅助功能"
3. 点击左下角的锁图标并输入密码解锁
4. 点击"+"按钮，添加您运行Python脚本的应用（如终端、PyCharm等）
5. 这样才能允许脚本控制QuickTime Player

### 3. 检查iMessage账户设置

确保您的Mac上已登录iMessage账户：
1. 打开"信息"应用
2. 前往"偏好设置" > "iMessage"
3. 确认账户已登录并启用

### 4. 运行项目

完成上述设置后，您可以运行项目：

```bash
# 启动项目
./start_env.sh

# 或者直接运行
source AppleScMv/bin/activate
python3 While_Message.py
```

### 5. 使用说明

- 通过iPhone上的信息应用向Mac发送"hello"将启动屏幕录制并锁屏
- 发送"stop"将停止录制并将视频文件保存到movie目录

### 6. 故障排除

如果仍然遇到"authorization denied"错误：

1. 确认已按上述步骤设置权限
2. 重启Mac以确保权限生效
3. 检查iMessage是否正在运行且已登录
4. 如果使用Python虚拟环境，请确保虚拟环境也获得了相应权限

注意：如果iMessage从未在Mac上使用过，可能不存在chat.db文件。需要先在Mac上使用信息应用发送/接收一条消息以创建数据库。
