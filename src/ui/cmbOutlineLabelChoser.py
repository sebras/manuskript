#!/usr/bin/env python
#--!-- coding: utf8 --!--
 
from qt import *
from enums import *

class cmbOutlineLabelChoser(QComboBox):
    
    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)
        self.activated[int].connect(self.submit)
        self._column = Outline.label.value
        self._index = None
        self._indexes = None
        self._updating = False
        
    def setModels(self, mdlLabels, mdlOutline):
        self.mdlLabels = mdlLabels
        self.mdlLabels.dataChanged.connect(self.updateItems)
        self.mdlOutline = mdlOutline
        self.mdlOutline.dataChanged.connect(self.update)
        self.updateItems()
        
    def updateItems(self):
        self.clear()
        for i in range(self.mdlLabels.rowCount()):
            item = self.mdlLabels.item(i, 0)
            if item:
                self.addItem(item.icon(),
                            item.text())
            
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
        
    def getLabel(self, index):
        item = index.internalPointer()
        label = item.data(self._column)
        if not label: 
            label = 0
        return int(label)
        
    def updateSelectedItem(self):
        
        if self._updating:
            return
        
        if self._index:
            label = self.getLabel(self._index)
            self.setCurrentIndex(label)
                
        elif self._indexes:
            labels = []
            same = True
            
            for i in self._indexes:
                labels.append(self.getLabel(i))
                
            for lbl in labels[1:]:
                if lbl != labels[0]:
                    same = False
                    break
            
            if same:
                self.setCurrentIndex(labels[0])
                
            else:
                self.setCurrentIndex(0)
        
        else:
            self.setCurrentIndex(0)
        
    def submit(self, idx):
        if self._index:
            self.mdlOutline.setData(self._index, self.currentIndex())
            
        elif self._indexes:
            self._updating = True
            for i in self._indexes:
                self.mdlOutline.setData(i, self.currentIndex())
            self._updating = False
            