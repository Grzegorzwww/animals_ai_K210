import time

class GSMModem:
    def __init__(self, uart, phone_number='48796070732'):
        self.uart = uart
        self.phone_number = phone_number

        # Komendy AT
        self.COMMAND_AT = "AT"
        self.AT_CSQ = "AT+CSQ"
        self.AT_COPS = "AT+COPS?"
        self.AT_CCID = "AT+CCID?"
        self.AT_CREG = "AT+CREG?"
        self.TEXT_MODE = "AT+CMGF=1"
        self.PREFIX_PHONE_NUMER = "AT+CMGS="
        self.RECIVE_SMS = "AT+CNMI=1,2,0,0,0"
        self.RECIVE_SMS2 = "AT+CMGL=\"ALL\""
        self.SET_DEFAULT_BAUDRATE = "AT+IPR=9600"
        self.DELETE_ALL_MESSAGES = "AT+CMGD=1,4"

    def send_command(self, cmd, delay=2):
        """Wysyła komendę i czeka na odpowiedź."""
        full_cmd = cmd + '\r\n'
        print(f"[WYSYŁAM] {cmd}")
        self.uart.write(full_cmd.encode('utf-8'))
        time.sleep(delay)
        #self.read_response()

    def read_response(self):
        """Czyta dane z UART jeśli są dostępne."""
        #while self.uart.in_waiting:
            #data = self.uart.readline().decode('utf-8', errors='ignore').strip()
            #if data:
                #print(f"[ODEBRANO] {data}")

    def initialize_modem(self):
        self.send_command(self.COMMAND_AT)
        self.send_command(self.AT_CSQ)
        self.send_command(self.AT_COPS)
        self.send_command(self.AT_CREG)
        self.send_command(self.TEXT_MODE)

    def send_sms(self, msg):
        cmd = f'{self.PREFIX_PHONE_NUMER}"+{self.phone_number}"'
        self.send_command(cmd, delay=4)

        self.uart.write(msg.encode('utf-8'))
        time.sleep(2)

        self.uart.write(chr(26).encode('utf-8'))  # CTRL+Z
        print("[INFO] Wysłano znak końca wiadomości (CTRL+Z)")
        time.sleep(4)
        self.read_response()

    def manual_command(self, cmd):
        self.send_command(cmd)
