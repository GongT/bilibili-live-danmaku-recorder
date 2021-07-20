try:
    if __name__ != '__main__':
        raise Exception("此文件必须直接运行")
    else:
        from mapper.main import main
        main()
except SystemExit:
    pass
