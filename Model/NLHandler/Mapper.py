
f = open("keywords.csv", "r")
while(True):
    line = f.readline()
    if not line:
        break
    nodetype = line[0:2]
    line = line[3:]
    kw = line[0:line.find(':')]
    line = line[(line.find(':')+1):(len(line)-1)]
    wordlist = line.split(',')
    print(wordlist)

f.close