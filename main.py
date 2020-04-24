import random
import sys
from math import sqrt
from PIL import Image, ImageDraw, ImageFont

wordsFile = './words.txt'

backgroundPngFile = './background.png'
fontSize = 16

marginX = 80
marginY = 90

clean = lambda line: stripLastComma(line.replace('\n','').strip()).replace(';','\n')
stripLastComma = lambda line: line[0:-1] if line and line[-1] == ',' else line

maxMode = True

def readFile():
    handle = open(wordsFile, encoding='utf-8')
    words = [clean(line) for line in handle.readlines()]
    handle.close()
    return words

def drawCenteredText(draw, x, y, word, font, fill='white', lineDistance = 1.2):
    lines = word.split('\n')
    for l in range(len(lines)):
        line = lines[l].strip()
        w, h = draw.textsize(line, font=font)
        drawX = x - .5 * w
        drawY = y + lineDistance * font.size * (l - .5 * (len(lines) + 1))
        draw.text((drawX, drawY), line, font=font, fill=fill)

def drawField(words, SEED):
    wordCount = len(words)
    fieldSize = int(sqrt(wordCount))
    if maxMode and wordCount == 48:
        wordCount = 49
        fieldSize = 7
    elif fieldSize * fieldSize != wordCount:
        print(f"line number in {wordsFile} must be a square number. Currently it is {wordCount}.")
        quit()

    image = Image.open(backgroundPngFile)
    imageWidth, imageHeight = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('comic-sans-ms.ttf', size=fontSize)

    random.seed(666)
    wordColor = {word: f'hsl({random.randint(0, 360)}, 100%, 70%)' for word in words}

    random.seed(666 * SEED)
    shuffledWords = random.sample(words, len(words))

    distanceX = (imageWidth - 2*marginX) / (fieldSize - 1)
    distanceY = (imageHeight - 2*marginY) / (fieldSize - 1)

    if maxMode:
        maxWord = 'Max ein\n"XW<3"\nschicken'
        shuffledWords = shuffledWords[0:24] + [maxWord] + shuffledWords[24:48]
        wordColor.update({maxWord: 'rgb(255,80,255)'})

        xw = Image.open('./xw.png')
        xwW, xwH = xw.size
        image.paste(xw, (round((imageWidth-xwW)/2), round((imageHeight-xwH)/2) + 7), mask=xw)

    for index in range(wordCount):
        posX = marginX + distanceX * (index % fieldSize)
        posY = marginY + distanceY * (int(index / fieldSize))
        word = shuffledWords[index]
        if maxMode and index == 24:
            drawCenteredText(draw, posX, posY - 20, word, font, fill = wordColor[word], lineDistance=1.1)
        else:
            drawCenteredText(draw, posX, posY, word, font, fill = wordColor[word])

    draw.text((imageWidth - .4*210 - 30, imageHeight - .1 * 210 - 10), 'QM says hi v2', fill='rgba(255,255,255,88)', font=font)

    fileName = f'./unibingo{SEED}.png'
    image.save(fileName, 'PNG')
    return fileName

if __name__ == '__main__':
    SEEDS = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [0]
    words = readFile()
    for seed in SEEDS:
        fileName = drawField(words, seed)
        print(f'written: {fileName}')
    print('done.')