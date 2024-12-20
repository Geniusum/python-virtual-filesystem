def get_list_a_not_in_b(a:list, b:list):
    return [_ for _ in a if _ not in b]

class Path():
    class NotAValidChar(BaseException): ...

    def __init__(self, *args):
        self.segments = []
        for arg in args:
            for char in arg:
                if not char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_éàÉÀùìÙÌôÔâÂ":
                    raise NotAValidChar(char)
            self.segments.append(arg)

    def absolute(self):
        return "/".join(self.segments).lower()

class Storage():
    # Note : Encoded in UTF-8

    class ByteLenghtException(BaseException): ...
    class PathNotExists(BaseException): ...
    class PathAlreadyExists(BaseException): ...
    
    def __init__(self, sizebytes:int):
        self.paths = {"": []}
        self.bytes = b"\x00" * sizebytes

    def assign_to_path(self, path:Path, addresses:list[int]):
        self.paths[path.absolute()] = addresses

    def assign(self, addresses:list[int]):
        self.paths[""] += addresses

    def get_all_taken_addresses(self):
        addresses = []
        for path_addresses in self.paths.values():
            addresses += path_addresses
        return addresses

    def get_all_addresses(self):
        return list(range(0, len(self.bytes)))

    def get_free_addresses(self):
        return get_list_a_not_in_b(self.get_all_addresses(), self.get_all_taken_addresses())

    def get_free_address(self):
        free_addresses = self.get_free_addresses()
        if len(free_addresses):
            return free_addresses[0]
        return None

    def put_byte(self, address:int, byte:bytes):
        if len(byte) > 1:
            raise self.ByteLenghtException(byte)
        b = [*self.bytes.decode("utf-8")]
        b[address] = byte.decode("utf-8")
        self.bytes = "".join(b).encode("utf-8")
        self.assign([address])
        return address

    def put_bytes(self, address:int, bytes_:bytes):
        r_addresses = []
        for byte_address in range(address, len(bytes_)):
            self.put_byte(byte_address, bytes_[byte_address])
            r_addresses.append(byte_address)
        return r_addresses

    def add_byte(self, byte:bytes):
        address = self.get_free_address()
        self.put_byte(address, byte)
        return address

    def add_bytes(self, bytes_:bytes):
        r_addresses = []
        for i, byte in enumerate(bytes_):
            address = self.get_free_address()
            self.put_byte(address, bytes_.decode("utf-8")[i].encode("utf-8"))
            r_addresses.append(address)
        return r_addresses

    def get_byte(self, address:int):
        b = [*self.bytes.decode("utf-8")]
        return b[address].encode("utf-8")

    def free_address(self, address:int):
        for path_addresses in self.paths.values():
            try:
                while address in path_addresses:
                    path_addresses.remove(address)
            except: pass

    def handle_file_exists(self, path:Path):
        if path.absolute() in self.paths.keys():
            raise self.PathAlreadyExists(path.absolute())

    def handle_file_not_exists(self, path:Path):
        if not path.absolute() in self.paths.keys():
            raise self.PathNotExists(path.absolute())

    def create_file(self, path:Path):
        self.handle_file_exists(path)
        
        self.paths[path.absolute()] = []
        return []

    def edit_file(self, path:Path, bytes_:bytes):
        self.handle_file_not_exists(path)
    
        for path_address in self.paths[path.absolute()]:
            self.free_address(path_address)

        r_addresses = self.add_bytes(bytes_)
        
        self.paths[path.absolute()] = r_addresses

        return r_addresses

    def delete_file(self, path:Path):
        self.handle_file_not_exists(path)
    
        for path_address in self.paths[path.absolute()]:
            self.free_address(path_address)

        self.paths.pop(path)

    def get_file(self, path:Path):
        self.handle_file_not_exists(path)
    
        buffer = b""
        
        for path_address in self.paths[path.absolute()]:
            buffer += self.get_byte(path_address)

        return buffer
