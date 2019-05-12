#Classe da camada física
import packet as pk
#import node as no
from numpy import linalg as LA
from scipy.spatial import distance
import logging as log

class PhysicalLayer():
    
    def __init__ (self):
        pass

    def send(self, packet, nos_send):
        log.info("Enviando pacote " +  str(packet.content))
        #print("Enviando pacote " +  str(packet.content))
        print("FISICA ---- Enviado do nó " + str(self.id) + " para o nó " + str(nos_send.id))
        

    def recieve(self, packet, no_recieve, nos_np):
        #print("Nó " + str(self.pos) + " recebeu o pacote " + str(packet.content))
        #no_recieve.link_recieve(packet, no_recieve, nos_np)
        print("FISICA ---- Nó " + str(self.id) + " recebeu o pacote " + str(packet.content))
        nos_np[no_recieve].link_recieve(nos_np, packet, no_recieve)
        pass
