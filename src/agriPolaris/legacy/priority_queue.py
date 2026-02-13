from __future__ import annotations

from agriPolaris.legacy.dependency import DLLNode, Entry

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


class DLLPriorityQueue:
    def __init__(self):
        self.size = 0
        self.head_guard = DLLNode(None)
        self.tail_guard = DLLNode(None)
        self.head_guard.set_next(self.tail_guard)
        self.tail_guard.set_prev(self.head_guard)

    def __repr__(self):
        display = []
        node = self.head_guard.get_next()
        while node != self.tail_guard:
            entry = node.get_item()
            priority = -entry.key
            lgu, crop = entry.value
            display.append(
                f"<LGU: {GREEN + BOLD + lgu + RESET}| "
                f"Priority: {YELLOW + BOLD}{priority}{RESET}| Crop: {crop}>"
            )
            node = node.get_next()

        display_text = ", ".join(display)
        return "{" + display_text + "}"

    def is_empty(self):
        return self.size == 0

    def to_object(self):
        result = []
        node = self.head_guard.get_next()

        while node != self.tail_guard:
            key = node.get_item().key
            value = node.get_item().value

            if isinstance(value, tuple) and len(value) == 2:
                lgu, crop = value
            else:
                lgu, crop = value, "Unknown"

            result.append({"priority": -key, "lgu": lgu, "crop": crop})
            node = node.get_next()

        return result


class UnsortedPQ(DLLPriorityQueue):
    def find_min_node(self):
        if self.is_empty():
            raise Exception("Empty PQ: cannot find min")

        current = self.head_guard.get_next()
        min_node = current

        while current != self.tail_guard:
            if current.get_item().key < min_node.get_item().key:
                min_node = current
            current = current.get_next()

        return min_node

    def insert(self, key, value):
        entry = Entry(key, value)
        ins_node = DLLNode(entry)
        first = self.head_guard.get_next()

        ins_node.set_prev(self.head_guard)
        ins_node.set_next(first)

        self.head_guard.set_next(ins_node)
        first.set_prev(ins_node)
        self.size += 1

    def remove_min(self):
        if self.is_empty():
            raise Exception("Empty PQ: cannot remove min")

        min_node = self.find_min_node()

        prev_node = min_node.get_prev()
        next_node = min_node.get_next()
        prev_node.set_next(next_node)
        next_node.set_prev(prev_node)

        min_node.set_next(None)
        min_node.set_prev(None)
        self.size -= 1
        return min_node.get_item().value

    def min(self):
        if self.is_empty():
            raise Exception("Empty PQ: no min")
        return self.find_min_node().get_item().value


class SortedPQ(DLLPriorityQueue):
    def insert(self, key, value):
        entry = Entry(key, value)
        ins_node = DLLNode(entry)
        current = self.head_guard.get_next()

        while current != self.tail_guard and current.get_item().key <= ins_node.get_item().key:
            current = current.get_next()

        prev_node = current.get_prev()
        ins_node.set_prev(prev_node)
        ins_node.set_next(current)
        prev_node.set_next(ins_node)
        current.set_prev(ins_node)

        self.size += 1

    def remove_from_pq(self, crop, lgu):
        del crop
        node = self.head_guard.get_next()

        while node != self.tail_guard:
            entry = node.get_item()
            value = entry.value
            if isinstance(value, tuple) and len(value) == 2 and value[0] == lgu:
                prev_node = node.get_prev()
                next_node = node.get_next()
                prev_node.set_next(next_node)
                next_node.set_prev(prev_node)

                node.set_next(None)
                node.set_prev(None)
                self.size -= 1
                return
            node = node.get_next()

    def remove_min(self):
        if self.is_empty():
            raise Exception("Empty PQ: cannot remove min")

        min_node = self.head_guard.get_next()
        new_min = min_node.get_next()
        new_min.set_prev(self.head_guard)
        self.head_guard.set_next(new_min)

        min_node.set_prev(None)
        min_node.set_next(None)

        self.size -= 1
        return min_node.get_item().value

    def min(self):
        if self.is_empty():
            raise Exception("Empty PQ: no min")
        return self.head_guard.get_next().get_item().value
