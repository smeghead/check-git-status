#!/usr/bin/python
import os, sys
import subprocess

def findRepogitories(baseDir, acc):
    for filename in os.listdir(baseDir):
        fullPath = os.path.join(baseDir, filename)
        if os.path.isdir(fullPath) and filename == '.git':
            acc.append(baseDir)
        if os.path.isdir(fullPath):
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
    return {
        'name': path.split('/')[-1],
        'path': path,
        'branch': branch,
        'status': status,
    }

def getRepogitoryInfos(repogitories):
    return map(createRepoInfo, repogitories)

def repogitoryInfos(path):
    repoPaths = findRepogitories(path, [])
    return getRepogitoryInfos(repoPaths)

if __name__ == '__main__':
    path = sys.argv[1]
    print 'begin test.'
    repoPaths = findRepogitories(path, [])
    repos = getRepogitoryInfos(repoPaths)
    print repos
    print 'completed test.'

# vim: set ts=4 sw=4 sts=4 expandtab fenc=utf-8:
