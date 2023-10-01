class CustomList(list):
    def __init__(self, a):
        self.a = a
        super().__init__()

    def firt(self):
        print(self.a)


lt = CustomList(223)
lt.firt()
