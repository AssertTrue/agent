from Agent import Agent
from Agent import AgentMessageQuit
from AgentFarm import AgentFarm
from AgentFarm import AgentFarmMessageAllDone
import MessageSystem

def doPrint(aMessage):
    
    print aMessage
    
farm = AgentFarm(doPrint, 3)
    
for i in range(0, 1000):

    MessageSystem.send(0, farm.identifier, "%d" % i)

MessageSystem.send(0, farm.identifier, AgentFarmMessageAllDone())
    
for i in range(0, 1000000):

    pass

    