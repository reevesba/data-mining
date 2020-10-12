# parses Tanagra tree description
# convert to python tree

import tree as t
import re

def next_tag():
    pass

with open("dat/tan-output.txt") as file_in:
  descr = file_in.read()

ul_a = "<UL>"
ul_b = "</UL>"
li = "<li>"

# fetch the unordered list
descr = re.search("<UL>(.*)</UL>", descr).group(0)

# remove noise
descr = re.sub("\(.*?\)", "", descr)
descr = re.sub("<\/?[b]>", "", descr)
#print(descr)

# try looping through all tags
end = False
index = 0
while not end:
    # get the next tag
    nexttag = re.search("<..>", descr[index:]).group(0)
    index = index + re.search("<..>", descr[index:]).end()

    if nexttag and nexttag == "<UL>":
        print(nexttag)

        nexttag = re.search("<..>", descr[index:]).group(0)
        index = index + re.search("<..>", descr[index:]).end()

        if nexttag and nexttag == "<LI>":
            print(nexttag)
            str_s = index
            end_s = str_s + re.search("<..>", descr[str_s:]).start()

            s = descr[str_s:end_s]
            print(s)
    elif nexttag and nexttag == "<LI>":
        print(nexttag)
        str_s = index
        if re.search("<..>", descr[str_s:]):
            end_s = str_s + re.search("<..>", descr[str_s:]).start()
            s = descr[str_s:end_s]
            print(s)
        else:
            end_s = None
            s = descr[str_s:end_s]
            print(s)
            end = True
    else:
        end = True


nexttag = re.search("<..>", descr).group(0)
end_idx = re.search("<..>", descr).end()


#if nexttag == "<LI>":
#    nexttag = re.search("<..>", descr).group(0)
#    print(nexttag)

if nexttag == "<UL>":
    nexttag = re.search("<..>", descr[end_idx:]).group(0)
    end_idx = re.search("<..>", descr[end_idx:]).end()

    if nexttag == "<LI>":
        str_s = end_idx + 4
        end_s = str_s + re.search("<..>", descr[str_s:]).start()

        s = descr[str_s:end_s]
        #print(s)



#root = t.Node("uc", 2.5)
#root.print_tree()