import subprocess


def run_batch_file(batch_file_path):
    """
    使用subprocess模块执行批处理文件，并捕获输出结果
    该函数运行一个批处理文件，捕获其输出，并返回执行结果
    参数:
        batch_file_path (str): 批处理文件的路径
    返回值:
        tuple: 包含退出状态码、标准输出和错误输出
    """
    try:
        # 启动批处理文件，并捕获输出结果
        process = subprocess.run(['cmd', '/c', batch_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, cwd="NapCat")
    except subprocess.CalledProcessError as e:
        # 捕获异常，返回错误信息
        return e.returncode, e.stdout, e.stderr


if __name__ == '__main__':
    batch_file_path = "launcher.bat"
    return_code, stdout, stderr = run_batch_file(batch_file_path)

    if return_code == 0:
        print("NapCat启动文件执行成功！")
    else:
        print(f"NapCat启动文件执行失败！\nstdout: {stdout}\nstderr: {stderr}")

    # 假设 server 是一个已经定义好的模块
    import server

    server.app.run(host='0.0.0.0', port=8080, debug=False)
