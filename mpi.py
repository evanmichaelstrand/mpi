from mpi4py import MPI
import requests

comm = MPI.COMM_WORLD
worker = comm.Get_rank()

def generateData(worker):

    apikey = "a32e46f5b6e645aca53203026240809"
    location = "Boulder"
    call = "http://api.weatherapi.com/v1/current.json?key=" + apikey + "&q=" + location + "&aqi=no"

    if worker == 0:
        response = requests.get(call)
        data = response.json()
        #print(data)
        #comm.send(data, dest=1, tag=11)
    else:
        data = None

    data = comm.bcast(data, root=0)

    return data

def processData(data):
    if worker == 1:
        location = "The location is " + data['location']['name'] + ", " + data['location']['region']
        #print("The location is", data['location']['name'], ", ", data['location']['region'])
        comm.send(location, dest=4)

    if worker == 2:
        temp = "The temperature at the current time of " + data['current']['last_updated'] + " is " + str(data['current']['temp_c']) + " celcius and " + str(data['current']['temp_f']), "fahrenheit."
        #print("The temperature at the current time of", data['current']['last_updated'], "is", data['current']['temp_c'], "celcius and", data['current']['temp_f'], "fahrenheit.")
        comm.send(temp, dest=4)

    if worker == 3: 
        condition = "The condition is " + data['current']['condition']['text'] + " with winds of " + str(data['current']['wind_mph']) + " mph."
        comm.send(condition, dest=4)

    if worker == 4:
        location = comm.recv(source=1)
        temp = comm.recv(source=2)
        condition = comm.recv(source=3)
        print(location)
        print(temp)
        print(condition)

data = generateData(worker)
processData(data)
