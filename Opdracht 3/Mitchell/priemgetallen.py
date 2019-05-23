# Copyright (C) 2019 Mitchell Faas
# This code must be considered confidential. No part of
# this code may be duplicated, shown, or used in any way
# without the express written permission of the Author -
# Mitchell Faas - email: Faas.Mitchell@gmail.com

from collections import deque
import multiprocessing as mp
from math import *
import itertools
import queue
import time


class BSPObject:
    # The main BSP class

    def __init__(self, cores, pid, pipe_dict, barrier):
        # These should be static
        self._pipe_dict = pipe_dict
        self._barrier = barrier

        self.cores = cores
        self.pid = pid

        # These are expected to be dynamic and change.
        self._to_send_dict = {}
        self._queue = deque()

    def _clear_to_send(self):
        self._to_send_dict = {}

    def sync(self):
        """sync()
            Ensures all threads have stopped and parse
            all communication
            Returns
            ----------
            out : None"""

        # Ensure every processor is done doing what it was doing before
        self._barrier.wait()

        # Send all data
        for key in self._to_send_dict:
            # Pick the right communication line
            comm_line = self._pipe_dict[key]
            send_queue = self._to_send_dict[key]

            while send_queue:
                # Pop the first message in send_queue, and send it.
                message = send_queue.popleft()
                # Assume comm_line is a pipe
                try:
                    # This is the problem line, it stalls within _WINAPI.WaitForMultiplObjects
                    comm_line.send(message)

                # Comm_line is a Queue, so use put
                except AttributeError as attErr:
                    if str(attErr) != "'Queue' object has no attribute 'send'":
                        raise attErr
                    comm_line.put_nowait(message)

        # Clear _to_send_dict
        self._clear_to_send()

        # Ensure sending is done
        self._barrier.wait()

        # Clear the previous incoming _queue
        self._queue = deque()

        # Go through every pipe (to get data)
        for key in self._pipe_dict:
            comm_line = self._pipe_dict[key]
            try:
                # Assume comm_line is a pipe
                if comm_line.poll():  # There is data to be read
                    message = comm_line.recv()
                else:  # No data to be read
                    continue  # Go to next key

            except AttributeError as attErr:
                if str(attErr) != "'Queue' object has no attribute 'recv'" and \
                        str(attErr) != "'Queue' object has no attribute 'poll'":
                    raise attErr
                # Comm_line is a Queue, so use get
                try:
                    message = comm_line.get_nowait()
                except queue.Empty:
                    # If empty, go to next key
                    continue

            self._queue.append(message)

        # Ensure getting is done
        self._barrier.wait()

        # Everyone is released and the _barrier reset.

    def send(self, message, send_pid):
        """send(message, pid)
            Sends any object to the processor with a pid of send_pid.
            Parameters
            ----------
            message : literally anything
              Whatever data you wish to transfer
              between processors
            send_pid : int
              The processor id to which you wish
              to send a message.
            Returns
            ----------
            out : None"""

        # Add message to _queue
        if send_pid not in self._to_send_dict:
            self._to_send_dict[send_pid] = deque()
        self._to_send_dict[send_pid].append(message)

    def move(self):
        """"move()
        Acquires the first message stored in the receiving queue
        Returns
        ----------
        out : queue data
          The first element in the processor's "receive" queue."""

        try:
            message = self._queue.popleft()
        except IndexError:
            message = None
        return message

    @staticmethod
    def time():
        """time()
        Records the current Unix time in seconds of the system as a float.
        Returns
        ----------
        out : float
          Current Unix time in seconds"""
        return time.time()

    def nprocs(self):
        """nprocs()
            Finds number of available processors.
            Returns
            ----------
            out : int
              Number of processors participating
                in the current BSP instance."""
        return self.cores


def _create_pipes(cores):
    # Create all combinations of channels
    channels = itertools.combinations(range(cores), 2)

    # This lists all graph edges.
    pipe_dict = {}
    # Add self references ((1,1), (2,2), etc)
    for core in range(cores):
        # Create a _queue
        self_queue = mp.Queue()
        pipe_dict[core] = {}
        pipe_dict[core][core] = self_queue

    for channel in channels:
        # Create the actual pipe
        end1, end2 = mp.Pipe()

        # Get processor numbers
        proc1, proc2 = channel

        # Every key already exists because we made self-relations.
        pipe_dict[proc1][proc2] = end1
        pipe_dict[proc2][proc1] = end2

    return pipe_dict


