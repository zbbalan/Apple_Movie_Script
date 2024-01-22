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

