from bangtal import *

# Objects
class helpScreen(Object):
    pass

class actionsRemained(Object):
    pass

class stageNumber(Object):
    pass

class mapObject(Object):
    def __init__(self, image, scene, x, y, shown = True, value = 0):
        super().__init__(image)
        self.locate(scene, x, y)
        if shown: self.show()
        self.value = value

class gameObject(Object):
    pass

class PLAYER(gameObject):
    pass

class PROFESSOR(gameObject):
    pass

class KEY(gameObject):
    pass

class DOOR(gameObject):
    pass

class DESK(gameObject):
    pass

class BOOKS(gameObject):
    pass

class FRIEND(gameObject):
    pass



# main
main = Scene('main', 'image/main/background.png')

# stage
def getLocation(i, j):
    pass

class Stage(Scene):
    mapObjects = ['GROUND', 'WALL', '']
    gameObjects = ['AIR', 'PLAYER', 'PROFESSOR', 'KEY', 'DOOR', 'DESK', 'BOOKS', 'FRIEND', 'FRIEND_ACTIVE', 'FIREND_DESK']
    stageDetails = [
        { # Tutorial
        },
        { # 1
            'map': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 1, 1, 1],
                [1, 0, 0, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            'object': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 6, 0, 0, 0, 0],
                [0, 0, 0, 6, 0, 6, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 5, 0, 0, 5, 0, 0, 0],
                [0, 0, 5, 0, 5, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            'actions': 23,
            'friendAction': False,
        },
    ]

    def __init__(self):
        # Scene('stage', 'image/stage/background.png')
        pass

    def clear(self, n):
        pass

    def setStage(self, n):
        pass

    def onKeyboard(self, key, pressed):
        pass

stage = Stage()

# start game
setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
startGame(main)