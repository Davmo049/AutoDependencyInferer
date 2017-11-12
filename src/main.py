import subprocess
import os
from os import listdir
import fnmatch

def loadSymbolicDependencyGraph(path):
    symbolSource = {}
    symbolDefinitionStength = {}
    requiredSyms = {}
    main_obj = []
    for f in listdir(path):
        abspath = path+'/'+f
        syms = loadSymbols(abspath)
        if 'main' in [s[1] for s in syms]:
            main_obj.append(abspath)
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
    return (dependency_graph, main_obj)

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
    weakSyms = ['v', 'V', 'w', 'W', 'r', 'b', 't'] #might be incorrect
    if symbol == 'U':
        return 0
    if symbol in weakSyms:
        return 1
    return 2

def loadIncludeDependencyGraph(path):
    filesToParse = []
    dependency_graph = {}
    suffixesToParse = ['.cpp', '.hpp', '.h', '.c']
    for path, dir, files in os.walk(path):
        for f in files:
            for s in suffixesToParse:
                if f[-len(s):] == s:
                    filesToParse.append(path+'/'+f)
    for f in filesToParse:
        local_path = os.path.os.path.split(f)
        dependency_graph[f] = naive_include_parse(f, list(local_path))
    return dependency_graph

def naive_include_parse(path, includePrefixes):
    include_val = []
    with open(path) as f:
        content = f.readlines()
        for line in content:
            targetPrefix = "#include "
            if line[:len(targetPrefix)] == targetPrefix:
                marker = line[9]
                if marker == '"':
                    endMarker = '"'
                elif marker == '<':
                    endMarker = '>'
                else:
                    raise Exception('#include has to use " or <')
                endMarkerIndex = line[10:].index(endMarker)+10
                include_val.append(line[10:endMarkerIndex])
    ret = []
    for inc in include_val:
        for prefix in includePrefixes:
            if os.path.isfile(prefix+'/'+inc):
                ret.append(os.path.normpath(prefix+'/'+inc)) #normpath to fix include "../xxx.hpp"
                break
    return ret

def findSourcesOfObjFiles(path):
    o_files = find_file(path, '*.o')
    cpp_files = find_file(path, '*.cpp')
    c_files = find_file(path, '*.c')
    src_files = c_files+cpp_files

    o_to_src = {}
    src_to_o = {}

    for c_f in src_files: ## hashmaps can do this in O(N^2) -> O(N)
        _, fileAndExt = os.path.split(c_f)
        c_base, _ = os.path.splitext(fileAndExt)
        matches = []
        for o_f in o_files:
            _, fileAndExt = os.path.split(o_f)
            o_base, _ = os.path.splitext(fileAndExt)
            if o_base == c_base:
                matches.append(o_f)
        if len(matches) == 1:
            src_to_o[c_f] = matches[0]
            o_to_src[matches[0]] = c_f
        else:
            raise Exception("could not match src -> o files: " + c_f)
    for o_f in o_files:
        try:
            _ = o_to_src[o_f]
        except KeyError:
            raise Exception("could not match o -> src files: " + o_f)
    return (o_to_src, o_to_src)

    

def find_file(path, pattern):
    ret = []
    for root, dirs, files in os.walk(path):
        for f in files:
            fullpath = os.path.join(root, f)
            if fnmatch.fnmatch(fullpath, pattern):
                ret.append(fullpath)
    return ret

def matchCAndHeader(path):
    cpp_files = find_file(path, '*.cpp')
    c_files = find_file(path, '*.c')
    compile_files = c_files+cpp_files

    hpp_files = find_file(path, '*.hpp')
    h_files = find_file(path, '*.h')
    header_files = h_files+hpp_files

    c_to_h = {}
    h_to_c = {}

    for c_f in compile_files: #repeated code
        _, fileAndExt = os.path.split(c_f)
        c_base, _ = os.path.splitext(fileAndExt)
        matches = []
        for h_f in header_files:
            _, fileAndExt = os.path.split(h_f)
            h_base, _ = os.path.splitext(fileAndExt)
            if h_base == c_base:
                matches.append(h_f)
        if len(matches) == 1:
            c_to_h[c_f] = matches[0]
        elif len(matches) > 1:
            raise Exception("could not match c -> h files")
        else:
            c_to_h[c_f] = ''
    for h_f in header_files:
        _, fileAndExt = os.path.split(h_f)
        h_base, _ = os.path.splitext(fileAndExt)
        matches = []
        for c_f in compile_files:
            _, fileAndExt = os.path.split(c_f)
            c_base, _ = os.path.splitext(fileAndExt)
            if h_base == c_base:
                matches.append(c_f)
        if len(matches) == 1:
            h_to_c[h_f] = matches[0]
        elif len(matches) > 1:
            raise Exception("could not match h -> c files")
        else:
            h_to_c[h_f] = ''

    return (c_to_h, h_to_c)

