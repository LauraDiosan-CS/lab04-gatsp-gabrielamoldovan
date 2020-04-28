def fitness(path, param):
    Q = 0
    if path[len(path) - 1] not in param[path[0]]:
        return 0
    for i in range(len(path) - 1):
        if path[i + 1] not in param[path[i]]:
            return 0
        else:
            Q = Q + int(param[path[i]][path[i + 1]])
    return Q

def read_file(file_name):
    file = open(file_name, "r")
    n = int(file.readline())
    mat = []
    for i in range(n):
        mat.append([])
        v = file.readline()
        v = v.split('\n')
        args = v[0].split(",")
        for arg in args:
            mat[i].append(arg)
    return {'mat': mat, 'noNodes': len(mat)}