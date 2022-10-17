import random
import json
import re
print("\n")
print(("-"*100+"\n"))
print("\nName: Wordle Assitant\nCreator: Rudra Barot\nDescription: Time to reply back to those green, yellow boxes.\n")
print(("-"*100+"\n"))
print("\nHere's how to use this:\n    1. Enter the guess you entered in the game when asked for it.\n    2. Enter the results as following:\n       '-'(hyphen) for grey box\n       '~' for yellow box\n       '!' for green box\n")
print("    For exmaples, please visit my github page: https://www.github.com/rudra2015/wordleAssitant.git\n")
print(("-"*100+"\n"))


class WordleAssitant():
    def __init__(self) -> None:
        self.BlackList = ''
        self.GreenList = ''
        self.YellowList = ''

        with open("Wordle/Wordle.json", "r") as f:
            Data = json.load(f)
            self.Guesses = Data["Guesses"]
            self.Answers = Data["Answers"]
            self.Frequency = Data["Frequency"]
            self.Probaility = Data["Probability"]

        for i in range(6):
            self.Guess = input("Enter your Guess: ")
            self.Result = input("Enter your Result: ")
            self.Guesses = self.ShortListData(
                self.Guess, self.Result, self.Guesses)
            self.Guesses = self.PrioritizeData(self.Guesses)
            self.Predcitions = self.Guesses[:10]
            if len(self.Predcitions) == 1:
                return print(f">>>Today's Wordle is: {self.Predcitions[0]}")
            elif self.Result == "!!!!!":
                return print("Congartulations!")
            else:
                print(
                    f"Here's what I think could be today's answer: {self.Predcitions}")

    def CleanLists(self, CurrentGreenList, CurrentYellowList, CurrentBlackList):
        NewBlackList = ''
        for i in CurrentBlackList:
            if i not in CurrentGreenList and i not in CurrentYellowList:
                NewBlackList += i
        CurrentBlackList = NewBlackList
        return [CurrentGreenList, CurrentYellowList, CurrentBlackList]

    def ShortListData(self, CurrentGuess, CurrentResult, CurrentData):
        # Defines
        GreenList = self.GreenList
        YellowList = self.YellowList
        BlackList = self.BlackList

        # Remove the current word from the data
        if CurrentGuess in CurrentData:
            CurrentData.remove(CurrentGuess)

        # Lists Cleaning
        GreenList, YellowList, BlackList = self.CleanLists(
            GreenList, YellowList, BlackList)

        # Making re pattern and updating lists
        Pattern = ''
        for i, j in zip(CurrentGuess, CurrentResult):
            if j == "!":
                Pattern += i
                if i not in GreenList:
                    GreenList += i
            elif j == "~":
                Pattern += f"([^{i}])"
                if i not in YellowList:
                    YellowList += i
            elif j == "-":
                Pattern += "(.)"
                if i in GreenList or i in YellowList:
                    pass
                elif i not in BlackList:
                    BlackList += i

        # Lists Cleaning
        GreenList, YellowList, BlackList = self.CleanLists(
            GreenList, YellowList, BlackList)

        # Shortlisting Main Database according to the blocklist
        NewData = []
        for Word in CurrentData:
            REMatch = re.match(Pattern, Word)
            ConditionStatus = len(set(Word).intersection(
                set(YellowList))) == len(YellowList)
            BlackListIntersection = len(set(Word).intersection(set(BlackList)))
            if BlackListIntersection == 0 and REMatch != None and ConditionStatus == True:
                NewData.append(Word)
        CurrentData = NewData

        # Optimizing
        CurrentData = list(set(CurrentData).intersection(set(self.Answers)))

        return CurrentData

    def PrioritizeData(self, CurrentData):
        DataSet = {}

        # Building Probaility Database
        for Word in CurrentData:
            for letter, n in zip(Word, range(5)):
                self.Probaility[letter][n] += 1

        # Making Word Score
        for Word in CurrentData:
            LocalLetterFrequencies = 0
            LoadedLetterFrequencies = 0
            WordDiversity = 0
            WordDiversityString = ''
            for letter, n in zip(Word, range(5)):
                if letter not in WordDiversityString:
                    WordDiversityString += letter
                    WordDiversity += 1
                    LocalLetterFrequencies += self.Probaility[letter][n]
                    LoadedLetterFrequencies += self.Frequency[letter]

            DataSet[Word] = int(LocalLetterFrequencies *
                                LoadedLetterFrequencies*WordDiversity)
            # DataSet[Word] = int(WordSum*LoadedLetterFrequencies)

        DataSet = sorted(DataSet.items(),
                         key=lambda kv: (kv[1], kv[0]))[::-1]

        CurrentData = [X for (X, __) in DataSet]

        return CurrentData


WordleAssitant()
