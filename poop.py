import argparse
import math
import random
import time
import sys
from filecmp import cmp
from operator import attrgetter

BoardType = 0
SOLVED_BOARD_4x4 = ['1', '2', '3', '4',
                    '5', '6', '7', '8',
                    '9', '10', '11', '12',
                    '13', '14', '15', '0']
SOLVED_BOARD_3x3 = ['1', '2', '3',
                    '4', '5', '6',
                    '7', '8', '0']

TEST_BOARD_4x4 = ['1', '2', '3', '4',
                  '5', '6', '7', '8',
                  '10', '13', '11', '12',
                  '0', '9', '14', '15']
SOLVED_BOARD = SOLVED_BOARD_4x4
START_BOARD = []
ZERO_FIELD = {}
ToProcess = []
DoneProcess = []
DONE_BOARD = {}
DEPTH = 20
Processed_Number = 0
Solved = {}
SOLVED = []
Process_Comp_Vis_Res = {}
# zmiany:
# USUNAC POTEM
ORDER = ['D', 'L', 'R', 'U']
PARAMETER_ORDER = ORDER


class NODE:
    def __init__(self, board, move, moves_before, ZeroField, error=0):
        self.board = board
        self.move = move
        self.moves_made = moves_before.copy()
        self.moves_made.append(move)
        self.zero = ZeroField.copy()
        self.depth = 1
        self.error = -1
        self.to_visit = ORDER.copy()

    def Innit_Child(self, board, move, zero, depth):
        child = NODE(board, move, self.moves_made, zero)
        child.depth = depth + 1
        ToProcess.append(child)
        return child

    def __cmp__(self, other):
        return cmp(self.error, other.error)

    def move_zero_dnf(self, move):
        tmp = self.board.copy()
        zero = self.zero.copy()
        # 0, 1, 2 ,3
        # 4, 5 ,6 ,7
        # 8, 9,10,11
        if move == 'R' and zero['zero'] % 4 != 3 and self.move != 'L':
            tmp[zero['zero']] = tmp[zero['zero'] + 1]
            tmp[zero['zero'] + 1] = '0'
            zero['zero'] += 1
            DFS(self.Innit_Child(tmp, move, zero, self.depth))
            return
        elif move == 'L' and zero['zero'] % 4 != 0 and self.move != 'R':
            tmp[zero['zero']], tmp[zero['zero'] - 1] = tmp[zero['zero'] - 1], tmp[zero['zero']]
            zero['zero'] -= 1
            DFS(self.Innit_Child(tmp, move, zero, self.depth))
            return
        elif move == 'D' and zero['zero'] <= 11 and self.move != 'U':
            tmp[zero['zero']], tmp[zero['zero'] + 4] = tmp[zero['zero'] + 4], tmp[zero['zero']]
            zero['zero'] += 4
            DFS(self.Innit_Child(tmp, move, zero, self.depth))
            return
        elif move == 'U' and zero['zero'] >= 4 and self.move != 'D':
            tmp[zero['zero']], tmp[zero['zero'] - 4] = tmp[zero['zero'] - 4], tmp[zero['zero']]
            zero['zero'] -= 4
            DFS(self.Innit_Child(tmp, move, zero, self.depth))
            return

    def move_zero_bnf(self, move):
        tmp = self.board.copy()
        zero = self.zero.copy()
        # 0, 1, 2 ,3
        # 4, 5 ,6 ,7
        # 8, 9,10,11
        # 8, 9,10,11
        if move == 'R' and zero['zero'] % 4 != 3 and self.move != 'L':
            tmp[zero['zero']] = tmp[zero['zero'] + 1]
            tmp[zero['zero'] + 1] = '0'
            zero['zero'] += 1
            self.Innit_Child(tmp, move, zero, self.depth)
            return

        elif move == 'L' and zero['zero'] % 4 != 0 and self.move != 'R':
            tmp[zero['zero']], tmp[zero['zero'] - 1] = tmp[zero['zero'] - 1], tmp[zero['zero']]
            zero['zero'] -= 1
            self.Innit_Child(tmp, move, zero, self.depth)
            return

        elif move == 'D' and zero['zero'] <= 11 and self.move != 'U':
            tmp[zero['zero']], tmp[zero['zero'] + 4] = tmp[zero['zero'] + 4], tmp[zero['zero']]
            zero['zero'] += 4
            self.Innit_Child(tmp, move, zero, self.depth)
            return

        elif move == 'U' and zero['zero'] >= 4 and self.move != 'D':
            tmp[zero['zero']], tmp[zero['zero'] - 4] = tmp[zero['zero'] - 4], tmp[zero['zero']]
            zero['zero'] -= 4
            self.Innit_Child(tmp, move, zero, self.depth)
            return

    def move_zero_astr(self, move):
        tmp = self.board.copy()
        zero = self.zero.copy()
        # 0, 1, 2 ,3
        # 4, 5 ,6 ,7
        # 8, 9,10,11
        # 8, 9,10,11
        if move == 'R' and zero['zero'] % 4 != 3 and self.move != 'L':
            tmp[zero['zero']] = tmp[zero['zero'] + 1]
            tmp[zero['zero'] + 1] = '0'
            zero['zero'] += 1
            ToProcess.append( self.Innit_Child(tmp, move, zero, self.depth) )
            return True

        elif move == 'L' and zero['zero'] % 4 != 0 and self.move != 'R':
            tmp[zero['zero']], tmp[zero['zero'] - 1] = tmp[zero['zero'] - 1], tmp[zero['zero']]
            zero['zero'] -= 1
            ToProcess.append( self.Innit_Child(tmp, move, zero, self.depth) )
            return True

        elif move == 'D' and zero['zero'] <= 11 and self.move != 'U':
            tmp[zero['zero']], tmp[zero['zero'] + 4] = tmp[zero['zero'] + 4], tmp[zero['zero']]
            zero['zero'] += 4
            ToProcess.append( self.Innit_Child(tmp, move, zero, self.depth) )
            return True

        elif move == 'U' and zero['zero'] >= 4 and self.move != 'D':
            tmp[zero['zero']], tmp[zero['zero'] - 4] = tmp[zero['zero'] - 4], tmp[zero['zero']]
            zero['zero'] -= 4
            x = self.Innit_Child(tmp, move, zero, self.depth)
            ToProcess.append( self.Innit_Child(tmp, move, zero, self.depth) )
            return True
        return False

