import random as r
import time
import matplotlib.pyplot as plt

class Fish:
    population = []
    ID = 0

    def __init__(self, parent1 = None, parent2 = None):
        Fish.population.append(self)
        
        self.parents = (parent1, parent2)

        self.isLookingForMate = False
        self.traits = Traits(self)

        Fish.ID += 1
        self.ID = Fish.ID

        self.reproduceLevel = 0
        self.disease = None
        self.hunger = 0


    def checkDeath(self):
        if self.hunger >= 100:
            self.die()


    def escapeShark(self, shark):
        if self.traits.speed >= shark.traits.speed:
            return True
        return False

    
    def update(self):
        # print(self)
        self.hunger += r.randint(0, 10)
        self.reproduceLevel += r.randint(0, 10)

        self.checkReproduce()
        self.searchForFood()

        self.checkInfection()

        self.checkDeath()


    def checkInfection(self):
        if self.disease == None:
            if r.randint(0, 750) == 1:
                self.disease = Disease(self)
                self.checkInfectionDeath()


    def checkInfectionDeath(self):
        if r.randint(0, 5) == 1:
            self.die()

    
    def checkReproduce(self):
        if self.reproduceLevel >= 50:
            self.isLookingForMate = True
            self.lookForMate()

    
    def lookForMate(self):
        for fish in Fish.population:
            if fish != self and fish.isLookingForMate:
                self.reproduce(fish)


    def reproduce(self, other):
        # The Funny Function™
        
        # Add genetics here
        self.isLookingForMate = False
        other.isLookingForMate = False

        self.reproduceLevel = 0
        other.reproduceLevel = 0

        newFish = Fish(self, other)
        # print(f"{newFish} has been birthed to fishes {self.ID} and {other.ID}")


    def searchForFood(self):
        if list(Food.availableFood).__len__() > 0 and self.hunger >= 0:
            chosenFood = Food.availableFood[r.randint(0, Food.availableFood.__len__() - 1)]
            self.hunger -= chosenFood.value
            chosenFood.checkIfEaten()


    def die(self):
        try:
            Fish.population.remove(self)
        except ValueError:
            pass

        del self


    def __repr__(self):
        return f"Fish {str(self.ID)} | Hunger: {self.hunger} | Reproduction: {self.reproduceLevel} | Disease: {self.disease} | Traits: {self.traits}"


class Shark:
    population = []
    ID = 0

    def __init__(self, parent1 = None, parent2 = None):
        Shark.population.append(self)
        Shark.ID += 1

        self.isLookingForMate = False
        self.ID = Shark.ID

        self.parents = (parent1, parent2)

        self.traits = Traits(self)

        self.reproduceLevel = 0
        self.hunger = 0
        self.disease = None


    def update(self):
        self.hunger += r.randint(10, 20)
        self.reproduceLevel += r.randint(10, 20)
        
        self.checkReproduce()
        self.searchForFood()

        if self.disease != None:
            self.spreadDisease()

        self.checkDeath()


    def checkReproduce(self):
        if self.reproduceLevel >= 100:
            self.isLookingForMate = True
            self.lookForMate()


    def lookForMate(self):
        for shark in Shark.population:
            if shark != self and shark.isLookingForMate:
                self.reproduce(shark)

    
    def spreadDisease(self):
        if r.randint(0, 100) <= self.disease.danger and Shark.population.__len__() > 1:
            chosenShark = Shark.population[r.randint(0, Shark.population.__len__() - 1)]

            if chosenShark == self: chosenShark = Shark.population[r.randint(0, Shark.population.__len__() - 1)]

            chosenShark.disease = self.disease

            chosenShark.checkInfectionDeath()


    def reproduce(self, other):
        # The Funny Function™
        
        # Add genetics here
        self.isLookingForMate = False
        other.isLookingForMate = False

        self.reproduceLevel = 0
        other.reproduceLevel = 0

        newShark = Shark(self, other)
        # print(f"{newShark} has been birthed to sharks {self.ID} and {other.ID}")


    def searchForFood(self):
        if Fish.population.__len__() > 0 and self.hunger > -25:
            chosenFish = Fish.population[r.randint(0, Fish.population.__len__() - 1)]
            self.eat(chosenFish)


    def checkDeath(self):
        if self.hunger >= 100:
            self.die()


    def die(self):
        print(f"Shark {self.ID} has died\n")
        try:
            Shark.population.remove(self)
        except ValueError:
            pass

        del self

    
    def eat(self, prey):       
        if not prey.escapeShark(self):

            self.hunger -= (100 - prey.hunger)

            if prey.disease != None:
                self.inheritDisease(prey)

            prey.die()


    def inheritDisease(self, prey):
        self.disease = prey.disease
        self.checkInfectionDeath()

    
    def checkInfectionDeath(self):
        if r.randint(0, 100) <= self.disease.danger:
            self.die()


    def __repr__(self):
        return f"Shark {str(self.ID)} | Hunger: {self.hunger} | Reproduction: {self.reproduceLevel} | Disease: {self.disease} | Traits: {self.traits}"        


