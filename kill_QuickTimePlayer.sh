##########################################################################
# File Name: kill_QuickTimePlayer.sh
# Author: zbb
# Created Time: 四  1/18 19:49:35 2024
#########################################################################
#!/bin/bash
pid=`ps -ef | grep QuickTime | grep -v grep | awk -F " " '{print $2}'`
kill -9 $pid
