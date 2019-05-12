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
import matplotlib.pyplot as plt

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
            
def connectpoints(x,y,p1,p2):
    x1, x2 = x[p1], x[p2]
    y1, y2 = y[p1], y[p2]
    plt.plot([x1,x2],[y1,y2],'k-',color='red')
    
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



list_posx = []
list_posy = []
list_id_nos = []
nos_np = np.array(nos)
for i in nos_np:
    log.info(str(i.pos))
    list_posx.append(i.pos[0])
    list_posy.append(i.pos[1])
    list_id_nos.append(str(i.id))


pkt1 = pk.Packet(0, [0,0,0], 3, 2)
#pkt1.link_header([0,1])
#pkt2 = pk.Packet(1, [0,0,1], 2, 1)
#pkt2.link_header([2,1])
#pkt3 = pk.Packet(2, [0,1,0], 0, 1)
#pkt3.link_header([0,1])

pkt =  [pkt1]

qt_pkts = len(pkt)
#print(qt_pkts)
pkt_enviado = []

print("PLT PLOT")
print(nos_np[1].pos[0],nos_np[1].pos[1])
#ax = plt.plot(list_posx,list_posy,'ro')
 
fig, ax = plt.subplots()
ax.scatter(list_posx, list_posy,100)

for i,txt in enumerate(list_id_nos):
    ax.annotate(txt,(list_posx[i]+0.02,list_posy[i]+0.02),color='blue')
    

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
            #for n in pkt[0].net_header:
                #connectpoints(list_posx,list_posy,n,n+1)
            while(len(pkt[0].net_header)-1):
                connectpoints(list_posx,list_posy,pkt[0].net_header[0],pkt[0].net_header[1])
                pkt[0].net_header.pop(0)
            connectpoints(list_posx,list_posy,pkt[0].net_header[0],pkt[0].header[1])
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
