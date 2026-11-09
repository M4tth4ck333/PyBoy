import serial
from pyboy import PyBoy

class RobotGameBridge:
    def __init__(self, rom_path: str, serial_port: str = "/dev/ttyACM0", baudrate: int = 115200):
        # PyBoy Instanz starten
        self.pyboy = PyBoy(rom_path)
        # Serielle Verbindung zum SKR-Board / Roboter-Bausatz
        try:
            self.robot_serial = serial.Serial(serial_port, baudrate, timeout=1)
        except Exception:
            self.robot_serial = None
            print("Warnung: Kein physisches Board angeschlossen. Simuliere Hardware.")

    def send_hardware_command(self, gcode: str):
        """Sendet Befehle an den Roboter-Bausatz oder SimpleEngraver"""
        if self.robot_serial and self.robot_serial.is_open:
            self.robot_serial.write((gcode + "\n").encode('utf-8'))
        else:
            print(f"[HW-Simulation]: {gcode}")

    def run_tick_loop(self):
        """Hauptschleife, die das Spiel und die Hardware synchronisiert"""
        running = True
        while running:
            # PyBoy einen Frame weiterführen
            running = self.pyboy.tick()

            # Beispiel: Lese RAM-Adresse aus (z.B. Spieler-Position oder Lebensenergie)
            # player_hp = self.pyboy.get_memory_value(0xD000) 

            # Wenn ein bestimmtes Spiel-Event eintritt -> Roboter triggern
            # if player_hp < 5:
            #     self.send_hardware_command("G1 X10 Y10 F1000") # Roboter bewegt sich

        self.pyboy.stop()
        if self.robot_serial:
            self.robot_serial.close()

# Verwendung:
# bridge = RobotGameBridge("roms/game.gb")
# bridge.run_tick_loop()
