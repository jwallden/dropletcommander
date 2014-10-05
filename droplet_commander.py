#!/usr/bin/python

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import digitalocean
import sys
import dcui

main_ui = uic.loadUiType("DropletCommander.ui")[0]


class DropletCommander(QtWidgets.QMainWindow, main_ui):
    
    apikey = ""
    manager = ""

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        #self.ui = dcui.Ui_MainWindow()
        self.setupUi(self)
        self.btnSaveApiKey.clicked.connect(self.save_api_key)
        self.actionQuit.triggered.connect(self.quit)
        self.treeDroplets.expanded.connect(self.resizeColumnToContents)
        self.treeDroplets.collapsed.connect(self.resizeColumnToContents)
        self.treeDroplets.clicked.connect(self.copy_droplet_id)
        #Load the api key into the text box
        self.load_api_key()

        #Get DigitalOcean manager object
        DropletCommander.manager = digitalocean.Manager(token=DropletCommander.apikey)

        #Populate TreeWidget with droplet info
        self.list_droplets(DropletCommander.manager.get_all_droplets())

    def save_api_key(self):
        key = self.txtApiKey.text()
        if key:
            with open("apiKey.txt", "wt") as outfile:
                outfile.write(key)
            self.ustatusbar.showMessage("Api key saved")

    def load_api_key(self):
        try:
            with open("apiKey.txt", "rt") as infile:
                DropletCommander.apikey = infile.read()
                self.txtApiKey.setText(DropletCommander.apikey)
        except OSError:
            pass

    def list_droplets(self, droplets):
        items = []
        
        for droplet in droplets:
            item = QtWidgets.QTreeWidgetItem([droplet.name, droplet.ip_address,\
             droplet.region["name"]])
            
            item.addChild(QtWidgets.QTreeWidgetItem(["ID: " + str(droplet.id)]))
            item.addChild(QtWidgets.QTreeWidgetItem(["Status: " +\
               str(droplet.status)]))
            item.addChild(QtWidgets.QTreeWidgetItem(["Kernel: " +\
               str(droplet.kernel["name"])]))
            item.addChild(QtWidgets.QTreeWidgetItem(["RAM: " +\
                str(droplet.memory) + " Mb"]))
            item.addChild(QtWidgets.QTreeWidgetItem(["CPUs: " +\
               str(droplet.vcpus)]))
            item.addChild(QtWidgets.QTreeWidgetItem(["Disk: " +\
               str(droplet.disk) + " Gb"]))
            item.addChild(QtWidgets.QTreeWidgetItem(["Price monthly: " + "$" +\
               str(int(droplet.size["price_monthly"]))]))
            
            if droplet.status == "active":
                item.setIcon(0, QtGui.QIcon("res/ok.png"))
            else:
                item.setIcon(0, QtGui.QIcon("res/fail.png"))
            
            items.append(item)

        self.treeDroplets.addTopLevelItems(items)

        #Adapt IP address column to content 
        self.treeDroplets.resizeColumnToContents(1)

    def copy_droplet_id(self, hej):
        self.item = self.treeDroplets.currentItem()
        if not self.item.parent():
            self.id = self.item.child(0).text(0)
            self.id = self.id[4:]
            print(self.id)

    def resizeColumnToContents(self):
        self.treeDroplets.resizeColumnToContents(0)


    def quit(self):
        sys.exit(0)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DropletCommander()
    window.show()
    sys.exit(app.exec_())