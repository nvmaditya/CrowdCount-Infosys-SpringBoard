TARGET = 369
K = 9

nums = list(range(1, 82))
used = [False] * 82
groups = []

def backtrack(start, count, total, current):
    if count == K:
        return total == TARGET
    
    if total > TARGET:
        return False
    
    for i in range(start, 82):
        if not used[i]:
            used[i] = True
            current.append(i)
            
            if backtrack(i + 1, count + 1, total + i, current):
                return True
            
            current.pop()
            used[i] = False
    
    return False

def solve():
    for _ in range(9):
        group = []
        if not backtrack(1, 0, 0, group):
            return False
        groups.append(group.copy())
    return True

solve()

for g in groups:
    print(g, sum(g))