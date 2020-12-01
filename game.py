from bangtal import *

# Objects
class helpScreen(Object):
    def __init__(self, scene):
        super().__init__('image')
        self.locate(scene, 0, 0)

class actionsRemained(Object):
    def __init__(self, scene, x, y = 0):
        super().__init__('image')
        self.locate(scene, x, y)
        self.set(0)
        self.show()

    def set(self, n):
        self.n = n
        self.setImage('')

class gameObject(Object):
    def __init__(self, image, scene, i, j, objectType):
        super().__init__(image)
        self.locate(scene, *getLocation(i, j))
        self.show()
        self.scene = scene
        self.position = i, j
        self.objectType = objectType

    def move(self, i, j):
        self.position = i, j
        self.locate(self.scene, *getLocation(i, j))

class PLAYER(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/PLAYER/Player_Idle1.png', scene, i, j, 'PLAYER')

    # def move(self, i, j):
    #     self.position = i, j
    #     self.locate(self.scene, *getLocation(i, j))

    def kick(self):
        pass

class PROFESSOR(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/PROFESSOR/Professor_idle1.png', scene, i, j, 'PROFESSOR')

class KEY(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/KEY/Key1.png', scene, i, j, 'KEY')

class DOOR(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/DOOR/Door.png', scene, i, j, 'DOOR')

class DESK(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/DESK/Desk.png', scene, i, j, 'DESK')

class BOOKS(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/BOOKS/Book.png', scene, i, j, 'BOOKS')

    # def move(self, i, j):
    #     self.position = i, j
    #     self.locate(self.scene, *getLocation(i, j))
    
    def destroy(self):
        self.hide()

class SPIKE(gameObject):
    def __init__(self, scene, i, j, active):
        super().__init__('image/stage/SPIKE/Thorn.png', scene, i, j, 'SPIKE')
        self.active = active


# main
main = Scene('main', 'image/main/background.png')


# stage
def getLocation(i, j):
    return 350 + 65 * j, 560 - 65 * i

class Stage(Scene):
    # mapObjects = ['GROUND', 'WALL']
    # gameObjects = ['GROUND', 'WALL', 'PROFESSOR', 'KEY', 'DOOR', 'DESK', 'BOOKS', 'SPIKE_ACTIVE', 'SPIKE_INACTIVE', 'SPIKE_DESK']
    stageDetails = [
        {
            'currentStage': 1,
        },
        { # 1
            'object': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 0, 1, 1],
                [1, 1, 0, 0, 6, 0, 0, 1, 1],
                [1, 1, 0, 6, 0, 6, 1, 1, 1],
                [1, 0, 0, 1, 1, 1, 1, 1, 1],
                [1, 0, 5, 0, 0, 5, 0, 1, 1],
                [1, 0, 5, 0, 5, 0, 0, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            'player': (1, 6),
            'actions': 23,
            'SpikeAction': False,
        },
        { # 2
            'object': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 6, 1, 7, 7, 0, 0, 1],
                [1, 0, 7, 1, 1, 9, 9, 5, 1],
                [1, 0, 0, 1, 1, 0, 7, 0, 1],
                [1, 0, 0, 1, 1, 0, 6, 0, 1],
                [1, 1, 1, 1, 1, 2, 0, 6, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            'player': (5, 1),
            'actions': 24,
            'SpikeAction': False,
        },
    ]

    def __init__(self):
        super().__init__('stage', 'image/stage/background/1.png')
        self.objects = {
            'helpScreen': helpScreen(self),
            'actionsRemained': [actionsRemained(self, 100), actionsRemained(self, 200)],
            'objects': [],
            'player': PLAYER(self, 0, 0),
        }
        self.setStage(1)

    def setStage(self, n):
        if len(self.stageDetails) > n:
            self.stageDetails[0]['currentStage'] = n
            s = self.stageDetails[self.stageDetails[0]['currentStage']]
            o = s['object']
            self.setImage('image/stage/background/' + str(n) + '.png')
            self.objects['player'].move(*s['player'])
            for v in self.objects['objects']:
                v.hide()
                del v
            for i, v in enumerate(o):
                for j, x in enumerate(v):
                    x = o[i][j]
                    if x == 2:
                        self.objects['objects'].append(PROFESSOR(self, i, j))
                    elif x == 3:
                        self.objects['objects'].append(KEY(self, i, j))
                    elif x == 4:
                        self.objects['objects'].append(DOOR(self, i, j))
                    elif x == 5:
                        self.objects['objects'].append(DESK(self, i, j))
                    elif x == 6:
                        self.objects['objects'].append(BOOKS(self, i, j))
                    elif x == 7:
                        self.objects['objects'].append(SPIKE(self, i, j, True))
                    elif x == 8:
                        self.objects['objects'].append(SPIKE(self, i, j, False))
                    elif x == 9:
                        self.objects['objects'].append(SPIKE(self, i, j, True))
                        self.objects['objects'].append(DESK(self, i, j))

    def cleared(self):
        print('success')
        self.setStage(self.stageDetails[0]['currentStage'] + 1)

    def failed(self):
        print('failed')

    def getObjectIndex(self, i, j, objectType):
        for idx , v in enumerate(self.objects['objects']):
            if v.position == (i, j) and v.objectType == objectType:
                return idx
        return -1

    def getObjectNumber(self, i, j):
        o = self.stageDetails[self.stageDetails[0]['currentStage']]['object']
        if 0 < i <= len(o) and 0 < j <= len(o[0]):
            return o[i][j]
        else:
            return 1

    def action(self):
        c = self.stageDetails[0]['currentStage']
        a = self.stageDetails[c]['actions']
        self.stageDetails[c]['actions'] -= 1
        print(a)
        self.objects['actionsRemained'][0].set(a // 10)
        self.objects['actionsRemained'][1].set(a % 10)

    def move(self, di, dj):
        c = self.stageDetails[0]['currentStage']
        s = self.stageDetails[c]
        p = self.objects['player'].position
        # o = s['object']
        to = (p[0] + di, p[1] + dj)
        tt = (p[0] + 2 * di, p[1] + 2 * dj)
        
        if s['actions'] > 0:
            self.action()
            if s['SpikeAction']:
                # destroy books, reduce actions
                pass

            f = self.getObjectNumber(*to)
            ff = self.getObjectNumber(*tt)
            print(f, ff)

            if f == 0 or f == 7 or f == 8:
                self.stageDetails[c]['player'] = to
                self.objects['player'].move(*to)
            elif f == 1:
                pass
            elif f == 2:
                pass
            elif f == 3:
                pass
            elif f == 4:
                pass
            elif f == 5:
                d = self.getObjectIndex(*to, 'DESK')
                self.objects['player'].kick()
                if ff == 0:
                    self.stageDetails[c]['object'][to[0]][to[1]] = 0
                    self.stageDetails[c]['object'][tt[0]][tt[1]] = 5
                    self.objects['objects'][d].move(*tt)
                elif ff == 7 or ff == 8:
                    self.stageDetails[c]['object'][to[0]][to[1]] = 0
                    self.stageDetails[c]['object'][tt[0]][tt[1]] = 9
                    self.objects['objects'][d].move(*tt)
            elif f == 6:
                b = self.getObjectIndex(*to, 'BOOKS')
                self.stageDetails[c]['object'][to[0]][to[1]] = 0
                self.objects['player'].kick()
                if ff == 1:
                    self.objects['objects'][b].destroy()
                elif ff == 7:                    
                    self.objects['objects'][b].move(*tt)
                    self.objects['objects'][b].destroy()
                else:
                    self.stageDetails[c]['object'][tt[0]][tt[1]] = 6
                    self.objects['objects'][b].move(*tt)
            elif f == 9:
                d = self.getObjectIndex(*to, 'DESK')
                k = self.getObjectIndex(*to, 'SPIKE')
                self.objects['player'].kick()
                if ff == 0:
                    self.stageDetails[c]['object'][to[0]][to[1]] = 8 - self.objects['objects'][k].active
                    self.stageDetails[c]['object'][tt[0]][tt[1]] = 5
                    self.objects['objects'][d].move(*tt)
                elif ff == 7 or ff == 8:
                    self.stageDetails[c]['object'][to[0]][to[1]] = 0
                    self.stageDetails[c]['object'][tt[0]][tt[1]] = 9
                    self.objects['objects'][d].move(*tt)

            r = self.objects['player'].position
            if self.getObjectNumber(r[0] + 1, r[1]) == 2 or self.getObjectNumber(r[0] - 1, r[1]) == 2 or self.getObjectNumber(r[0], r[1] + 1) == 2 or self.getObjectNumber(r[0], r[1] - 1) == 2:
                self.cleared()
            elif self.getObjectNumber(*r) == 7:
                self.action()

        else:
            self.failed()

    def onKeyboard(self, key, pressed):
        if pressed:
            if key == 23 or key == 84:
                self.move(-1, 0)
            elif key == 1 or key == 82:
                self.move(0, -1)
            elif key == 19 or key == 85:
                self.move(1, 0)
            elif key == 4 or key == 83:
                self.move(0, 1)

stage = Stage()

# start game
setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
startGame(stage)