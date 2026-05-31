from graph import graph  

__all__ = ["graph"]

#What's it used for ?

#Without __init__.py Flight_agent is just a folder and whenever u type -> "from Flight_agent import graph" it wont't work because
#it's not a package it's just a folder. this file basically converts this folder into a package from where Python can "import" modules from.
#think of it like a car with all the parts but have no chassis plate which makes it legally a car without which its just smth sitting in a garage.