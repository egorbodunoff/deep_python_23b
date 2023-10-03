import math


class SomeModel:
    @staticmethod
    def predict(message: str) -> float:
        if isinstance(message, str):
            return 1 / (1 + 100 * math.exp(-0.4 * len(message)))
        else:
            raise TypeError


def predict_message_mood(
        message: str,
        model: SomeModel,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:
    predict = model.predict(message)
    if predict > good_thresholds:
        return "отл"
    elif predict < bad_thresholds:
        return "неуд"
    else:
        return "норм"
