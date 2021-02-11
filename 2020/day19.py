"""AdventOfCode Day19."""
import re
import copy

test_input_1 = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb\
"""


def get_input():
    """Get puzzle input."""
    with open("input/day19.txt") as f:
        return f.read()


def convertToInt(input):
    numbers = []
    for stringNumber in input:
        numbers.append(int(stringNumber))
    return numbers


def getRules(puzzleInput):
    rules = {}
    missing = {}
    splitInput = puzzleInput.split("\n")
    newInput = copy.deepcopy(splitInput)
    for rule in splitInput:
        match = re.match('([0-9]+): "(.+)"', rule)
        if match:
            rules[int(match.groups()[0])] = [match.groups()[1]]
            newInput.remove(rule)
        else:
            match = re.match("([0-9]+): (.+)", rule)
            missing[int(match.groups()[0])] = match.groups()[1]

    ls = copy.deepcopy(missing)
    for key in ls.keys():
        getRule(key, rules, missing)
    return rules


def getRule(rule, rules, missing):
    if rule in rules.keys():
        return rules[rule]

    match = re.fullmatch("(([ ]?[0-9]+)+)", missing[rule])
    if match:
        subrules = convertToInt(match.groups()[0].split(" "))
        result = getResult(subrules, rules, missing)
        rules[rule] = result
    else:
        match = re.fullmatch("(([ ]?[0-9]+)+) \| (([ ]?[0-9]+)+)", missing[rule])
        if match:
            alternatives = []
            alternatives.append(match.groups()[0])
            alternatives.append(match.groups()[2])
            completeResult = []
            for alternative in alternatives:
                subrules = convertToInt(alternative.split(" "))
                result = getResult(subrules, rules, missing)
                completeResult += result
            rules[rule] = completeResult

    del missing[rule]
    return rules[rule]


def getResult(subrules, rules, missing):
    result = []
    for subrule in subrules:
        alternatives = getRule(subrule, rules, missing)
        if not result:
            result = copy.deepcopy(alternatives)
        else:
            tmp = []
            for partResult in result:
                for alternative in alternatives:
                    tmp.append(partResult + alternative)
            result = tmp
    return result


def preprocess(s: str):
    """Preprocess."""
    m = {}
    messages = []
    for line in s.strip().split("\n"):
        if line == "":
            continue
        if ":" in line:
            v = line.split(":")
            m[v[0]] = v[1].strip().replace('"', "")
        else:
            messages.append(line.strip())
    return m, messages


def part1(input_str: str):
    """Part1."""
    s = input_str.split("\n\n")
    rules = getRules(s[0])
    messages = s[1].split("\n")

    cnt = 0
    for msg in messages:
        if msg in rules[0]:
            cnt += 1
    return cnt


def part2(input_str: str):
    """Part2."""
    s = input_str.split("\n\n")
    rules = getRules(s[0])
    messages = s[1].split("\n")

    blobSize = len(rules[42][0])
    count = 0
    for message in messages:
        if message in rules[0]:
            count += 1
        else:
            count42 = 0
            count31 = 0
            successful = True
            for position in range(0, len(message) - blobSize + 1, blobSize):
                messageSlice = message[position : (position + blobSize)]  # noqa
                if messageSlice in rules[42]:
                    count42 += 1
                    if count31:
                        successful = False
                        break
                elif messageSlice in rules[31]:
                    count31 += 1
            if successful and count31 and count42 - count31 > 0:
                count += 1

    return count


if __name__ == "__main__":
    print("Day 19")
    assert part1(test_input_1) == 2
    print(f"Part1: {part1(get_input())}")
    print(f"Part2: {part2(get_input())}")
