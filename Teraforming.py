from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from mcpi.minecraft import Minecraft
from mcpi import block
global translated

import picraft
from picraft import Vector, X, Y, Z

import collections
#import io
#import random
import select
import socket
import threading
#import time
#import timeit

try:
    import queue
except ImportError:
    import Queue as queue
    
"""
0 = North
1 = East
0 = South
0 = West
"""
    
outerReference = [[], [], [], []]
avgOuterReference = [[], [], [], []]

layer1 = [[], [], [], []]
avgLayer1 = [[], [], [], []]

layer2 = [[], [], [], []]
avgLayer2 = [[], [], [], []]

foundation = []
avgFoundation = 0.0


    

def query_blocks(connection, requests, fmt, parse_fn, thread_count = 0):
    """Perform a batch of Minecraft server queries.
    The following Minecraft Pi edition socket query functions
    are supported:
     - world.getBlock(x,y,z) -> blockId
     - world.getBlockWithData(x,y,z) -> blockId,blockData
     - world.getHeight(x,z) -> y
    Parameters:
      connection
              A picraft "connection.Connection" object for an active
              Minecraft server.  Must have attributes:
              _socket, encoding.
      requests
              An iterable of coordinate tuples.  See the examples.
              Note that if thread_count > 0, this will be accessed
              from another thread, and if thread_count > 1, it
              will be accessed from multiple threads.
      fmt
              The request format string, one of:
                  world.getBlock(%d,%d,%d)
                  world.getBlockWithData(%d,%d,%d)
                  world.getHeight(%d,%d)
      parse_fn
              Function to parse the results from the server, one of:
                  int
                  lambda ans: tuple(map(int, ans.split(",")))
              Note that responses have the form "0" or "0,0".
      thread_count
              Number of threads to create.  If thread_count == 0, no
              threads are created and work is done in the current thread.
              If thread_count > 0 and the "requests" parameter is a
              generator function, consider thread safety issues.
              The maximum recommended thread_count == 30 for very large
              query sizes.
    Generated values:
      tuple(request, answer), where
        request - is a value from the "requests" parameter
        answer - is the matching response from the server, as parsed
                 by parse_fn
      Note: If thread_count <= 1, tuples are generated in the same
      order as the "requests" parameter.  Otherwise, there is no such
      guarantee.
    """
    
    def worker_fn(mc_socket, request_iter, request_lock, answer_queue):
        """Single threaded worker function to keep its socket
        as full of requests as possible.
        The worker does this: Dequeue requests, format them, and
        write them into the socket as fast as it will take them.
        At the same time, read responses from the socket as fast
        as they appear, parse them, match them with the request,
        and enqueue the answers.
        """
        more_requests = True
        request_buffer = bytes()
        response_buffer = bytes()
        pending_request_queue = collections.deque()
        while more_requests or len(pending_request_queue) > 0:
            # Grab more requests
            while more_requests and len(request_buffer) < 4096:
                with request_lock:
                    try:
                        pos = next(request_iter)
                    except StopIteration:
                        more_requests = False
                        continue
                    new_request = (fmt % pos).encode(socket_encoding)
                    request_buffer = request_buffer + new_request + b"\n"
                    pending_request_queue.append(pos)
            if not (more_requests or len(pending_request_queue) > 0):
                continue

            # Select I/0 we can perform without blocking
            w = [mc_socket] if len(request_buffer) > 0 else []
            r, w, x = select.select([mc_socket], w, [], 1)
            allow_read = bool(r)
            allow_write = bool(w)

            # Write requests to the server
            if allow_write:
                # Write exactly once
                bytes_written = mc_socket.send(request_buffer)
                request_buffer = request_buffer[bytes_written:]
                if bytes_written == 0:
                    raise RuntimeError("unexpected socket.send()=0")

            # Read responses from the server
            if allow_read:
                # Read exactly once
                bytes_read = mc_socket.recv(1024)
                response_buffer = response_buffer + bytes_read
                if bytes_read == 0:
                    raise RuntimeError("unexpected socket.recv()=0")

            # Parse the response strings
            responses = response_buffer.split(b"\n")
            response_buffer = responses[-1]
            responses = responses[:-1]
            for response_string in responses:
                request = pending_request_queue.popleft()
                answer_queue.put((request, parse_fn(response_string.decode(socket_encoding))))

    socket_encoding = connection.encoding
    request_lock = threading.Lock()
    answer_queue = queue.Queue()
    if thread_count == 0:
        worker_fn(connection._socket,
                  iter(requests),
                  request_lock,
                  answer_queue)
    else:
        sockets = []
        socket_host, socket_port = connection._socket.getpeername()
        try:
            for i in range(thread_count):
                sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                sockets[-1].connect((socket_host, socket_port))
            workers = []
            threading.stack_size(128 * 1024)  # bytes; reset when done?
            for w in range(thread_count):
                t = threading.Thread(target = worker_fn,
                                     args = (sockets[w],
                                             iter(requests),
                                             request_lock,
                                             answer_queue))
                t.start()
                workers.append(t)
            for w in workers:
                w.join()
        except socket.error as e:
            print("Socket error:", e)
            print("Is the Minecraft server running?")
            raise e
        finally:
            for s in sockets:
                try:
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                except socket.error as e:
                    pass
    while not answer_queue.empty():
        yield answer_queue.get()


