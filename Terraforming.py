from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from mcpi.minecraft import Minecraft
from mcpi import block as mcpiBlock
    
import picraft
from picraft import Vector, X, Y, Z

import collections
import select
import socket
import threading

try:
    import queue
except ImportError:
    import Queue as queue
    
def terraform(anchorX, anchorZ, sizeHouseX, sizeHouseZ):
    
    blocksAvoid = [0, 8, 9, 10, 11, 18, 31, 32, 37, 38, 39, 40, 78, 81]
    
    # Layer is the general class which houses information used in a ring around the foundation (known as a layer) which has the height
    # avg height stores the average of the 4 directional heights so setblocks can be used later to speed up foundation placement
    # north, east, south and west each store block data for that direction on the layer, each block having x, y, z data
    # n, e, s, w avg stores the average height for that cardinal direction
    # n, e, s, w blocks stores each block in order for that layer to be placed later
        
    class Layer():
        def __init__(self):
            self.avgHeight = 0
            
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
                
        def getCardinal(self, direction):
            if direction == 0:
                return self.north
                
            elif direction == 1:
                return self.east
                
            elif direction == 2:
                return self.south
                
            elif direction == 3:
                return self.west
            
        def getAvg(self, direction):
            if direction == 0:
                return self.northAvg
                
            elif direction == 1:
                return self.eastAvg
                
            elif direction == 2:
                return self.southAvg
                
            elif direction == 3:
                return self.westAvg
            
        def getBlocksCardinal(self, direction):
            if direction == 0:
                return self.northBlocks
                
            elif direction == 1:
                return self.eastBlocks
                
            elif direction == 2:
                return self.southBlocks
                
            elif direction == 3:
                return self.westBlocks
            
        def clearCardinal(self, direction):
            if direction == 0:
                self.north = []
                
            elif direction == 1:
                self.east = []
                
            elif direction == 2:
                self.south = []
                
            elif direction == 3:
                self.west = []
            
        def setAvgHeight(self):
            self.avgHeight = round((self.northAvg + self.eastAvg + self.southAvg + self.westAvg)/4)
            
        def getAvgHeight(self):
            return self.avgHeight
    
    # Below class is just for the foundation, as it doesn't need to store individual cartisional directions
    # Coords stores the coords of the blocks to be placed
    # Average heights stores the average height of the foundation
    # Blocks stores the actual blocks used by the foundation
    
    class Foundation():
        def __init__(self):
            self.coords = []
            
            self.averageHeights = 0.0
            
            self.blocks = []
            
        def addCoord(self, coord):
            self.coords += [coord, ]
                
        def addAvg(self, avg):
            self.averageHeight = round(avg, 0)
                
        def addBlock(self, block):
            self.blocks += [block, ]
            
        def getCoords(self):
            return self.coords
                
        def getAvg(self):
            return self.averageHeight
                
        def getBlocks(self):
            return self.blocks
            
        def clearCoords(self):
            self.coords = [] 
        
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
            layer.addCoord(0, temp)
            layer.addBlock(0, mc.getBlockWithData(temp))
            
        scannedArea.pop(0)
        
        if scannedArea == []:
            return 0
        
        colLen = len(scannedArea) - 1
        
        for coords in range(rowLen):
            temp = scannedArea[colLen].pop(0)
            layer.addCoord(2, temp)
            layer.addBlock(2, mc.getBlockWithData(temp))

        scannedArea.pop(colLen)
        
    def stripRightLeft(scannedArea, layer):
        for row in scannedArea:
            temp = row.pop(0)
            layer.addCoord(1, temp)
            layer.addBlock(1, mc.getBlockWithData(temp))
            
        rowLen = len(scannedArea[0]) - 1
        
        for row in scannedArea:
            temp = row.pop(rowLen)
            layer.addCoord(3, temp)
            layer.addBlock(3, mc.getBlockWithData(temp))
        
    # Below functions should grab each height from a given direction in a given layer 
    # Then, get both the total number of values and the sum and average them out
    # This average is then stored in an array for the corrisponding layer and direction (or just layer if no direction is rquired)

    # Eg. layer1[0] (north) gets averaged and storec in avgLayer1[0] (o is north)

    def averageHeight(layer):
        
        array = [layer.north, layer.east, layer.south, layer.west]

        for direction in range(4):
            total = 0.0
            coordNum = 0
            
            for coord in array[direction]:
                total += int(coord[1])
                coordNum += 1
                
            layer.addAvg(direction, total/coordNum)
            
        insertAvgHeight(layer)
            
    def averageHeightFoundation(foundation):
        total = 0.0
        coordNum = 0
                
        for coord in foundation.coords:
            total += int(coord[1])
            coordNum += 1
            
        foundation.addAvg(total/coordNum)
            
        insertAvgFoundation(foundation)

    # Below functions should insert the average heights into their respective arrays through creating new vectors and overwriting existing ones
    # This is done through making new vectors as they are immutable

    # Eg. outerReference north's y coord get updated with outerReference north's average y

    def insertAvgHeight(layer):
        
        for direction in range(4):
            array = layer.getCardinal(direction)
            layer.clearCardinal(direction)
            for coord in array:
                layer.addCoord(direction, Vector(coord.x, int(round(layer.getAvg(direction))), coord.z))
                
                
    def insertAvgFoundation(foundation):
        array = foundation.getCoords()
        foundation.clearCoords()
        for coord in array:
            foundation.addCoord(Vector(coord.x, int(round(foundation.getAvg())), coord.z))

    # Below function handle placing the new blocks for teraforming. Using layerreferences and layerBlockReferences
    # Should scan through each coord in each layer reference, placing that spesific block in the spesific location
    # Should also scan for if the block above the block is solid, and if so replace it with air

    def placeBlock(startCoord, endCoord, height, blockId, data):
        startX = startCoord.x
        startY = height
        startZ = startCoord.z
        
        endX = endCoord.x
        endZ = endCoord.z
        
        mc.setBlocks(startX, startY, startZ, endX, startY - 10, endZ, blockId, data)
        mc.setBlocks(startX, startY + 1, startZ, endX, startY + 1000, endZ, 0)
                
        
    def placeFoundation(layer):
        
        try:
            temp = layer.getCardinal(0)
            layered = True
            
        except:
            layered = False
            
        if layered:
            print("aaaaaaAAAAAAAAAAAAAAAA")
            fillBlock = getBlockToFill(layer.getBlocksCardinal(0))
            startCoord = layer.getCardinal(0)[0]
            endCoord = layer.getCardinal(2)[len(layer.getCardinal(2))-1]
            height = layer.getAvgHeight()
            placeBlock(startCoord, endCoord, height, fillBlock.id, fillBlock.data)
            return fillBlock
                    
        elif layered == False:
            coords = layer.getCoords()
            print("aaaaaaAAAAAAAAAAAAAAAA")
            fillBlock = getBlockToFill(layer.getBlocks())
            startCoord = coords[0]
            endCoord = coords[len(coords)-1]
            placeBlock(startCoord, endCoord, coords[0].y, fillBlock.id, fillBlock.data)
            return fillBlock

    def getBlockToFill(blocks):
        for blockIndex in blocks:
            valid = True
            
            for scan in blocksAvoid:
                scannedBlock = blockIndex.id
                print(scannedBlock)
                
                if scannedBlock == scan:
                    print("Inside if")
                    valid = False
                    break
                    
            if valid:
                return blockIndex
            
        if valid == False:
            return mcpiBlock.GRASS
                    
    
    #TODO for each block in a given gardinal direction, scan a nlacklist and if the block is in a blacklist then go to the next block, default to grass

    layers = []

    numLayers = 3

    for i in range(numLayers):
        layers += [Layer(), ]
        
    layers += [Foundation(), ]

    mc = Minecraft.create()

    anchor = mc.player.getTilePos()

    sizeX = sizeHouseX + (len(layers) - 1) * 2
    sizeZ = sizeHouseZ + (len(layers) - 1) * 2

    startX = anchorX
    endX = anchorX + sizeX - 1

    startZ = anchorZ
    endZ = anchorZ + sizeZ - 1

    scannedArea = scanArea(startX, startZ, endX, endZ, sizeX, sizeZ)

    for layerIndex in range(len(layers)-1):
        stripLayer(scannedArea, layers[layerIndex])

    rowLen = len(scannedArea[0])
    colLen = len(scannedArea)

    foundation = layers[len(layers)-1]

    for row in range(colLen):
        for coord in range(rowLen):
            temp = scannedArea[0].pop(0)
            foundation.addBlock(mc.getBlockWithData(temp))
            foundation.addCoord(temp)
            
        scannedArea.pop(0)

    for layerIndex in range(len(layers) - 1):
        averageHeight(layers[layerIndex])
        layers[layerIndex].setAvgHeight()

    averageHeightFoundation(foundation)

    for layerIndex in layers:
        foundationBlock = placeFoundation(layerIndex)
    
    return foundation.getCoords(), foundationBlock