import threading
import MessageSystem

class AgentMessageQuit:
    pass
    
class MessageHeader:

    def __init__(self, aFromIdentifier, aMessage):
        
        self.fromIdentifier= aFromIdentifier
        self.message = aMessage
        
class Agent(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.agentAccessLock = threading.Lock()
        self.agentHandleLock = threading.Lock()
        self.doQuit = False
        self.messageQueue = []
        self.identifier = MessageSystem.register(self)
        self.start()
    
    def _message(self, aFromIdentifier, aMessage):
    
        with self.agentAccessLock:
        
            if (isinstance(aMessage, AgentMessageQuit)):
            
                self.doQuit = True
        
            else:
            
                self.messageQueue = self.messageQueue + [MessageHeader(aFromIdentifier, aMessage)]
        
    def _shuttingDown(self):
    
        with self.agentAccessLock:
            result = self.doQuit

        return result
        
    def _nextMessage(self):
    
        result = None
        
        with self.agentAccessLock:
        
            if len(self.messageQueue) > 0:
                
                result = self.messageQueue[0]
                self.messageQueue.pop(0)
        
        return result
        
    def handle(self, aFromIdentifier, aMessage):
    
        pass
    
    def run(self):
    
        while not self._shuttingDown():
        
            next = self._nextMessage()
            if next:
            
                with self.agentHandleLock:
                
                    self.handle(next.fromIdentifier, next.message)
                
        MessageSystem.unregister(self)