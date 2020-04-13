#!/usr/bin/env python

# Author: Ryan Myers
# Models: Jeff Styers, Reagan Heller
#
# Last Updated: 2015-03-13
#
# This tutorial provides an example of creating a character
# and having it walk around on uneven terrain, as well
# as implementing a fully rotatable camera.
from gtts import gTTS
from playsound import playsound
import os
global playagain
playagain = True
import random
randomnum = list(range(65,90))

deletemp3 = True 
allfolder = os.listdir()
if deletemp3:
    for f in allfolder:
        if f[-3:] == 'mp3':
            os.remove(f)

def generatename():
    nm = ''
    for i in range(15):
        rd = chr(random.choice(randomnum))
        nm += rd
    nm += '.mp3'
    return nm

#allfilename = []





#-------------------------
import threading
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import CollideMask
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
import random
import sys
import os
import math
import time

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.10,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft,font = loader.loadFont("japanese.ttf"))

def addInstructions2(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.10,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft,font = loader.loadFont("THSarabunNew.ttf"))


def addInstructions3(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.10,
                        shadow=(0, 0, 0, 1), parent=base.a2dBottomRight,
                        pos=(-0.1, 1.8), align=TextNode.ARight,font = loader.loadFont("THSarabunNew.ttf"))



# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.10,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1),font = loader.loadFont("THSarabunNew.ttf"),)



class Allbox:
    def __init__(self):
        self.box = Actor("models/Box")
        self.box.reparentTo(render)
        self.box.setScale(.2)
        self.box.setPos(-102,0.3,-0.5)


class RoamingRalphDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)

        self.question = {1:{'qa':'猫はタイ語で何ですか？',
                            'ans':3,
                            'a1':'ไก่',
                            'a2':'หนู',
                            'a3':'แมว',
                            'a4':'ช้าง'},
                         2:{'qa':'あかはタイ語で何ですか？',
                            'ans':1,
                            'a1':'สีแดง',
                            'a2':'สีเหลือง',
                            'a3':'สีส้ม',
                            'a4':'สีดำ'}}
        self.currentqa = 1
        self.allfilename = []

        # Set the background color to black
        self.win.setClearColor((0, 0, 0, 1))

        # This is used to store which keys are currently pressed.
        self.keyMap = {
            "left": 0, "right": 0, "forward": 0, "cam-left": 0, "cam-right": 0}

        # Post the instructions
        #self.font = loader.loadFont("tahoma.ttf")
        self.title = addTitle("เกมฝึกภาษาญี่ปุ่น โดย ลุงวิศวกรจร้าา")
        self.qa = addInstructions(0.10, " ")
        self.a1 = addInstructions2(0.20, " ")
        self.a2 = addInstructions2(0.30, " ")
        self.a3 = addInstructions2(0.40, " ")
        self.a4 = addInstructions2(0.50, " ")

        # Set up the environment
        #
        # This environment model contains collision meshes.  If you look
        # in the egg file, you will see the following:
        #
        #    <Collide> { Polyset keep descend }
        #
        # This tag causes the following mesh to be converted to a collision
        # mesh -- a mesh which is optimized for collision, not rendering.
        # It also keeps the original mesh, so there are now two copies ---
        # one optimized for rendering, one for collisions.

        self.environ = loader.loadModel("models/world")
        self.environ.reparentTo(render)

        # Create the main character, Ralph

        ralphStartPos = self.environ.find("**/start_point").getPos()
        self.ralph = Actor("models/ralph",
                           {"run": "models/ralph-run",
                            "walk": "models/ralph-walk"})
        self.ralph.reparentTo(render)
        self.ralph.setScale(.2)
        self.ralph.setPos(ralphStartPos + (0, 0, 0.5))


        #for i in range(5):
        '''
        self.box = Actor("models/Box")
        self.box.reparentTo(render)
        self.box.setScale(.2)
        self.box.setPos(-102,0.3,-0.5)
        '''
        
        model = Allbox()
        self.box = model.box


        
        # Create a floater object, which floats 2 units above ralph.  We
        # use this as a target for the camera to look at.

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.ralph)
        self.floater.setZ(1.0)

        # Accept the control keys for movement and rotation

        self.accept("escape", sys.exit)
        self.accept("a", self.setKey, ["left", True])
        self.accept("d", self.setKey, ["right", True])
        self.accept("w", self.setKey, ["forward", True])
        #self.accept("a", self.setKey, ["cam-left", True])
        #self.accept("s", self.setKey, ["cam-right", True])
        self.accept("a-up", self.setKey, ["left", False])
        self.accept("d-up", self.setKey, ["right", False])
        self.accept("w-up", self.setKey, ["forward", False])
        #self.accept("a-up", self.setKey, ["cam-left", False])
        #self.accept("s-up", self.setKey, ["cam-right", False])
        

        
        self.accept('z', self.openBox)

        self.ans = 1



        self.accept('1', self.CheckResult,[1])
        self.accept('2', self.CheckResult,[2])
        self.accept('3', self.CheckResult,[3])
        self.accept('4', self.CheckResult,[4])




        taskMgr.add(self.move, "moveTask")

        # Game state variables
        self.isMoving = False

        # Set up the camera
        self.disableMouse()
        self.camera.setPos(self.ralph.getX(), self.ralph.getY() + 10, 2)

        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.
        self.cTrav = CollisionTraverser()
 
        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0, 0, 9)
        self.ralphGroundRay.setDirection(0, 0, -1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(CollideMask.bit(0))
        self.ralphGroundCol.setIntoCollideMask(CollideMask.allOff())
        self.ralphGroundColNp = self.ralph.attachNewNode(self.ralphGroundCol)
        self.ralphGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0, 0, 9)
        self.camGroundRay.setDirection(0, 0, -1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(CollideMask.bit(0))
        self.camGroundCol.setIntoCollideMask(CollideMask.allOff())
        self.camGroundColNp = self.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)

        # Uncomment this line to see the collision rays
        #self.ralphGroundColNp.show()
        #self.camGroundColNp.show()

        # Uncomment this line to show a visual representation of the
        # collisions occuring
        #self.cTrav.showCollisions(render)

        # Create some lighting

        
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection((-5, -5, -5))
        directionalLight.setColor((1, 1, 1, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))




        #Add Sound
        self.box_sound = loader.loadSfx("box.ogg")


        # Score
        self.score = 0
        self.a5 = addInstructions3(0.3, "Score: {}".format(self.score))
        self.playagain = True



    def speak(self,word):
        

        

        tts = gTTS(text= word, lang='ja')
        name = generatename()
        tts.save(name + '.mp3')
        playsound(name + '.mp3')
        
        


    # Records the state of the arrow keys
    def CheckResult(self,number):
               

        self.playsound = True
        current = self.question[self.currentqa]
        if number == self.question[self.currentqa]['ans']:
            self.score += 1
            self.a5.setText("Score: {}".format(self.score))
            selectqa = self.question[self.currentqa]
            if number == 1:
                self.a1.setText('[1] '+ selectqa['a1'] + ' O')
                self.a2.setText('[2] '+ selectqa['a2'])
                self.a3.setText('[3] '+ selectqa['a3'])
                self.a4.setText('[4] '+ selectqa['a4'])
            elif number == 2:
                self.a2.setText('[2] '+ selectqa['a2'] + ' O')
                self.a1.setText('[1] '+ selectqa['a1'])
                self.a3.setText('[3] '+ selectqa['a3'])
                self.a4.setText('[4] '+ selectqa['a4'])
            elif number == 3:
                self.a3.setText('[3] '+ selectqa['a3'] + ' O')
                self.a1.setText('[1] '+ selectqa['a1'])
                self.a2.setText('[2] '+ selectqa['a2'])
                self.a4.setText('[4] '+ selectqa['a4'])
            elif number == 4:
                self.a4.setText('[4] '+ selectqa['a4'] + ' O')
                self.a3.setText('[3] '+ selectqa['a3'])
                self.a2.setText('[2] '+ selectqa['a2'])
                self.a1.setText('[1] '+ selectqa['a1'])
            else:
                pass

            task1 = threading.Thread(target=self.speak,args=('はい、そうです。',))
            task1.start()
            self.closeBox()
            #self.speak('はい、そうです。')
        else:
            selectqa = self.question[self.currentqa]
            if number == 1:
                self.a1.setText('[1] '+ selectqa['a1'] + ' x')
                self.a2.setText('[2] '+ selectqa['a2'])
                self.a3.setText('[3] '+ selectqa['a3'])
                self.a4.setText('[4] '+ selectqa['a4'])
            elif number == 2:
                self.a2.setText('[2] '+ selectqa['a2'] + ' x')
                self.a1.setText('[1] '+ selectqa['a1'])
                self.a3.setText('[3] '+ selectqa['a3'])
                self.a4.setText('[4] '+ selectqa['a4'])
            elif number == 3:
                self.a3.setText('[3] '+ selectqa['a3'] + ' x')
                self.a1.setText('[1] '+ selectqa['a1'])
                self.a2.setText('[2] '+ selectqa['a2'])
                self.a4.setText('[4] '+ selectqa['a4'])
            elif number == 4:
                self.a4.setText('[4] '+ selectqa['a4'] + ' x')
                self.a3.setText('[3] '+ selectqa['a3'])
                self.a2.setText('[2] '+ selectqa['a2'])
                self.a1.setText('[1] '+ selectqa['a1'])
            else:
                pass
            task1 = threading.Thread(target=self.speak,args=('じゃないです。',))
            task1.start()
            self.closeBox()



    

    def setKey(self, key, value):
        self.keyMap[key] = value

    def openBox(self):
        print('CURRENT: ',self.allfilename)
        pry = self.ralph.getY()
        pby = self.box.getY()
        prx = self.ralph.getX()
        pbx = self.box.getX()

        check1 = prx < pbx + 1.5 and prx > pbx -1.5
        check2 = pry < pby + 1.5 and pry > pby -1.5

        print(prx-pbx,':',pry-pby)
        
        print(check1, check2)
        startpos = self.ralph.getPos()
        print(startpos,'BY', self.box.getY(),'BX', self.box.getX())
        def Play():
            tts = gTTS(text= selectqa['qa'], lang='ja')
            name = generatename()
            tts.save(name + '.mp3')
            playsound(name + '.mp3')

        if  check1 and check2:

            rdnum = list(range(1,3))
            number = random.choice(rdnum)
            selectqa = self.question[number]

            self.currentqa = number

            self.qa.setText('Question: '+ selectqa['qa'])
            self.a1.setText('[1] '+ selectqa['a1'])
            self.a2.setText('[2] '+ selectqa['a2'])
            self.a3.setText('[3] '+ selectqa['a3'])
            self.a4.setText('[4] '+ selectqa['a4'])
            self.box.play('openBox')
            self.box_sound.play()

            task1 = threading.Thread(target=Play)
            task1.start()
            
            
            
            # if self.playagain == True:
            #     name = generatename()
            #     self.allfilename.append(name)

            #     tts.save(name)
            #     self.playagain = False


            
            # if len(self.allfilename) > 1:
            #     os.remove(self.allfilename[0])
            #     del self.allfilename[0]
            # playsound(self.allfilename[0])

            

    def closeBox(self):
        self.box.play('closeBox')

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        if self.keyMap["cam-left"]:
            self.camera.setX(self.camera, -10 * dt)
        if self.keyMap["cam-right"]:
            self.camera.setX(self.camera, +10 * dt)

        # if base.mouseWatcherNode.hasMouse():
        #     mpos = base.mouseWatcherNode.getMouse()  # get the mouse position
        #     self.maze.setP(mpos.getY() * -10)
        #     self.maze.setR(mpos.getX() * 10)

        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()

            if mpos.getX() < -0.2 or mpos.getX() > 0.2:
                self.camera.setX(self.camera, mpos.getX() * -5 * dt)
                print('Mouse: ' ,mpos.getX())




        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.ralph.getPos()

        #print(startpos,'BY', self.box.getY(),'BX', self.box.getX())


        #self.title.setText('X: {:.3f} , Y: {:.3f}, Z: {:.3f}'.format(self.ralph.getX(),self.ralph.getY(),self.ralph.getZ()))

        # If a move-key is pressed, move ralph in the specified direction.

        if self.keyMap["left"]:
            self.ralph.setH(self.ralph.getH() + 200 * dt)
        if self.keyMap["right"]:
            self.ralph.setH(self.ralph.getH() - 200 * dt)
        if self.keyMap["forward"]:
            self.ralph.setY(self.ralph, -25 * dt)

        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if self.keyMap["forward"] or self.keyMap["left"] or self.keyMap["right"]:
            if self.isMoving is False:
                self.ralph.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.ralph.stop()
                self.ralph.pose("walk", 5)
                self.isMoving = False

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.ralph.getPos() - self.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if camdist > 10.0:
            self.camera.setPos(self.camera.getPos() + camvec * (camdist - 10))
            camdist = 10.0
        if camdist < 5.0:
            self.camera.setPos(self.camera.getPos() - camvec * (5 - camdist))
            camdist = 5.0

        # Normally, we would have to call traverse() to check for collisions.
        # However, the class ShowBase that we inherit from has a task to do
        # this for us, if we assign a CollisionTraverser to self.cTrav.
        #self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = list(self.ralphGroundHandler.getEntries())
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        if len(entries) > 0 and entries[0].getIntoNode().getName() == "terrain":
            self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.ralph.setPos(startpos)

        # Keep the camera at one foot above the terrain,
        # or two feet above ralph, whichever is greater.

        entries = list(self.camGroundHandler.getEntries())
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        if len(entries) > 0 and entries[0].getIntoNode().getName() == "terrain":
            self.camera.setZ(entries[0].getSurfacePoint(render).getZ() + 1.0)
        if self.camera.getZ() < self.ralph.getZ() + 2.0:
            self.camera.setZ(self.ralph.getZ() + 2.0)

        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        self.camera.lookAt(self.floater)

        return task.cont





demo = RoamingRalphDemo()
demo.run()
