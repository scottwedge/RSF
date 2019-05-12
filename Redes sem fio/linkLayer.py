#Classe da camada de enlace
from physicalLayer import PhysicalLayer
import packet as pk 
from packet import Packet
from scipy.spatial import distance

class LinkLayer(PhysicalLayer):

    def __init__ (self):
        pass

    def enlace(self, nos_np, pkt):
        pkt_enviado = []
        enviaram = []
        while True:
            for i in nos_np:
                i.busy_tone = 0

            count = 0
            for i in nos_np:
                if distance.seuclidean(self.pos, i.pos, [1, 1]) == 1:
                    if enviaram.count(i):
                        count+=1
                    else:
                        pkt_send = pk.Packet(pkt.id, pkt.content[:], pkt.header[0], pkt.header[1])
                        if pkt.flooding == 1:
                            pkt_send.set_flooding()
                        if pkt.flooding_response == 1:
                            pkt_send.set_flooding_response()
                        count += 1    
                        pkt_send.link_header([self.id, i.id])
                        nos_send = i
                        if nos_np[pkt_send.mac_header[0][0]].busy_tone == 0:
                            print("PKT MAC HEADER --> " + str(pkt_send.mac_header[0]))
                            no = nos_np[pkt_send.mac_header[0][0]].id 
                            #print("Nó = " + str(no) + " ----> Enviando pacote " + str(i.content))
                            enviou = nos_np[no].link_send(nos_send, pkt_send)
                            if enviou:
                                pkt_enviado.append(nos_send)
                                enviaram.append(nos_send)
                            else:
                                pkt_enviado.clear()
                        else:
                            print("BUSY TONE: " + str(nos_np[pkt_send.mac_header[0][0]].busy_tone))
            
            
            print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
            #print(str(pkt_enviado))
            for i in pkt_enviado:
                pkt_copia = pk.Packet(pkt.id, pkt.content[:], pkt.header[0], pkt.header[1])
                pkt_copia.link_header(pkt.mac_header[:])
                pkt_copia.net_header = pkt.net_header[:]
                if pkt.flooding == 1:
                    pkt_copia.set_flooding()
                if pkt.flooding_response == 1:
                    pkt_copia.set_flooding_response()
                i.recieve(pkt_copia, i.id, nos_np)
                i.busy_tone = 0
                #print("VIZINHOS: " + str(nos_np[pkt[i].mac_header[0][0]].vizinhos))
                #if len(nos_np[pkt.mac_header[0][0]].vizinhos):
                #    for j in nos_np[pkt.mac_header[0][0]].vizinhos:
                #        no_recieve = j
                #        nos_np[no_recieve].recieve(pkt, no_recieve,nos_np)
            #nos_np[pkt.mac_header[0][0]].busy_tone = 0   
            pkt_enviado.clear()
            #print("ENVIADOS ---> " + str(teste) + "  COUNT ---> " + count)
            if len(enviaram) == count:
                break



    def link_send(self, nos_send, pkt):
        ocupado = 0
        self.busy_tone = 1
        self.vizinhos.clear()
       
        if nos_send.busy_tone == 1:
            ocupado = 1
            self.vizinhos.clear()
        else:
            nos_send.busy_tone = 1
            self.vizinhos.append(nos_send.id)
        if ocupado:
            print("CANAL OCUPADO --- NÓ " + str(self.id) + " NÃO PODE ENVIAR PARA " + str(nos_send.id))
            return 0
        else:        
            for i in self.vizinhos:
                super().send(pkt, nos_send)
        #nos_np[no].vizinhos = super().send(pkt, nos_np)
        print("VIZINHOS " + str(self.vizinhos))
        return 1

    def link_recieve(self, nos_np, pkt, no_recieve):
        print("-------LINK RECIEVE-------")
        nos_np[no_recieve].busy_tone = 0
        nos_np[no_recieve].net_recieve(pkt, nos_np, no_recieve)
        