class LineUpDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"line_descr_{name}"

    def __get__(self, obj, obj_type):
        res = getattr(obj, self.name)
        line_up = f"Cтартовый состав на сегодняшний матч: {res[0]} \n"

        for x in res[1:]:
            line_up += 38 * " " + x + "\n"

        return line_up[:-1]

    def __set__(self, obj, line_up):
        if not isinstance(line_up, list):
            raise TypeError("необходимо передать список игроков")

        for val in line_up:
            if not isinstance(val, str):
                raise TypeError("имена игроков должны быть строками")

        if len(line_up) > 11:
            raise ValueError("В стартовом составе не может быть больше 11 игроков")

        return setattr(obj, self.name, line_up)


class CardDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"card_descr_{name}"

    def __get__(self, obj, obj_type):
        res = getattr(obj, self.name)

        return f"В матче было получено {res} карточек"

    def __set__(self, obj, count_card):
        if not isinstance(count_card, int):
            raise TypeError("Количество карточек должно быть целым числом")

        if count_card > 11 or count_card < 0:
            raise ValueError("Количество карточек должно лежать в диапазоне [0, 11]")

        return setattr(obj, self.name, count_card)


class ResDescriptor:
    def __set_name__(self, owner, name):
        self.name = f"line_descr_{name}"

    def __get__(self, obj, obj_type):
        res = getattr(obj, self.name)
        name = list(res.keys())
        val = list(res.values())

        line_name = name[0] + " --- " + name[1] + "\n"
        line_val1 = (int(len(name[0]) / 2) * " " + str(val[0])
                     + (4 + int(len(name[0]) / 2)) * " ")
        line_val2 = int(len(name[1]) / 2) * " " + str(val[1])

        return line_name + line_val1 + line_val2

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
    count_card = CardDescriptor()
    res = ResDescriptor()

    def __init__(self, line_up, count_card, res):
        self.line_up = line_up
        self.count_card = count_card
        self.res = res


a = Match(["messi", "ronaldo", "магваер"], 6, {"efimov": 1, "xalikov": 4})
print(a.res)
