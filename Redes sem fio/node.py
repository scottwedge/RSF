#Classe de nós
from networkLayer import NetworkLayer

class Node(NetworkLayer):
	# Atributos da classe (class atributes)
	# Construtor do objeto (initializer)
	
	def __init__(self, id, posX, posY):
		self.id = id
		self.pos = [posX,posY]
		self.busy_tone = 0
		self.vizinhos = []
		self.rotas = {self.id : self.id}
		#self.rotas = {}
		self.pkt_recebidos = []

	def set_caminho(self, saltos):
		self.caminho = saltos
	
