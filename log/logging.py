from typing import Optional, Any, Callable
from functools import wraps

file_path = r'C:\Users\liudo\PycharmProjects\Project1_eroshkinalv\log'


def log(filename: Optional[str] = None) -> Callable:

    """Декоратор для логирования вызовов функции и их результатов.
        :param filename: Имя файла для логирования. Если не указано, логирование происходит в консоль.
        :return: Обёртка для декорируемой функции."""

    def log_decorator(my_function: Callable) -> Callable:
        @wraps(my_function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            try:
                result = my_function(*args, **kwargs)

                for arg in args:
                    if not isinstance(arg, int) or isinstance(arg, float):
                        raise TypeError()

            except TypeError:

                if filename is not None:
                    with open(rf'..\log\{filename}.log', "a", encoding="utf-8") as file:
                        file.write(f"my_function error: <TypeError>. Inputs: {args}, {kwargs}\n")

                return f"my_function error: <TypeError>. Inputs: {args}, {kwargs}\n"

            else:

                if filename is not None:
                    with open(rf'..\log\{filename}.log', "a", encoding="utf-8") as file:
                        file.write("my_function ok\n")
                        return result
                else:
                    return result

        return wrapper
    return log_decorator
