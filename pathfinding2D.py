
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
from mcpi import minecraft
from mcpi import block
import picraft
from picraft import Vector, X, Y, Z

import collections
import io
import random
import select
import socket
import threading
import time
import timeit
try:
    import queue
except ImportError:
    import Queue as queue


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
    print(vrange)
    return [Vector(pos[0], data, pos[1]) for (pos, data) in
            query_blocks(world.connection,
                         ((v[0], v[2]) for v in vrange),
                         
                         "world.getHeight(%d,%d)",

                         int,
                         thread_count = 0)]

    #for i in h:
        #print(i)
    #print(h)
translated = [0,0]
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.p = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a Path from the given start to the given end in the given maze"""

    # Create start and end node
    StartNode = Node(None, start)
    StartNode.g = StartNode.h = StartNode.f = 0
    StartNode.hei = 0

    EndNode = Node(None, end)
    EndNode.g = EndNode.h = EndNode.f = 0

    # Initialize both open and closed list
    OpenList = []
    ClosedList = []

    # Add the start node
    OpenList.append(StartNode)

    # Loop until you find the end
    while len(OpenList) > 0:

        # Get the Current node
        CurrentNode = OpenList[0]
        CurrentIndex = 0
        for index, Item in enumerate(OpenList):
            if Item.f < CurrentNode.f:
                CurrentNode = Item
                CurrentIndex = index
                #y = mc.getHeight(CurrentNode.position[0],CurrentNode.position[1])
                #mc.setBlock(CurrentNode.position[0],y,CurrentNode.position[1],5)
        # Pop current off open list, add to closed list
        OpenList.pop(CurrentIndex)
        ClosedList.append(CurrentNode)

        # Found the goal
        if CurrentNode == EndNode:
            Path = []
            Current = CurrentNode
            while Current is not None:
                Path.append(Current.position)
                Current = Current.parent
                #print(Path)
            return Path[::-1] # Return reversed Path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            NodePosition = (CurrentNode.position[0] + new_position[0], CurrentNode.position[1] + new_position[1])

            # Make sure within range
            if NodePosition[0] > (len(maze) - 1) or NodePosition[0] < 0 or NodePosition[1] > (len(maze[len(maze)-1]) -1) or NodePosition[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[NodePosition[0]][NodePosition[1]] == -1:
                continue

            # Create new node
            new_node = Node(CurrentNode, NodePosition)

            # Append
            #print(NodePosition)
            #y=(mc.getHeight(NodePosition))
            #mc.setBlock(NodePosition[0],y,NodePosition[1],4)
            
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for ClosedChild in ClosedList:
                if child == ClosedChild:
                    continue

            # Create the f, g, and h values
            child.g = CurrentNode.g + 1
            child.h = ((child.position[0] - EndNode.position[0]) ** 2) + ((child.position[1] - EndNode.position[1]) ** 2)
            child.p = abs((maze[child.position[0]][child.position[1]])-(maze[CurrentNode.position[0]][CurrentNode.position[1]]))*5
            #print(CurrentNode.p)
            print(CurrentNode.p)

            x = child.position[0]-translated[0]
            z = child.position[1]-translated[1]
            y=mc.getHeight(x,z)
            #print (mc.getHeight)
            mc.setBlock(x,y,z,35)
            #print(child.position)

            #print(translated[0])
            #print(x)
            
           # print(translated[1])
            #print(z)
            #print(x)
            #print(z)
            #print(x)
            #print(z)
            #child.hei = mc.getHeight(x,z)
            #print(child.hei)
            #if CurrentNode.hei>child.hei+1:
            #    child.p+=15
            #if CurrentNode.hei<child.hei-1:
            #    child.p+=15
            #print(child.g)
            #print(child.h)
            child.f = child.g + child.h +child.p #+ child.hei*5

            # Child is already in the open list
            for OpenNode in OpenList:
                if child == OpenNode and child.g > OpenNode.g:
                    continue

            # Add the child to the open list
            OpenList.append(child)
            

import random
mc = minecraft.Minecraft.create()
def main():
    print("ay")
    
    print(mc.getBlock(12,92  ,4))
    print("hey")

    
    
    maze = []   
    for i in range(0,30):
        nrow=[]
        for j in range(0,30):
            nrow.append(0)
        maze.append(nrow)
        print(nrow)

    global translated
    def getVals(listval1, listval2, translatedval):
        world = picraft.World()
        world.say("Hello mcpi_fast_query!")
        #print(listval1)
        #print(listval2)

        if listval1[0] <= listval2[0]:
            val1 = listval1[0]-translatedval[0]-5
        elif listval1[0] > listval2[0]:
            val1 = listval2[0]-translatedval[0]-5
        if listval1[1] <= listval2[1]:
            val2 = listval1[1]-translatedval[1]-5
        elif listval1[1] > listval2[1]:
            val2 = listval2[1]-translatedval[1]-5



        cuboid = picraft.vector_range(Vector(val1, 0, val2), Vector(val1+100, 0, val2+100) + 1)
        my_blocks = {}
        for pos, blk in query_blocks(
                world.connection,
                cuboid,
                "world.getBlockWithData(%d,%d,%d)",
                lambda ans: tuple(map(int, ans.split(","))),
                thread_count=0):
            my_blocks[pos] = blk
        #print(my_blocks)
        
        x = alt_picraft_getblock_vrange(world, cuboid)
        #print(x)
        y = world.blocks[cuboid]
        #print(y)
        #print(x==y)

        global h
        h = alt_picraft_getheight_vrange(world, cuboid)
        #for i in h:
            #print(i)
        #for i in h:
            #print(i)
    start = [4015,4060]
    end = [4060,4020]
    
    translated = [4015,4060]
    #print(start, end)
    if start[0]<5:
        tempStore = start[0]
        start[0]=5
        dif = tempStore-start[0]
        end[0]-=dif
    if start[1]<5:
        tempStore = start[1]
        start[1]=5
        dif = tempStore-start[1]
        end[1]-=dif

    if end[0]<5:
        tempStore = end[0]
        end[0]=5
        dif = tempStore-end[0]
        start[0]-=dif
    if end[1]<5:
        tempStore = end[1]
        end[1]=5
        dif = tempStore-end[1]
        start[1]-=dif
        
    if start[0]>95:
        tempStore = start[0]
        start[0]=95
        dif = tempStore-start[0]
        end[0]-=dif

    if start[1]>95:
        tempStore = start[1]
        start[1]=95
        dif = tempStore-start[1]
        end[1]-=dif

    if end[0]>95:
        tempStore = end[0]
        end[0]=95
        dif = tempStore-end[0]
        start[0]-=dif
        
    if end[1]>95:
        tempStore = end[1]
        end[1]=95
        dif = tempStore-end[1]
        start[1]-=dif



    #print(start, end)

    translated = [-(translated[0]-start[0]),-(translated[1]-start[1])]
    getVals(start,end, translated)
    print(start, end)
    #print(start)
    #print(end)
    s = (start[0], start[1])
    e = (end[0], end[1])
    #print(translated)
    maze = []
    for i in range (0,100):
        nrow = []
        for j in range (0,100):
            x = random.randint(1, 3)
            hval = j+100*i
            nrow.append(int(h[hval].y))
        maze.append(nrow)
    #print(maze)
    #print(maze)
        #print(nrow)
    
    #print(maze)

    Path = astar(maze, s, e)
    print(Path)
    for i in Path:


        y=(mc.getHeight(i))
        #print(translated[0])
        #print("translation")
        #print(translated[0])
        #print(translated[1])
        #print(i[0])
        #print(i[1])
        x = i[0] -translated[0]
        #print(x)
        z = i[1] -translated[1]
        #print(z)
        #print(x)
        #print(z)
        y = mc.getHeight(x,z)
        #print(x,z)
        mc.setBlock(x,y,z,14)
        #print(maze)
        

if __name__ == '__main__':
    main()
#check for places already gone over, if taken already then add to closed list. 