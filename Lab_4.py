from typing import Union


class TransmissionLine:
    def __init__(self, disp_name: str, length: Union[int, float], u_nom: Union[int, float]):
        """
        Создание и подготовка к работе объекта "Линия электропередачи"

        :param disp_name: Диспетчерское наименование ЛЭП (униакльное и неизменное)
        :param length: Длина ЛЭП, км (фактическое/реальное значение)
        :param u_nom: Номинальное напряжение ЛЭП, кВ
        """
        self._disp_name = None
        self.length = None
        self.u_nom = None
        self._set_line_data(disp_name, length, u_nom)

        self.conditional_length = self.length  # Условное значение длины ЛЭП, используемое в технических расчетах

    def __str__(self):
        return f'Линия электропередачи: {self._disp_name}'

    def __repr__(self):
        return f'{self.__class__.__name__}(disp_name={self._disp_name}, length={self.length}, u_nom={self.u_nom})'

    def _set_line_data(self, disp_name: str, length: Union[int, float], u_nom: Union[int, float]) -> None:
        """
        Валидация данных ЛЭП (метод для использования внутри класса)

        :param disp_name: Диспетчерское наименование ЛЭП (униакльное и неизменное)
        :param length: Длина ЛЭП, км
        :param u_nom: Номинальное напряжение ЛЭП, кВ

        :raise ValueError: Если длина ЛЭП неположительная, то вызываем ошибку
        :raise ValueError: Если номинальное напряжение ЛЭП неположительное, то вызываем ошибку
        """
        if not isinstance(disp_name, str):
            raise TypeError('Disp_name must be "str" type')

        if not isinstance(length, (int, float)):
            raise TypeError('Length must be "int" or "float" type')
        if length <= 0:
            raise ValueError('Length must be > 0')

        if not isinstance(u_nom, (int, float)):
            raise TypeError('U_nom must be "int" or "float" type')
        if u_nom <= 0:
            raise ValueError('U_nom must be > 0')

        self._disp_name = disp_name
        self.length = length
        self.u_nom = u_nom

    @property
    def disp_name(self):
        return self._disp_name

    def is_backbone_line(self) -> bool:
        """
        Определение по критерию номинального напряжения: является ли ЛЭП системообразующей

        :return: Логическое значение в соответствии с критерием
        """
        if self.u_nom >= 330:
            print(f'Линия {self._disp_name!r} - системообразующая')
            return True
        else:
            print(f'Линия {self._disp_name!r} - не системообразующая')
            return False

    def add_parallel_lines(self, num_of_lines: int) -> None:
        """
        Изменение условной длины ЛЭП при добавлении/учете параллельных линий/цепей

        :param num_of_lines: Общее количество параллельных линий/цепей

        :raise ValueError: Если количество параллельных линий/цепей неположительное, то вызываем ошибку
        """
        if not isinstance(num_of_lines, int):
            raise TypeError('Num_of_lines must be "int" type')
        if num_of_lines <= 0:
            raise ValueError('Num_of_lines must be > 0')

        self.conditional_length /= num_of_lines


class OverheadLine(TransmissionLine):
    def __init__(self, disp_name: str, length: Union[int, float], u_nom: Union[int, float], z: complex, y: complex):
        """
        Создание и подготовка к работе объекта "Воздушная линия"

        :param disp_name: Диспетчерское наименование ЛЭП (униакльное и неизменное)
        :param length: Длина ЛЭП, км
        :param u_nom: Номинальное напряжение ЛЭП, кВ
        :param z: Комплексное (полное) сопротивление ВЛ, Ом
        :param y: Комплексная (полная) проводимость ВЛ на землю, мкСм
        """
        super().__init__(disp_name, length, u_nom)
        self.z = None
        self.y = None
        self._set_overhead_line_data(z, y)

    def __repr__(self):
        return f'{self.__class__.__name__}(disp_name={self._disp_name!r}, length={self.length}, u_nom={self.u_nom}, ' \
               f'z={self.z}, y={self.y})'

    def _set_overhead_line_data(self, z: complex, y: complex) -> None:
        """
        Валидация данных ВЛ (метод для использования внутри класса)

        :param z: Комплексное (полное) сопротивление ВЛ, Ом
        :param y: Комплексная (полная) проводимость ВЛ на землю, мкСм

        :raise ValueError: Если действительная часть полного сопротивления отрицательная, то вызываем ошибку
        :raise ValueError: Если мнимая часть полного сопротивления неположителная, то вызываем ошибку
        :raise ValueError: Если действительная часть полной проводимости отрицательная, то вызываем ошибку
        :raise ValueError: Если мнимая часть полной проводимости неположителная, то вызываем ошибку
        """
        if not isinstance(z, complex):
            raise TypeError('Z must be "complex" type')
        if z.real < 0:
            raise ValueError('Real part of Z must be >= 0')
        if z.imag <= 0:
            raise ValueError('Imaginary part of Z must be > 0')

        if not isinstance(y, complex):
            raise TypeError('Y must be "complex" type')
        if y.real < 0:
            raise ValueError('Real part of Y must be >= 0')
        if y.imag <= 0:
            raise ValueError('Imaginary part of Y must be > 0')

        self.z = z
        self.y = y

    def add_parallel_lines(self, num_of_lines: int) -> None:
        """
        Изменение параметров ВЛ при добавлении/учете параллельных линий/цепей
        Перегрузка метода родительского класса в связи с наличием конкретных параметров ВЛ

        :param num_of_lines: Общее количество параллельных линий/цепей

        :raise ValueError: Если количество параллельных линий/цепей неположительное, то вызываем ошибку
        """
        if not isinstance(num_of_lines, int):
            raise TypeError('Num_of_lines must be "int" type')
        if num_of_lines <= 0:
            raise ValueError('Num_of_lines must be > 0')

        self.z /= num_of_lines
        self.y *= num_of_lines