def BFS():
    base_node = NODE(TEST_BOARD_4x4, None, [], ZERO_FIELD)
    base_node.moves_made.clear()
    ToProcess.append(base_node)

    while len(ToProcess) != 0:
        node = ToProcess[0]
        String = ListToString(node.board)

        if SOLVED_BOARD == node.board:
            Process_Comp_Vis_Res['length'] = len(node.moves_made)
            print('Solved')
            print(node.board)
            print(node.moves_made)
            Process_Comp_Vis_Res['Moves'] = node.moves_made
            if node.depth > Process_Comp_Vis_Res.get('Recursion'):
                Process_Comp_Vis_Res['Recursion'] = node.depth
            return

        if String in DONE_BOARD:
            Process_Comp_Vis_Res['Completed'] += 1
            ToProcess.remove(ToProcess[0])
            continue

        if node.depth > Process_Comp_Vis_Res.get('Recursion'):
            print(node.depth)
            Process_Comp_Vis_Res['Recursion'] = node.depth

        if (node.depth > DEPTH):
            print(node.depth)
            Process_Comp_Vis_Res['Completed'] += 1
            DONE_BOARD[String] = node.moves_made
            ToProcess.remove(ToProcess[0])
            continue

        for param in reversed(PARAMETER_ORDER):
            node.move_zero_bnf(param)
            Process_Comp_Vis_Res['Visited'] += 1
        DONE_BOARD[String] = node.moves_made
        ToProcess.remove(ToProcess[0])
        Process_Comp_Vis_Res['Completed'] += 1


def ListToString(s):
    listToStr = ' '.join([str(elem) for elem in s])
    return listToStr


def DFS(node):
    if '0' in Solved:
        return
    if SOLVED_BOARD == node.board:
        print('Solved')
        print(node.board)
        print(node.moves_made)
        Solved['0'] = True
        Process_Comp_Vis_Res['length'] = len(node.moves_made)
        Process_Comp_Vis_Res['Moves'] = node.moves_made
        SOLVED.append(node)
        return

    String = ListToString(node.board)
    if String in DONE_BOARD:
        if len(node.moves_made) > len(DONE_BOARD.get(String)):
            Process_Comp_Vis_Res['Completed'] += 1
            return
        else:
            DONE_BOARD[String] = node.moves_made

    if node.depth > Process_Comp_Vis_Res.get('Recursion'):
        Process_Comp_Vis_Res['Recursion'] = node.depth

    if DEPTH == node.depth:
        DONE_BOARD[String] = node.moves_made
        Process_Comp_Vis_Res['Completed'] += 1
        return

    for param in PARAMETER_ORDER:
        Process_Comp_Vis_Res['Visited'] += 3
        node.move_zero_dnf(param)
    DONE_BOARD[String] = node.moves_made
    Process_Comp_Vis_Res['Completed'] += 1
    return


