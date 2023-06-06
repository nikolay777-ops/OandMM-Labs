test = [5, 2, 'xxx', 1, 'xxx']
test_2 = test[:]

while 'xxx' in test:
    test.pop(
        test.index('xxx'))

print(test_2.index(min(test)))