class CableLine(TransmissionLine):
    def __init__(self, disp_name: str, length: Union[int, float], u_nom: Union[int, float], z: complex, y: complex,
                 insulator: str):
        """
        Создание и подготовка к работе объекта "Кабельная линия"

        :param disp_name: Диспетчерское наименование ЛЭП (униакльное и неизменное)
        :param length: Длина ЛЭП, км
        :param u_nom: Номинальное напряжение ЛЭП, кВ
        :param z: Комплексное (полное) сопротивление КЛ, Ом
        :param y: Комплексная (полная) проводимость КЛ на землю, мкСм
        :param insulator: Материал изоляции кабеля (определяется при проектировании и монтаже)
        """
        super().__init__(disp_name, length, u_nom)
        self.z = None
        self.y = None
        self._insulator = None
        self._set_cable_line_data(z, y, insulator)

    def __repr__(self):
        return f'{self.__class__.__name__}(disp_name={self._disp_name!r}, length={self.length}, u_nom={self.u_nom}, ' \
               f'z={self.z}, y={self.y}, insulator={self._insulator})'

    def _set_cable_line_data(self, z: complex, y: complex, insulator: str) -> None:
        """
        Валидация данных КЛ (метод для использования внутри класса)

        :param z: Комплексное (полное) сопротивление КЛ, Ом
        :param y: Комплексная (полная) проводимость КЛ на землю, мкСм
        :param insulator: Материал изоляции кабеля (определяется при проектировании и монтаже)

        :raise ValueError: Если действительная часть полного сопротивления отрицательная, то вызываем ошибку
        :raise ValueError: Если мнимая часть полного сопротивления неположителная, то вызываем ошибку
        :raise ValueError: Если действительная часть полной проводимости отрицательная, то вызываем ошибку
        :raise ValueError: Если мнимая часть полной проводимости неположителная, то вызываем ошибку
        """
        if not isinstance(z, complex):
            raise TypeError('Z must be "complex" type')
        if z.real < 0:
            raise ValueError('Real part of Z must be >= 0')
        if z.imag <= 0:
            raise ValueError('Imaginary part of Z must be > 0')

        if not isinstance(y, complex):
            raise TypeError('Y must be "complex" type')
        if y.real < 0:
            raise ValueError('Real part of Y must be >= 0')
        if y.imag <= 0:
            raise ValueError('Imaginary part of Y must be > 0')

        if not isinstance(insulator, str):
            raise TypeError('Insulator must be "str" type')

        self.z = z
        self.y = y
        self._insulator = insulator

    @property
    def insulator(self):
        return self._insulator

    def add_parallel_lines(self, num_of_lines: int) -> None:
        """
        Изменение параметров КЛ при добавлении/учете параллельных линий/цепей
        Перегрузка метода родительского класса в связи с наличием конкретных параметров КЛ

        :param num_of_lines: Общее количество параллельных линий/цепей

        :raise ValueError: Если количество параллельных линий/цепей неположительное, то вызываем ошибку
        """
        if not isinstance(num_of_lines, int):
            raise TypeError('Num_of_lines must be "int" type')
        if num_of_lines <= 0:
            raise ValueError('Num_of_lines must be > 0')

        self.z /= num_of_lines
        self.y *= num_of_lines


if __name__ == '__main__':
    base_line = TransmissionLine('ВЛ-330 Каменный Бор-Петрозаводск', 171, 330)
    print(base_line)
    print(repr(base_line) + '\n')

    line_1 = OverheadLine('ВЛ-330 Кондопога-Петрозаводск', 76, 330, 1+1j, 0.5+0.5j)
    print(line_1)
    print(repr(line_1) + '\n')

    line_2 = CableLine('КЛ-220 Василеостровская-Северная', 4.8, 220, 0.1+0.1j, 0.05+0.05j, 'XLPE')
    print(line_2)
    print(repr(line_2) + '\n')

    base_line.is_backbone_line()
    line_1.is_backbone_line()
    line_2.is_backbone_line()
    print()

    base_line.add_parallel_lines(3)
    print(base_line.conditional_length)
    print()

    line_1.add_parallel_lines(2)
    print(line_1.conditional_length)
    print(line_1.z)
    print(line_1.y)
    print()

    line_2.add_parallel_lines(2)
    print(line_2.conditional_length)
    print(line_2.z)
    print(line_2.y)
