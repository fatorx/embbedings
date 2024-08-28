import vanna
from vanna.remote import VannaDefault


vn = VannaDefault(model='chinook', api_key='7c20521ab8584db99f493d3d274f8337')
vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')
vn.ask("Quais são os 10 albuns mais vendidos?")
