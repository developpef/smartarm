# server OPCUA python
- pour générer les PK + certificats, voir la ligne de commande dans les examples
- utiliser le bash GIT pour avoir accès à OpenSSL

# creation du device Cumulocity
- lancer une registration via l'IHM cumulocity
- démarrer l'agent OPC UA
- ne pas créer le device via l'API C8Y

# config C8Y OPCUA
- URL : opc.tcp://0.0.0.0:4840/freeopcua/server/
- ServoLeft :
-- Path : 0:Objects/2:GFISmartFleet