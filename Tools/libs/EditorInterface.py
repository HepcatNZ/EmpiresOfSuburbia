
class Interfacer:
    def __init__(self,win_editor,win_panda):
        self.editor = win_editor
        print self.editor
        self.panda = win_panda

    def add_tower(self,tower):
        name = tower.get_name()
        self.editor.ls_towers.append([name])

    def add_army(self,army):
        pass