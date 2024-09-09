Simple MPI file for NCAR
=======

This is a simple program written in python with the mpi4py library. The program assumes the definition of 4 processors. 

**Rank 0:** Gathers data from the [https://www.weatherapi.com/](weather api) and broadcasts the data to other processors.

**Rank 1:** Processes **location** and **temperature** data.

**Rank 2:** Processes **condition** and **precipitation** data.

**Rank 3:** Collects the processed data from processors 1 and 2 and prints them out. 
