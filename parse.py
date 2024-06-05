class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.children = []
        self.parent = parent
        self.next_rule = 0 
        self.start_index = 0
        self.prev_stack = 0
    
def is_nonterminal(node):
    if node is None:
        return False
    return node.value.isupper()

def get_rule_to_expand(node):
    rules = [
        ('S', ['A', 'B']),
        ('S', ['B', 'C']),
        ('S', ['e']),
        ('A', ['a']),
        ('B', ['A', 'b']),
        ('C', ['c']),
        ('C', ['d']),
    ]

    for i in range(node.next_rule, len(rules)):
        if rules[i][0] == node.value:
            node.next_rule = i + 1
            return rules[i][1] 
    return None

input_words = ['a', 'b', 'c', 'd','eof']
current_index = 0

def get_word():
    global current_index
    if current_index < len(input_words):
        word = input_words[current_index]
        return word
    return None

def match(node, word):
    if node is None:
        return False
    return node.value == word

status = True
def parse():
    global current_index
    root = Node('S')
    focus = root
    prev_focus = focus
    stack = [None]
    root.prev_stack = 1
    word = get_word()

    def backtrack():
        global current_index
        global status
        nonlocal focus
        nonlocal stack
        nonlocal word
        if focus is None:
            focus = prev_focus

        focus = focus.parent
        if focus is None:
            status = False
            return
        current_index = focus.start_index
        word = input_words[current_index]

        focus.children = []
        stack = stack[:focus.prev_stack]
         
    
    while status:
        print("#########################")
        print_tree(root)
        print("-------------------------")
        print_stack(stack)
        print("-------------------------")
        print("focus:", focus.value if focus else None)
        print("-------------------------")
        print("word:", word)
        print("#########################")
        if is_nonterminal(focus):
            rule = get_rule_to_expand(focus)
            if rule == None:
                backtrack()
                continue

            children = [Node(beta, parent=focus) for beta in rule]
            focus.children.extend(children)
            stack.extend(children[::-1])
            focus = stack.pop()
            if focus:
                focus.start_index = current_index
                focus.prev_stack = len(stack)
        elif match(focus, word):
            current_index += 1
            word = get_word()
            prev_focus = focus
            focus = stack.pop()
            if focus:
                focus.start_index = current_index
                focus.prev_stack = len(stack)
        elif word == 'eof' and focus is None:
            return root
        else:
            backtrack()

def print_tree(node, level=0):
    indent = ' ' * (level * 2)  # 每层缩进2个空格
    print(f"{indent}{node.value}")
    for child in node.children:
        print_tree(child, level + 1)
    
def print_stack(stack):
    print("Stack:")
    for node in stack[1:]:
        print(node.value)

# 开始解析
root = parse()
if root:
    print("解析完成")
    print_tree(root)
else:
    print("解析失败")
