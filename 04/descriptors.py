class LineUpDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"line_descr_{name}"

    def __get__(self, obj, obj_type):
        res = getattr(obj, self.name)

        line_up = ', '.join(res)

        return "Cтартовый состав на сегодняшний матч: " + line_up.rstrip()

    def __set__(self, obj, line_up):
        if not isinstance(line_up, list):
            raise TypeError("необходимо передать список игроков")

        for val in line_up:
            if not isinstance(val, str):
                raise TypeError("имена игроков должны быть строками")

        if len(line_up) > 5 or len(line_up) < 3:
            raise ValueError("В стартовом составе должно быть от 3 до 5 игроков")

        return setattr(obj, self.name, line_up)


class DurationDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"card_descr_{name}"

    def __get__(self, obj, obj_type):
        res = getattr(obj, self.name)

        if res % 10 == 1 and res != 11:
            return f"Длительность матча {res} минута"
        if res % 10 in [2, 3, 4] and res not in [12, 13, 14]:
            return f"Длительность матча {res} минуты"
        if res % 10 in [0, 5, 6, 7, 8, 9] or res in [11, 12, 13, 14]:
            return f"Длительность матча {res} минут"

    def __set__(self, obj, duration):
        if not isinstance(duration, int):
            raise TypeError("продолжительность матча должна быть целым числом")

        if duration > 60 or duration < 0:
            raise ValueError("длительность матча должна лежать в диапазоне [0, 60]")

        return setattr(obj, self.name, duration)


class ResDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"line_descr_{name}"

    def __get__(self, obj, obj_type):
        res = getattr(obj, self.name)
        name = list(res.keys())
        val = list(res.values())

        if val[0] > val[1]:
            return f"со счетом {val[0]} : {val[1]} победила команда {name[0]}"
        if val[0] < val[1]:
            return f"со счетом {val[1]} : {val[0]} победила команда {name[1]}"
        else:
            return f"ничейный резултат"

    def __set__(self, obj, res):
        if not isinstance(res, dict):
            raise TypeError("необходимо передать результаты в виде словаря"
                            "например {Искра: 3, Звезда: 1")

        for name, val in res.items():
            if not isinstance(val, int):
                raise TypeError("количество забитых мячей должно быть целым числом")

            if not isinstance(name, str):
                raise TypeError("названия команд должны быть строками")

            if val < 0:
                raise ValueError("количество голов не может быть меньше 0")

        return setattr(obj, self.name, res)


class Match:
    line_up = LineUpDescriptor()
    duration = DurationDescriptor()
    res = ResDescriptor()

    def __init__(self, line_up, duration, res):
        self.line_up = line_up
        self.duration = duration
        self.res = res


# a = Match(['11', "efw", "c"], 25, {})
# print(a.duration)
