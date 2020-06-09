import FreeCAD as App
import FreeCADGui as Gui
import Part
import math as Math

from pivy.coin import *
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide

class MerziLinie:
    """This class will create a line after the user clicked 2 points on the screen"""

    def Activated(self):
        # neue Datei erzeugen wenn nicht vorhanden
        if not(App.ActiveDocument):
            #Create new document
            App.newDocument("merzi")
            App.setActiveDocument("merzi")
            App.ActiveDocument=App.getDocument("merzi")
            Gui.ActiveDocument=Gui.getDocument("merzi")
            
        self.view = Gui.ActiveDocument.ActiveView
        self.stack = []
        self.callback = self.view.addEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.getpoint) 
        
    def getpoint(self,event_cb):
        event = event_cb.getEvent()
        if event.getState() == SoMouseButtonEvent.DOWN:
            pos = event.getPosition()
            point = self.view.getPoint(pos[0],pos[1])
            self.stack.append(point)
            if len(self.stack) == 2:
                l = Part.LineSegment(self.stack[0],self.stack[1])
                shape = l.toShape()
                Part.show(shape)
                self.view.removeEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.callback)
    def GetResources(self): 
        return {'MenuText': 'Line', 'ToolTip': 'Creates a line by clicking 2 points on the screen'} 
        
class makeKugellager:

    def Activated(self):
        # neue Datei erzeugen wenn nicht vorhanden
        if not(App.ActiveDocument):
            #Create new document
            App.newDocument("merzi")
            App.setActiveDocument("merzi")
            App.ActiveDocument=App.getDocument("merzi")
            Gui.ActiveDocument=Gui.getDocument("merzi")
            
        # Aufruf Funktion
        self.callback = self.KugellagerZeichnen()


    def GetResources(self): 
        return {'MenuText': 'Kugellager', 'ToolTip': '...'} 

    def KugellagerZeichnen(self):
    
    
        #VALUES#
        #(radius of shaft/inner radius of inner ring)
        R1=15.0
        #(outer radius of inner ring)
        R2=25.0
        #(inner radius of outer ring)
        R3=30.0
        #(outer radius of outer ring)
        R4=40.0
        #(thickness of bearing)
        TH=15.0
        #(number of balls)
        NBall=15
        #(radius of ball)
        RBall=5.0
        #(rounding radius for fillets)
        RR=1
        #first coordinate of center of ball
        CBall=((R3-R2)/2)+R2
        #second coordinate of center of ball
        PBall=TH/2
        #Inner Ring#
        #Inner Ring#
        #B1=Part.makeCylinder(R1,TH)
        cyOuterRingCut = App.ActiveDocument.addObject("Part::Cylinder","cyOuterRingCut")
        cyOuterRingCut.Radius=R1
        cyOuterRingCut.Height=TH     
        
        #B2=Part.makeCylinder(R2,TH)
        cyOuterRing = App.ActiveDocument.addObject("Part::Cylinder","cyOuterRing")
        cyOuterRing.Radius=R2
        cyOuterRing.Height=TH
        #
        ### Begin command Part_Cut
        App.activeDocument().addObject("Part::Cut","cutOuterRing")
        App.activeDocument().cutOuterRing.Base = App.activeDocument().cyOuterRing
        App.activeDocument().cutOuterRing.Tool = App.activeDocument().cyOuterRingCut
        Gui.activeDocument().cyOuterRing.Visibility=False
        Gui.activeDocument().cyOuterRingCut.Visibility=False
        App.getDocument('merzi').getObject('cutOuterRing').ViewObject.ShapeColor=getattr(App.getDocument('merzi').getObject('cyOuterRing').getLinkedObject(True).ViewObject,'ShapeColor',App.getDocument('merzi').getObject('cutOuterRing').ViewObject.ShapeColor)
        App.getDocument('merzi').getObject('cutOuterRing').ViewObject.DisplayMode=getattr(App.getDocument('merzi').getObject('cyOuterRing').getLinkedObject(True).ViewObject,'DisplayMode',App.getDocument('merzi').getObject('cutOuterRing').ViewObject.DisplayMode)
        App.ActiveDocument.recompute()
        ### End command Part_Cut
        
        # *** #get edges and apply fillets
        # *** Bedges=IR.Edges
        # *** IRF=IR.makeFillet(RR,Bedges)
        # *** #create groove and show shape
        # *** T1=Part.makeTorus(CBall,RBall)
        # *** T1.translate(App.Vector(0,0,TH/2))
        # *** InnerRing=IRF.cut(T1)
        # *** Part.show(InnerRing)
        # *** #
        # *** #Outer Ring#
        # *** B3=Part.makeCylinder(R3,TH)
        # *** B4=Part.makeCylinder(R4,TH)
        # *** OR=B4.cut(B3)
        # *** #get edges and apply fillets
        # *** Bedges=OR.Edges
        # *** ORF=OR.makeFillet(RR,Bedges)
        # *** #create groove and show shape
        # *** T2=Part.makeTorus(CBall,RBall)
        # *** T2.translate(App.Vector(0,0,TH/2))
        # *** OuterRing=ORF.cut(T2)
        # *** Part.show(OuterRing)
        # *** #
        # *** #Balls#
        # *** for i in range(NBall):
        # ***     Ball=Part.makeSphere(RBall)
        # ***     Alpha=(i*2*Math.pi)/NBall
        # ***     BV=(CBall*Math.cos(Alpha),CBall*Math.sin(Alpha),TH/2)
        # ***     Ball.translate(BV)
        # ***     Part.show(Ball)
        # *** #
        #Make it pretty#
        Gui.SendMsgToActiveView("ViewFit")
        #
        
        
# *** class makeBalken:
# *** 
# ***     def Activated(self):
# ***         # neue Datei erzeugen wenn nicht vorhanden
# ***         if not(App.ActiveDocument):
# ***             #Create new document
# ***             App.newDocument("merzi")
# ***             App.setActiveDocument("merzi")
# ***             App.ActiveDocument=App.getDocument("merzi")
# ***             Gui.ActiveDocument=Gui.getDocument("merzi")
# ***             
# ***         # Aufruf Funktion
# ***         self.callback = self.Balken()
# *** 
# *** 
# ***     def GetResources(self): 
# ***         return {'MenuText': 'Kugellager', 'ToolTip': '...'} 
# *** 
# ***     def Balken(self):
# ***         # START Balken
# ***         objBalken=App.ActiveDocument.addObject("Part::Box","Balken")
# ***         objBalken.Length = 20
# ***         objBalken.Label = "Balken"
# ***         # END Balken
# ***         # Anzeige
# ***         App.ActiveDocument.recompute()
# ***         Gui.SendMsgToActiveView("ViewFit")
        
Gui.addCommand('MerziLinie', MerziLinie())   
Gui.addCommand('Kugellager', makeKugellager())     
# Gui.addCommand('Balken', makeBalken())