class Food:
    availableFood = []

    def __init__(self):
        self.value = r.randint(0, 10)
    
    @staticmethod
    def generateSupply(amount = 50):
        for i in range(amount):
            Food.availableFood.append(Food())


    @staticmethod
    def regenerateSupply():
        for i in range(r.randint(5, 10)):
            Food.availableFood.append(Food())

    
    def checkIfEaten(self):
        if r.randint(0, 10) >= 5:
            Food.availableFood.remove(self)
            del self


    def __repr__(self):
        return f"Food | Food Value: {self.value}"
        

class Disease:
    def __init__(self, fish):
        self.name = self.generateName()
        self.danger = r.randint(25, 100) # Higher means more dangerous
        # print(f"New Disease {self.name} has been created in fish {fish.ID}!!!!")


    def generateName(self):
        name = ""
        for i in range(97, 123):
            if r.randint(0, 10) >= 8:
                name += chr(i)
        return name


    def __repr__(self):
        return f"{self.name}, danger: {self.danger}"


class Generation:
    day = 0
    days = []
    FishPopulation = []
    avgFishGenetics = {"speed": [], "sense": []}
    avgSharkGenetics = {"speed": [], "sense": []}
    SharkPopulation = []
    food = []

    @staticmethod
    def updateLists():
        Generation.food.append(Food.availableFood.__len__())
        Generation.FishPopulation.append(Fish.population.__len__())

        Generation.avgFishGenetics["speed"].append(Generation.getAverage("speed", Fish))
        Generation.avgSharkGenetics["speed"].append(Generation.getAverage("speed", Shark))
        Generation.avgFishGenetics["sense"].append(Generation.getAverage("sense", Fish))
        Generation.avgSharkGenetics["sense"].append(Generation.getAverage("sense", Shark))

        Generation.SharkPopulation.append(Shark.population.__len__())
        Generation.days.append(Generation.day)

    @staticmethod
    def progressDay():
        Generation.day += 1

        print("\nDay: " + str(Generation.day) + "\n")
        Generation.updateLists()
        for fish in list(Fish.population):
            fish.update()

        for shark in list(Shark.population):
            shark.update()

        Food.regenerateSupply()

    @staticmethod
    def getAverage(trait, animal):
        # only does speed. update to do others.
        if trait == "speed" and animal.population.__len__() != 0:
                total = 0
                for a in animal.population:
                    total += a.traits.speed
                return total/animal.population.__len__()
        

