import os
import threading
import time

from frida_tools.application import Reactor
import frida

input_str = """111111111111111111111111111111111111111111111111\n"""
print("input:", input_str)

target = ".\\TrueOperator.exe"
script_file = "trace_input_windows.js"
time_to_input = 0
android = False
pause_before_target_loaded = True
attach = False


if android:
    args = [target]
else:
    args = [target,input_str]

class Application:
    def __init__(self):
        self._stop_requested = threading.Event()
        self._reactor = Reactor(run_until_return=lambda reactor: self._stop_requested.wait())
        if android:
            self._device = frida.get_usb_device()
        else:
            self._device = frida.get_local_device()
        self._sessions = set()
        self._pids = set()

        self._device.on("child-added", lambda child: self._reactor.schedule(lambda: self._on_child_added(child)))
        self._device.on("child-removed", lambda child: self._reactor.schedule(lambda: self._on_child_removed(child)))
        self._device.on("output", lambda pid, fd, data: self._reactor.schedule(lambda: self._on_output(pid, fd, data)))

    def run(self):
        self._reactor.schedule(lambda: self._start())
        self._reactor.run()

    def _start(self):
        global args

        argv = args
        env = {
            "BADGER": "badger-badger-badger",
            "SNAKE": "mushroom-mushroom",
        }

        print(f"✔ spawn(argv={argv})")
        if android:
            if attach:
                pid = self._device.get_frontmost_application().pid
            else:
                pid = self._device.spawn(argv)
        else:
            if attach:
                pid = self._device.get_process(target).pid
            else:
                pid = self._device.spawn(argv, env=env, stdio="pipe")
        self._instrument(pid)

    def _stop_if_idle(self):
        if len(self._sessions) == 0:
            self._stop_requested.set()

    def _instrument(self, pid):
        global script_file

        self._pids.add(pid)

        print(f"✔ attach(pid={pid})")
        session = self._device.attach(pid)

        session.on(
            "detached",
            lambda reason: self._reactor.schedule(
                lambda: self._on_detached(pid, session, reason)
            )
        )
        if not android:
            print("✔ enable_child_gating()")
            session.enable_child_gating()

        print("✔ create_script()")
        with open(script_file, "r", encoding="utf-8") as file:
            content = file.read()

        script = session.create_script(content)

        script.on(
            "message",
            lambda message, data: self._reactor.schedule(
                lambda: self._on_message(pid, message)
            )
        )

        print("✔ load()")
        script.load()
        if not pause_before_target_loaded:
            self._device.resume(pid)
        self._sessions.add(session)

    def write_input(self, pid, input_str):
        global time_to_input

        if time_to_input >= 0:
            time.sleep(time_to_input)
        else:
            input("Enter to input")
        if not android:
            self._device.input(target=pid, data=input_str.encode())

    def _on_child_added(self, child):
        print(f"⚡ child_added: {child}")
        self._instrument(child.pid)

    def _on_child_removed(self, child):
        print(f"⚡ child_removed: {child}")

    def _on_output(self, pid, fd, data):
        print(data.decode(errors="ignore"), end="", flush=True)

    def _on_detached(self, pid, session, reason):
        print(f"⚡ detached: pid={pid}, reason='{reason}'")
        self._sessions.discard(session)
        self._reactor.schedule(self._stop_if_idle, delay=0.5)

    def _on_message(self, pid, message):
        if message["type"] == "send" and message["payload"] == "script_ready":
            print(f"✔ resume(pid={pid})")
            if (not attach) and pause_before_target_loaded:
                self._device.resume(pid)
                threading.Thread(
                    target=self.write_input,
                    args=(pid, input_str),
                    daemon=True
                ).start()
        else:
            print(f"⚡ message: pid={pid}, payload={message}")

    def kill_all(self):
        print("\n[!] Ctrl+C, killing frida spawned processes...")

        for pid in list(self._pids):
            try:
                print(f"[!] kill pid={pid}")
                self._device.kill(pid)
            except Exception as e:
                print(f"[!] kill pid={pid} failed: {e}")

        os._exit(130)


app = Application()

t = threading.Thread(target=app.run, daemon=True)
t.start()

try:
    while t.is_alive():
        t.join(0.2)
except KeyboardInterrupt:
    app.kill_all()