from bangtal import *
import copy

# Objects


class clearScreen(Object):
    def __init__(self, scene):
        super().__init__('image/stage/clear.png')
        self.locate(scene, 355, 138)


class actionsRemained(Object):
    def __init__(self, scene, x, y=120):
        super().__init__('image/stage/n/x.png')
        self.locate(scene, x, y)
        self.set(0)
        self.show()

    def set(self, n):
        self.n = n
        self.setImage('image/stage/n/' + str(n) + '.png')


class button(Object):
    def __init__(self, scene, name, x, y):
        super().__init__('image/buttons/' + name + '.png')
        self.locate(scene, x, y)
        self.show()
        self.scene = scene


class button_back(button):
    def __init__(self, scene):
        super().__init__(scene, 'back', 700, 40)

    def onMouseAction(self, x, y, action):
        if action == MouseAction.CLICK:
            main.enter()


class button_exit(button):
    def __init__(self, scene):
        super().__init__(scene, 'exit', 867, 120)

    def onMouseAction(self, x, y, action):
        if action == MouseAction.CLICK:
            endGame()


class button_help(button):
    def __init__(self, scene):
        super().__init__(scene, 'help', 460, 120)

    def onMouseAction(self, x, y, action):
        if action == MouseAction.CLICK:
            helpScene.enter()


class button_main(button):
    def __init__(self, scene):
        super().__init__(scene, 'main', 460, 140)

    def onMouseAction(self, x, y, action):
        if action == MouseAction.CLICK:
            main.enter()


class button_next(button):
    def __init__(self, scene):
        super().__init__(scene, 'next', 460, 180)

    def onMouseAction(self, x, y, action):
        if action == MouseAction.CLICK:
            stage.setStage(stage.stageDetails[0]['currentStage'] + 1)


class button_start(button):
    def __init__(self, scene):
        super().__init__(scene, 'start', 71, 120)

    def onMouseAction(self, x, y, action):
        if action == MouseAction.CLICK:
            stage.setStage(1)
            stage.enter()


class gameObject(Object):
    def __init__(self, image, scene, i, j, objectType):
        super().__init__(image)
        self.locate(scene, *getLocation(i, j))
        self.show()
        self.scene = scene
        self.position = i, j
        self.objectType = objectType
        self.speed_animation = 0.15

    def move(self, i, j):
        self.position = i, j
        self.locate(self.scene, *getLocation(i, j))


class PLAYER(gameObject):
    def __init__(self, scene, i, j):
        self.direction = ['Right', 'Left']
        self.dir = 0
        super().__init__('image/stage/PLAYER/Player_Idle1_' + self.get_direct() + '.png', scene, i, j, 'PLAYER')
        self.animate()

    # animation code complete
    def animate(self):
        timer = Timer(self.speed_animation)
        self.src_count = 1
        def timer_timeout():
            self.setImage('image/stage/PLAYER/Player_Idle'+str(self.src_count)+'_'+self.get_direct() + '.png')
            if self.src_count >= 3:
                self.src_count = 1
            else:
                self.src_count += 1
            timer.set(self.speed_animation)
            timer.start()
        timer.onTimeout = timer_timeout
        timer.start()

    # animation code ongoing (not complete)
    def move(self, p_i, p_j, i, j, d):
        super().move(i, j)
        #print(self.position)
        #print(getLocation(*self.position))
        #print(getLocation(i, j))
        self.set_direct(d)
        print(p_i, p_j, i, j, self.direction[self.dir])


    # animation code ongoing
    def kick(self):
        timer = Timer(self.speed_animation-0.14)
        self.src_count_kick = 1
        def timer_timeout():
            self.setImage('image/stage/PLAYER/Player_Kick'+str(self.src_count_kick)+'_'+self.get_direct() +'.png')
            if self.src_count_kick >= 3:
                self.src_count_kick = 1
                self.setImage('image/stage/PLAYER/Player_Idle1_'+self.get_direct() +'.png')
            else:
                self.src_count_kick += 1
                timer.set(self.speed_animation)
                timer.start()
        timer.onTimeout = timer_timeout
        timer.start()

    def fail(self):
        # async
        # animation code here
        timer = Timer(self.speed_animation)
        self.src_count_fail = 1
        def timer_timeout():
            self.setImage('image/stage/PLAYER/Player_Over'+str(self.src_count)+'_'+self.get_direct() +'.png')
            if self.src_count >= 5:
                self.src_count = 1
                return
            else:
                self.src_count += 1
                timer.set(self.speed_animation)
                timer.start()
        timer.onTimeout = timer_timeout
        timer.start()

    # change right and left
    def change_direct(self):
        if self.dir == 0:
            self.dir = 1
        elif self.dir == 1:
            self.dir = 0
        else:
            print("error: value of direct not in range")
    
    # set right and left
    def set_direct(self, d):
        if d == -1:
            self.dir = 1
        elif d == 1:
            self.dir = 0
        else:
            pass

    def get_direct(self):
        return self.direction[self.dir]