def astr(heuristic):
    if heuristic == 'manh':
        def calculate_error(current_board, solved_board):
            manh_error = 0
            for i in range(1,len(current_board)):
                position = SOLVED_BOARD.index(str(i))
                temp = current_board.index(str(i))
                self_col = temp % 4
                self_row = temp // 4
                temp_col = position % 4
                temp_row = position // 4
                print("pop")
                manh_error += abs(self_row - temp_row) + abs(self_col - temp_col)
            return manh_error
    else:
        def calculate_error(current_board, solved_board):
            hamm_error = 0
            for i in range(1,len(current_board)):
                position = SOLVED_BOARD.index(str(i))
                temp = current_board.index(str(i))
                self_col = temp % 4
                self_row = temp // 4
                temp_col = position % 4
                temp_row = position // 4
                if abs(self_row - temp_row) + abs(self_col - temp_col) != 0:
                    hamm_error += 1
            return hamm_error

    base_node = NODE(TEST_BOARD_4x4, None, [], ZERO_FIELD)
    base_node.error = calculate_error(base_node.board, SOLVED_BOARD)
    base_node.moves_made.clear()
    ToProcess.append(base_node)

    while True:
        if SOLVED_BOARD == base_node.board:
            print('Solved')
            print(base_node.board)
            print(base_node.moves_made)
            Solved['0'] = True
            Process_Comp_Vis_Res['length'] = len(base_node.moves_made)
            Process_Comp_Vis_Res['Moves'] = base_node.moves_made
            SOLVED.append(base_node)
            return

        if DEPTH == base_node.depth:
            Process_Comp_Vis_Res['Completed'] += 1
        else:
            if base_node.depth > Process_Comp_Vis_Res.get('Recursion'):
                Process_Comp_Vis_Res['Recursion'] = base_node.depth

            for f in PARAMETER_ORDER:
                if (base_node.move_zero_astr(f)):
                    Process_Comp_Vis_Res['Visited'] += 1
                    ToProcess[-1].error = calculate_error(ToProcess[-1].board, SOLVED_BOARD)
            ToProcess.remove(base_node)
            Process_Comp_Vis_Res['Completed'] += 1
        base_node = min(ToProcess , key=attrgetter('error'))


def find_0_in_Start_Board(board):
    for j in range(len(board)):
        if board[j] == '0':
            ZERO_FIELD['zero'] = j


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

PAR = argparse.ArgumentParser(description="strategy, parameter, txt_source, txt_solution, txt_additional.")
PAR.add_argument('strategy')
PAR.add_argument('parameter')
PAR.add_argument('txt_source')
PAR.add_argument('txt_solution')
PAR.add_argument('txt_additional')
args = PAR.parse_args()

for elem in args.parameter:
    PARAMETER_ORDER.append(elem)

TEST_BOARD_4x4.clear()
with open(args.txt_source) as board:
    first_line_flag = True
    for line in board:
        if first_line_flag:
            first_line_flag = False
            continue
        else:
            for n in line.split():
                TEST_BOARD_4x4.append(n)
find_0_in_Start_Board(TEST_BOARD_4x4)


DoneProcess.clear()
DONE_BOARD.clear()
ToProcess.clear()
Process_Comp_Vis_Res['length'] = -1
Process_Comp_Vis_Res['Completed'] = 0
Process_Comp_Vis_Res['Visited'] = 0
Process_Comp_Vis_Res['Recursion'] = 0
Process_Comp_Vis_Res['Moves'] = None

if args.strategy == "bfs":
    PARAMETER_ORDER.clear()
    for n in args.parameter:
        PARAMETER_ORDER.append(n)
    start_time = time.time()
    BFS()
    Process_Comp_Vis_Res['time'] = round((time.time() - start_time) * 1000, 3)
    print(Process_Comp_Vis_Res)
if args.strategy == "dfs":
    PARAMETER_ORDER.clear()
    for n in args.parameter:
        PARAMETER_ORDER.append(n)
    base_node = NODE(TEST_BOARD_4x4, None, [], ZERO_FIELD)
    base_node.moves_made.clear()
    start_time = time.time()
    DFS(base_node)
    Process_Comp_Vis_Res['time'] = round((time.time() - start_time) * 1000, 3)
    print(Process_Comp_Vis_Res)
if args.strategy == "astr":
    base_node = NODE(TEST_BOARD_4x4, None, [], ZERO_FIELD)
    base_node.moves_made.clear()
    start_time = time.time()
    astr(args.parameter)
    Process_Comp_Vis_Res['time'] = round((time.time() - start_time) * 1000, 3)
    print(Process_Comp_Vis_Res)

# astr('manh')

#
# base_node = NODE(TEST_BOARD_4x4, None, [], ZERO_FIELD)
# base_node.move_zero('L')
# base_node.move_zero('R')

file = open(args.txt_solution, 'w+')
file.write(str(Process_Comp_Vis_Res['length']))
if Process_Comp_Vis_Res['length'] != -1:
    file.write('\n')
    file.write(str(Process_Comp_Vis_Res['Moves']))

file = open(args.txt_additional, 'w+')
file.write(str(Process_Comp_Vis_Res['length']))
file.write('\n')

file.write(str(Process_Comp_Vis_Res['Visited']))
file.write('\n')

file.write(str(Process_Comp_Vis_Res['Completed']))
file.write('\n')

file.write(str(Process_Comp_Vis_Res['Recursion']))
file.write('\n')

file.write(str(Process_Comp_Vis_Res['time']))