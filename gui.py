from classes import Simulation
import pygame
import math

class GUI:
    def __init__(self, width = 1000, height = 350, colorFocus = 50):
        pygame.init()
        self.width = width
        self.height = height
        self.WIN = pygame.display.set_mode((width, height))

        self.fontSize = 32
        
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontSize)

        self.colors = self.generateColorList()

        self.objects = []
        self.addObjs()
        btnWidth = 175
        self.button = Button(0, 250, btnWidth, self.fontSize, Simulation.ecosystem)
        self.button.rect.centerx = self.width / 2

    def run(self):
        run = True
        bgIndex = 0
        while run:
            pygame.time.delay(25)

            self.update(bgIndex)
            bgIndex += 1
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()


    def generateColorList(self):
        colors = [(255, 0, 0)]

        vals = [i for i in range(0, 255)]
        vals_back = vals.copy()
        vals_back.reverse()

        rgb_index = 1
        forward = True

        count = 0
        while count < 6:
            color = [colors[-1][0], colors[-1][1], colors[-1][2]]

            if forward:
                for val in vals:
                    color = [colors[-1][0], colors[-1][1], colors[-1][2]]

                    color[rgb_index] = val
                    colors.append(color)
            else:
                for val in vals_back:
                    color = [colors[-1][0], colors[-1][1], colors[-1][2]]

                    color[rgb_index] = val
                    colors.append(color)
            
            count += 1
            rgb_index -= 1

            if rgb_index < 0:
                rgb_index = 2
                
            if forward:
                forward = False
            else:
                forward = True
            

        return colors


    def addObjs(self):
        # slider for fishAmount
        self.objects.append(Slider(
            x = 150, 
            y = 50, 
            width = 50, 
            height = 250, 
            maxVal = 5000,
            sliderColor = (155, 0, 0),
            buttonColor = (0, 0, 255)
            ))

        self.objects.append(Slider(
            x = self.width - self.width // 5, 
            y = 50, 
            width = 50, 
            height = 250, 
            maxVal = 1000,
            sliderColor = (155, 0, 0),
            buttonColor = (0, 0, 255)
            ))


    def displayObjects(self):
        clicks = pygame.mouse.get_pressed()
        for obj in self.objects:

            if obj.check():
                btncolor = (125, 125, 255)
                if clicks[0] == 1:
                    obj.checkMovements()
            else:
                btncolor = obj.buttonColor

            pygame.draw.rect(self.WIN, obj.sliderColor, obj.sliderRect)
            pygame.draw.rect(self.WIN, (0, 0, 0), obj.sliderRect, 3)

            pygame.draw.rect(self.WIN, btncolor, obj.buttonRect)
            pygame.draw.rect(self.WIN, (0, 0, 0), obj.buttonRect, 3)

            pygame.draw.rect(self.WIN, self.button.color, self.button.rect)
            pygame.draw.rect(self.WIN, (0, 0, 0), self.button.rect, 3)
            
    
    def drawText(self, text, x, y, color, font, fontSize = None):
        if fontSize != None:
            font = pygame.font.Font('freesansbold.ttf', fontSize)
        a = font.render(text, True, color)
        self.WIN.blit(a, (x, y))


    def displayText(self):
        pygame.draw.rect(self.WIN, (0, 0, 0), (0, 0, self.width, self.fontSize))
        
        self.drawText("Begin Simulation", self.button.rect[0] + 3, self.button.rect[1] + 5, (255, 255, 255), self.font, 20)
        self.drawText(f"Fish Population: {math.floor(self.objects[0].getVal())}", 10, 0, (255, 255, 255), self.font)
        self.drawText(f"Shark Population: {math.floor(self.objects[1].getVal())}", self.width - 400, 0, (255, 255, 255), self.font)


    def update(self, bgIndex):
        if bgIndex >= self.colors.__len__():
            bgIndex = 0

        self.WIN.fill(self.colors[bgIndex])

        self.displayObjects()
        self.displayText()
        self.button.check(self.objects[0].getVal(), self.objects[1].getVal())

        pygame.display.flip()


class Slider:
    def __init__(self, x, y, width, height, maxVal, sliderColor, buttonColor) -> None:
        self.sliderRect = pygame.Rect(x, y, width, height)
        self.sliderColor = sliderColor

        self.maxVal = maxVal

        buttonWidth = width * 3
        buttonX = self.sliderRect.centerx - (buttonWidth // 2)

        self.buttonRect = pygame.Rect(buttonX, y, buttonWidth, height // 3)

        self.buttonColor = buttonColor

    def check(self):
        pos = pygame.mouse.get_pos()
        if self.buttonRect.collidepoint(pos[0], pos[1]):
            return True
        return False

    def checkMovements(self):
        pos = pygame.mouse.get_pos()
        prev = self.buttonRect.centery 
        self.buttonRect.centery = pos[1]

        if self.buttonRect.top < self.sliderRect.top or self.buttonRect.bottom > self.sliderRect.bottom:
            self.buttonRect.centery = prev

    def getVal(self):
        percent = ((self.sliderRect[1] - self.buttonRect[1]) / (self.sliderRect[3] - self.buttonRect[3])) * -1 # no idea why it's negative. Don't care! :)
        return self.maxVal * percent


class Button:
    def __init__(self, x, y, width, height, onclick, color = (255, 125, 125)) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.onclick = onclick

    def check(self, fishPop, sharkPop):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos[0], pos[1]):
            self.color = (255, 0, 0)
            pressed = pygame.mouse.get_pressed()
            if pressed[0] == 1:
                pygame.quit()
                self.onclick(int(fishPop), int(sharkPop))
        else:
            self.color = (255, 125, 125)
        

gui = GUI()
gui.run()