class MemoryManager:
    def __init__(self, heap_size=1024):
        self.heap_size = heap_size
        self.heap = [None] * heap_size
        self.allocated_blocks = {}  # start_address -> size
        self.named_blocks = {}      # name -> start_address
        self.free_blocks = [(0, heap_size)]  # List of (start, size) tuples for free blocks

    def detect_memory_leaks(self):
        leaks = {}
        for addr, size in self.allocated_blocks.items():
            name = None
            for n, a in self.named_blocks.items():
                if a == addr:
                    name = n
                    break
            # Ensure that leaks contain a tuple (size, name), not just address or size
            leaks[addr] = (size, name)  # Storing the tuple
        return leaks



    def malloc(self, size, name=None):
        if size <= 0 or size > self.heap_size:
            raise ValueError("Invalid size for allocation")

        for idx, (start, free_size) in enumerate(self.free_blocks):
            if free_size >= size:
                # Allocate memory
                for i in range(start, start + size):
                    self.heap[i] = "ALLOCATED"
                self.allocated_blocks[start] = size

                if name:
                    self.named_blocks[name] = start

                # Update free blocks: split if necessary
                if free_size > size:
                    self.free_blocks[idx] = (start + size, free_size - size)
                else:
                    del self.free_blocks[idx]  # Entire block is now allocated

                return start

        raise MemoryError("Not enough memory available")

    def free(self, identifier):
        if isinstance(identifier, str):
            if identifier not in self.named_blocks:
                raise ValueError(f"No allocation found with name '{identifier}'")
            start = self.named_blocks.pop(identifier)
        else:
            start = identifier

        if start in self.allocated_blocks:
            size = self.allocated_blocks.pop(start)
            for i in range(start, start + size):
                self.heap[i] = None

            # Merge the freed block back into free blocks
            self.free_blocks.append((start, size))
            self.free_blocks.sort()  # Keep free blocks sorted by starting address

        else:
            raise ValueError("Invalid memory address or block name")

    def get_address_by_name(self, name):
        return self.named_blocks.get(name, None)

    def get_heap_status(self):
        return self.heap

    def get_named_blocks(self):
        return self.named_blocks

    def detect_fragmentation(self):
        # Just return the free blocks for visualization
        return self.free_blocks

    def detect_memory_leaks(self):
        leaks = {}
        for addr, size in self.allocated_blocks.items():
            name = None
            for n, a in self.named_blocks.items():
                if a == addr:
                    name = n
                    break
            leaks[addr] = (size, name)
        return leaks
