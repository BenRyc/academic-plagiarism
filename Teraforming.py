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
    
class Layer():
    def __init__(self):
        self.north = []
        self.east = []
        self.south = []
        self.west = []
        
        self.northAvg = 0.0
        self.eastAvg = 0.0
        self.southAvg = 0.0
        self.westAvg = 0.0
        
        self.northBlocks = []
        self.eastBlocks = []
        self.southBlocks = []
        self.westBlocks = []
        
    def addCoord(self, direction, coord):
        if direction == 0:
            self.north += [coord, ]
            
        elif direction == 1:
            self.east += [coord, ]
            
        elif direction == 2:
            self.south += [coord, ]
            
        elif direction == 3:
            self.west += [coord, ]
            
    def addAvg(self, direction, avg):
        if direction == 0:
            self.northAvg = round(avg, 0)
            
        elif direction == 1:
            self.eastAvg = round(avg, 0)
            
        elif direction == 2:
            self.southAvg = round(avg, 0)
            
        elif direction == 3:
            self.westAvg = round(avg, 0)
            
    def addBlock(self, direction, block):
        if direction == 0:
            self.northBlocks += [block, ]
            
        elif direction == 1:
            self.eastBlocks += [block, ]
            
        elif direction == 2:
            self.southBlocks += [block, ]
            
        elif direction == 3:
            self.westBlocks += [block, ]
            
class Foundation():
    def __init__(self):
        self.coords = []
        
        self.averageHeights = 0.0
        
        self.blocks = []
        
    def addCoord(self, coord):
        self.north += [coord, ]
            
    def addAvg(self, direction, avg):
        self.averageHeights = round(avg, 0)
            
    def addBlock(self, direction, block):
        self.blocks += [block, ]
        
layers = []

numLayers = 3

for i in range(numLayers):
    layers += [Layer(), ]
    
layers += [Foundation(), ]
    
    
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
    
    
# Below functions should scan the nearby area of the player and clean up the results into an array with rows being properly represented

# EG. If scanArea returns [Vector1, Vector2, Vector3, Vector4], cleanUpScan will return [[Vector1, Vector2],[Vector3, Vector4]]

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

def stripLayer(scannedArea, layer):
    
    stripTopBottom(scannedArea, layer)
    
    if scannedArea == []:
        return 0
    
    stripRightLeft(scannedArea, layer)

def stripTopBottom(scannedArea, layer):
    rowLen = len(scannedArea[0])
    
    for coords in range(rowLen):
        temp = scannedArea[0].pop(0)
        layer.addBlock(0, mc.getBlockWithData(temp))
        layer.addCoord(0, temp)
        
    scannedArea.pop(0)
    
    if scannedArea == []:
        return 0
    
    colLen = len(scannedArea) - 1
    
    for coords in range(rowLen):
        temp = scannedArea[colLen].pop(0)
        layer.addBlock(2, mc.getBlockWithData(temp))
        layer.addCoord(2, temp)

    scannedArea.pop(colLen)
    
def stripRightLeft(scannedArea, layer):
    for row in scannedArea:
        temp = row.pop(0)
        layer.addBlock(1, mc.getBlockWithData(temp))
        layer.addCoord(1, temp)
        
    rowLen = len(scannedArea[0]) - 1
    
    for row in scannedArea:
        temp = row.pop(rowLen)
        layer.addBlock(3, mc.getBlockWithData(temp))
        layer.addCoord(3, temp)
    
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

# Below function handle placing the new blocks for teraforming. Using layerreferences and layerBlockReferences
# Should scan through each coord in each layer reference, placing that spesific block in the spesific location
# Should also scan for if the block above the block is solid, and if so replace it with air

def isAirAbove(coord):
    if mc.getBlock(coord.x, coord.y + 1, coord .z) == 0:
        return True
    else:
        return False
    
def fillAirAbove(coord):
    if isAirAbove(coord) == False:
        mc.setBlock(coord.x, coord.y + 1, coord.z, 0)
        fillAirAbove(Vector(coord.x, coord.y + 1, coord.z))
        
    else:
        return 0
    
def isAirBelow(coord):
    if mc.getBlock(coord.x, coord.y - 1, coord.z) == 0:
        return True
    else:
        return False
    
def fillAirBelow(coord, blockId, data):
    if isAirBelow(coord):
        mc.setBlock(coord.x, coord.y - 1, coord.z, blockId, data)
        fillAirBelow(Vector(coord.x, coord.y - 1, coord.z), blockId, data)
        
    else:
        return 0

def placeBlock(coord, blockId, data, fillBelow):
    x = coord.x
    y = coord.y
    z = coord.z
    
    if fillBelow:
        mc.setBlock(x, y, z, blockId, data)
        fillAirAbove(coord)
        fillAirBelow(coord, blockId, data)
        
    else:
        if isAirBelow(coord) == False:
            mc.setBlock(x, y, z, blockId, data)
            fillAirAbove(coord) 
            
    
def placeFoundation(layerReference, layerBlockReference):
    
    try:
        temp = layerReference[0][0][0]
        layered = True
    except:
        layered = False
    
    if layered:
        for i in range(len(layerBlockReference)):
            for x in range(len(layerReference[i])):
                coord = layerReference[i][x]
                block = layerBlockReference[i][x]
                placeBlock(coord, block.id, block.data, False)
                
    elif layered == False:
        for x in range(len(layerReference)):
                coord = layerReference[x]
                block = layerBlockReference[x]
                placeBlock(coord, block.id, block.data, True)

mc = Minecraft.create()

print("World created!")

anchor = mc.player.getTilePos()

print("Anchor stored")

sizehouseX = 5
sizehouseZ = 5

print("Size of the house's X is:" + str(sizehouseX))
print("Size of the house's Z is:" + str(sizehouseZ))

sizeX = sizehouseX + 6
sizeZ = sizehouseZ + 6

print("Size of the overall X is:" + str(sizeX))
print("Size of the overall Z is:" + str(sizeZ))

startX = anchor.x
endX = anchor.x + sizeX - 1

print("Start X is: " + str(startX) + "\nEnd X is: " + str(endX))

startZ = anchor.z
endZ = anchor.z + sizeZ - 1

print("Start Z is: " + str(startZ) + "\nEnd Z is: " + str(endZ))

scannedArea = scanArea(startX, startZ, endX, endZ, sizeX, sizeZ)

print("Area scanned!")

for layerIndex in range(len(layers)):
    if layer in layers:
        stripLayer(scannedArea, layer)


stripLayer(scannedArea, layer1[0], layer1[1], layer1[2], layer1[3], layer1Blocks)
stripLayer(scannedArea, layer2[0], layer2[1], layer2[2], layer2[3], layer2Blocks)

rowLen = len(scannedArea[0])
colLen = len(scannedArea)

for row in range(colLen):
    
    for coord in range(rowLen):
        temp = scannedArea[0].pop(0)
        foundationBlocks += [block.BEDROCK, ]
        #foundationBlocks += [mc.getBlockWithData(temp), ]
        foundation += [temp, ]
        
    scannedArea.pop(0)
    
print("Layers stripped!")
    
averageHeight(outerReference, avgOuterReference)
averageHeight(layer1, avgLayer1)
averageHeight(layer2, avgLayer2)
avgFoundation = averageHeightFoundation(foundation)

print("Average heights found!")

placeFoundation(outerReference, outerReferenceBlocks)
placeFoundation(layer1, layer1Blocks)
placeFoundation(layer2, layer2Blocks)
placeFoundation(foundation, foundationBlocks)

print("Foundation placed, all done!")




