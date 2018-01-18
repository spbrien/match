
def uniq(oldlist):
    cleanlist = []
    for x in oldlist:
        if x not in cleanlist:
            cleanlist.append(x)
    return cleanlist
