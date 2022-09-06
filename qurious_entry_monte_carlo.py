import typing as T
import random
from tqdm import tqdm
from tabulate import tabulate
from multiprocessing import Pool
import functools

# Parameters
N_MONTE_CARLO_LOOP = 100000000
FLAG_CONSIDER_DROP_SKILL = True

N_PROCESS = 6
N_IMAP_CHUNK_SIZE = 1
N_PART_SIZE = 10000

_NOTHING = -1
_DROP_SKILL = -2
_SKILL_1 = 0
_SKILL_2 = 1
_SKILL_3 = 2
_SKILL_4 = 3
_SKILL_5 = 4
_DECO_1 = 5
_DECO_2 = 6
_DECO_3 = 7
_DECO_4 = 8

ARR_WORDS = ['SKILL_1', 'SKILL_2', 'SKILL_3', 'SKILL_4', 'SKILL_5', 'DECO_1', 'DECO_2', 'DECO_3', 'DECO_4+']
ARR_MULS = [1/32, 1/26, 1/18, 1/13, 1/12, 1, 1, 1, 1]

ENTRIES_1 = [
    # EFFECT, COST, PROBABILITY * 1000
    (_NOTHING, 1, 80),  # 0, Defense
    (_NOTHING, 5, 80),  # 1, Defense
    (_NOTHING, 10, 80), # 2, Defense
    (_NOTHING, 15, 40), # 3, Defense
    (_NOTHING, 20, 40), # 4, Defense
    (_NOTHING, -3, 40), # 5, Defense
    (_NOTHING, -5, 40), # 6, Defense
    (_NOTHING, 2, 150), # 7, Elem-Defense
    (_NOTHING, -2, 90), # 8, Elem-Defense
    (_NOTHING, -3, 60), # 9, Elem-Defense
    (_SKILL_1, 3, 60),  # 10, Skill
    (_SKILL_2, 6, 40),  # 11, Skill
    (_SKILL_3, 9, 36),  # 12, Skill
    (_SKILL_4, 12, 28), # 13, Skill
    (_SKILL_5, 15, 16), # 14, Skill
    (_DROP_SKILL, -10, 20), # 15, Skill
    (_DECO_1, 6, 70),   # 16, Deco
    (_DECO_2, 12, 25),  # 17, Deco
    (_DECO_3, 18, 5),   # 18, Deco
]

ENTRIES_2 = [
    # EFFECT, COST, PROBABILITY * 1000
    (_NOTHING, 1, 80),  # 0, Defense
    (_NOTHING, 5, 80),  # 1, Defense
    (_NOTHING, 10, 80), # 2, Defense
    (_NOTHING, 14, 40), # 3, Defense
    (_NOTHING, 18, 40), # 4, Defense
    (_NOTHING, -3, 40), # 5, Defense
    (_NOTHING, -5, 40), # 6, Defense
    (_NOTHING, 2, 150), # 7, Elem-Defense
    (_NOTHING, -2, 90), # 8, Elem-Defense
    (_NOTHING, -3, 60), # 9, Elem-Defense
    (_SKILL_1, 3, 60),  # 10, Skill
    (_SKILL_2, 6, 40),  # 11, Skill
    (_SKILL_3, 9, 36),  # 12, Skill
    (_SKILL_4, 12, 28), # 13, Skill
    (_SKILL_5, 15, 16), # 14, Skill
    (_DROP_SKILL, -10, 20), # 15, Skill
    (_DECO_1, 6, 70),   # 16, Deco
    (_DECO_2, 12, 25),  # 17, Deco
    (_DECO_3, 18, 5),   # 18, Deco
]

