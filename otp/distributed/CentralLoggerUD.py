from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class CentralLoggerUD(DistributedObjectGlobalUD):
	notify = DirectNotifyGlobal.directNotify.newCategory('CentralLoggerUD')

	def announceGenerate(self):
		DistributedObjectGlobalUD.announceGenerate(self)
		self.notify.setInfo(True)

	def sendMessage(self, category, description, sender, receiver):
		self.air.writeServerEventMessage(category, sender, receiver, description)
		self.notify.info('%s has reported someone of %s!' % (sender,category))

	def logAIGarbage(self):
		pass
