#!/bin/bash
#Inspired from https://unix.stackexchange.com/questions/230481/how-to-download-portion-of-video-with-youtube-dl-command
# prerequisite
# 1-Youtube-dl https://ytdl-org.github.io/youtube-dl/index.html
# 2-FFMPEG https://www.ffmpeg.org/
if [ $# -lt 4 ]; then
        echo "Usage: $0 <youtube's URL> <HH:mm:ss from time> <HH:mm:ss to time> <output_file_name>"
        echo "e.g.:"
        echo "$0 https://www.youtube.com/watch?v=T1n5gXIPyws 00:00:25 00:00:42 intro.mp4"
        exit 1
fi

echo "processing..."

from=$(date "+%s" -d "UTC 01/01/1970 $2")
to=$(date "+%s" -d "UTC 01/01/1970 $3")

from_pre=$(($from - 30))

if [ $from_pre -lt 0 ]
then
        from_pre=0
fi

from_pre_command_print=$(date -u "+%T" -d @$from_pre)
from_command_print=$(date -u "+%T" -d @$(($from - $from_pre)))$(grep -o "\..*" <<< $2)
to_command_print=$(date -u "+%T" -d @$(($to - $from_pre)))$(grep -o "\..*" <<< $3)

command="ffmpeg "

for uri in $(youtube-dl -g $1)
do
        command+="-ss $from_pre_command_print -i $uri "
done

command+="-map 0:v -map 1:a -ss $from_command_print -to $to_command_print  -c:v libx264 -c:a aac $4"
$command