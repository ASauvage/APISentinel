

class Error:
    @property
    def explicit_content(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return "{}: unexpected error occured".format(
            self.explicit_content
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content
        )


class HttpCodeError(Error):
    def __init__(self, status_code: int):
        self.status_code = status_code

    def __str__(self) -> str:
        return "{}: request return an error code {}".format(
            self.explicit_content,
            self.status_code
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            status_code=self.status_code
        )


class NotJsonError(Error):
    def __init__(self):
        pass

    def __str__(self) -> str:
        return "{}: response did not return content in JSON format".format(
            self.explicit_content
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content
        )


class MissingFieldError(Error):
    def __init__(self, field: list[str | int]):
        self.field = field

    def __str__(self) -> str:
        return "{}: field '{}' is missing".format(
            self.explicit_content,
            '.'.join(map(str, self.field)),
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field
        )


class WrongTypeError(Error):
    def __init__(self, field: list[str | int], received: type, expected: list[type]):
        self.field = field
        self.received = received
        self.expected = expected

    def __str__(self) -> str:
        return "{}: '{}' should be a(n) {} not '{}'".format(
            self.explicit_content,
            '.'.join(map(str, self.field)),
            [x.__name__ for x in self.expected],
            self.received.__name__
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field,
            received=self.received,
            expected=self.expected
        )


class WrongValueError(Error):
    def __init__(self, field: list[str | int], received: any, expected: list[any]):
        self.field = field
        self.received = received
        self.expected = expected

    def __str__(self) -> str:
        return "{}: '{}' should be in {} but got '{}' instead".format(
            self.explicit_content,
            '.'.join(map(str, self.field)),
            self.expected,
            self.received
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field,
            received=self.received,
            expected=self.expected
        )


class WrongFormatError(Error):
    def __init__(self, field: list[str | int], received: type, expected: str):
        self.field = field
        self.received = received
        self.expected = expected

    def __str__(self) -> str:
        return "{}: '{}' should be a(n) '{}' but got '{}' instead".format(
            self.explicit_content,
            '.'.join(map(str, self.field)),
            self.expected,
            self.received.__name__
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field,
            received=self.received,
            expected=self.expected
        )


class WrongDatetimeFormatError(Error):
    def __init__(self, field: list[str | int], received: str, format: str):
        self.field = field
        self.received = received
        self.format = format

    def __str__(self) -> str:
        return "{}: '{}' does not follow the '{}' format, got '{}'".format(
            self.explicit_content,
            '.'.join(map(str, self.field)),
            self.format,
            self.received
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field,
            format=self.format,
            received=self.received
        )


class RegexError(Error):
    def __init__(self, field: list[str | int], pattern: str, value: str):
        self.field = field
        self.pattern = pattern
        self.value = value

    def __str__(self) -> str:
        return "{}: '{}' should match pattern '{}' but got '{}'".format(
            self.explicit_content,
            '.'.join(map(str, self.field)),
            self.pattern,
            self.value
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field,
            pattern=self.pattern,
            value=self.value
        )


class EmptyStringError(Error):
    def __init__(self, field: list[str | int]):
        self.field = field

    def __str__(self) -> str:
        return "{}: '{}' return an empty string".format(
            self.explicit_content,
            '.'.join(map(str, self.field))
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field
        )


class MinLenghtError(Error):
    def __init__(self, field: list[str | int], received: int, expected: int):
        self.field = field
        self.received = received
        self.expected = expected

    def __str__(self) -> str:
        return "{}: '{}' got {} values but {} minimum required".format(
            self.explicit_content,
            '.'.join(map(str, self.field)),
            self.received,
            self.expected
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field,
            received=self.received,
            expected=self.expected
        )


class MaxLenghtError(Error):
    def __init__(self, field: list[str | int], received: int, expected: int):
        self.field = field
        self.received = received
        self.expected = expected

    def __str__(self) -> str:
        return "{}: '{}' got {} values but {} maximum required".format(
            self.explicit_content,
            '.'.join(map(str, self.field)),
            self.received,
            self.expected
        )

    def as_dict(self) -> dict[str, any]:
        return dict(
            explicit_content=self.explicit_content,
            field=self.field,
            received=self.received,
            expected=self.expected
        )
