from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTCodeRedemptionMgrAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.notify.setInfo(True)
        self.notify.info("Creating code redeemer...")

    def giveAwardToToonResult(self, todo0, todo1):
        pass

    def redeemCode(self, context, code):
        avId = self.air.getAvatarIdFromSender()
        if code == "this-code-works":
            result = 0
        else:
            result = 1
        awardMgrResult = 0
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, result, awardMgrResult])

    def redeemCodeAiToUd(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def redeemCodeResultUdToAi(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def redeemCodeResult(self, todo0, todo1, todo2):
        pass

