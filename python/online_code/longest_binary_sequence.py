def continuous_ones(bin_str):
    x = [len(x) for x in bin_str.replace('0', ' ').split(' ') if len(x)]
    if not x:
        return None
    return max(x)


def continuous_ones1(bin_str):
    if not bin_str:
        return None
    seqs = []
    count = 0
    for i in bin_str:
        if i == '1':
            count += 1
        else:
            if count > 0:
                seqs.append(count)
            count = 0
    else:
        if count > 0:
            seqs.append(count)
    if not seqs:
        return None
    return max(seqs)


print('11000111100001', continuous_ones('11000111100001') == 4)
print('111', continuous_ones('111') == 3)
print('1', continuous_ones('1') == 1)
print('', continuous_ones('') == None)
print('0', continuous_ones('0') == None)
