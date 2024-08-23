import subprocess
import merge_audio
def clip_video(input_video, output_video, start_time, duration):
    """
    自动剪辑视频
    :param input_video: 输入视频文件路径
    :param output_video: 输出视频文件路径
    :param start_time: 剪辑起始时间（秒）
    :param duration: 剪辑持续时间（秒）
    """
    # 构建ffmpeg命令
    command = [
        'ffmpeg',
        '-i', input_video,
        '-ss', f'{start_time}',
        '-t', f'{duration}',
        '-c', 'copy',
        output_video
    ]

    # 调用subprocess运行ffmpeg命令
    subprocess.run(command, check=True)

# 使用示例
#input_video_path = 'input.mp4'
input_video_path = 'D:\c.mp4'
output_video_path = 'input_video.mp4'
clip_start_time = 10  # 从10秒开始剪辑
clip_duration = 30    # 剪辑30秒的内容

clip_video(input_video_path, output_video_path, clip_start_time, clip_duration)