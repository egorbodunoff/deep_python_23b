class CustomList(list):
    def __add__(self, other):
        if isinstance(other, list):
            result = CustomList()

            for i in range(len(self)):
                if i < len(other):
                    result.append(self[i] + other[i])
                else:
                    result.append((self[i]))

            if len(other) > len(self):
                for i in range(len(self), len(other)):
                    result.append(other[i])

            return result

        else:
            raise TypeError("слагаемые должны иметь тип CustomList или list")

    def __radd__(self, other):
        if isinstance(other, list):

            return self.__add__(other)

        else:
            raise TypeError("слагаемые должны иметь тип CustomList или list")

    def __sub__(self, other):
        if isinstance(other, list):
            result = CustomList()

            for i in range(len(self)):
                if i < len(other):
                    result.append(self[i] - other[i])
                else:
                    result.append((self[i]))

            if len(other) > len(self):
                for i in range(len(self), len(other)):
                    result.append(-other[i])

            return result

        else:
            raise TypeError("слагаемые должны иметь тип CustomList или list")

    def __rsub__(self, other):
        if isinstance(other, list):
            result = CustomList()

            for i in range(len(other)):
                if i < len(self):
                    result.append(other[i] - self[i])
                else:
                    result.append((other[i]))

            if len(self) > len(other):
                for i in range(len(other), len(self)):
                    result.append(-self[i])

            return result

        else:
            raise TypeError("слагаемые должны иметь тип CustomList или list")

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __ne__(self, other):
        if isinstance(other, CustomList):
            return sum(self) != sum(other)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __le__(self, other):
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __gt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __ge__(self, other):
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __str__(self):

        return (f"элементы CustomList: {[(self[i]) for i in range(len(self))]}"
                f", их сумма: {sum(self)}")
