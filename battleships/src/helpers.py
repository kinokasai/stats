def to_dual(i):
    return (i % 10, int(i/10))

def add_to_stack(pos, stack):
    x, y = pos
    stack.append((x + 1, y))
    stack.append((x - 1, y))
    stack.append((x, y + 1))
    stack.append((x, y - 1))
