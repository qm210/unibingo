import random
import sys
from math import sqrt
from PIL import Image, ImageDraw, ImageFont

wordsFile = './words.txt'

backgroundPngFile = './background.png'
fontSize = 17

marginX = 80
marginY = 90

clean = lambda line: stripLastComma(line.replace('\n','').strip()).replace(';','\n')
stripLastComma = lambda line: line[0:-1] if line and line[-1] == ',' else line

def readFile():
    handle = open(wordsFile, encoding='utf-8')
    words = [clean(line) for line in handle.readlines()]
    handle.close()
    return words

def generateField(words):
    wordCount = len(words)
    fieldSize = int(sqrt(wordCount))
    if fieldSize*fieldSize != wordCount:
        print(f"line number in {wordsFile} must be a square number. Currently it is {wordCount}.")
        quit()

    field = []
    for row in range(fieldSize):
        fieldRow = []
        for column in range(fieldSize):
            fieldRow.append(words[row * fieldSize + column])
        field.append(fieldRow)

    return field, fieldSize, wordCount

def drawCenteredText(draw, x, y, word, font, fill='white'):
    lines = word.split('\n')
    lineDistance = 1.2 * font.size
    for l in range(len(lines)):
        line = lines[l].strip()
        w, h = draw.textsize(line, font=font)
        drawX = x - .5 * w
        drawY = y + lineDistance * (l - .5 * (len(lines) + 1))
        draw.text((drawX, drawY), line, font=font, fill=fill)
        #draw.text((drawX+1, drawY), line, font=font, fill=fill)

def drawField(words, field, SEED):
    wordCount = len(words)
    fieldSize = sqrt(wordCount)

    image = Image.open(backgroundPngFile)
    imageWidth, imageHeight = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('comic-sans-ms.ttf', size=fontSize)

    random.seed(666)
    wordColor = {word: f'hsl({random.randint(0, 360)}, 100%, 70%)' for word in words}

    random.seed(666 * SEED)
    shuffledWords = random.sample(words, wordCount)

    distanceX = (imageWidth - 2*marginX) / (fieldSize - 1)
    distanceY = (imageHeight - 2*marginY) / (fieldSize - 1)

    for index in range(wordCount):
        posX = marginX + distanceX * (index % fieldSize)
        posY = marginY + distanceY * (int(index / fieldSize))
        word = shuffledWords[index]
        drawCenteredText(draw, posX, posY, word, font, fill = wordColor[word])

    draw.text((imageWidth - 210 - 10, imageHeight - .1 * 210 - 10), 'QM says hi (super-soberly)', fill='rgba(255,255,255,128)', font=font)

    fileName = f'./final{SEED}.png'
    image.save(fileName, 'PNG')
    return fileName

if __name__ == '__main__':
    SEEDS = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [0]
    words = readFile()
    field = generateField(words)
    for seed in SEEDS:
        fileName = drawField(words, field, seed)
        print(f'written: {fileName}')
    print('done.')