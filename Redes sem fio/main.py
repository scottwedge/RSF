'''
Trabalho de Redes sem fio
Prof: Fernando Menezes Matos
'''

import node as no
import packet as pk 
import physicalLayer as phy
import random
import numpy as np
import logging as log
from scipy.spatial import distance

log.basicConfig(filename='redes.log',filemode='w',level=log.DEBUG)

def GenerateNetwork(nodes,size, nos): # Função que cria a topologia da rede
    lista = []
    for i in range(nodes):
        while(True):
            rx = random.randint(0, size)
            ry = random.randint(0, size)
            r = [rx, ry]
            if r not in lista: 
                lista.append(r)
                nos.append(no.Node(i,rx,ry))
                break

nos = []
count = 0  
pacotes = []     
# Leitura de entrada de um arquivo
f = open("input.txt","r") # abre o arquivo input.txt em modo de leitura (read)
if f.mode == 'r':
    num_nos = f.readline()
    tamanho = f.readline()
    if f.readline() == "sim\n":
        for lines in f:
            if lines != "parou\n":
                #print(lines[0])
                nos.append(no.Node(count,int(lines[0]),int(lines[2])))
                count = count + 1
            else:
                break
'''           
        for linhas in f:
            print(linhas[4:])
            pacotes = pk.Packet(count,[linhas[4:]])
            pacotes.link_header([0,0])
'''
#nos = []

#GenerateNetwork(4,1, nos)

nos_np = np.array(nos)
for i in nos_np:
    log.info(str(i.pos))

pkt1 = pk.Packet(0, [0,0,0], 0, 1)
#pkt1.link_header([0,1])
pkt2 = pk.Packet(1, [0,0,1], 2, 1)
#pkt2.link_header([2,1])
pkt3 = pk.Packet(2, [0,1,0], 0, 1)
#pkt3.link_header([0,1])

pkt =  [pkt1, pkt2, pkt3]

qt_pkts = len(pkt)
#print(qt_pkts)
pkt_enviado = []

id_flood = 10000
tentativas = 0
while(True):
    if len(pkt):
        print("MAIN ---- TENTANDO ENVIAR PACOTE " + str(pkt[0].id))
        if pkt[0].header[1] in nos_np[pkt[0].header[0]].rotas.keys():
            print("MAIN ----TEM NA TABELA")
            nos_np[pkt[0].header[0]].pkt_recebidos.append(pkt[0].id)
            nos_np[pkt[0].header[0]].net_send(pkt[0], nos_np, nos_np[pkt[0].header[0]].id)
            pass
        else:
            print("MAIN ----NÃO TEM NA TABELA")
            nos_np[pkt[0].header[0]].pkt_recebidos.append(pkt[0].id)
            nos_np[pkt[0].header[0]].route_request(id_flood, pkt[0].header[0], pkt[0].header[1], nos_np)
            id_flood += 1
            pass
        if pkt[0].id in nos_np[pkt[0].header[1]].pkt_recebidos:
            print("MAIN ---- PACOTE " + str(pkt[0].id) + " ENVIADO COM SUCESSO")
            pkt.pop(0)
        else:
            tentativas += 1
        if tentativas == 10:
            print("MAIN ---- PACOTE " + str(pkt[0].id) + " NÃO CONSEGUIU ENTREGAR")
            pkt.pop(0)
            tentativas = 0
    else:
        break

for i in nos_np:
    print("\nTABELA DE ROTAS DO ROTEADOR " + str(i.id))
    print("DESTINO : PROXIMO ROTEADOR")
    for k, v in i.rotas.items():
        print(str(k) + "       : " + str(v))
        pass
    pass

'''
while(True):
    if len(pkt) != 0:
        for i in nos_np:
            i.busy_tone = 0
            pass
        count = 0
        for i in pkt:
            if nos_np[i.mac_header[0][0]].busy_tone == 0:
                no = nos_np[i.mac_header[0][0]].id 
                #print("Nó = " + str(no) + " ----> Enviando pacote " + str(i.content))
                enviou = nos_np[i.mac_header[0][0]].link_send(nos_np, i)
                if enviou:
                    pkt_enviado.append(count)
                    count+=1    
            else:
                print("BUSY TONE: " + str(nos_np[i.mac_header[0][0]].busy_tone))

        print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
        print(str(pkt_enviado))
        for i in pkt_enviado:
            #print("VIZINHOS: " + str(nos_np[pkt[i].mac_header[0][0]].vizinhos))
            if len(nos_np[pkt[i].mac_header[0][0]].vizinhos):
                for j in nos_np[pkt[i].mac_header[0][0]].vizinhos:
                    no_recieve = j
                    nos_np[no_recieve].recieve(pkt[i], no_recieve,nos_np)
    
            nos_np[pkt[i].mac_header[0][0]].busy_tone = 0
            pkt.pop(i)   
        pkt_enviado.clear()
    else:
        print("ENVIADO TODOS OS PACOTES")
        break
    pass
'''
#nos_np[0].send(pkt1, nos_np)
#nos_np[0].send_rts(1, 2, 1, 0,nos_np)