class Traits:
    def __init__(self, animal):
        """
        For Fish

        Speed - Allows the fish to have a chance to escape sharks if they are faster than them
        Sense - Allows the fish to determine what food is most profitable to eat and which ones to avoid
        Cunning - Allows the fish to eat food faster than others
        Intelligence - Allows the fish to determine when they can afford not eating to give their food to starving fish
        Attractiveness - Allows the fish to be selected more often than others when fish are trying to reproduce.


        For Sharks

        Speed - Allows the shark to have a chance to eat the fish if they are faster than them
        Sense - Allows the shark to detect which fish has diseases and avoid them
        Cunning - Allows the shark to eat fish faster than others
        Intelligence - Allows the shark to not eat the fish if the fish population is low
        Attractiveness - Allows the shark to be selected more often than others when fish are trying to reproduce.

        """


        self.animal = animal

        if Generation.day == 0:
            if animal.__class__ == Shark:
                self.speed = r.randint(2, 102)
            else:
                self.speed = r.randint(0, 100)

            self.sense = r.randint(0, 100)
            self.cunning = r.randint(0, 100)
            self.intelligence = r.randint(0, 100)
            self.attractiveness = r.randint(0, 100)
        else:
            self.speed = self.getParentsTraits("speed")
            self.sense = r.randint(0, 100)
            self.cunning = r.randint(0, 100)
            self.intelligence = r.randint(0, 100)
            self.attractiveness = r.randint(0, 100)

    
    def getParentsTraits(self, trait):
        # only does speed. update to do others.
        if trait == "speed":
            return (self.animal.parents[0].traits.speed + self.animal.parents[1].traits.speed) / 2
        elif trait == "sense":
            return (self.animal.parents[0].traits.sense + self.animal.parents[1].traits.speed) / 2
        else:
            return -1


    def __repr__(self):
        return f"{self.speed} speed, {self.sense} sense, {self.cunning} cunning, {self.intelligence} intelligence, {self.attractiveness} attractiveness"


class Plot:
    @staticmethod
    def all(show, food):
        plt.figure(1)
        plt.plot(Generation.days, Generation.FishPopulation, label="Fish Population")
        plt.plot(Generation.days, Generation.SharkPopulation, label="Shark Population")
        if food:
            plt.plot(Generation.days, Generation.food, label="Amount of Food")
        plt.legend(loc="upper right")
        plt.title("Summary")
        plt.ylabel("Number")
        plt.xlabel("Days")
        if show:
            plt.show()

    @staticmethod
    def traits(show):
        plt.figure(2)
        plt.plot(Generation.days, Generation.avgFishGenetics["speed"], label="Speed")
        plt.title("Average Fish Trait Level Over Days")
        plt.ylabel("Trait Level")
        plt.xlabel("Days")
        plt.legend(loc="upper left")

        plt.figure(3)
        plt.plot(Generation.days, Generation.avgSharkGenetics["speed"], label="Speed")
        plt.title("Average Shark Trait Level Over Days")
        plt.ylabel("Trait Level")
        plt.xlabel("Days")
        plt.legend(loc="upper left")
        if show:
            plt.show()

       

class Simulation:

    @staticmethod
    def ecosystem(fishAmount = 50, sharkAmount = 5, dayLimit = 100):
        plt.rcParams['animation.html'] = 'jshtml'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.suptitle("Shark and Fish Population over Days")
        plt.xlabel("Day")
        plt.ylabel("Population Number")
        fig.show()

        x = []
        y1 = []
        y2 = []

        fishPlot, = ax.plot(x, y1, color='b')
        sharkPlot, = ax.plot(x, y2, color='r')
        fishPlot.set_label("Fish Population")
        sharkPlot.set_label("Shark Population")

        for i in range(fishAmount):
            Fish()

        for i in range(sharkAmount):
            Shark()

        Food.generateSupply()

        while Fish.population.__len__() > 0 or Shark.population.__len__() > 0:
            Generation.progressDay()

            x.append(Generation.day)
            y1.append(Generation.FishPopulation[-1])
            y2.append(Generation.SharkPopulation[-1])

            fishPlot, = ax.plot(x, y1, color='b')
            sharkPlot, = ax.plot(x, y2, color='r')

            ax.legend()

            fig.canvas.draw()
            time.sleep(0.05)

            if Generation.day >= dayLimit:
                break

        Generation.updateLists()
        plt.show()