class bazel_item:
    def __init__(self, name, content):
        self._name = name
        self._deps = set()
        self._content = content

    def add_deps(self, new_dep):
        self._deps.add(new_dep)

    def deps(self):
        return self._deps

    def name(self):
        return self._name

    def content(self):
        return self._content

    def __str__(self):
        indentedContent = ['\t\t'+s for s in self.content()];
        content_str = '\n'.join(indentedContent)
        indentedDeps = ['\t\t'+n.name() for n in self.deps()];
        dependencies_str = '\n'.join(indentedDeps)
        return self.name() + ":\n" + \
               "\t Content:\n" + \
               content_str + '\n' + \
               "\t Dependencies:\n" + \
               dependencies_str

def init_bazel_nodes(h2c, c2h):
    bazel_nodes = []
    for h, c in h2c.items():
        _, fileAndExt = os.path.split(h)
        base, _ = os.path.splitext(fileAndExt)
        if c != '':
            contents = set([h, c])
            bazel_nodes.append(bazel_item(base, contents))
        else:
            bazel_nodes.append(bazel_item(base, set([h])))
    for c, h in c2h.items():
        _, fileAndExt = os.path.split(c)
        base, _ = os.path.splitext(fileAndExt)
        if h == '':
            bazel_nodes.append(bazel_item(base, set([c])))
    return bazel_nodes

def connect_bazel_nodes(bazel_nodes, includeDependencyGraph):
    file2bazel_item = {}
    for node in bazel_nodes:
        for content in node.content():
            file2bazel_item[content] = node # works because all non pod is ref in python
    for node in bazel_nodes:
        for content in node.content():
            neededIncludes = includeDependencyGraph[content]
            for inc in neededIncludes:
                if not inc in node.content():
                    node.add_deps(file2bazel_item[inc])

def bazel_merge_strong_connections(bazel_nodes):
    strong_connections = find_bazel_strong_connections(bazel_nodes)
    number_of_strong_connection_groups_added = 0
    for connections in strong_connections:
        if len(connections) > 1:
            name = "tangle#"+ str(number_of_strong_connection_groups_added)
            number_of_strong_connection_groups_added += 1
            prev_names = set()
            for n in connections:
                prev_names.add(n.name())
            content = set()
            for n in connections:
                for c in n.content():
                    content.add(c)
            deps = set()
            for n in connections:
                for d in n.deps():
                    if not d.name() in prev_names:
                        deps.add(d)
            new_item = bazel_item(name, content)
            for d in deps:
                new_item.add_deps(d)
            bazel_nodes = [n for n in bazel_nodes if not n.name() in prev_names]
            bazel_nodes.append(new_item)
            for n in bazel_nodes:
                if len([d for d in n.deps() if d.name() in prev_names]) != 0:
                    n.add_deps(new_item)
                    n._deps = [d for d in n.deps() if not d.name() in prev_names]
    return bazel_nodes

#tarjan's strongly connected algo see
# https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
class tarjan_internals:
    def __init__(self):
        self.index = -1
        self.lowlink = -1
        self.on_stack = False
class tarjan_globals:
    def __init__(self):
        self.indexForInit = 0
        self.node_stack = []
        self.strong_connection_list = []

def find_bazel_strong_connections(bazel_nodes):
    node_extras = {}
    for n in bazel_nodes:
        node_extras[n] = tarjan_internals()
    globs = tarjan_globals()
    for n in bazel_nodes:
        if (node_extras[n].index == -1):
            strongconnect(n, node_extras, globs)
    return globs.strong_connection_list

def strongconnect(node, node_extras, globs):
    node_internal = node_extras[node]
    node_internal.index = globs.indexForInit
    node_internal.lowlink = globs.indexForInit
    globs.indexForInit = globs.indexForInit + 1
    globs.node_stack.append(node)
    node_internal.on_stack = True
    for child in node.deps():
        child_internals = node_extras[child]
        if node_extras[child].index == -1:
            strongconnect(child, node_extras, globs)
            node_internal.lowlink = min(node_internal.lowlink, child_internals.lowlink)
        elif child_internals.on_stack:
            node_internal.lowlink = min(node_internal.lowlink, child_internals.index)
    
    if (node_internal.lowlink == node_internal.index):
        toAdd = []
        while True:
            w = globs.node_stack.pop()
            node_extras[w].on_stack = False
            toAdd.append(w)
            if (w == node):
                break
        globs.strong_connection_list.append(toAdd)



