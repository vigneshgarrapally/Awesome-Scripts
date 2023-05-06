<#
USAGE: 
powershell\yt-dl_trim.ps1 -yt_url https://www.youtube.com/watch?v=T1n5gXIPyws -start 00:00:05 -end 00:00:35
prerequisite
1-Youtube-dl https://ytdl-org.github.io/youtube-dl/index.html
2-FFMPEG https://www.ffmpeg.org/
#>
param (
    [Parameter(Mandatory=$true)][string]$yt_url,
    [string]$output="output.mp4",
    [string]$start= $( Read-Host " Enter Start Time"),
    [string]$end = $( Read-Host "Enter End Time, please" )
 )
Write-Output "processing..."
$buffer="00:00:30"
$TimeDiff = New-TimeSpan $buffer $start
if($TimeDiff.Seconds -lt 0)
{
    $start_pre="00:00:00"
    $temp=$start

}
else {
    $hrs,$mns,$sec = ($TimeDiff.Hours),($TimeDiff.Minutes),($TimeDiff.Seconds)
    $start_pre='{0:00}:{1:00}:{2:00}' -f $hrs,$mns,$sec
    $temp="00:00:30"
}
$duration=New-TimeSpan $start $end
$diff='{0:00}:{1:00}:{2:00}' -f $duration.Hours,$duration.Minutes,$duration.Seconds
$video_url,$audio_url=yt-dlp --youtube-skip-dash-manifest -g $yt_url
$command="ffmpeg -ss  $start_pre -i '$video_url' -ss $start_pre -i '$audio_url' -map 0:v -map 1:a -ss $temp -t $diff -c:v libx264 -c:a aac $output"
#Write-Output "downloading with the following command:"
#Write-Output "$command"
Invoke-Expression $command


        