class PROFESSOR(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/PROFESSOR/Professor_idle1.png', scene, i, j, 'PROFESSOR')
        self.animate()

    #animation code complete
    def animate(self):
        timer = Timer(self.speed_animation)
        self.src_count = 1
        def timer_timeout():
            self.setImage('image/stage/PROFESSOR/Professor_idle'+str(self.src_count)+'.png')
            if self.src_count >= 3:
                self.src_count = 1
            else:
                self.src_count += 1
            timer.set(self.speed_animation)
            timer.start()
        timer.onTimeout = timer_timeout
        timer.start()


class KEY(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/KEY/Key1.png', scene, i, j, 'KEY')


class DOOR(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/DOOR/Door.png', scene, i, j, 'DOOR')

    def open(self):
        self.hide()


class DESK(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/DESK/Desk.png', scene, i, j, 'DESK')


class BOOKS(gameObject):
    def __init__(self, scene, i, j):
        super().__init__('image/stage/BOOKS/Book.png', scene, i, j, 'BOOKS')
    
    # animation code ongoing (not work)
    def destroy(self):
        timer = Timer(self.speed_animation)
        self.src_count = 1
        def timer_timeout():
            self.setImage('image/stage/BOOKS/Book_Crash'+str(self.src_count)+'.png')
            if self.src_count >= 3:
                self.src_count = 1
            else:
                self.src_count += 1
                timer.set(self.speed_animation)
                timer.start()
        timer.onTimeout = timer_timeout
        timer.start()
        self.hide()


class SPIKE(gameObject):
    def __init__(self, scene, i, j, active):
        super().__init__('image/stage/SPIKE/Thorn.png', scene, i, j, 'SPIKE')
        self.active = active


# main
main = Scene('main', 'image/main/background.png')
_ = [button_start(main), button_help(main), button_exit(main)]

helpScene = Scene('help', 'image/help/background.png')
_ = button_back(helpScene)

ending = Scene('ending', 'image/ending/background.png')
_ = button_main(ending)

# stage


def getLocation(i, j):
    return 350 + 65 * j, 560 - 65 * i


class Stage(Scene):
    # gameObjects = ['GROUND', 'WALL', 'PROFESSOR', 'KEY', 'DOOR', 'DESK', 'BOOKS', 'SPIKE_ACTIVE', 'SPIKE_INACTIVE', 'SPIKE_DESK']
    stageDetails = [
        {
            'currentStage': 1,
            'keysInHand': 0,
        },
        {  # 1
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
        {  # 2
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
        {  # 3
            'object': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 2, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 4, 1],
                [1, 1, 1, 0, 7, 7, 0, 0, 0],
                [1, 1, 1, 7, 1, 7, 1, 0, 0],
                [1, 1, 1, 0, 0, 6, 7, 7, 1],
                [1, 3, 1, 7, 1, 7, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 6, 0, 1],
            ],
            'player': (3, 8),
            'actions': 32,
            'SpikeAction': False,
        },
        {  # 4
            'object': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 3, 0, 5, 1, 1, 1, 1],
                [0, 5, 7, 9, 0, 4, 0, 1, 1],
                [5, 0, 5, 0, 5, 5, 0, 2, 1],
                [0, 5, 0, 5, 0, 5, 5, 0, 1],
                [1, 0, 5, 0, 5, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            'player': (2, 0),
            'actions': 23,
            'SpikeAction': False,
        },
    ]

    def __init__(self):
        super().__init__('stage', 'image/stage/background/1.png')
        self.objects = {
            'clearScreen': [clearScreen(self), button_next(self)],
            'actionsRemained': [actionsRemained(self, 75), actionsRemained(self, 132)],
            'objects': [],
            'player': PLAYER(self, 0, 0),
        }
        self.setStage(1)

    def setStage(self, n):
        for v in self.objects['clearScreen']:
            v.hide()
        self.keyBlocked = False
        if len(self.stageDetails) > n:
            self.stageDetails[0]['currentStage'] = n
            self.stageMap = copy.deepcopy(
                self.stageDetails[self.stageDetails[0]['currentStage']])
            s = self.stageMap
            o = s['object']
            self.setImage('image/stage/background/' + str(n) + '.png')
            self.action(0)
            self.stageDetails[0]['keysInHand'] = 0
            self.objects['player'].move(0, 0, *s['player'], 1)
            self.objects['player'].show()
            for _ in range(len(self.objects['objects'])):
                self.objects['objects'][-1].hide()
                del self.objects['objects'][-1]
            self.objects['objects'] = []
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
                        self.objects['objects'].append(
                            SPIKE(self, i, j, False))
                    elif x == 9:
                        self.objects['objects'].append(SPIKE(self, i, j, True))
                        self.objects['objects'].append(DESK(self, i, j))

        elif len(self.stageDetails) == n:
            ending.enter()

    def cleared(self):
        self.keyBlocked = True
        self.objects['player'].hide()
        for v in self.objects['objects']:
            v.hide()
            del v
        for v in self.objects['clearScreen']:
            v.show()

    def failed(self):
        self.objects['player'].fail()
        self.setStage(self.stageDetails[0]['currentStage'])

    def getObjectIndex(self, i, j, objectType):
        for idx, v in enumerate(self.objects['objects']):
            if v.position == (i, j) and v.objectType == objectType:
                return idx
        return -1

    def getObjectNumber(self, i, j):
        o = self.stageMap['object']
        if 0 <= i < len(o) and 0 <= j < len(o[0]):
            return o[i][j]
        else:
            return 1

    def action(self, n=1):
        self.stageMap['actions'] -= n
        a = self.stageMap['actions']
        self.objects['actionsRemained'][0].set(a // 10)
        self.objects['actionsRemained'][1].set(a % 10)

    def move(self, di, dj):
        # c = self.stageDetails[0]['currentStage']
        s = self.stageMap
        m = s['object']
        p = self.objects['player']
        o = self.objects['objects']

        # move have to previous position (fr variabel = from position)
        fr = p.position
        to = (p.position[0] + di, p.position[1] + dj)
        tt = (p.position[0] + 2 * di, p.position[1] + 2 * dj)

        if s['actions'] > 0:
            self.action()
            if s['SpikeAction']:
                # destroy books, reduce actions
                pass

            f = self.getObjectNumber(*to)
            ff = self.getObjectNumber(*tt)

            if f == 0 or f == 7 or f == 8:
                s['player'] = to
                p.move(*fr, *to, dj)
            elif f == 1:
                pass
            elif f == 2:
                pass
            elif f == 3:
                k = self.getObjectIndex(*to, 'KEY')
                s['player'] = to
                p.move(*fr, *to, dj)
                m[to[0]][to[1]] = 0
                o[k].pick()
                self.stageDetails[0]['keysInHand'] += 1
            elif f == 4:
                d = self.getObjectIndex(*to, 'DOOR')
                if self.stageDetails[0]['keysInHand']:
                    self.stageDetails[0]['keysInHand'] -= 1
                    o[d].open()
                    m[to[0]][to[1]] = 0
                    s['player'] = to
                    p.move(*fr, *to, dj)
            elif f == 5:
                d = self.getObjectIndex(*to, 'DESK')
                p.kick()
                if ff == 0:
                    m[to[0]][to[1]] = 0
                    m[tt[0]][tt[1]] = 5
                    o[d].move(*tt)
                elif ff == 7 or ff == 8:
                    m[to[0]][to[1]] = 0
                    m[tt[0]][tt[1]] = 9
                    o[d].move(*tt)
            elif f == 6:
                b = self.getObjectIndex(*to, 'BOOKS')
                m[to[0]][to[1]] = 0
                p.kick()
                if ff == 1:
                    o[b].destroy()
                elif ff == 7:
                    m[tt[0]][tt[1]] = 6
                    o[b].move(*tt)
                    o[b].destroy()
                else:
                    m[tt[0]][tt[1]] = 6
                    o[b].move(*tt)
            elif f == 9:
                d = self.getObjectIndex(*to, 'DESK')
                k = self.getObjectIndex(*to, 'SPIKE')
                p.kick()
                if ff == 0:
                    m[to[0]][to[1]] = 8 - o[k].active
                    m[tt[0]][tt[1]] = 5
                    o[d].move(*tt)
                elif ff == 7 or ff == 8:
                    m[to[0]][to[1]] = 0
                    m[tt[0]][tt[1]] = 9
                    o[d].move(*tt)

            r = p.position
            if self.getObjectNumber(r[0] + 1, r[1]) == 2 or self.getObjectNumber(r[0] - 1, r[1]) == 2 or self.getObjectNumber(r[0], r[1] + 1) == 2 or self.getObjectNumber(r[0], r[1] - 1) == 2:
                self.cleared()
            elif self.getObjectNumber(*r) == 7:
                self.action()

        else:
            self.failed()

    def onKeyboard(self, key, pressed):
        if pressed and not self.keyBlocked:
            if key == 23 or key == 84:
                self.move(-1, 0)
            elif key == 1 or key == 82:
                self.move(0, -1)
            elif key == 19 or key == 85:
                self.move(1, 0)
            elif key == 4 or key == 83:
                self.move(0, 1)
            elif key == 18:
                self.objects['player'].fail()
                self.setStage(self.stageDetails[0]['currentStage']) 


stage = Stage()

# start game
setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
startGame(main)