ENTRIES_3 = [
    # EFFECT, COST, PROBABILITY * 1000
    (_NOTHING, 1, 80),  # 0, Defense
    (_NOTHING, 5, 80),  # 1, Defense
    (_NOTHING, 8, 80), # 2, Defense
    (_NOTHING, 12, 40), # 3, Defense
    (_NOTHING, 16, 40), # 4, Defense
    (_NOTHING, -3, 40), # 5, Defense
    (_NOTHING, -5, 40), # 6, Defense
    (_NOTHING, 2, 150), # 7, Elem-Defense
    (_NOTHING, -2, 90), # 8, Elem-Defense
    (_NOTHING, -3, 60), # 9, Elem-Defense
    (_SKILL_1, 3, 60),  # 10, Skill
    (_SKILL_2, 6, 40),  # 11, Skill
    (_SKILL_3, 9, 36),  # 12, Skill
    (_SKILL_4, 12, 28), # 13, Skill
    (_SKILL_5, 15, 16), # 14, Skill
    (_DROP_SKILL, -10, 20), # 15, Skill
    (_DECO_1, 6, 70),   # 16, Deco
    (_DECO_2, 12, 25),  # 17, Deco
    (_DECO_3, 18, 5),   # 18, Deco
]

ENTRIES_4 = [
    # EFFECT, COST, PROBABILITY * 1000
    (_NOTHING, 1, 80),  # 0, Defense
    (_NOTHING, 5, 80),  # 1, Defense
    (_NOTHING, 7, 80), # 2, Defense
    (_NOTHING, 10, 40), # 3, Defense
    (_NOTHING, 14, 40), # 4, Defense
    (_NOTHING, -3, 40), # 5, Defense
    (_NOTHING, -5, 40), # 6, Defense
    (_NOTHING, 2, 150), # 7, Elem-Defense
    (_NOTHING, -2, 90), # 8, Elem-Defense
    (_NOTHING, -3, 60), # 9, Elem-Defense
    (_SKILL_1, 3, 60),  # 10, Skill
    (_SKILL_2, 6, 40),  # 11, Skill
    (_SKILL_3, 9, 36),  # 12, Skill
    (_SKILL_4, 12, 28), # 13, Skill
    (_SKILL_5, 15, 16), # 14, Skill
    (_DROP_SKILL, -10, 20), # 15, Skill
    (_DECO_1, 6, 70),   # 16, Deco
    (_DECO_2, 12, 25),  # 17, Deco
    (_DECO_3, 18, 5),   # 18, Deco
]

ENTRIES_5 = [
    # EFFECT, COST, PROBABILITY * 1000
    (_NOTHING, 1, 80),  # 0, Defense
    (_NOTHING, 5, 80),  # 1, Defense
    (_NOTHING, 6, 80), # 2, Defense
    (_NOTHING, 9, 40), # 3, Defense
    (_NOTHING, 12, 40), # 4, Defense
    (_NOTHING, -3, 40), # 5, Defense
    (_NOTHING, -5, 40), # 6, Defense
    (_NOTHING, 2, 150), # 7, Elem-Defense
    (_NOTHING, -2, 90), # 8, Elem-Defense
    (_NOTHING, -3, 60), # 9, Elem-Defense
    (_SKILL_1, 3, 60),  # 10, Skill
    (_SKILL_2, 6, 40),  # 11, Skill
    (_SKILL_3, 9, 36),  # 12, Skill
    (_SKILL_4, 12, 28), # 13, Skill
    (_SKILL_5, 15, 16), # 14, Skill
    (_DROP_SKILL, -10, 20), # 15, Skill
    (_DECO_1, 6, 70),   # 16, Deco
    (_DECO_2, 12, 25),  # 17, Deco
    (_DECO_3, 18, 5),   # 18, Deco
]

