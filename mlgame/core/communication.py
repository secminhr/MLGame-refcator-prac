from threading import Thread
from queue import Queue

from mlgame.core.exceptions import GameError

from mlgame.core.env import WS_WAIT_GAME_TIMEOUT


class CommunicationHandler:
    """
    A data class for storing a sending and a receiving communication objects
    and providing interface for accessing them
    """

    def __init__(self):
        self._recv_end = None
        self._send_end = None

    def set_recv_end(self, comm_obj):
        """
        Set the communication object for receiving

        @param comm_obj The communication object which has `recv` and `poll` function
        """
        if not hasattr(comm_obj, "recv") or not hasattr(comm_obj, "poll"):
            raise ValueError("'comm_obj' doesn't have 'recv' or 'poll' function")

        self._recv_end = comm_obj

    def set_send_end(self, comm_obj):
        """
        Set the communication object for sending

        @param comm_obj The communication object which has `send` function
        """
        if not hasattr(comm_obj, "send"):
            raise ValueError("'comm_obj' doesn't have 'send' function")

        self._send_end = comm_obj

    def poll(self):
        return self._recv_end.poll()

    def recv(self):
        return self._recv_end.recv()

    def send(self, obj):
        self._send_end.send(obj)


class CommunicationSet:
    """
    A data class for storing a set of communication objects and
    providing an interface for accessing these objects

    Communication objects used for receiving objects must provide `recv()` and `poll()`,
    and them used for sending objects must provide `send()`.
    For example, the object of `multiprocessing.connection.Connection` is a valid
    communication object for both sending and receiving.

    @var _recv_end A dictionary storing communication objects which are used to
         receive objects
    @var _send_end A dictionary storing communication objects which are used to
         send objects
    """

    def __init__(self):
        self._comm_handlers: dict[str, CommunicationHandler] = {}

    def add_comm_handler(self, name: str, comm: CommunicationHandler):
        if name in self._comm_handlers:
            raise ValueError("The name '{}' already exists in 'comm_handlers'".format(name))

        self._comm_handlers[name] = comm

    def get_comm_handler_names(self):
        return self._comm_handlers.keys()

    def poll(self, name: str):
        """
        Check whether the specified communication object has data to read

        @param name The name of the communication object
        """
        return self._comm_handlers[name].poll()

    def recv(self, name: str, to_wait: bool = False):
        """
        Receive object from the specified communication object

        @param name The name of the communication object
        @param to_wait Whether to wait until the object is arrived
        @return The received object. If `to_wait` is False and nothing available from
                the specified communication object, return None.
        """
        if not to_wait and not self.poll(name):
            return None

        return self._comm_handlers[name].recv()

    def recv_all(self, to_wait: bool = False):
        """
        Receive objects from all communication object registered for receiving

        If `to_wait` is True, it will wait for the object one by one.

        @param to_wait Whether to wait until the object is arrived
        @return A dictionary storing received objects. The key is the name of
                the communication object, the value is the received object.
                If `to_wait` is False and nothing to receive, the value will be None.
        """
        objs = {}
        for comm_name in self.get_comm_handler_names():
            objs[comm_name] = self.recv(comm_name, to_wait)

        return objs

    def send(self, obj, name: str):
        """
        Send object via the specified communication object

        @param obj The object to be sent
        @param name The name of the communication object
        """
        self._comm_handlers[name].send(obj)

    def send_all(self, obj):
        """
        Send object via all communication objects registered for sending

        @param obj The object to be sent
        """
        for comm_handlers in self._comm_handlers.values():
            comm_handlers.send(obj)

