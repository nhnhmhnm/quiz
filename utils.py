class InputCancelled(Exception):
    """사용자가 입력을 중단했을 때 프로그램 흐름을 정리하기 위한 예외."""


def prompt_input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt) as error:
        raise InputCancelled() from error
