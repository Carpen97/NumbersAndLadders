from Utils import *


class Player:
    counter = 0  #Keep track of number of Player instances
    name_counter = 0 

    @classmethod
    def get_next_color(cls):
        color_keys = list(ANSI_COLORS.keys())
        color = color_keys[cls.counter % len(color_keys)]
        cls.counter += 1
        return color

    @classmethod
    def get_next_name(cls):
        name = GENERIC_NAMES[cls.name_counter % len(GENERIC_NAMES)]
        cls.name_counter += 1
        return name

    def __init__(self, name, strategy, played_by_human = False, cubes = None, color = None):
        self.strategy = strategy
        self._name = name
        self.cubes = cubes if cubes!= None else 0
        self.color = color if color!= None else Player.get_next_color()
        self.numbers = [] #Keep track of what numbers belong to this player
        self._played_by_human = played_by_human

    @property
    def played_by_human(self):
        return self._played_by_human

    @property
    def name(self) -> str:
        return color_text(self.color, self._name)

    def get_name(self, format = None, n: int = 0):
        if format == 'center':
            return color_text(self.color, self._name.center(n))
        elif format =='rjust':
            return color_text(self.color, self._name.rjust(n))
        elif format =='ljust':
            return color_text(self.color, self._name.ljust(n))
        return color_text(self.color, self._name)

    @property
    def score(self) -> float:
        sorted_nums = sorted(set(self.numbers))
        score = 0
        i = 0
        while i < len(sorted_nums):
            start = i
            while i + 1 < len(sorted_nums) and sorted_nums[i + 1] == sorted_nums[i] + 1:
                i += 1
            score += sorted_nums[start]
            i += 1
        return 95 - score + self.cubes

    @property
    def ladders(self) -> List[List[int]]:
        """Get the players numbers structured as ladders
        [[ladder1], [ladder2], ...] 
        (ladder looks like [n1, n2, n3, ...])
        """
        sorted_nums = sorted(set(self.numbers))
        res = []
        current = []
        for i, n in enumerate(sorted_nums):
            if n-1>=0 and sorted_nums[i-1] == n - 1:  # Is ladder
                current.append(n)
            else:
                if current:
                    res.append(current)
                current = [n]
        res.append(current)
        return res

    def get_numbers_formatted_as_ladders(self) -> str:
        if not self.numbers: return ""
        text=""
        for ladder in self.ladders:
            temp="["
            for n in ladder:
                temp+=str(n)+"-"
            text += temp[:-1]+"] "
        return color_text(self.color,text)


    def format_number(self, number):
        return color_text(self.color, f'[{str(number).rjust(2)}]')

    def __str__(self):
        return f"|{self.get_name('center',14)}|{format_pile(self.cubes).center(7)}| {self.get_numbers_formatted_as_ladders()}"

    def __lt__(self, other):
        return self.score > other.score

def format_pile(pile) -> str:
    if pile == 0:
        return "<empty>"
    if pile < 5:
        return "■"*pile 
    return f"■ x {pile}"

def get_dims(lines) -> Tuple[int,int]:
    h = len(lines)
    w = 0
    for line in lines: 
        #print(line,len(line))
        w = max(w, len(line))
    return w-45,h


