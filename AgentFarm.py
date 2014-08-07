from Agent import Agent
from Agent import AgentMessageQuit
import sys
import MessageSystem

class WorkerBeeMessageProcessed:
    pass
    
class AgentFarmMessageAllDone:
    pass

class AgentFarmMessageQuit:
    pass
    
class WorkerBee(Agent):

    def __init__(self, aMessageProcessorFunction):
    
        Agent.__init__(self)
        self.messageProcessor = aMessageProcessorFunction
        
    def handle(self, aFromIdentifier, aMessage):
    
        self.messageProcessor(aMessage)
        
        MessageSystem.send(self.identifier, aFromIdentifier, WorkerBeeMessageProcessed())

class AgentFarm(Agent):

    def __init__(self, aMessageProcessorFunction, aAgentCount):
    
        Agent.__init__(self)
        
        self.agents = []
        
        self.processedCount = 0
        self.receivedCount = 0
        self.exitOnDone = False
        self.messageDataQueue = []
        self.agentIdentifierQueue = []
        
        for index in range(0, aAgentCount):
        
            agent= WorkerBee(aMessageProcessorFunction)
            self.agents = self.agents + [agent]
            self.agentIdentifierQueue += [agent.identifier]
            
    def handleShutdown(self):
    
        for agent in self.agents:
                
            MessageSystem.send(self.identifier, agent.identifier, AgentMessageQuit())
            
        MessageSystem.send(self.identifier, self.identifier, AgentMessageQuit())
            
    def handle(self, aFromIdentifier, aMessage):
    
        if (isinstance(aMessage, WorkerBeeMessageProcessed)):
        
            self.processedCount = self.processedCount + 1
            self.agentIdentifierQueue += [aFromIdentifier]
            
            self.assignNextMessage()
            
            if (self.exitOnDone and self.processedCount == self.receivedCount):
            
                self.handleShutdown()
                
        elif (isinstance(aMessage, AgentFarmMessageQuit)):
        
            self.handleShutdown()
            
        elif (isinstance(aMessage, AgentFarmMessageAllDone)):
        
            self.exitOnDone = True
            
        else:
        
            self.receivedCount = self.receivedCount + 1
            self.messageDataQueue += [aMessage]
            
            self.assignNextMessage()
            
    def assignNextMessage(self):
    
        if (len(self.agentIdentifierQueue) > 0 and len(self.messageDataQueue) > 0):
        
            message = self.messageDataQueue[0]
            self.messageDataQueue.pop(0)
            agentIdentifier= self.agentIdentifierQueue[0]
            self.agentIdentifierQueue.pop(0)
            MessageSystem.send(self.identifier, agentIdentifier, message)