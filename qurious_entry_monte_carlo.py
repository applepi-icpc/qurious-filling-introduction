import typing as T
import random
from tqdm import tqdm
from tabulate import tabulate

# Parameters
MONTE_CARLO_LOOPS = 5000000
CONSIDER_DROP_SKILL = True

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

WORDS = ['SKILL_1', 'SKILL_2', 'SKILL_3', 'SKILL_4', 'SKILL_5', 'DECO_1', 'DECO_2', 'DECO_3', 'DECO_4+']
MULS = [1/32, 1/26, 1/18, 1/13, 1/12, 1, 1, 1, 1]

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

def main():
    title = ['COST'] + WORDS
    content = []

    for (entries, start_cost) in zip(ENTRIES, START_COSTS):
        count = [0] * len(WORDS)
        for _ in tqdm(range(MONTE_CARLO_LOOPS)):
            ret = single_emu(start_cost, entries)
            cur = [0] * len(WORDS)
            deco = 0
            ok = True
            for entry in ret:
                if entry[0] == _DECO_1:
                    deco += 1
                elif entry[0] == _DECO_2:
                    deco += 2
                elif entry[0] == _DECO_3:
                    deco += 3
                elif entry[0] == _DROP_SKILL:
                    if CONSIDER_DROP_SKILL:
                        ok = False
                elif entry[0] != _NOTHING:
                    cur[entry[0]] = 1
            if not ok:
                continue
            if deco == 1:
                cur[_DECO_1] = 1
            elif deco == 2:
                cur[_DECO_2] = 1
            elif deco == 3:
                cur[_DECO_3] = 1
            elif deco >= 4:
                cur[_DECO_4] = 1
            for i in range(len(WORDS)):
                count[i] += cur[i]
        row = [start_cost] + ["{:.3f} %".format(count[i] / MONTE_CARLO_LOOPS * 100 * MULS[i]) for i in range(len(WORDS))]
        content.append(row)
    
    print(tabulate(content, title, "github"))

if __name__ == '__main__':
    main()