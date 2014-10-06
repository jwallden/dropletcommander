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
        pos = QtGui.QCursor.pos()
        pos.setX(pos.x() + 10)
        print(self.treeDroplets.currentItem().child(1).text(0))
        if self.treeDroplets.currentItem().child(1).text(0) == "Status: active":
            self.context_menu.actions()[0].setEnabled(False)
        else:
            self.context_menu.actions()[0].setEnabled(True)
        self.context_menu.exec_(pos)

    def get_droplet_id(self):
        item = self.treeDroplets.currentItem()
        print(item)
        if not item.parent():
            id = item.child(0).text(0)
            #We want only the droplet ID. So, cut off the label.
            id = id[4:]
            print(id)
            return id

    def start_droplet(self):
        id = str(self.get_droplet_id())
        print("Starting " + self.get_droplet_id())
        for droplet in DropletCommander.manager.get_all_droplets():
            if str(droplet.id) == id:
                droplet.power_on()
                print("Reloading tree")
                #TODO check status and update when started
                self.reload_droplet_tree()
        print("DONE starting " + id)

    def stop_droplet(self):
        id = str(self.get_droplet_id())
        print("STOPPING " + id)
        for droplet in DropletCommander.manager.get_all_droplets():
            if str(droplet.id) == id:
                print("Trying power_off")
                print(droplet.power_off()["action"]["type"])
                #for action in droplet.get_actions():
                #    if action.type == "power_off":
                #        print("found action power_off")
                #        while str(action.status) != str("completed"):
                #            pass
                print("Reloading tree")
                self.reload_droplet_tree()
        print("DONE stopping " + id)

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