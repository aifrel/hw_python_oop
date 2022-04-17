from dataclasses import dataclass, asdict, fields
from typing import Type, Dict

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Метод должен быть определен в дочернем классе - '
            f'{self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    MEAN_SPEED__COEF_1 = 18
    MEAN_SPEED_COEF_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.MEAN_SPEED__COEF_1 * self.get_mean_speed()
             - self.MEAN_SPEED_COEF_2)
            * self.weight
            / self.M_IN_KM
            * self.duration * self.MINUTES
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_1 = 0.035
    INDEX = 2
    WEIGHT_2 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            self.WEIGHT_1 * self.weight
            + (self.get_mean_speed() ** self.INDEX // self.height)
            * self.WEIGHT_2
            * self.weight
        ) * self.duration * self.MINUTES


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MEAN_SPEED_COEF_1 = 1.1
    WEIGHT_COEF = 2

    length_pool: int
    count_pool: int

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.MEAN_SPEED_COEF_1)
                * self.WEIGHT_COEF * self.weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type not in training_types:
        raise KeyError(workout_type)
    if len(fields(training_types[workout_type])) != len(data):
        raise TypeError(len(fields(training_types[workout_type])))
    return training_types[workout_type](*data)


def main(packages) -> None:
    """Главная функция."""
    for workout_type, data in packages:
        try:
            print(read_package(workout_type, data).show_training_info().get_message())
        except KeyError as key_err:
            print(f"Тип тренировки {key_err} отсутствует в словаре training_types. Проверьте данные.")
        except TypeError as type_error:
            print(f"Количество переданных данных в класс {workout_type} не соответствует количеству полей этого класса. "
                f"Ожидается: {type_error}, Передано: {len(data)}")


if __name__ == "__main__":
    packages = [
        ("SWMf", [720, 1, 80, 25, 4]),
        ("RUN", [15000, 1, 75, 234]),
        ("WLK", [9000, 1, 75, 180])
    ]

    main(packages)
