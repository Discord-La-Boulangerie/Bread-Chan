class MaClasseTest:
    def __init__(self, *args, **kwds):
        super().__init__()

    @classmethod
    def ma_methode(cls):
        print("Je suis une méthode de la classe MaClasseTest")


class MaClasseTest2(MaClasseTest):
    pass


e = MaClasseTest2()
e.ma_methode()
