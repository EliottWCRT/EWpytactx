import j2l.pytactx.agent as pytactx

agent = pytactx.AgentFrCibleAleatoire(
	nom=input("👾 id: "), 
	arene=input("🎲 arena: "), 
	username="demo",
	password=input("🔑 password: "), 
	url="mqtt.jusdeliens.com", 
	verbosite=3
)

while True:
	agent.orienter((agent.orientation+1)%4)
	agent.actualiser()