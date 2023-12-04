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


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    print(day3_part2(lines))
