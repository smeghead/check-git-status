#!/usr/bin/python
import os, sys
import subprocess

def findRepogitories(baseDir, acc):
    for filename in os.listdir(baseDir):
        fullPath = os.path.join(baseDir, filename)
        if os.path.isdir(fullPath) and filename == '.git':
            acc.append(baseDir)
        elif os.path.isdir(fullPath):
            findRepogitories(fullPath, acc)
    return acc

def execCommand(cmd, path):
    p = subprocess.Popen(cmd, shell=True, cwd=path, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        close_fds=True)
    return p.stdout.read().strip()

def createRepoInfo(path):
    branch = execCommand('git symbolic-ref HEAD', path)
    status = execCommand('git status', path)
    flag = 'C' if status.find('Changes not staged for commit:') > -1 else '_'
    flag += 'U' if status.find('Untracked files:') > -1 else '_'
    name = path.split('/')[-1] 
    menuItem = name 
    if branch != u'refs/heads/master':
        menuItem += ' (' + branch + ')'
    return {
        'name': name,
        'path': path,
        'branch': branch,
        'status': status,
        'flag': flag,
        'menuItem': menuItem
    }

def getRepogitoryInfos(repogitories):
    return map(createRepoInfo, repogitories)

def repogitoryInfos(path):
    repoPaths = findRepogitories(path, [])
    return getRepogitoryInfos(repoPaths)

def notCleanRepogitoryInfos(path):
    return filter(lambda x: x['status'].find('working directory clean') == -1, repogitoryInfos(path))

def flatten(lst):
    if isinstance(lst, list):
       return reduce(lambda a,b: a + flatten(b), lst, [])
    else:
        return [lst]

def notCleanRepogitoryInfosByPathes(pathes):
    return flatten(map(notCleanRepogitoryInfos, pathes))

if __name__ == '__main__':
    pathes = sys.argv[1:]
    print 'begin test.'
    repos = notCleanRepogitoryInfosByPathes(pathes)
    print repos
    print 'completed test.'

# vim: set ts=4 sw=4 sts=4 expandtab fenc=utf-8:
