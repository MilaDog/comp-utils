import re


class Files:
    """Collection of helper functions related to handling files."""

    @staticmethod
    def extract_ints(file: str) -> list[int]:
        """Extract all integers from the given `file`.

        Args:
            file (str): File to parse for integers.

        Returns:
            list[int]: Iterable of all extracted integers from the file.
        """
        content: str = open(file, "r").read()

        return list(map(int, re.findall(r"\d+", content)))

    @staticmethod
    def extract_floats(file: str) -> list[float]:
        """Extract all floats from the given `file`.

        Args:
            file (str): String to parse for floats.

        Returns:
            list[float]: Iterable of all extracted floats from the file.
        """
        content: str = open(file, "r").read()
        return list(map(float, re.findall(r"\d+.\d+", content)))
