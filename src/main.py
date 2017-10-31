import subprocess
from os import listdir

def loadDependencyGraph(path):
    symbolSource = {}
    symbolDefinitionStength = {}
    requiredSyms = {}
    for f in listdir(path):
        abspath = path+'/'+f
        syms = loadSymbols(abspath)
        requiredSyms[abspath]=getRequiredSyms(syms)
        updateSymbols(symbolSource, symbolDefinitionStength, abspath, syms)
    dependency_graph = {}
    undefined_vals = set()
    for key, values in requiredSyms.items():
        deps = set()
        for value in values:
            try:
                deps.add(symbolSource[value])
            except:
                undefined_vals.add(value)
        dependency_graph[key] = deps
        print(key + ': ' + str([i for i in deps]))
    print("undefined:" + str([i for i in undefined_vals]))
    print(dependency:graph)

def loadSymbols(path):
    ret = []
    with open('/tmp/nmFile', 'w') as f:
        subprocess.call(['nm', path], stdout=f)
    with open('/tmp/nmFile') as f:
        content = f.readlines()
        for line in content:
            cur_sym = line[17]
            symbol_val = line[19:-1]
            ret.append((cur_sym, symbol_val))
    return ret

def getRequiredSyms(syms):
    ret = []
    for sym in syms:
        symbol_type = sym[0]
        symbol_value = sym[1]
        if symbol_type == 'U':
            ret.append(symbol_value)
    return ret

def updateSymbols(symbolSource, symbolDefinitionStength, abspath, syms):
    for sym in syms:
        symbol_type = sym[0]
        cur_symbol_strength = getSymbolStrength(symbol_type)
        symbol_value = sym[1]
        symbolNotDefined = not(symbol_value in symbolDefinitionStength)
        if symbolNotDefined:
            if cur_symbol_strength > 0:
                addSymbol = True
            else:
                addSymbol = False
        else:
            someVal = symbolDefinitionStength[symbol_value]
            workaround = (someVal < cur_symbol_strength and cur_symbol_strength > 0)
            if workaround:
                addSymbol = True
            else:
                addSymbol = False


        if addSymbol:
                symbolDefinitionStength[symbol_value] = cur_symbol_strength
                symbolSource[symbol_value] = abspath
        elif cur_symbol_strength == 2:
                print(abspath+ " and "+symbolSource[symbol_value]+" both define "+symbol_value)

def getSymbolStrength(symbol):
    weakSyms = ['v', 'V', 'w', 'W', 'r', 'R', 'b', 'B', 't', 'T']
    if symbol == 'U':
        return 0
    if symbol in weakSyms:
        return 1
    return 2

def main():
    dir_to_infer = '/media/data/code/AutoDependencyInferer/ExampleSetup/build'
    dependencyGraph = loadDependencyGraph(dir_to_infer)

if __name__ == "__main__":
    main()
