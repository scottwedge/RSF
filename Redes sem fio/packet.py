# Classe de pacotes

class Packet(object): 
	# Atributos da classe (class atributes)
	# Construtor do objeto (initializer)
	

	#def __new__(cls, *args, **kwargs):
	#	obj = super(Packet,cls).__new__(cls)
	#    obj._from_base_class = type(obj) == Packet
    #    return obj

	def __init__(self, id, content, origem, destino):
		self.id = id
		self.content = content # Conteúdo do pacote (lista)
		self.mac_header = []
		self.net_header = [origem]
		self.header = [origem, destino]
		self.flooding = 0
		self.flooding_response = 0

	def link_header(self,dado):
		self.mac_header.append(dado)

	def network_header(self, net_header):
		self.net_header.append(net_header)
		
	def set_flooding(self):
		self.flooding = 1
	
	def set_flooding_response(self):
		self.flooding_response = 1
	
		