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
    else:
        data = None

    data = comm.bcast(data, root=0)

    return data

def processData(data):
    if worker == 1:
        location = "The location is " + data['location']['name'] + ", " + data['location']['region']
        temp = "The temperature at the current time of " + data['current']['last_updated'] + " is " + str(data['current']['temp_c']) + " celcius and " + str(data['current']['temp_f']) + " fahrenheit."
        data = location, temp
        comm.send(data, dest=3)

    if worker == 2:
        condition = "The condition is " + data['current']['condition']['text'] + " with winds of " + str(data['current']['wind_mph']) + " mph."
        rain = "The current precipitation amount is " + str(data['current']['precip_in']) + " inches."
        status = condition, rain
        comm.send(status, dest=3)

    if worker == 3: 
        location, temp = comm.recv(source=1)
        condition, rain = comm.recv(source=2)
        print(location)
        print(temp)
        print(condition)
        print(rain)
        

data = generateData(worker)
processData(data)
