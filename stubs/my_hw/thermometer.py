from pathlib import Path
from threading import Event, Thread
from typing import Callable, List, Optional, Set


def get_temperature() -> float:
    """ Returns temperature in degC"""
    return 12.345


class Ds18b20:

    @classmethod
    def find_all(cls) -> List['Ds18b20']:
        return [cls(path) for path in Path('/sys/bus/w1/devices').glob('28-*') if path.is_dir()]

    def __init__(self, directory: Path):
        self._id:                bytes                        = (directory/'id').read_bytes()
        self._temperature_file:  Path                         = directory/'temperature'
        self._temperature:       Optional[float]              = None
        self._auto_updating:     bool                         = False
        self._updater:           Optional[Thread]             = None
        self._temperature_ready: Event                        = Event()
        self._listeners:         Set[Callable[[float], None]] = set()

        self.start()

    @property
    def id(self) -> bytes:
        return self._id

    def get_temperature(self) -> float:
        if not self._auto_updating:
            self._update_temperature()
        else:
            self._temperature_ready.wait()
        return self._temperature

    def start(self):
        self._auto_updating = True
        self._temperature_ready.clear()
        self._updater = Thread(target=self._auto_update, daemon=True)
        self._updater.start()

    def stop(self):
        self._auto_updating = False
        self._updater.join()

    def add_listener(listener: Callable[[float], None]):
        self._listeners.add(listener)

    def remove_listener(listener: Callable[[float], None]):
        self._listeners.remove(listener)

    def _update_temperature(self):
        temp_mC = int(self._temperature_file.read_text())
        self._temperature = temp_mC/1000.0
        if not self._temperature_ready.is_set():
            self._temperature_ready.set()

        # Notify listeners
        for listener in self._listeners:
            listener(self._temperature)

    def _auto_update(self):
        while self._auto_updating:
            self._update_temperature()
