import subprocess


def merge_videos(input_video, input_video2, output_video):
    """
   自动剪辑视频
   :param input_video: 输入视频文件路径
   :param output_video: 输出视频文件路径
   """
    # 构建ffmpeg命令
    command = [
        'ffmpeg',
        '-i', input_video,
        '-i', input_video2,
        '-filter_complex', '[0:v:0][0:a:0] [1:v:0][1:a:0] concat=n=2:v=1:a=1 [v] [a]',
        '-map', '[v]', '-map', '[a]',
        output_video
    ]
    # 调用FFmpeg命令
    subprocess.run(command)


# 使用函数合并视频
merge_videos('input_video.mp4', 'input_video2.mp4', 'merged_video.mp4')
