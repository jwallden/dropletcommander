#!/usr/bin/python

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import digitalocean
import sys
import time

main_ui = uic.loadUiType("DropletCommander.ui")[0]


class DropletCommander(QtWidgets.QMainWindow, main_ui):
    
    apikey = ""
    manager = ""

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        
        #Setup signal and slots
        self.setupUi(self)
        self.btnSaveApiKey.clicked.connect(self.save_api_key)
        self.treeDroplets.expanded.connect(self.resizeColumnToContents)
        self.treeDroplets.collapsed.connect(self.resizeColumnToContents)
        self.treeDroplets.customContextMenuRequested.connect(self.show_context_menu)
        self.btnRefresh.clicked.connect(self.reload_droplet_tree)
        self.btnId.clicked.connect(self.get_droplet_id)
        self.actionQuit.triggered.connect(self.quit)
        self.actionStart.triggered.connect(self.start_droplet)
        self.actionStop.triggered.connect(self.stop_droplet)
        self.actionReboot.triggered.connect(self.reboot_droplet)


        #Setup context menu for the droplets
        self.context_menu = QtWidgets.QMenu()
        self.context_menu.addAction(self.actionStart)
        self.context_menu.addAction(self.actionStop)
        self.context_menu.addAction(self.actionReboot)

        #Load the api key into the text box
        self.load_api_key()

        #Get DigitalOcean manager object
        self.get_manager()

        #Populate TreeWidget with droplet info
        self.list_droplets(DropletCommander.manager.get_all_droplets())

    def get_manager(self):
        
        DropletCommander.manager = digitalocean.Manager(token=DropletCommander.apikey)

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

    def reload_droplet_tree(self):
        self.treeDroplets.clear()
        self.list_droplets(DropletCommander.manager.get_all_droplets())

    def show_context_menu(self, pos):
        item = self.treeDroplets.currentItem()

        #Don't show context menu if a subitem is clicked.
        if not item.parent():
            pos = QtGui.QCursor.pos()
            pos.setX(pos.x() + 10)
            if item.child(1).text(0) == "Status: active":
                self.context_menu.actions()[0].setEnabled(False)
            else:
                self.context_menu.actions()[0].setEnabled(True)
            self.context_menu.exec_(pos)

    def get_droplet_id(self):
        item = self.treeDroplets.currentItem()
        if not item.parent():
            id = item.child(0).text(0)
            #We want only the droplet ID. So, cut off the label.
            id = id[4:]
            print(id)
            return id

    def start_droplet(self):
        self.treeDroplets.setCursor(QtCore.Qt.BusyCursor)
        try:
            id = str(self.get_droplet_id())
            print("Starting " + id)
            droplet = DropletCommander.manager.get_droplet(id)
            #Power on the droplet and record the action id
            actionid = droplet.power_on()['action']['id']
            action = DropletCommander.manager.get_action(actionid)
            timenow = time.time()
            timepassed = 0
            timeout = False

            while (str(action.status) != "completed" and timepassed <= 15):
                action.load()
                timepassed = time.time() - timenow
                if timepassed >= 15:
                    timeout = True

            self.reload_droplet_tree()
            if timeout:
                msgbox = QtWidgets.QMessageBox()
                msgbox.setIcon(3)
                msgbox.setText("The action timed out. Please refresh the droplet list manually to check on droplet status")
                msgbox.exec_()


        except Exception as e:
            print(e)
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(3)
            msgbox.setText("Something went wrong")
            msgbox.exec_()
        
        self.treeDroplets.unsetCursor()

    def stop_droplet(self):
        self.treeDroplets.setCursor(QtCore.Qt.BusyCursor)
        id = str(self.get_droplet_id())
        print("STOPPING " + id)
        droplet = DropletCommander.manager.get_droplet(id)
        
        actionid = droplet.power_off()["action"]["id"]
        action = DropletCommander.manager.get_action(actionid)

        while str(action.status) != "completed":
            action.load()
            print(str(action.status))

        self.reload_droplet_tree()
        self.treeDroplets.unsetCursor()

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