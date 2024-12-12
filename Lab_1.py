# TODO Написать 3 класса с документацией и аннотацией типов
from typing import Union
import doctest


class TransmissionLine:
    def __init__(self, r: Union[int, float], x: Union[int, float], b: Union[int, float], length: Union[int, float]):
        """
        Создание и подготовка к работе объекта "Линия электропередачи"

        :param r: Активное сопротивление ЛЭП, Ом/км
        :param x: Реактивное сопротивление ЛЭП, Ом/км
        :param b: Реактивная проводимость ЛЭП на землю, мкСм/км
        :param length: Длина ЛЭП, км

        Примеры:
        >>> line_1 = TransmissionLine(0.01, 0.03, 3.25, 100) # Инициализация экзкмпляра класса
        """
        if not isinstance(length, (int, float)):
            raise TypeError('Неверный тип данных: длина линии')
        if length <= 0:
            raise ValueError('Длина линии должна быть полпожительным')
        self.length = length

        if not isinstance(r, (int, float)):
            raise TypeError('Неверный тип данных: активное сопротивление линии')
        if r < 0:
            raise ValueError('Активное сопротивление линии должно быть неотрицательным')
        self.R_line = r * length

        if not isinstance(x, (int, float)):
            raise TypeError('Неверный тип данных: реактивное сопротивление линии')
        if x <= 0:
            raise ValueError('Реактивное сопротивление линии должно быть положительным')
        self.X_line = x * length

        if not isinstance(b, (int, float)):
            raise TypeError('Неверный тип данных: реактивная проводимость линии на землю')
        if b < 0:
            raise ValueError('Реактивная проводимость линии на землю должна быть неотрицательной')
        self.B_line = b * length * 10 ** (-6)

    def add_parallel_lines(self, num_of_lines: int) -> None:
        """
        Изменение параметров линии при добавлении/учете параллельных линий/цепей.

        :param num_of_lines: Общее количество параллельных линий/цепей

        :raise ValueError: Если количество параллельных линий/цепей неположительное, то вызываем ошибку

        Примеры:
        >>> line_1 = TransmissionLine(0.01, 0.03, 3.25, 100)
        >>> line_1.add_parallel_lines(2)
        """
        if not isinstance(num_of_lines, int):
            raise TypeError('Неверный тип данных: количество параллельных линий/цепей')
        if num_of_lines <= 0:
            raise ValueError('Количество параллельных линий/цепей должно быть положительным')
        self.R_line /= num_of_lines
        self.X_line /= num_of_lines
        self.B_line *= num_of_lines

    def line_compensation(self, x_comp: Union[int, float]) -> None:
        """
        Изменение параметров линии при добавлении/учете УПК (устройства продольной компенсации)

        :param x_comp: Емкостное сопротивление (отрицательное) УПК

        :raise ValueError: Если емкостное сопротивление УПК положительное, то вызываем ошибку

        Примеры:
        >>> line_1 = TransmissionLine(0.01, 0.03, 3.25, 100)
        >>> line_1.line_compensation(-15)
        """
        if not isinstance(x_comp, (int, float)):
            raise TypeError('Неверный тип данных: емкостное сопротивление УПК')
        if x_comp > 0:
            raise ValueError('Емкостное сопротивление УПК должно быть отрицательным')
        self.X_line += x_comp


