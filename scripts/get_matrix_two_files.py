import sys


filein = open(sys.argv[1],'r')
fileout = open(sys.argv[2],'w')

set_x = set()
set_y = set()


matrix = {}
for line in filein:
    line = line.rstrip()
    fields = line.split()
    key = fields[1]+'-'+fields[2]
    matrix[key] = matrix.get(key,0) + 1
    
for x in range(max(list(set_x))):
    for y in range(max(list(set_y))):
        to_print = str(x)+'-'+str(y)+' '+ \
        str(matrix.get(str(x)+'-'+str(y),0)) +'\n'
        
        fileout.write(to_print)
        
fileout.close()
