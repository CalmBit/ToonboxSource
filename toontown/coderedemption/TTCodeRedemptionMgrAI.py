from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.catalog.CatalogItem import CatalogItem
from toontown.catalog.CatalogClothingItem import CatalogClothingItem
from toontown.coderedemption.TTCodeRedemptionConsts import *
from toontown.rpc.AwardManagerConsts import *
from toontown.toonbase import ToontownGlobals
from toontown.toon import ToonDNA
import time

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTCodeRedemptionMgrAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.notify.setInfo(True)
        self.failAttempts = 0
        self.notify.info("Creating code redeemer...")
        self.activeCodes = {'for-girls': (RedeemErrors.Success, CatalogClothingItem(1204, 0)),
                            'for-boys': (RedeemErrors.Success, CatalogClothingItem(1745, 0)),
                            'for-both': (RedeemErrors.Success, CatalogClothingItem(1785, 0)),
                            'for-none': (RedeemErrors.CodeIsInactive, CatalogClothingItem(1786, 0))}

    def giveAwardToToonResult(self, todo0, todo1):
        pass

    def redeemCode(self, context, code):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if self.failAttempts > MaxCodeAttempts:
            result = RedeemErrors.TooManyAttempts
            awardMgrResult = GiveAwardErrors.Success
            self.failAttempts = 0
        else:
            if code in self.activeCodes:
                result = self.activeCodes[code][0]
                awardMgrResult = GiveAwardErrors.Success
                if result == RedeemErrors.Success:
                    reward = self.activeCodes[code][1]
                    if len(av.mailboxContents) + len(av.onOrder) >= ToontownGlobals.MaxMailboxContents:
                        result = RedeemErrors.AwardCouldntBeGiven
                        awardMgrResult = GiveAwardErrors.FullMailbox
                    else:
                        limited = reward.reachedPurchaseLimit(av)
                        if reward.notOfferedTo(av):
                            result = RedeemErrors.AwardCouldntBeGiven
                            awardMgrResult = GiveAwardErrors.WrongGender
                        elif limited == 0:
                            reward.deliveryDate = int(time.time()/60)
                            av.onOrder.append(reward)
                            av.b_setDeliverySchedule(av.onOrder)
                        elif limited == 1:
                            result = RedeemErrors.AwardCouldntBeGiven
                            awardMgrResult = GiveAwardErrors.AlreadyInOrderedQueue
                        elif limited == 2:
                            result = RedeemErrors.AwardCouldntBeGiven
                            awardMgrResult = GiveAwardErrors.AlreadyInMailbox
                        elif limited == 3:
                            result = RedeemErrors.AwardCouldntBeGiven
                            awardMgrResult = GiveAwardErrors.AlreadyBeingWorn
                        elif limited == 4:
                            result = RedeemErrors.AwardCouldntBeGiven
                            awardMgrResult = GiveAwardErrors.AlreadyInCloset
            else:
                result = RedeemErrors.CodeDoesntExist
                awardMgrResult = GiveAwardErrors.Success
                self.failAttempts = self.failAttempts + 1
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, result, awardMgrResult])

    def redeemCodeAiToUd(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def redeemCodeResultUdToAi(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def redeemCodeResult(self, todo0, todo1, todo2):
        pass

