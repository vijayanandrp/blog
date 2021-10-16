
def process(num):
    cube = num**3
    square =num**2
    print("Cube - ", cube)
    print("Square - ", square)
    if num % 2 == 0:
        print("Even")
    else:
        print("Odd")

class ProcessNum:
    name = "Process Num"

    def __init__(self, num) -> None:
        self.num = num
        self.square = num**2
        self.cube = num**3
    
    def process(self):
        cube = self.num**3
        square = self.num**2
        print("Cube - ", cube)
        print("Square - ", square)
        if self.num % 2 == 0:
            print("Even")
        else:
            print("Odd")

    @staticmethod
    def nothing():
        print(" Chummaa called... Bye..")


process(2)
