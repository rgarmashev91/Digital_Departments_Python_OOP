BOOKS_DATABASE = [
    {
        "id": 1,
        "name": "test_name_1",
        "pages": 200,
    },
    {
        "id": 2,
        "name": "test_name_2",
        "pages": 400,
    }
]


class Book:  # TODO написать класс Book
    def __init__(self, id_: int, name: str, pages: int):
        """
        Создание и подготовка к работе объекта "Книга"

        :param id_: идентификатор книги
        :param name: название книги
        :param pages: количество страниц в книге
        """
        self.check_data(id_, name, pages)

        self.id = id_
        self.name = name
        self.pages = pages

    @staticmethod
    def check_data(id_: int, name: str, pages: int) -> None:
        """
        Валидация входных данных
        """
        if not isinstance(id_, int):
            raise TypeError('Параметр id должен быть типа int')

        if not isinstance(name, str):
            raise TypeError('Параметр name должен быть типа str')

        if not isinstance(pages, int):
            raise TypeError('Параметр pages должен быть типа int')
        if pages <= 0:
            raise ValueError('Количество страниц должно быть положительным')

    def __str__(self):
        return f'Книга "{self.name}"'

    def __repr__(self):
        return f'{self.__class__.__name__}(id_={self.id}, name={self.name!r}, pages={self.pages})'


if __name__ == '__main__':
    # инициализируем список книг
    list_books = [
        Book(id_=book_dict["id"], name=book_dict["name"], pages=book_dict["pages"]) for book_dict in BOOKS_DATABASE
    ]
    for book in list_books:
        print(book)  # проверяем метод __str__

    print(list_books)  # проверяем метод __repr__