def main():
    dir_to_infer_sym = '/media/data/code/AutoDependencyInferer/ExampleSetup/build'
    dir_to_infer_inc = '/media/data/code/AutoDependencyInferer/ExampleSetup/src'
    (symDependencyGraph, main_objects) = loadSymbolicDependencyGraph(dir_to_infer_sym)
    includeDependencyGraph = loadIncludeDependencyGraph(dir_to_infer_inc)
    (o_to_c, c_to_o) = findSourcesOfObjFiles('/media/data/code/AutoDependencyInferer/ExampleSetup')
    (c_to_h, h_to_c) = matchCAndHeader('/media/data/code/AutoDependencyInferer/ExampleSetup')

    # check all includes needed are in compiled file
    for o_file, o_file_deps in symDependencyGraph.items():
        src_file = o_to_c[o_file]
        src_deps_sym = [o_to_c[f] for f in o_file_deps]
        src_deps_decl = includeDependencyGraph[src_file]
        compiled_deps_decl = []
        for f in src_deps_decl:
            if h_to_c[f] != '' and h_to_c[f] != src_file:
                compiled_deps_decl.append(h_to_c[f])
        for f in src_deps_sym:
            if not f in compiled_deps_decl:
                print(src_file + " should probably include " + c_to_h[f])

        for f in compiled_deps_decl:
            if not f in src_deps_sym:
                print(src_file + " might not need to include " + c_to_h[f]) #might since struct declarations and inline/template functions will be false positives
    print(main_objects)
    bazel_nodes = init_bazel_nodes(h_to_c, c_to_h)
    connect_bazel_nodes(bazel_nodes, includeDependencyGraph)
    bazel_nodes = bazel_merge_strong_connections(bazel_nodes)
    main_src_files = [o_to_c[f] for f in main_objects]
    generate_bazel_files(bazel_nodes, main_src_files, "/media/data/code/AutoDependencyInferer/ExampleSetup")
    for n in bazel_nodes:
        print(n)

class bazel_generate_files_extra_fields:
    def __init__(self):
        self.pathOfNode = ''
        self.isMain = False

def generate_bazel_files(bazel_nodes, main_files, workspace_dir):
    extra_stuff = {}
    nodeInPath = {}
    for n in bazel_nodes:
        to_add = bazel_generate_files_extra_fields()
        pathToUse = ''
        if len(n.content()) == 1:
            pathToUse = os.path.split(list(n.content())[0])[0]
        else:
            pathToUse = os.path.commonpath(list(n.content()))
        if pathToUse in nodeInPath.keys():
            nodeInPath[pathToUse].add(n)
        else:
            nodeInPath[pathToUse] = set([n])
        to_add.pathOfNode = pathToUse
        extra_stuff[n] = to_add

    for n in bazel_nodes:
        for c in n.content():
            if c in main_files:
                extra_stuff[n].isMain = True

    for n in bazel_nodes:
        file_string = ''
        if extra_stuff[n].isMain:
            file_string = 'cc_binary(\n'
        else:
            file_string = 'cc_library(\n'
        file_string += """name = "{}",\n""".format(n.name())
        file_string += """visibility = ["//visibility:public"],\n"""
        (srcs, hdrs) = findSourceStrings(n, extra_stuff)
        if len(srcs) != 0:
            file_string += """srcs = ["{}"],\n""".format('", "'.join(srcs))
        else:
            file_string += """srcs = [],\n"""
        if not extra_stuff[n].isMain:
            if len(hdrs) != 0:
                file_string += """hdrs = ["{}"],\n""".format('", "'.join(hdrs))
            else:
                file_string += """hdrs = [],\n"""
        deps = findStringsForDeps(n, extra_stuff, workspace_dir)
        if len(deps) != 0:
            file_string += """deps = ["{}"],\n""".format('", "'.join(deps))
        file_string += ")"
        extra_stuff[n].bazel_file_string = file_string

    for path,nodes in nodeInPath.items():
        bazel_file = os.path.join(path, 'BUILD')
        with open(bazel_file, 'w') as f:
            for n in nodes:
                f.write(extra_stuff[n].bazel_file_string)
                f.write('\n\n')

def findSourceStrings(node, extra_stuff):
    srcs = []
    hdrs = []
    for c in node.content():
        pathToUse = extra_stuff[node].pathOfNode
        relative = c[len(pathToUse)+1:]
        _, ext = os.path.splitext(c)
        if ext in ['.cpp', 'c']:
            srcs.append(relative)
        else:
            hdrs.append(relative)
    return (srcs, hdrs)

def findStringsForDeps(node, extra_stuff, workspace_dir):
    deps = []
    for d in node.deps():
        bazel_build_file_to_use = ''
        if extra_stuff[node].pathOfNode != extra_stuff[d].pathOfNode:
            path_rel_to_ws = os.path.relpath(extra_stuff[d].pathOfNode, workspace_dir)
            bazel_build_file_to_use = '//'+path_rel_to_ws
        deps.append(bazel_build_file_to_use+':'+d.name())
    return deps

if __name__ == "__main__":
    main()