def alt_picraft_getblock_vrange(world, vrange):
    """Drop-in replacement for picraft: b = world.blocks[vrange]
    This is intended as a drop-in replacement for
    picraft.world.World.blocks.__getitem__(vector_range).
    This invokes query_blocks and returns a list of block data
    in the same order as the input vrange.
    Note that vrange is iterated twice.
    """
    ans = { pos: data for (pos, data) in
            query_blocks(world.connection,
                         vrange,
                         "world.getBlockWithData(%d,%d,%d)",
                         lambda ans: tuple(map(int, ans.split(",")))) }
    return [picraft.Block(*ans[v]) for v in vrange]


def alt_picraft_getheight_vrange(world, vrange):
    """Drop-in replacement for picraft: b = world.height[vrange]
    This is intended as a drop-in replacement for
    picraft.world.World.height.__getitem__(vector_range).
    This invokes query_blocks and returns a list of vectors
    in the same order as the input vrange.
    Alternate design: If thread_count > 1 is desired, this could
    first get the query_blocks dict, then iterate vrange again.
    """
    return [Vector(pos[0], data, pos[1]) for (pos, data) in
            query_blocks(world.connection,
                         ((v[0], v[2]) for v in vrange),
                         "world.getHeight(%d,%d)",
                         int,
                         thread_count = 0)]
    
    
def cleanUpScan(scannedArea, sizeX, sizeZ):
    filtered = []
    index = 0
        
    for i in range(sizeX):
        row = []
        
        for j in range(sizeZ):
            row.append(scannedArea[index])
            index += 1
            
        filtered.append(row)
        
    return filtered

    
def scanArea(startX, startZ, endX, endZ, sizeX, sizeZ):
    world = picraft.World()
    
    cuboid = picraft.vector_range(Vector(startX, 0, startZ), Vector(endX, 0, endZ) + 1)
    my_blocks = {}
    for pos, blk in query_blocks(
            world.connection,
            cuboid,
            "world.getBlockWithData(%d,%d,%d)",
            lambda ans: tuple(map(int, ans.split(","))),
            thread_count=0):
        my_blocks[pos] = blk
    
    x = alt_picraft_getblock_vrange(world, cuboid)
    y = world.blocks[cuboid]

    global h
    h = alt_picraft_getheight_vrange(world, cuboid)
    
    filtered = cleanUpScan(h, sizeX, sizeZ)
    
    return filtered

# Below functions should strip a layer off of a given 2d array, starting with the top (north) and bottom (south), then right (east) and left (west)
# Checking should also take place in case the array is too small to make it through both the top and bottom removal functions, as well as the right and left removal functions
# If an array is found to be too small, the funciton simply returns what is has

def stripLayer(scannedArea, north, east, south, west):
    
    stripTopBottom(scannedArea, north, south)
    
    if scannedArea == []:
        return 0
    
    stripRightLeft(scannedArea, east, west)