def run(function, cores=0, *args):
    """run(function, [cores], [*args])
        Execute function on number of cores specified.
        Needs to be nested in an if __name__ = '__main__' statement.
        Parameters
        ----------
        function : callable
          A callable function to run in BSP.
        cores : int, optional
          The amount of cores you wish to use
          Defaults to all available cores
        *args : optional
          Any arguments you wish to pass on to your function.
        Returns
        ----------
        out : None"""
    try:
        # If cores isn't given or is 0, then set to maximum
        if not cores:
            cores = mp.cpu_count()
        # Core exception handling
        if type(cores) != int:
            raise TypeError("Cores must be an int")
        if cores < 0:
            raise ValueError("Cores must be positive")

        # Function exception handling
        if not callable(function):
            raise TypeError("Function must be callable")

        # First open all communication channels.
        # There will be be n(n-1)/2 channels.
        pipe_dict = _create_pipes(cores)

        # Then create a _barrier
        barrier = mp.Barrier(cores)

        # Start all processes one after the other.
        for i in range(cores):
            # Create a BSP data object
            bsp = BSPObject(cores=cores, pid=i, pipe_dict=pipe_dict[i], barrier=barrier)

            # Send BSP object
            p = mp.Process(target=function, args=(bsp, *args))
            p.start()
    except RuntimeError:
        raise RuntimeError('''
        An attempt has been made to start a new process before the
        current process has finished its bootstrapping phase.
        This probably means that you tried to use the run function
        but have forgotten to use the proper safequard:
            if __name__ == '__main__':
                run(function, cores)
        This is essential for the program to run properly.''')


def max_cores():
    """max_cores()
        Finds number of available processors.
        Returns
        ----------
        out : int
          Maximum number of available processors."""
    return mp.cpu_count()


def spmd(bsp: BSPObject, n, pipey):
    p = bsp.cores
    s = bsp.pid

    if s == 0:
        for i in range(p):
            bsp.send(n, i)

    bsp.sync()

    max_n = bsp.move()
    sqrt_n = floor(sqrt(max_n))
    sieveList = Sieve(sqrt_n+1)

    # Generate list of primes this core has to do and comb them
    per_core = max_n / p
    start = max(2, s*per_core) # make sure we don't count 0 and 1
    end = min(max_n, (s+1)*per_core)
    primeList = Comb(sieveList, start = start, end = end)
    primeAmount = len(primeList)

    #bsp.send(primeAmount, 0)
    bsp.send(primeList, 0)
    bsp.sync()

    if s == 0:
#        total = 0
        total = []
        for i in range(p):
            total += bsp.move()

        total.sort()

        pipey.send(total)

        # Prints the complete list
        #print(total)


def Sieve(n: int):
    # Initialize primes array
    primes = [1]*n
    for i in range(n):
        primes[i] = i

    # Start sieving
    foundPrimes = 0
    for i in range(2,n):
        # if i isn't sieved out, discard its multiples
        if primes[i] != 0:
            foundPrimes += 1
            for j in range(2*i, n, i):
                primes[j] = 0

    # Fill primeList
    primeList = []
    for i, x in enumerate(primes[2:]): # Discard the first 2 elements (0, 1)
        if x != 0:
            primeList.append(i+2)

    return primeList


def Comb(primesSieved: list, start: int, end: int):
    # Do some type cleanup
    start = int(start)
    end = int(end)
    # Initialize checklist
    numbers = [1]*(end-start)

    # comb out the non-primes
    for prime in primesSieved:
        # x*primeList[i] - start --> needs to be positive
        pSieveSqrd = prime**2

        # Ensure we we don't try to access weird indicies
        if start > pSieveSqrd:
            # If the start is larger than psquared, define jStart
            # at the next index to cross off
            if start % prime == 0:
                jStart = start
            else:
                jStart = start + (prime - start % prime)
        else:
            jStart = pSieveSqrd

        # Do the sieving
        for j in range(jStart, end, prime):
            numbers[j - start] = 0


    # Go through the sieved list
    primesList = []
    counter = 0
    for i, x in enumerate(numbers):
        if x != 0:
            primesList.append(start+i)

    return primesList


def priemzeef(n):
    if __name__ == 'priemgetallen' or __name__ == '__main__':
        #n = 10**4 #int(input("n="))

        recv_end, send_end = mp.Pipe(duplex=False)
        run(spmd, mp.cpu_count(), n, send_end)

        return recv_end.recv()

if __name__ == '__main__':
    a = priemzeef(100000)

    print(a)