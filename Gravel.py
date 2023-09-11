from subprocess import Popen
from random import randint
from time import sleep
class fluid():
    def __init__(self, file_path) -> None:
        self.fp = file_path
        self.lines, self.max_len = self.getlines()

    def down(self, two_lines:list):
        for i, c in enumerate(two_lines[0]):
            if c == ' ': continue

            choices = []

            if two_lines[1][i] == ' ': 
                for _ in range(6):              # down
                    choices.append(0)
            if i+1<self.max_len and two_lines[1][i+1] == ' ': 
                for _ in range(4):              # rightdown
                    choices.append(1)
            if i-1>0 and two_lines[1][i-1] == ' ': 
                for _ in range(2):              # leftdown
                    choices.append(2)
            if i+1<self.max_len and two_lines[0][i+1] == ' ': 
                for _ in range(4):              # right
                    choices.append(3)
            if i-1>0 and two_lines[0][i-1] == ' ':
                for _ in range(1):              # left
                    choices.append(4)

            if len(choices) == 0: continue
            while len(choices) != 1: 
                l = len(choices)-1
                rd = choices[randint(0,l)]
                choices.remove(rd)
            ch = choices[0]
            
            if ch == 0:
                two_lines[0] = two_lines[0][:i]+' '+two_lines[0][i+1:]
                two_lines[1] = two_lines[1][:i]+c+two_lines[1][i+1:]
            elif ch == 1:
                two_lines[0] = two_lines[0][:i]+' '+two_lines[0][i+1:]
                two_lines[1] = two_lines[1][:i+1]+c+two_lines[1][i+2:]
            elif ch == 2:
                two_lines[0] = two_lines[0][:i]+' '+two_lines[0][i+1:]
                two_lines[1] = two_lines[1][:i-1]+c+two_lines[1][i:]
            elif ch == 3:
                two_lines[0] = two_lines[0][:i]+' '+c+two_lines[0][i+2:]
            elif ch == 4:
                two_lines[0] = two_lines[0][:i-1]+c+' '+two_lines[0][i+1:]

        return two_lines

    def update(self):
        for i in range(len(self.lines)-1):
            new_two_line = self.down(self.lines[i:i+2])
            self.lines = self.lines[:i] + new_two_line +self.lines[i+2:]

        full_line = 0
        empty_line = 0
        for i,line in enumerate(self.lines):
            actual_len = len(line.rstrip())
            if actual_len == self.max_len: 
                if full_line <= 7: full_line += 1
                else: self.lines.pop(i)
            if actual_len == 0:
                if empty_line <= 42: empty_line += 1
                else: self.lines.pop(i)

    def getlines(self):
        with open(self.fp, 'r') as f:
            text = f.read()
            text.replace('\t', '    ')
            lines = [' '] + text.split('\n')
            max_len = len(max(lines,key=len))
            for i, line in enumerate(lines):
                lines[i] += ' '*(max_len-len(line))
                assert len(lines[i]) == max_len
            return lines, max_len

    def show(self):
            res = ''
            for line in self.lines[-59:]: res += line+'\n'  # shell height
            res += '#'*self.max_len
            print(res,end='',flush=True)

    def run(self):
        while True:
            self.show()
            self.update()
            sleep(0.4)
            Popen('cls',shell=True).wait()
            


if __name__ == '__main__':
    f = fluid('../cross_game/Gobang.py')
    f.show()
    c = input('\n'+' Press <Enter> to continue... '.center(f.max_len,'#'))
    if c != 'q': f.run()
    