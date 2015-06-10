#!/usr/bin/env python
#--!-- coding: utf8 --!--
 



from qt import *
from enums import *

class cmbOutlinePersoChoser(QComboBox):
    
    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)
        self.activated[int].connect(self.submit)
        self._column = Outline.POV.value
        self._index = None
        self._indexes = None
        self._updating = False
        
    def setModels(self, mdlPersos, mdlOutline):
        self.mdlPersos = mdlPersos
        self.mdlPersos.dataChanged.connect(self.updateItems)
        self.mdlOutline = mdlOutline
        self.mdlOutline.dataChanged.connect(self.update)
        self.updateItems()
        
    def updateItems(self):
        self.clear()
        self.addItem("")
        for i in range(self.mdlPersos.rowCount()):
            try:
                self.addItem(self.mdlPersos.item(i, Perso.name.value).text(), self.mdlPersos.item(i, Perso.ID.value).text())
                self.setItemData(i+1, self.mdlPersos.item(i, Perso.name.value).text(), Qt.ToolTipRole)
            except:
                pass
            
        if self._index or self._indexes:
            self.updateSelectedItem()
        
    def setCurrentModelIndex(self, index):
        self._indexes = None
        if index.column() != self._column:
            index = index.sibling(index.row(), self._column)
        self._index = index
        self.updateSelectedItem()
            
    def setCurrentModelIndexes(self, indexes):
        self._indexes = []
        self._index = None
        
        for i in indexes:
            if i.isValid():
                if i.column() != self._column:
                    i = i.sibling(i.row(), self._column)
                self._indexes.append(i)
        
        self.updateSelectedItem()
        
    def update(self, topLeft, bottomRight):
        
        if self._updating:
            # We are currently putting data in the model, so no updates
            return
        
        if self._index:
            if topLeft.row() <= self._index.row() <= bottomRight.row():
                self.updateSelectedItem()
                
        elif self._indexes:
            update = False
            for i in self._indexes:
                if topLeft.row() <= i.row() <= bottomRight.row():
                    update = True
            if update:
                self.updateSelectedItem()
        
    def getPOV(self, index):
        item = index.internalPointer()
        POV = item.data(self._column)
        return POV
        
    def selectPOV(self, POV):
        idx = self.findData(POV)
        if idx != -1:
            self.setCurrentIndex(idx)
        else:
            self.setCurrentIndex(0)
        
    def updateSelectedItem(self, idx1=None, idx2=None):
        
        if self._updating:
            return
        
        if self._index:
            POV = self.getPOV(self._index)
            self.selectPOV(POV)
                
        elif self._indexes:
            POVs = []
            same = True
            
            for i in self._indexes:
                POVs.append(self.getPOV(i))
                
            for POV in POVs[1:]:
                if POV != POVs[0]:
                    same = False
                    break
            
            if same:
                self.selectPOV(POVs[0])
                
            else:
                self.setCurrentIndex(0)
        
        else:
            self.setCurrentIndex(0)
        
    def submit(self, idx):
        if self._index:
            self.mdlOutline.setData(self._index, self.currentData())
            
        elif self._indexes:
            self._updating = True
            for i in self._indexes:
                self.mdlOutline.setData(i, self.currentData())
            self._updating = False