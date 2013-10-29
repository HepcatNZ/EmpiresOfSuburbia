

class EconomyManager:
    def __init__(self,gold):
        self.tick_delay = 4.0

        self.gold = gold
        self.gold_inc = 0

        self.cost_army_gold = 25

        taskMgr.doMethodLater(self.tick_delay,self.task_resources, "updateResources")

    def task_resources(self,task):
        self.gold += self.gold_inc
        base.vis_manager.update()
        return task.again