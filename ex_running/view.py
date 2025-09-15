from ex_running import controller


def main():
    ctrl = controller.Controller()
    records = ctrl.preprocess()
    print(records)


if __name__ == "__main__":
    main()
