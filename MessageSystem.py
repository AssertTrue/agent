import threading

class PrivateMessageSystem(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.accessLock = threading.Lock()
        self.nextIdentifier = 1
        self.agents = dict()
        self.start()
        
    def send(self, aFromIdentifier, aToIdentifier, aMessage):
    
        agent = None
        
        with self.accessLock:
        
            if aToIdentifier in self.agents.keys():
            
                agent = self.agents[aToIdentifier]
                
        if not agent is None:
        
            agent._message(aFromIdentifier, aMessage)
                
    def register(self, aAgent):
    
        identifier= 0
        
        with self.accessLock:
        
            identifier = self.nextIdentifier
            self.nextIdentifier = self.nextIdentifier + 1
            self.agents[identifier] = aAgent
            
        return identifier
        
    def unregister(self, aId):
    
        with self.accessLock:
        
            if aId in self.agents.keys():
            
                del self.agents[aId]

messageSystem = PrivateMessageSystem()
        
def send(aFromIdentifier, aToIdentifier, aMessage):

    messageSystem.send(aFromIdentifier, aToIdentifier, aMessage)
    
def register(aAgent):

    return messageSystem.register(aAgent)
    
def unregister(aId):

    messageSystem.unregister(aId)