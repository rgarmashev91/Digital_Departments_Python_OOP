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
        self.id = None
        self.name = None
        self.pages: None

        self.check_data(id_, name, pages)

        self.id = id_
        self.name = name
        self.pages = pages

    @staticmethod
    def check_data(id_, name, pages) -> None:
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


class Library:  # TODO написать класс Library
    def __init__(self, books: list = None):
        """
        Создание и подготовка к работе объекта "Библиотека"

        :param books: список книг
        """
        if books is None:
            self.books = []
        else:
            self.books = books

    def get_next_book_id(self) -> int:
        """
        Метод, возвращающий идентификатор для добавления новой книги в библиотеку
        """
        if len(self.books) == 0:
            return 1
        else:
            return self.books[-1].id + 1

    def get_index_by_book_id(self, id_) -> int | str:
        """
        Метод, возвращающий индекс книги в списке, который хранится в атрибуте экземпляра класса

        :param id_: запрашиваемый id книги
        """
        try:
            id_list = [book.id for book in self.books]
            return id_list.index(id_)
        except ValueError:
            return 'Книги с запрашиваемым id не существует'


if __name__ == '__main__':
    empty_library = Library()  # инициализируем пустую библиотеку
    print(empty_library.get_next_book_id())  # проверяем следующий id для пустой библиотеки

    list_books = [
        Book(id_=book_dict["id"], name=book_dict["name"], pages=book_dict["pages"]) for book_dict in BOOKS_DATABASE
    ]
    library_with_books = Library(books=list_books)  # инициализируем библиотеку с книгами
    print(library_with_books.get_next_book_id())  # проверяем следующий id для непустой библиотеки

    print(library_with_books.get_index_by_book_id(1))  # проверяем индекс книги с id = 1
