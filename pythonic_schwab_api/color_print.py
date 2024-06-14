class ColorPrint:
    COLORS = {
        'info': '\033[92m[INFO]: \033[00m',
        'warning': '\033[93m[WARN]: \033[00m',
        'error': '\033[91m[ERROR]: \033[00m',
        'input': '\033[94m[INPUT]: \033[00m',
        'user': '\033[1;31m[USER]: \033[00m'
    }

    @staticmethod
    def print(message_type, message, end="\n"):
        print(f"{ColorPrint.COLORS.get(message_type, '[UNKNOWN]: ')}{message}", end=end)

    @staticmethod
    def input(message):
        return input(f"{ColorPrint.COLORS['input']}{message}")

    @staticmethod
    def user_input(message):
        return input(f"{ColorPrint.COLORS['user']}{message}")



if __name__ == '__main__':
    ColorPrint.print('info', 'This is an informational message')