ENTRIES_6 = [
    # EFFECT, COST, PROBABILITY * 1000
    (_NOTHING, 1, 80),  # 0, Defense
    (_NOTHING, 3, 80),  # 1, Defense
    (_NOTHING, 5, 80), # 2, Defense
    (_NOTHING, 7, 40), # 3, Defense
    (_NOTHING, 10, 40), # 4, Defense
    (_NOTHING, -3, 40), # 5, Defense
    (_NOTHING, -5, 40), # 6, Defense
    (_NOTHING, 2, 150), # 7, Elem-Defense
    (_NOTHING, -2, 90), # 8, Elem-Defense
    (_NOTHING, -3, 60), # 9, Elem-Defense
    (_SKILL_1, 3, 60),  # 10, Skill
    (_SKILL_2, 6, 40),  # 11, Skill
    (_SKILL_3, 9, 36),  # 12, Skill
    (_SKILL_4, 12, 28), # 13, Skill
    (_SKILL_5, 15, 16), # 14, Skill
    (_DROP_SKILL, -10, 20), # 15, Skill
    (_DECO_1, 6, 70),   # 16, Deco
    (_DECO_2, 12, 25),  # 17, Deco
    (_DECO_3, 18, 5),   # 18, Deco
]

ENTRIES = [ENTRIES_1, ENTRIES_2, ENTRIES_3, ENTRIES_4, ENTRIES_5, ENTRIES_6]
START_COSTS = [20, 18, 16, 14, 12, 10]

def random_select_in(entries):
    total_p = 0
    for entry in entries:
        total_p += entry[2]
    r = random.randrange(total_p)
    for entry in entries:
        if r < entry[2]:
            return entry
        r -= entry[2]
    assert False, "random_select_in fault"

def single_emu(cost, entries):
    ret = []

    def test(ent):
        nonlocal ret, cost
        if cost - ent[1] > 0:
            ret.append(ent)
            cost -= ent[1]

    # Stage 1
    test(random_select_in(entries[0:7])) # Defense
    if (cost == 0):
        return ret
    test(random_select_in(entries[10:16])) # Skill
    if (cost == 0):
        return ret

    # Stage 2
    for i in range(50):
        push_count = 6 - len(ret)
        for j in range(push_count):
            test(random_select_in(entries))
            if (cost == 0):
                return ret
        if len(ret) == 6:
            break
    
    return ret

def proc_emu_result(ret):
    cur = [0] * len(ARR_WORDS)
    deco = 0
    for entry in ret:
        if entry[0] == _DECO_1:
            deco += 1
        elif entry[0] == _DECO_2:
            deco += 2
        elif entry[0] == _DECO_3:
            deco += 3
        elif entry[0] == _DROP_SKILL:
            if FLAG_CONSIDER_DROP_SKILL:
                # give up
                return [0] * len(ARR_WORDS)
        elif entry[0] != _NOTHING:
            cur[entry[0]] = 1
    if deco == 1:
        cur[_DECO_1] = 1
    elif deco == 2:
        cur[_DECO_2] = 1
    elif deco == 3:
        cur[_DECO_3] = 1
    elif deco >= 4:
        cur[_DECO_4] = 1
    return cur


def _do(start_cost, entries, _):
    length = len(ARR_WORDS)
    s = [0] * length
    for _ in range(N_PART_SIZE):
        ret = single_emu(start_cost, entries)
        cur = proc_emu_result(ret)
        for k in range(length):
            s[k] += cur[k]
    return s

def main():
    title = ['COST'] + ARR_WORDS
    content = []

    for (entries, start_cost) in zip(ENTRIES, START_COSTS):
        arr_size = (N_MONTE_CARLO_LOOP + N_PART_SIZE - 1) // N_PART_SIZE
        actual_attempts = arr_size * N_PART_SIZE

        with Pool(N_PROCESS) as pool:
            curs = list(
                tqdm(pool.imap_unordered(
                    functools.partial(_do, start_cost, entries), 
                    range(arr_size), chunksize=N_IMAP_CHUNK_SIZE), 
                total=arr_size))

        count = functools.reduce(
            lambda arr1, arr2: [x + y for (x, y) in zip(arr1, arr2)], curs)

        row = [start_cost] + ["{:.6f} % ({})".format(count[i] / actual_attempts * 100 * ARR_MULS[i], count[i]) for i in range(len(ARR_WORDS))]
        content.append(row)
    
    print(tabulate(content, title, "github"))

if __name__ == '__main__':
    main()