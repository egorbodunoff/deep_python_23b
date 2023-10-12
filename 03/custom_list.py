class CustomList(list):
    def __init__(self, *args, **kwargs):
        self.data = args[0]
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_completion(list1, list2):
        add_list = [0] * abs(len(list1) - len(list2))

        if len(list1) < len(list2):
            return list1 + add_list, list2
        else:
            return list1, list2 + add_list

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, val):
        if isinstance(val, list):
            self.__data = val
        else:
            raise TypeError("необходимо передать list")

    def __add__(self, other):
        if isinstance(other, CustomList):
            list1, list2 = self.list_completion(self.__data, other.__data)

            return CustomList([list1[i] + list2[i] for i in range((len(list1)))])

        elif isinstance(self.data, type(other)):
            list1, list2 = self.list_completion(self.__data, other)

            return CustomList([list1[i] + list2[i] for i in range((len(list1)))])

        else:
            raise TypeError("слагаемые должны иметь тип CustomList или list")

    def __radd__(self, other):
        if isinstance(self.data, type(other)):
            list1, list2 = self.list_completion(self.__data, other)

            return CustomList([list1[i] + list2[i] for i in range((len(list1)))])

        else:
            raise TypeError("слагаемые должны иметь тип CustomList или list")

    def __sub__(self, other):
        if isinstance(other, CustomList):
            list1, list2 = self.list_completion(self.__data, other.__data)

            return CustomList([list1[i] - list2[i] for i in range((len(list1)))])

        elif isinstance(self.data, type(other)):
            list1, list2 = self.list_completion(self.__data, other)

            return CustomList([list1[i] - list2[i] for i in range((len(list1)))])

        else:
            raise TypeError("слагаемые должны иметь тип CustomList или list")

    def __rsub__(self, other):
        if isinstance(self.data, type(other)):
            list1, list2 = self.list_completion(self.__data, other)

            return CustomList([list2[i] - list1[i] for i in range((len(list1)))])

        else:
            raise TypeError("слагаемые должны иметь тип CustomList или list")

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self.__data) == sum(other.__data)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self.__data) < sum(other.__data)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __le__(self, other):
        if isinstance(other, CustomList):
            return sum(self.__data) <= sum(other.__data)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __gt__(self, other):
        if isinstance(other, CustomList):
            return sum(self.__data) > sum(other.__data)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __ge__(self, other):
        if isinstance(other, CustomList):
            return sum(self.__data) >= sum(other.__data)
        else:
            raise TypeError("объекты должны иметь тип CustomList")

    def __str__(self):
        return f"элементы: {self.__data}, их сумма: {sum(self.__data)}"
