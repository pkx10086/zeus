import db_conn;

import os
import time
import DESUtil

class RangeRemove(object):
    def __init__(self, root_path, delete_path):
        self.root_path = root_path
        self.actual_path = root_path + delete_path

    def delete_files_recursively(self):
        # 检查路径是否存在且是目录
        if not os.path.exists(self.actual_path) or not os.path.isdir(self.actual_path):
            print(f"错误: '{self.actual_path}' 不是一个有效的目录路径。")
            return

        start_time = time.time()
        total_deleted_files = 0
        total_deleted_size = 0

        # 递归遍历目录及其子目录中的所有文件
        for root_dir, dirs, files in os.walk(self.actual_path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    total_deleted_files += 1
                    total_deleted_size += file_size
                    print(f"已删除: {file_path}")
                except Exception as e:
                    print(f"删除 {file_path} 时出错: {e}")

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"删除完成！总共删除了 {total_deleted_files} 个文件，总大小约为 {total_deleted_size / (1024 ** 3):.2f} GB.")
        print(f"耗时: {elapsed_time:.2f} 秒.")


# 使用示例
directory_to_path= '/var/www/dream/webroot/range/'
if __name__ == '__main__':
    db_connect = db_conn.DBConnect()
    lives = db_connect.read_db("select * from record where user_id=16 limit 1")
    print(lives)
    for data in lives:
        delete_path = "accountid-{}/liveid-{}/".format(DESUtil.id_encrypt(str(data[3])), DESUtil.id_encrypt(str(data[0])))
        print(delete_path)
        #拼接删除目录
        rangeRemove = RangeRemove(directory_to_path, delete_path)
        rangeRemove.delete_files_recursively()



