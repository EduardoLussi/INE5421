def dict_deep_length(dic):
    l = 0
    for e in dic:
        if isinstance(e, list):
            l += len(e)
        else:
            l += 1
    return l