def stripTopBottom(scannedArea, north, south):
    rowLen = len(scannedArea[0])
    
    for coords in range(rowLen):
        north += [scannedArea[0].pop(0), ]
        
    scannedArea.pop(0)
    
    if scannedArea == []:
        return 0
    
    colLen = len(scannedArea) - 1
    
    for coords in range(rowLen):
        south += [scannedArea[colLen].pop(0), ]

    scannedArea.pop(colLen)
    
def stripRightLeft(scannedArea, east, west):
    for row in scannedArea:
        east += [row.pop(0), ]
        
    rowLen = len(scannedArea[0]) - 1
    
    for row in scannedArea:
        west += [row.pop(rowLen), ]
    
# Below functions should grab each height from a given direction in a given layer 
# Then, get both the total number of values and the sum and average them out
# This average is then stored in an array for the corrisponding layer and direction (or just layer if no direction is rquired)

# Eg. layer1[0] (north) gets averaged and storec in avgLayer1[0] (o is north)

def averageHeight(array, avgArray):

    for direction in range(len(array)):
        total = 0.0
        coordNum = 0
        
        for coord in array[direction]:
            total += int(coord[1])
            coordNum += 1
            
        avgArray[direction] = total/coordNum
        
    insertAvgHeight(array, avgArray)
        
def averageHeightFoundation(foundation):
    total = 0.0
    coordNum = 0
            
    for coord in foundation:
        total += int(coord[1])
        coordNum += 1
        
    return insertAvgFoundation(foundation, total/coordNum)

# Below functions should insert the average heights into their respective arrays through creating new vectors and overwriting existing ones
# This is done through making new vectors as they are immutable

# Eg. outerReference north's y coord get updated with outerReference north's average y

def insertAvgHeight(array, avgArray):
    
    for direction in range(len(array)):
        for coord in range(len(array[direction])):
            temp = Vector(array[direction][coord].x, int(avgArray[direction]), array[direction][coord].z)
            array[direction][coord] = temp
            
def insertAvgFoundation(foundation, average):
    for coord in range(len(foundation)):
        temp = Vector(foundation[coord].x, int(average), foundation[coord].z)
        foundation[coord] = temp
        
    return average
            

mc = Minecraft.create()

anchor = mc.player.getTilePos()

sizehouseX = 5
sizehouseZ = 5

sizeX = sizehouseX + 6
sizeZ = sizehouseZ + 6

startX = anchor.x
endX = anchor.x + sizeX - 1

startZ = anchor.z
endZ = anchor.z + sizeZ - 1

scannedArea = scanArea(startX, startZ, endX, endZ, sizeX, sizeZ)

stripLayer(scannedArea, outerReference[0], outerReference[1], outerReference[2], outerReference[3])
stripLayer(scannedArea, layer1[0], layer1[1], layer1[2], layer1[3])
stripLayer(scannedArea, layer2[0], layer2[1], layer2[2], layer2[3])

rowLen = len(scannedArea[0])
colLen = len(scannedArea)

for row in range(colLen):
    
    for coord in range(rowLen):
        foundation += [scannedArea[0].pop(0), ]
        
    scannedArea.pop(0)
    
averageHeight(outerReference, avgOuterReference)
averageHeight(layer1, avgLayer1)
averageHeight(layer2, avgLayer2)
avgFoundation = averageHeightFoundation(foundation)

        
print("Outer Reference")
print(avgOuterReference[0])
print(outerReference[0])
print()
print(avgOuterReference[1])
print(outerReference[1])
print()
print(avgOuterReference[2])
print(outerReference[2])
print()
print(avgOuterReference[3])
print(outerReference[3])
print()
print("Layer 1")
print(avgLayer1[0])
print(layer1[0])
print()
print(avgLayer1[1])
print(layer1[1])
print()
print(avgLayer1[2])
print(layer1[2])
print()
print(avgLayer1[3])
print(layer1[3])
print()
print("Layer 2")
print(avgLayer2[0])
print(layer2[0])
print()
print(avgLayer2[1])
print(layer2[1])
print()
print(avgLayer2[2])
print(layer2[2])
print()
print(avgLayer2[3])
print(layer2[3])
print()
print("Foundation")
print(avgFoundation)
print(foundation)
