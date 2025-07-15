from user import User
def main():
    user = User()
    user.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        input('运行完毕，按回车键退出...')
