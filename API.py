def check():
    print('\nHello world from API.py!\n')

def GetNextMove(FEN):
    import requests

    rowLetters = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    rowNumbers = {8:0, 7:1, 6:2, 5:3, 4:4, 3:5, 2:6, 1:7}

    response = requests.post('https://chess.apurn.com/nextmove',
                        data=FEN                              
                        )

    print(response.content.decode("utf-8"))

    responceString = response.content.decode("utf-8")

    startRow = rowLetters[responceString[0]]
    StartCol = rowNumbers[int(responceString[1])]

    endRow = rowLetters[responceString[2]]
    endCol = rowNumbers[int(responceString[3])]

    print(f"api{startRow, StartCol, endRow, endCol}")
    return [startRow, StartCol, endRow, endCol]
    
'''

from API

8 # # # # # # # # 
7 # # # # # # # # 
6 # # # # # # # # 
5 # # # # # # # # 
4 # # # # # # # # 
3 # # # # # # # # 
2 # # # # # # # # 
1 # # # # # # # # 
- A B C D E F G H

My game

0 # # # # # # # # 
1 # # # # # # # # 
2 # # # # # # # # 
3 # # # # # # # # 
4 # # # # # # # # 
5 # # # # # # # # 
6 # # # # # # # # 
7 # # # # # # # # 
- 0 1 2 3 4 5 6 7

'''
