"""
This module provides the ColorPrint class for printing colored messages
to the console. It supports different message types such as info, warning,
error, input, and user.
"""

class ColorPrint:
    """
    A class used to print colored messages to the console.
    
    Attributes
    ----------
    COLORS : dict
        A dictionary mapping message types to their corresponding ANSI color codes.
    """
    COLORS = {
        'info': '\033[92m[INFO]: \033[00m',
        'warning': '\033[93m[WARN]: \033[00m',
        'error': '\033[91m[ERROR]: \033[00m',
        'input': '\033[94m[INPUT]: \033[00m',
        'user': '\033[1;31m[USER]: \033[00m'
    }

    @staticmethod
    def print(message_type, message, end="\n"):
        """
        Prints a message to the console with a specified color based on the message type.
        
        Parameters
        ----------
        message_type : str
            The type of the message (e.g., 'info', 'warning', 'error', 'input', 'user').
        message : str
            The message to be printed.
        end : str, optional
            The end character (default is newline).
        """
        print(f"{ColorPrint.COLORS.get(message_type, '[UNKNOWN]: ')}{message}", end=end)

    @staticmethod
    def input(message):
        """
        Prompts the user for input with a colored message.
        
        Parameters
        ----------
        message : str
            The message to be displayed to the user.
        
        Returns
        -------
        str
            The user's input.
        """
        return input(f"{ColorPrint.COLORS['input']}{message}")

    @staticmethod
    def user_input(message):
        """
        Prompts the user for input with a colored user message.
        
        Parameters
        ----------
        message : str
            The message to be displayed to the user.
        
        Returns
        -------
        str
            The user's input.
        """
        return input(f"{ColorPrint.COLORS['user']}{message}")

if __name__ == '__main__':
    ColorPrint.print('info', 'This is an informational message')
