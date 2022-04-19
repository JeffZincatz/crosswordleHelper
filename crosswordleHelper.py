def readWordPool():
    '''
    Get all valid wordle answer words.
    '''
    pool = []

    with open("wordle-answers-alphabetical.txt") as f:
        pool = f.readlines()

    pool = list(map(lambda raw: raw[:-1] if raw[-1] == "\n" else raw, pool))
    return pool

WORD_POOL = readWordPool()

def getWordPool():
    return WORD_POOL.copy()

def fitPattern(inputW:str, pattern:str, word:str):
    '''
    Check if a input word fit a given word by a pattern
    A pattern must be a string of 5 numbers consists of only 0, 1, or 2.
    A word must be exactly 5 letters long.
    0: miss; 1: hit but wrong position; 2: hit and correct position.
    Pattern and word format should be handled by input function.
    '''
    
    word = word.upper()
    inputW = inputW.upper()

    # check for any hit in word
    remainedStr = "" # all char except those hit
    for i in range(5):
        if pattern[i] != '2':
            # not hit
            remainedStr += word[i]

    
    # check for not perfect hits / no hits
    for i in range(5):
        p = pattern[i]
        if p == '0' and inputW[i] in remainedStr:
            return False
        elif p == '1' and (inputW[i] not in word or inputW[i] == word[i]):
            return False
        elif p == '2' and (inputW[i] != word[i]):
            return False
    return True

def inputFiveLetterWord():
    result = ""
    while True:
        result = input("Enter a 5-letter word: ")
        if isFiveLetterWord(result):
            return result.upper()

def isFiveLetterWord(word:str):
    return word.isalpha() and len(word) == 5

def inputPattern():
    result = ""
    while True:
        result = input("Enter input pattern: ")
        if not isPattern(result):
            continue
        break
    return result

def isPattern(pattern:str):
    return len(pattern) == 5 and set(pattern).issubset({'0', '1', '2'})

def inputNoOfGuesses():
    '''
    Prompt user to input number of words required to be filled in, excluding answer word.
    '''
    nGuesses = int()
    while True:
        nGuesses = int(input("Number of words required (excluding answer word): ")) + 1
        if nGuesses in range(2, 7): # 2 <= nGuesses <= 6
            return nGuesses

def inputAllPatterns(nGuess:int):
    '''
    Get user inputs for all patterns, top to bottom, excluding the last pattern, which is always 22222.
    '''
    print(f"Give all patterns, using 0, 1, and 2, from top to bottom (exclude 22222):")
    patterns = list()
    for i in range(nGuess - 1):
        patterns.append(inputPattern())
    patterns.append('22222')
    patterns.reverse()
    return patterns

def inputStartWord():
    '''
    Prompt user to input start word.
    '''
    print(f"Start word - ", end="")
    return inputFiveLetterWord()

def filterPool(pool:list, pattern:str, word:str):
    '''
    Filter pool of valid words, given input word and pattern.
    If 
    '''

class State:
    nGuess = int() # number of total guesses
    nGuessLeft = int() # number of guess left to make
    patterns = list() # patterns of the problem, bottom to top
    guesses = list() # list of words guessed, bottom to top
    mustInclude = list()
    mustExclude = list()

    def __init__(self, nGuess:int, nGuessLeft:int, patterns:list, guesses:list, mustExclude:list):
        self.nGuess = nGuess
        self.nGuessLeft = nGuessLeft
        self.patterns = patterns
        self.guesses = guesses
        self.mustExclude = mustExclude

    
    def __repr__(self) -> str:
        rep = dict()
        rep["Patterns"] = self.patterns
        rep["Words guessed"] = self.guesses

        return str(rep)
    
    def getNextGuessIndex(self):
        '''
        Get the index of the word to make a guess next, 0-index.
        '''
        return self.nGuess - self.nGuessLeft
    
    def checkValidByMustexclude(self, word:str):
        '''
        Check if word must be excluded, given state's list of letters to exclude.
        Return True if the word passes the check i.e. contains no letter to be excluded, False otherwise.
        '''
        word = word.upper()
        for each in self.mustExclude:
            if each in word:
                return False
        return True
    
    def checkFollowHardMode(self, word:str):
        '''
        Check if a word follows hard mode guessing rule as next gussing word.
        Any missing letter must not be used again i.e. in mustExclude.
        Any exist letter ('1') must be reused.
        Any hit letter ('2') must be reused at the same place.
        Return True if it follows correctly, False otherwise.
        '''
        
        word = word.upper()
        nGuessIndex = self.getNextGuessIndex()
        currPattern = self.patterns[nGuessIndex]
        prevWord = self.guesses[-1]


        letterCount = dict()
        for c in prevWord:
            if c in letterCount:
                letterCount[c] += 1
            else:
                letterCount[c] = 1

        for i in range(5):
            p = currPattern[i]
            c = word[i]
            if p == '0' and word[i] in prevWord:
                return False
            elif p == '2':
                if word[i] != prevWord[i] or letterCount[c] <= 0:
                    return False
                letterCount[c] -= 1

            elif p == '1':
                if (word[i] not in prevWord or word[i] == prevWord[i]) or letterCount[c] <= 0:
                    return False
                letterCount[c] -= 1
            
        return True

    def getDomainValues(self):
        '''
        Get the valid guess word pool for the current guess, from bottom to top, given state.
        '''
        if self.nGuessLeft <= 0:
            return list()
        nGuessIndex = self.getNextGuessIndex()
        pool = getWordPool()
        currPattern = self.patterns[nGuessIndex]

        possibleWords = list(filter(lambda word: self.checkValidByMustexclude(word) and fitPattern(word, currPattern, self.guesses[0]) and self.checkFollowHardMode(word), pool))
        possibleWords = list(map(lambda word: word.upper(), possibleWords))

        return possibleWords

    def copy(self):
        return State(self.nGuess, self.nGuessLeft, self.patterns.copy(), self.guesses.copy(), self.mustExclude.copy())
    
    def makeGuess(self, word:str):
        nGuessIndex = self.getNextGuessIndex()
        self.guesses.append(word)
        self.nGuessLeft -= 1
        currPattern = self.patterns[nGuessIndex]

        mustExclude = list()
        for i in range(5):
            p = currPattern[i]
            if p == '0':
                mustExclude.append(word[i])
        self.mustExclude += mustExclude


def getInitState():
    nGuess = inputNoOfGuesses()
    patterns = inputAllPatterns(nGuess)
    startWord = inputStartWord()
    state = State(nGuess, nGuess - 1, patterns, [startWord], list())
    return state


def search(state:State):
    if state.nGuessLeft <= 0:
        return state.guesses
    
    domainValues = state.getDomainValues()

    for each in domainValues:
        temp = state.copy()
        temp.makeGuess(each)
        res = search(temp)
        if res:
            return res
    
    return None

def runCrosswordleHelper():
    initState = getInitState()
    goalState = search(initState)
    if goalState is None:
        return "No solution found"
    goalState.reverse()
    return goalState


if __name__ == "__main__":
    print(runCrosswordleHelper())
    input("Press enter to exit.")