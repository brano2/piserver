from pathlib import Path
from threading import Event, Thread
from typing import Callable, ClassVar, Dict, List, Optional, Set


def get_temperature() -> float:
    """ Returns temperature in degC"""
    return 12.345


class Ds18b20:
    _instances: ClassVar[Dict[Path, 'Ds18b20']] = {}

    @classmethod
    def _find_all(cls):
        known_sensor_dirs = set(cls._instances.keys())
        for path in Path('/sys/bus/w1/devices').glob('28-*'):
            if path.is_dir() and (path/'id').exists() and (path/'temperature').exists():
                if path in known_sensor_dirs:
                    known_sensor_dirs.remove(path)
                else:
                    cls._instances[path] = cls(path)  # New sensor found
        # Remove old sensors that are no longer connected
        for sensor_dir in known_sensor_dirs:
            cls._instances[sensor_dir].stop()
            del cls._instances[sensor_dir]

    @classmethod
    def get_all(cls) -> List['Ds18b20']:
        cls._find_all()
        return list(cls._instances.values())

    def __init__(self, directory: Path):
        self._id:                bytes                        = (directory/'id').read_bytes()
        self._temperature_file:  Path                         = directory/'temperature'
        self._temperature:       Optional[float]              = None
        self._auto_updating:     bool                         = False
        self._updater:           Optional[Thread]             = None
        self._temperature_ready: Event                        = Event()
        self._listeners:         Set[Callable[[float], None]] = set()
        self._operational:       bool                         = True

        self.start()

    @property
    def id(self) -> bytes:
        return self._id

    @property
    def operational(self) -> bool:
        return self._operational

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
        # Read the temperature safely
        if self._temperature_file.exists():
            temp_mC = self._temperature_file.read_text()  # Takes about 800ms usually
        else:
            temp_mC = ''  # Empty string is also often read when the sensor is disconnected
        self._operational = temp_mC != ''

        # Update
        if self._operational:
            self._temperature = int(temp_mC)/1000.0
        if not self._temperature_ready.is_set():
            self._temperature_ready.set()

        # Notify listeners
        for listener in self._listeners:
            listener(self._temperature)

    def _auto_update(self):
        while self._auto_updating:
            self._update_temperature()