class GameCommManager:
    """
    The commnuication manager for the game process
    """

    def __init__(self):
        self._comm_to_ml_set = CommunicationSet()
        self._comm_to_others = CommunicationSet()

    def add_comm_to_ml(self, ml_name, recv_end, send_end):
        """
        Set communication objects for communicating with specified ml process
        """
        comm_handler = CommunicationHandler()
        comm_handler.set_recv_end(recv_end)
        comm_handler.set_send_end(send_end)
        self._comm_to_ml_set.add_comm_handler(ml_name, comm_handler)

    def get_ml_names(self):
        """
        Get the name of all registered ml process
        """
        return self._comm_to_ml_set.get_comm_handler_names()

    def send_to_ml(self, obj, ml_name):
        """
        Send the object to the specified ml process
        """
        self._comm_to_ml_set.send(obj, ml_name)

    def send_to_all_ml(self, obj):
        """
        Send the object to all ml process
        """
        self._comm_to_ml_set.send_all(obj)

    def recv_from_ml(self, ml_name):
        """
        Receive the object from the specified ml process

        If the received object is `MLProcessError`, raise the exception.
        """
        obj = self._comm_to_ml_set.recv(ml_name, to_wait=False)
        return obj

    def recv_from_all_ml(self):
        """
        Receive objects from all the ml processes
        """
        return self._comm_to_ml_set.recv_all(to_wait=False)

    def add_comm_to_others(self, client_name, recv_end, send_end):
        """
        Set communication objects for communicating with specified ml process
        """
        comm_handler = CommunicationHandler()
        comm_handler.set_recv_end(recv_end)
        comm_handler.set_send_end(send_end)
        self._comm_to_others.add_comm_handler(client_name, comm_handler)

    def send_game_result(self, game_result):
        self._send_data_to_others("game_result", game_result)

    def send_system_message(self, message):
        self._send_data_to_others("system_message", {"message": message})

    def send_game_info(self, game_info_dict):
        self._send_data_to_others("game_info", game_info_dict)

    def send_game_progress(self, game_progress_dict):
        """
        Send the game progress to the transition server
        """
        self._send_data_to_others("game_progress", game_progress_dict)

    def send_game_error_with_obj(self, error: GameError):
        self._send_data_to_others("game_error", {
            "message": error.message,
            "error_type": error.error_type.name,
            "frame": error.frame
        })

    def send_end_message(self):
        self._send_to_others(None)

    def _send_data_to_others(self, type, data):
        self._send_to_others({
            "type": type,
            "data": data
        })

    def _send_to_others(self, obj):
        """
        Send the object to all ml process
        """
        # print(obj)
        self._comm_to_others.send_all(obj)

    def recv_from_others(self):
        """
        Receive objects from all the ml processes
        """
        return self._comm_to_others.recv_all(to_wait=False)


class MLCommManager:
    """
    The communication manager for the ml process
    """

    def __init__(self, ml_name):
        self._comm_to_game = CommunicationHandler()
        self._ml_name = ml_name

    def set_comm_to_game(self, recv_end, send_end):
        """
        Set communication objects for communicating with game process

        @param recv_end The communication object for receiving objects from game process
        @param send_end The communication object for sending objects to game process
        """
        self._comm_to_game.set_recv_end(recv_end)
        self._comm_to_game.set_send_end(send_end)

    def start_recv_obj_thread(self):
        """
        Start a thread to keep receiving objects from the game
        """
        self._obj_queue = Queue(15)

        thread = Thread(target=self._keep_recv_obj_from_game)
        thread.start()

    def _keep_recv_obj_from_game(self):
        """
        Keep receiving object from the game and put it in the queue

        If the queue is full, the received object will be dropped.
        """
        while True:
            if self._obj_queue.full():
                self._obj_queue.get()
                print("Warning: The object queue for the process '{}' is full. "
                      "Drop the oldest object."
                      .format(self._ml_name))

            obj = self._comm_to_game.recv()
            self._obj_queue.put(obj)
            if obj is None:  # Received `None` from the game, quit the loop.
                break

    def recv_from_game(self):
        """
        Receive an object from the game process

        @return The received object
        """
        try:
            return self._obj_queue.get()
        except Exception:
            return None

    def send_to_game(self, obj):
        """
        Send an object to the game process

        @param obj An object to be sent
        """
        try:
            self._comm_to_game.send(obj)
        except BrokenPipeError:
            print("Process '{}': The connection to the game process is closed."
                  .format(self._ml_name))


class TransitionCommManager:
    """
    The communication manager for the transition process
    """

    def __init__(self, recv_end=None, send_end=None):
        self._comm_to_game = CommunicationHandler()
        self.set_comm_to_game(recv_end, send_end)
        self.count = 0

    def start_recv_obj_thread(self):
        """
        Start a thread to keep receiving objects from the game
        """
        self._obj_queue = Queue(1500)

        thread = Thread(target=self._keep_recv_obj_from_game)
        thread.start()

    def _keep_recv_obj_from_game(self):
        """
        Keep receiving object from the game and put it in the queue

        """
        while True:
            if self._obj_queue.full():
                # self._obj_queue.get()
                print("Warning: The object queue for the process 'ws_comm' is full. ")

            obj = self._comm_to_game.recv()
            self._obj_queue.put(obj)
            if obj is None:  # Received `None` from the game, quit the loop.
                break

    def set_comm_to_game(self, recv_end, send_end):
        """
        Set communication objects for communicating with game process

        @param recv_end The communication object for receiving objects from game process
        @param send_end The communication object for sending objects to game process
        """
        self._comm_to_game.set_recv_end(recv_end)
        self._comm_to_game.set_send_end(send_end)

    def recv_from_game(self):
        """
        Receive the object sent from the game process
        """
        try:
            return self._obj_queue.get(block=True, timeout=WS_WAIT_GAME_TIMEOUT)
        except Exception as e:
            print(e.__str__())
            return None

    def send_exception(self, exception):
        """
        Send an exception to the game process
        """
        self._comm_to_game.send(exception)
