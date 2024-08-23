import subprocess

# 构建FFmpeg命令
commands = []
# 输出文件名
output_file = 'clips_concatenated.mp4'
# 删除临时文件
temp_files = []
with open("filename.txt", "r") as file:
    i = 0
    for line in file:
        times = line.strip().split(',')
        start = times[1]
        end = times[2]
        temp_file = f'temp{i}.ts'
        print(temp_file)
        temp_files.append(temp_file)
        commands.append(f'ffmpeg -i {times[0]} -ss {start} -to {end} -c copy -f mpegts temp{i}.ts')
        i = i + 1

#commands.append(f'ffmpeg -f concat -i input.txt -c copy {output_file}')

commands.append([
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'input.txt',
    '-c', 'copy',
    output_file
])
# 执行命令
for command in commands:
    print(command)
    subprocess.run(command, shell=True)

# # 删除临时文件
# for temp_file in temp_files:
#     try:
#         subprocess.run(f'rm {temp_file}', shell=True)
#     except Exception as e:
#         print(f'Error deleting temp file: {e}')