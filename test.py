from crosswordleHelper import fitPattern


def test_fp(tests:tuple):
    for i, (inputWord, pattern, word) in enumerate(tests):
        res = fitPattern(inputWord, pattern, word)
        if res:
            print(f"Test case {i}: Passed.")
        else:
            print(f"Test case {i}: Failed. Input: {inputWord}. Pattern: {pattern}. Word: {word}.")


# a tuple of test cases: 0 - input word, 1 - pattern, 2 - word to match
tests = (('eeezz', '11000', 'yyyee'), ('speed', '00110', 'leake'), ('zzzzz', '00000', 'aaaaa'), ('raise', '22222', 'raise'), ('abcab', '11200', 'bacdc'))
test_fp(tests)




