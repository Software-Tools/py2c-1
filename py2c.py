import sys

#global vars
variables = {}
indent = ''
blockend = False

def getIndent(string):
    l = string.split(' ')
    indent = 0
    for i in l:
        if i != '': 
            break
        indent += 1
    return indent*' '

def getType(var):
    var = var.strip()
    if var[0]=='[':
        try:
            if '.' in var:
                return 'float list'
            elif getType(var[1]) == 'int':
                return 'int list'
        except: pass
    try:
        if(int(var) == float(var)):
            return 'int'
    except:
        try:
            var = float(var)
            return 'float'
        except: pass
    if len(var) > 3: return 'string'
    return 'char'

def convert(line):

    global variables, indent

    newLine = '  '
    
    if getIndent(line) == indent + '  ':
        newLine += indent
        indent += '  '
        newLine += '{\n  '
    elif indent != '' and getIndent(line) != indent:
        indent = getIndent(line)
        newLine += indent+'}\n'
    
    newLine += indent
    line = line.strip()
    if '=' in line and '==' not in line:
        lhs, rhs = line.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()
        type = getType(rhs)
        if type == 'int':
            newLine += 'int '+str(lhs)+'='+str(rhs)+';\n'
        elif type == 'float':
            newLine += 'float '+str(lhs)+'='+str(rhs)+';\n'
        elif type == 'char':
            newLine += 'char '+str(lhs)+'='+str(rhs)+';\n'
        elif type == 'string':
            newLine += 'char '+str(lhs)+'['+str(len(rhs)-2)+']='+str(rhs)+';\n'
        elif type == 'int list':
            newLine += 'int '+str(lhs)+'['+str(len(rhs)/2)+']={'
            newLine += rhs[1:-1]+'};\n'

        elif type == 'float list':
            newLine += 'float '+str(lhs)+'['+str(len(rhs)/2)+']={'
            newLine += rhs[1:-1]+'};\n'
        variables[lhs] = type

    elif 'elif' in line:
        line = line[:-1].split('elif')
        newLine += 'else if('+ line[1] +')\n'

    elif 'if' in line:
        line = line[:-1].split('if')
        newLine += 'if('+ line[1] +')\n'

    elif 'else' in line:
        line = line[:-1].split('else')
        newLine += 'else'+ line[1] +'\n'

    elif 'while' in line:
        line = line[:-1].split('while')
        newLine += 'while('+line[1]+')\n'

    elif 'for' in line:
        line = line[:-1].split(' ')
        counter = line[1]
        start = int(line[-1][-6])
        end = int(line[-1][-4])+1
        step = int(line[-1][-2])
        newLine += 'for(int '+str(counter)+ '='+str(start)+';'+str(counter)+'<='+str(end)+';'+str(counter)+'+='+str(step)+')\n'

    elif 'print' in line:
        printLine = line[5:].strip()
        sameLine = False
        try:
            if printLine[-1] == ",":
                sameLine = True
            else:
                sameLine = False
        except: pass
        try:
            type = variables[printLine]
        except:
            type = 'string'
        if len(printLine) == 0:
            newLine += 'printf("\\n");\n'
        else:
            if type == 'char':
                if not sameLine:
                    newLine += 'printf("%c\\n",'+str(printLine)+');\n'
                else:
                    newLine += 'printf("%c ",'+str(printLine[:-1])+');\n'
            if type == 'int':
                if not sameLine:
                    newLine += 'printf("%d\\n",'+str(printLine)+');\n'
                else:
                    newLine += 'printf("%d ",'+str(printLine[:-1])+');\n'
            if type == 'float':
                if not sameLine:
                    newLine += 'printf("%f\\n",'+str(printLine)+');\n'
                else:
                    newLine += 'printf("%f ",'+str(printLine[:-1])+');\n'
            if type == 'string':
                if not sameLine:
                    newLine += 'printf("%s\\n",'+str(printLine)+');\n'
                else:
                    newLine += 'printf("%s ",'+str(printLine[:-1])+');\n'
        

    elif line != '':
        newLine += line + ';\n'

    return newLine


if __name__=="__main__":
    
    #opening read and write files
    f1 = open(sys.argv[1],"r+")
    f2 = open(sys.argv[1][:-2]+"c","w+")

    #writing header files
    f2.write("#include<stdio.h>\n")
    f2.write("#include<stdlib.h>\n")
    f2.write("#include<string.h>\n")
    f2.write("#include<math.h>\n")
    f2.write("\n\nint main()\n{\n")

    #reading through each line in python file and copying to c file
    for line in f1.readlines():
        f2.write(convert(line)+'\n')

    f2.write("return(0);\n}\n")

    #closing both files...
    f1.close()
    f2.close()



