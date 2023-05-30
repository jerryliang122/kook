import random

class RandomNumberGenerator:
    def __init__(self, num):
        self.num = num

    async def generate(self):
        while True:
            random.seed(self.num)
            rand_num = random.randint(1, 100)
            if await self.check_association(rand_num):
                return rand_num

    async def check_association(self, num2):
        random.seed(self.num)
        rand_num = random.randint(1, 100)
        if abs(rand_num - num2) <= 25:
            return True
        else:
            return False
