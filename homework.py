from dataclasses import dataclass, asdict
from typing import Type


MINUTES = 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Метод должен быть определен в дочернем классе - '
            f'{self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    MEAN_SPEED_1: float = 18
    MEAN_SPEED_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.MEAN_SPEED_1 * self.get_mean_speed() - self.MEAN_SPEED_2)
            * self.weight
            / self.M_IN_KM
            * self.duration * MINUTES
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_1: float = 0.035
    MEAN_SPEED: int = 2
    WEIGHT_2: float = 0.029

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            self.WEIGHT_1 * self.weight
            + (self.get_mean_speed() ** self.MEAN_SPEED // self.height)
            * self.WEIGHT_2
            * self.weight
        ) * self.duration * MINUTES


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    MEAN_SPEED_1: float = 1.1
    MEAN_SPEED_2: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.MEAN_SPEED_1)
                * self.MEAN_SPEED_2 * self.weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Type[Training] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }

    try:
        return training_types[workout_type](*data)
    except KeyError as key_error:
        print(f"Invalid key {key_error}. Check workout types.")


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