class Transformer:
    def __init__(self, r: Union[int, float], x: Union[int, float], b: Union[int, float],
                 u_hv: Union[int, float], u_lv: Union[int, float]):
        """
        Создание и подготовка к работе объекта "Трансформатор"

        :param r: Активное сопротивление тр-ра (приведенное к обмоке ВН), Ом
        :param x: Реактивное сопротивление тр-ра (приведенное к обмотке ВН), Ом
        :param b: Реактивная проводимость тр-ра на землю (приведенная к обмотке ВН), мкСм
        :param u_hv: Номинальное напряжение обмотки ВН тр-ра, кВ
        :param u_lv: Номинальное напряжение обмотки НН тр-ра, кВ

        Примеры:
        >>> trans_1 = Transformer(2, 20, -15, 110, 10) # Инициализация экзкмпляра класса
        """
        if not isinstance(r, (int, float)):
            raise TypeError('Неверный тип данных: активное сопротивление тр-ра')
        if r < 0:
            raise ValueError('Активное сопротивление тр-ра должно быть неотрицательным')
        self.R_trans = r

        if not isinstance(x, (int, float)):
            raise TypeError('Неверный тип данных: реактивное сопротивление тр-ра')
        if x <= 0:
            raise ValueError('Реактивное сопротивление тр-ра должно быть положительным')
        self.X_trans = x

        if not isinstance(b, (int, float)):
            raise TypeError('Неверный тип данных: реактивная проводимость тр-ра на землю')
        if b > 0:
            raise ValueError('Реактивная проводимость тр-ра на землю должна быть неположительной')
        self.B_trans = b * 10 ** (-6)

        if not isinstance(u_hv, (int, float)):
            raise TypeError('Неверный тип данных: номинальное напряжение обмотки ВН тр-ра')
        if u_hv <= 0:
            raise ValueError('Номинальное напряжение обмотки ВН тр-ра должно быть положительным')
        self.U_high_volt = u_hv

        if not isinstance(u_lv, (int, float)):
            raise TypeError('Неверный тип данных: номинальное напряжение обмотки НН тр-ра')
        if u_lv <= 0:
            raise ValueError('Номинальное напряжение обмотки НН тр-ра должно быть положительным')
        self.U_low_volt = u_lv

        self.k_trans = u_lv / u_hv

    def bring_to_low_voltage(self) -> None:
        """
        Изменение параметров тр-ра при их приведении к обмотке НН

        Примеры:
        >>> trans_1 = Transformer(2, 20, -15, 115, 10.5)
        >>> trans_1.bring_to_low_voltage()
        """
        self.R_trans *= (self.k_trans ** 2)
        self.X_trans *= (self.k_trans ** 2)
        self.B_trans /= (self.k_trans ** 2)

        self.k_trans **= -1

    def soldering_changing(self, n_sol: int, delta_u: Union[int, float]) -> None:
        """
        Изменение коэффициента трансформации тр-ра при переключении отпайки устройства РПН

        :param n_sol: Номер отпайки устройства РПН
        :param delta_u: Изменение напряжения на каждую отпайку, %

        :raise ValueError: Если изменение напряжения на отпайку РПН отрицательное, то вызываем ошибку

        Примеры:
        >>> trans_1 = Transformer(2, 20, -15, 115, 10.5)
        >>> trans_1.soldering_changing(-2, 1.78)
        """
        if not isinstance(n_sol, int):
            raise TypeError('Неверный тип данных: номер отпайки утройства РПН')

        if not isinstance(delta_u, (int, float)):
            raise TypeError('Неверный тип данных: изменение напряжения на отпайку РПН')
        if delta_u < 0:
            raise ValueError('Изменение напряжения на отпайку РПН должно быть неотрицательное')

        if self.k_trans > 1:
            self.k_trans = (self.U_high_volt * (1 + n_sol * (delta_u / 100))) / self.U_low_volt
        else:
            self.k_trans = self.U_low_volt / (self.U_high_volt * (1 + n_sol * (delta_u / 100)))


class Generator:
    def __init__(self, u_nom: Union[int, float], p: Union[int, float], tg_phi: Union[int, float]):
        """
        Создание и подготовка к работе объекта "Синхронный генератор"

        :param u_nom: Номинальное напряжение генератора, кВ
        :param p: Активная мощность, выдаваемая генератором в сеть, МВт
        :param tg_phi: Коэффициент мощности генератора

        Примеры:
        >>> gen_1 = Generator(15.75, 100, 0.75) # Инициализация экземпляра класса
        """
        if not isinstance(u_nom, (int, float)):
            raise TypeError('Неверный тип данных: номинальное напряжение генератора')
        if u_nom <= 0:
            raise ValueError('Номинальное напряжение генератора должно быть положительное')
        self.U_nom = u_nom

        if not isinstance(p, (int, float)):
            raise TypeError('Неверный тип данных: активная мощность генератора')
        if p < 0:
            raise ValueError('Активная мощность генератора должна быть неотрицательная')
        self.P = p

        self.tg_phi = tg_phi
        self.Q = p * tg_phi

    def generation_changing(self, p_new: Union[int, float]) -> None:
        """
        Изменение генерации активной и реактивной мощности синхронного генератора

        :param p_new: Новое знвчение активной мощности, выдаваемой генератором в сеть, МВт

        :raise ValueError: Если новое значение активной мощности генератора отрицательное, то вызываем ошибку

        Примеры:
        >>> gen_1 = Generator(15.75, 100, 0.75)
        >>> gen_1.generation_changing(50)
        """
        if not isinstance(p_new, (int, float)):
            raise TypeError('Неверный тип данных: новая активная мощность генератора')
        if p_new < 0:
            raise ValueError('Новая активная мощность генератора должна быть неотрицательная')

        self.P = p_new
        self.Q = p_new * self.tg_phi

    def motor_mode_switching(self, p_motor: Union[int, float], q_motor: Union[int, float]) -> None:
        """
        Изменение активной и реактивной мощности синхронного генератора за счет перехода в двигательный режим

        :param p_motor: Активная мощность (отрицательная), потребляемая двигателем, МВт
        :param q_motor: Реактивная мощность двигателя, Мвар

        :raise ValueError: Если активная мощность двигателя положительная, то вызываем ошибку
        :raise ValueError: Если реактивная мощность двигателя больше активной (по модулю), то вызываем ошибку

        Примеры:
        >>> gen_1 = Generator(15.75, 100, 0.75)
        >>> gen_1.motor_mode_switching(-50, 20)
        """
        if not isinstance(p_motor, (int, float)):
            raise TypeError('Неверный тип данных: активная мощность двигателя')
        if p_motor > 0:
            raise ValueError('Активная мощность двигателя должна быть неположительной')
        self.P = p_motor

        if not isinstance(q_motor, (int, float)):
            raise TypeError('Неверный тип данных: реактивная мощность двигателя')
        if abs(q_motor) > abs(p_motor):
            raise ValueError('Реактивная мощность двигателя должна быть меньше активной по модулю')
        self.Q = q_motor


if __name__ == "__main__":
    # TODO работоспособность экземпляров класса проверить с помощью doctest
    doctest.testmod()
