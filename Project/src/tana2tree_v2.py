# parses Tanagra tree description
# convert to python tree

import tree as t
import re

def next_tag(s, i):
    return re.search("</*..>", s[i:])

with open("dat/tan-output.txt") as file_in:
  descr = file_in.read()

f = open("out/tan_descr.txt", "w+")

# extract the unordered list
descr = re.search("<UL>(.*)</UL>", descr).group(0)

# remove noise
descr = re.sub("\(.*?\)", "", descr)
descr = re.sub("<\/?[b]>", "", descr)

# loop through tags
depth = 0
end = False
start = 0
my_tree = None

while not end:
    if next_tag(descr, start):
        tag = next_tag(descr, start).group(0)
        start = start + next_tag(descr, start).end()

        parent = ""

        if tag == "<UL>":
            depth = depth + 1
            #print(tag)
            #print(depth)

        elif tag == "<LI>":
            #print(tag)
            s = descr[start:start + next_tag(descr, start).start()]
            #print(s)

            f.write(str(depth) + " " + s + "\n")

            # 3. check for then
            #       a. if < branch left
            #       b. if >= branch right

            # if depth is 1 create root node

            # create attribute labels
            if s.find("<") != -1:
                ss = s[:s.find("<")]
                op = "<"
            else:
                ss = s[:s.find(">")]
                op = ">"

            attr = "".join(c[0] for c in ss.split())

            # get the values, find numbers with commas, floats, and ints
            value = float(re.search('[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', s).group(0))
            #print(value)

            if depth == 1 and op == "<":
                my_tree = t.Node(attr, value)

            if op == "<" and "then" in s:
                target = s[s.find("target = ") + len("target = "):]
                #my_tree.insert_left(attr, target, 0)
            if op == ">" and "then" in s:
                target = s[s.find("target = ") + len("target = "):]
                #my_tree.insert_right(attr, target, 0)
            if op == "<" and "then" not in s:
                pass
            if op == ">" and "then" not in s:
                pass
                
        else:
            depth = depth - 1
            #print(tag)
            #print(depth)
    else:
        end = True

f.close
my_tree.print_tree()