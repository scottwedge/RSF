#Classe da camada de redes
from linkLayer import LinkLayer
import packet as pk 
from packet import Packet
from scipy.spatial import distance

class NetworkLayer(LinkLayer):
    def __init__ (self):
        pass

    def route_request(self, id_flood, origem, destino, nos_np):
        print("ENVIANDO O ROUTE REQUEST! ")
        pkt_flood = pk.Packet(id_flood,[-1],origem, destino)
        pkt_flood.set_flooding()
        super().enlace(nos_np, pkt_flood)
        pass        
    
    def route_response(self, pkt_flood, nos_np):
        print("ENVIANDO O ROUTE RESPONSE! ")
        id_flood_response = pkt_flood.id + 10000
        pkt_flood_response = pk.Packet(id_flood_response, [-1], pkt_flood.header[1], pkt_flood.header[0])
        pkt_flood_response.set_flooding()
        pkt_flood_response.set_flooding_response()
        super().enlace(nos_np, pkt_flood_response)
        pass

    def net_recieve(self, pkt_recieve, nos_np, no_recieve):
        print("-------NET RECEIVE-------")
        if pkt_recieve.id in nos_np[no_recieve].pkt_recebidos:
            print("------- JÁ RECEBI ESSE PACOTE -------")
        else:
            nos_np[no_recieve].pkt_recebidos.append(pkt_recieve.id)
            if pkt_recieve.flooding == 1:
                if pkt_recieve.header[1] == nos_np[no_recieve].id:
                    print("NET ----- FLOOD CHEGOU NO DESTINO")
                    tam_net_header = len(pkt_recieve.net_header)
                    next_address = pkt_recieve.net_header[tam_net_header-1]
                    for key in pkt_recieve.net_header:
                        if key is not nos_np[no_recieve].id:
                            nos_np[no_recieve].rotas[key] = next_address
                        
                    if pkt_recieve.flooding_response == 0:
                        self.route_response(pkt_recieve, nos_np)
                    
                else:
                    print("NET ----- ATUALIZANDO TABELA E REPASSANDO FLOOD")
                    tam_net_header = len(pkt_recieve.net_header)
                    next_address = pkt_recieve.net_header[tam_net_header-1]
                    for key in pkt_recieve.net_header:
                        if key is not nos_np[no_recieve].id:
                            nos_np[no_recieve].rotas[key] = next_address
                        
                    pkt_recieve.network_header(nos_np[no_recieve].id)
                    print("NETWORK HEADER ---> " + str(pkt_recieve.net_header))
                    pkt_recieve.mac_header.clear()
                    super().enlace(nos_np, pkt_recieve)
                    pass
                pass
            else:
                if pkt_recieve.header[1] == nos_np[no_recieve].id:
                    print("PACOTE " + str(pkt_recieve.id) + " DE DADOS ENTREGUE COM SUCESSO DO ROTEADOR --->" + str(pkt_recieve.header[0]) + "PARA O ROTEADOR --> " +str(nos_np[no_recieve].id))
                    nos_np[no_recieve].set_caminho(pkt_recieve.net_header)
                    pass
                else:
                    if pkt_recieve.header[1] in nos_np[no_recieve].rotas.keys():
                        print("NETWORK -------- TEM NA TABELA")
                        next_roteador = nos_np[no_recieve].rotas[pkt_recieve.header[1]]
                        pkt_recieve.mac_header.clear()
                        pkt_recieve.link_header([nos_np[no_recieve].id, next_roteador])
                        pkt_recieve.network_header(nos_np[no_recieve].id)
                        super().enlace(nos_np, pkt_recieve)
                        pass
                    else:
                        print("NETWORK -------- NÃO TEM NA TABELA")
                        id_flood = pkt_recieve.id + 20000
                        nos_np[no_recieve].route_request(id_flood, nos_np[no_recieve].id, pkt_recieve.header[1], nos_np)
                        print("NETWORK -------- DESCOBRI A ROTA")
                        next_roteador = nos_np[no_recieve].rotas[pkt_recieve.header[1]]
                        pkt_recieve.mac_header.clear()
                        pkt_recieve.link_header([nos_np[no_recieve].id, next_roteador])
                        super().enlace(nos_np, pkt_recieve)
                        pass
        pass

    def net_send(self, pkt_send, nos_np, no_send):
        print("------ NET SEND ------")
        next_roteador = nos_np[no_send].rotas[pkt_send.header[1]]
        pkt_send.link_header([nos_np[no_send].id, next_roteador])
        super().enlace(nos_np, pkt_send)  
        pass
