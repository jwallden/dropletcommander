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
        self.actionStart.triggered.connect(self.start_droplet)
        self.actionStop.triggered.connect(self.stop_droplet)
        self.actionReboot.triggered.connect(self.reboot_droplet)


        

        self.treeDroplets.expanded.connect(self.resizeColumnToContents)
        self.treeDroplets.collapsed.connect(self.resizeColumnToContents)
        self.treeDroplets.customContextMenuRequested.connect(self.show_context_menu)
        
        #Setup context menu for the droplets
        self.context_menu = QtWidgets.QMenu()
        self.context_menu.addAction(self.actionStart)
        self.context_menu.addAction(self.actionStop)
        self.context_menu.addAction(self.actionReboot)

        #Load the api key into the text box
        self.load_api_key()

        #Get DigitalOcean manager object
        DropletCommander.manager = digitalocean.Manager(token=DropletCommander.apikey)

        #Populate TreeWidget with droplet info
        self.list_droplets(DropletCommander.manager.get_all_droplets())

    def get_manager(self):
        pass

    def save_api_key(self):
        key = self.txtApiKey.text()
        if key:
            with open("apiKey.txt", "wt") as outfile:
                outfile.write(key)
            self.statusbar.showMessage("Api key saved")

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

    def show_context_menu(self, pos):
        pos = QtGui.QCursor.pos()
        pos.setX(pos.x() + 10)
        print(self.treeDroplets.currentItem().child(1).text(0))
        if self.treeDroplets.currentItem().child(1).text(0) == "Status: active":
            self.context_menu.actions()[0].setEnabled(False)
        else:
            self.context_menu.actions()[0].setEnabled(True)
        self.context_menu.exec_(pos)

    def get_droplet_id(self):
        self.item = self.treeDroplets.currentItem()
        if not self.item.parent():
            self.id = self.item.child(0).text(0)
            #Get only the droplet ID. So, cut off the label.
            self.id = self.id[4:]
            #print(self.id)
            return self.id

    def start_droplet(self):
        print("Starting " + self.get_droplet_id())
        DropletCommander.manager.

    def stop_droplet(self):
        pass

    def reboot_droplet(self):
        pass


    def resizeColumnToContents(self):
        self.treeDroplets.resizeColumnToContents(0)


    def quit(self):
        sys.exit(0)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DropletCommander()
    window.show()
    sys.exit(app.exec_())