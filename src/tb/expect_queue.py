import collections
import logging

log = logging.getLogger("cocotb")

class ExpectQueue:
    def __init__(self, name="expect_queue"):
        self.queue = collections.deque()
        self.name = name

    def expect(self, expectation):
        log.debug(f"{self.name}: expecting {expectation}")
        self.queue.append(expectation)

    def check(self, actual):
        log.debug(f"{self.name}: checking {actual}")
        assert len(self.queue) > 0, f"{self.name}: unexpected actual: {actual}"
        expected = self.queue.popleft()
        assert expected == actual, f"{self.name}: mismatch [E, R]: [{expected},{actual}]"

    def clear(self):
        self.queue.clear()

    def get_count(self):
        return len(self.queue)

    def teardown(self, allowed_items_remaining=0):
        assert len(self.queue) == allowed_items_remaining, f"{self.name}: {len(self.queue)} expectations remaining after test (vs {allowed_items_remaining} allowed)"
        