def day1_part1(lines):
    res = 0
    for line in lines:
        x = ''
        for c in line:
            if c.isdigit():
                x += c
                break
        for c in line[::-1]:
            if c.isdigit():
                x += c
                break
        res += int(x)
    return res


def day1_part2(lines):
    hmap = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'}

    res = 0
    for line in lines:
        x = ''
        s = ''
        for c in line:
            if c.isdigit():
                x += c
                break
            s = s + c
            for k, v in hmap.items():
                if s.endswith(k):
                    x += v
                    break
            if len(x) == 1:
                break
        s = ''
        for c in line[::-1]:
            if c.isdigit():
                x += c
                break
            s = c + s
            for k, v in hmap.items():
                if s.startswith(k):
                    x += v
                    break
            if len(x) == 2:
                break

        res += int(x)
    return res


def day2_part1(lines):

    def possible(line):
        line = line.split(': ')[1].rstrip()
        for subsets in line.split('; '):
            for n_color in subsets.split(', '):
                n, color = n_color.split(' ')
                n = int(n)
                if color == 'red' and n > 12:
                    return False
                elif color == 'green' and n > 13:
                    return False
                elif color == 'blue' and n > 14:
                    return False
        return True

    res = 0
    for i, line in enumerate(lines, 1):
        if possible(line):
            res += i
    return res


def day2_part2(lines):

    def count(line):
        red = green = blue = 0

        line = line.split(': ')[1].rstrip()
        for subsets in line.split('; '):
            for n_color in subsets.split(', '):
                n, color = n_color.split(' ')
                n = int(n)
                if color == 'red':
                    red = max(red, n)
                elif color == 'green':
                    green = max(green, n)
                else:
                    blue = max(blue, n)
        return red * green * blue

    return sum(count(line) for line in lines)


def day3_part1(lines):
    mat = [l.rstrip() for l in lines]
    n, m = len(mat), len(mat[0])
    ds = (0, 1), (1, 0), (0, -1), (-1, 0), \
         (1, 1), (1, -1), (-1, -1), (-1, 1)

    def is_part_num(i, j):
        for x, y in ds:
            r, c = i + x, j + y
            if r in (-1, n) or c in (-1, m):
                continue
            x = mat[r][c]
            if not x.isdigit() and x != '.':
                return True
        return False

    res = 0
    for i in range(n):
        num = 0
        yes = False
        for j in range(m):
            x = mat[i][j]

            if x.isdigit():
                num = num * 10 + int(x)
                if is_part_num(i, j):
                    yes = True

            if not x.isdigit() or j == m - 1:
                if yes:
                    res += num
                num = 0
                yes = False
    return res


def day3_part2(lines):
    from collections import defaultdict

    mat = [l.rstrip() for l in lines]
    n, m = len(mat), len(mat[0])
    ds = (0, 1), (1, 0), (0, -1), (-1, 0), \
         (1, 1), (1, -1), (-1, -1), (-1, 1)

    def get_stars(i, j):
        stars = []
        for x, y in ds:
            r, c = i + x, j + y
            if r in (-1, n) or c in (-1, m):
                continue
            if mat[r][c] == '*':
                stars.append((r, c))
        return stars

    hmap = defaultdict(list)
    for i in range(n):
        num = 0
        srt = set()
        for j in range(m):
            x = mat[i][j]

            if x.isdigit():
                num = num * 10 + int(x)
                srt |= set(get_stars(i, j))

            if not x.isdigit() or j == m - 1:
                for star in srt:
                    hmap[star].append(num)
                num = 0
                srt = set()

    res = 0
    for nums in hmap.values():
        if len(nums) == 2:
            res += nums[0] * nums[1]
    return res


def day4_part1(lines):
    res = 0
    for line in lines:
        win, has = line.split(': ')[1].split(' | ')
        get = set(win.split()) & set(has.split())
        res += 1 << len(get) >> 1
    return res


def day4_part2(lines):
    n = len(lines)
    hmap = {}
    for i, line in enumerate(lines):
        win, has = line.split(': ')[1].split(' | ')
        get = set(win.split()) & set(has.split())

        hmap[i] = hmap.get(i, 1)
        for j in range(i + 1, min(n, i + len(get) + 1)):
            hmap[j] = hmap.get(j, 1) + hmap[i]
    return sum(hmap.values())


def day5_part1(lines):
    res = float('inf')
    for a in map(int, lines[0].split(': ')[1].split()):
        mapping = []
        for row in lines[2:] + ['\n']:
            if row == '\n':
                for yxl in mapping[1:]:
                    y, x, l = map(int, yxl.split())
                    if x <= a < x + l:
                        a = y + a - x
                        break
                mapping.clear()
            else:
                mapping.append(row)
        res = min(res, a)
    return res


def day5_part2(lines):
    intervals = []
    for x in map(int, lines[0].split(': ')[1].split()):
        if not intervals or len(intervals[-1]) == 2:
            intervals.append([x])
        else:
            intervals[-1].append(intervals[-1][0] + x - 1)

    mappings = []
    for line in lines[2:]:
        if 'map' in line:
            mappings.append([])
        elif line[0].isdigit():
            dst, src, length = map(int, line.split())
            mappings[-1].append([dst, src, length])

    for mapping in mappings:
        new = []
        for start, end in intervals:
            used = []

            for dst, src, length in mapping:
                left = max(start, src)
                right = min(end, src + length - 1)
                if left <= right:
                    diff = dst - src
                    new.append([left + diff, right + diff])
                    used.append([left, right])

            for left, right in sorted(used):
                if start < left:
                    new.append([start, left - 1])
                start = right + 1
            if start <= end:
                new.append([start, end])
        intervals = new

    return min(x[0] for x in intervals)


def day6_part1(lines):
    time = map(int, lines[0].split()[1:])
    dist = map(int, lines[1].split()[1:])
    res = 1
    for t, d in zip(time, dist):
        sub = 0
        for i in range(t):
            if i * (t - i) > d:
                sub += 1
        res *= sub
    return res


def day6_part2(lines):
    time = int(''.join(lines[0].split()[1:]))
    dist = int(''.join(lines[1].split()[1:]))
    res = 0
    for i in range(time):
        if i * (time - i) > dist:
            res += 1
    return res


def day7_part1(lines):
    from collections import Counter

    cards = 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'

    def sort_key(line):
        hand = line.split()[0]
        vals = sorted(Counter(hand).values(), reverse=True)
        vals = vals + [1] * (5 - len(vals))
        return vals, [-cards.index(c) for c in hand]

    res = 0
    for rank, line in enumerate(sorted(lines, key=sort_key), 1):
        _, bid = line.split()
        res += int(bid) * rank
    return res


def day7_part2(lines):
    from collections import Counter

    cards = 'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'

    def sort_key(line):
        hand = line.split()[0]
        cnt = Counter([c for c in hand if c != 'J'])
        jokers = len([c for c in hand if c == 'J'])

        if jokers == 5:
            cnt['J'] = 5
        else:
            max_k = max(cnt.keys(), key=lambda k: cnt[k])
            for k in cnt:
                if k == max_k:
                    cnt[k] += jokers
                    break

        vals = sorted(cnt.values(), reverse=True)
        vals = vals + [1] * (5 - len(vals))
        return vals, [-cards.index(c) for c in hand]

    res = 0
    for rank, line in enumerate(sorted(lines, key=sort_key), 1):
        _, bid = line.split()
        res += int(bid) * rank
    return res


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    print(day7_part2(lines))
