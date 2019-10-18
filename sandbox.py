L1 = [2,3,4]
L2 = [1,2]


S1 = set(L1)
S2 = set(L2)

if S1.intersection(S2):
    print('within')
else:
    print('not within')