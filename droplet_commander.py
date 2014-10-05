#!/usr/bin/python

from PyQt5 import QtCore, QtGui, QtWidgets
import digitalocean
import sys
import dcui

class DropletCommander(QtWidgets.QMainWindow):
    
    apikey = ""
    manager = ""

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = dcui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnSaveApiKey.clicked.connect(self.save_api_key)
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.treeDroplets.expanded.connect(self.resizeColumnToContents)
        self.ui.treeDroplets.collapsed.connect(self.resizeColumnToContents)
        self.ui.treeDroplets.clicked.connect(self.copy_droplet_id)
        #Load the api key into the text box
        self.load_api_key()

        #Get DigitalOcean manager object
        DropletCommander.manager = digitalocean.Manager(token=DropletCommander.apikey)

        #Populate TreeWidget with droplet info
        self.list_droplets(DropletCommander.manager.get_all_droplets())

    def save_api_key(self):
        key = self.ui.txtApiKey.text()
        if key:
            with open("apiKey.txt", "wt") as outfile:
                outfile.write(key)
            self.ui.statusbar.showMessage("Api key saved")

    def load_api_key(self):
        try:
            with open("apiKey.txt", "rt") as infile:
                DropletCommander.apikey = infile.read()
                self.ui.txtApiKey.setText(DropletCommander.apikey)
        except OSError:
            pass

    def list_droplets(self, droplets):
        items = []
        
        for droplet in droplets:
            item = QtWidgets.QTreeWidgetItem([ddroplet.name, droplet.ip_address,\
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

        self.ui.treeDroplets.addTopLevelItems(items)

        #Adapt IP address column to content 
        self.ui.treeDroplets.resizeColumnToContents(1)

    def copy_droplet_id(self, hej):
        self.item = self.ui.treeDroplets.currentItem()
        if not self.item.parent():
            self.id = self.item.child(0).text(0)
            self.id = self.id[4:]
            print(self.id)

    def resizeColumnToContents(self):
        self.ui.treeDroplets.resizeColumnToContents(0)


    def quit(self):
        sys.exit(0)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DropletCommander()
    window.show()
    sys.exit(app.exec_())