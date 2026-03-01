import os
import threading
import time

from frida_tools.application import Reactor

import frida

input_str = """DASCTF{1111111111111111111111111111111111111111}\n"""
print("input:",input_str)
target = "./Warning"
script_file = "trace_input.js"
args = [target,input_str]
time_to_input = 0
class Application:
    def __init__(self):
        self._stop_requested = threading.Event()
        self._reactor = Reactor(run_until_return=lambda reactor: self._stop_requested.wait())

        self._device = frida.get_local_device()
        self._sessions = set()

        self._device.on("child-added", lambda child: self._reactor.schedule(lambda: self._on_child_added(child)))
        self._device.on("child-removed", lambda child: self._reactor.schedule(lambda: self._on_child_removed(child)))
        self._device.on("output", lambda pid, fd, data: self._reactor.schedule(lambda: self._on_output(pid, fd, data)))

    def run(self):
        self._reactor.schedule(lambda: self._start())
        self._reactor.run()

    def _start(self):
        global args,input_str
        argv = args
        env = {
            "BADGER": "badger-badger-badger",
            "SNAKE": "mushroom-mushroom",
        }
        print(f"✔ spawn(argv={argv})")
        pid = self._device.spawn(argv, env=env, stdio="pipe")
        self._instrument(pid)

        self.write_input(pid,input_str)

    def _stop_if_idle(self):
        if len(self._sessions) == 0:
            self._stop_requested.set()

    def _instrument(self, pid):
        global script_file
        print(f"✔ attach(pid={pid})")
        session = self._device.attach(pid)
        session.on("detached", lambda reason: self._reactor.schedule(lambda: self._on_detached(pid, session, reason)))
        print("✔ enable_child_gating()")
        session.enable_child_gating()
        print("✔ create_script()")

        with open(script_file, 'r', encoding='utf-8') as file:
            content = file.read()
        script = session.create_script(
            content
        )
        script.on("message", lambda message, data: self._reactor.schedule(lambda: self._on_message(pid, message)))
        print("✔ load()")
        script.load()
        print(f"✔ resume(pid={pid})")
        self._device.resume(pid)
        self._sessions.add(session)

    def write_input(self, pid,input_str):
        global time_to_input
        if time_to_input>=0 :
            time.sleep(time_to_input)
        else:
            input("Enter to input")
        print(input_str.encode())
        self._device.input(target= pid,data=input_str.encode())

    def _on_child_added(self, child):
        global input_str
        print(f"⚡ child_added: {child}")
        self._instrument(child.pid)
        self.write_input(child.pid,input_str)


    def _on_child_removed(self, child):
        print(f"⚡ child_removed: {child}")

    def _on_output(self, pid, fd, data):
        print(f"⚡ ###### output: pid={pid}, fd={fd}")
        print(data.decode( errors='ignore'), end='')

    def _on_detached(self, pid, session, reason):
        print(f"⚡ detached: pid={pid}, reason='{reason}'")
        self._sessions.remove(session)
        self._reactor.schedule(self._stop_if_idle, delay=0.5)

    def _on_message(self, pid, message):
        print(f"⚡ message: pid={pid}, payload={message}")


app = Application()
app.run()