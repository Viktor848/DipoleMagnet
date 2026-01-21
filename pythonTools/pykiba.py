#!/usr/bin/env python
# coding: utf-8
# pykiba V3.0 – initially named pykibaNew
#     - Added timeout before sending a command
#     - Replaced .split(',') with re.split
#     - Appended '\n' when sending commands
# Note: No use of the Walrus operator!
# Compatible with old functions, but redesigned
# V3.1 – Added def install_arduino_commands(self)

import serial
import re
import time
from tools import print_my_ip, search_by_manufacturer, serial_ports_list


def prepare_line_to_send(*args):
    """Converts all input arguments into a formatted byte string ready to send via serial.

    Handles int, float, and string input types. Adds carriage return at the end.
    Floats are scaled (x1000) and appended with a marker "-3".

    Returns
    -------
    bytes
        A single byte string to send via serial.
    """
    output_buffer = []
    for word in args:
        if type(word) is int:
            word = str(word).encode()
        elif type(word) is float: 
            word = int(word * 1000)
            word = str(word).encode()
            word = word + b' -3'
        elif type(word) is str:
            word = word.encode()

        if word[-1] == 13:  # Remove trailing carriage return if exists
            word = word[:-1]

        output_buffer.append(word)
        output_buffer.append(b' ')

    output_buffer.pop(-1)  # Remove last space
    output_buffer.append(b'\r')

    return b''.join(output_buffer)


def parse_line(line):
    """Parses a byte line received from serial into Python types.

    Splits the line into tokens and attempts to convert each to int or float,
    otherwise returns them as strings.

    Parameters
    ----------
    line : bytes
        A raw line of serial data in bytes.

    Returns
    -------
    Union[int, float, str, List[Union[int, float, str]]]
        Parsed value or list of parsed values.
    """
    line = line.decode().strip()
    line = re.split(r"[, ;#!?:]+", line)

    output_val = [] 
    for word in line:   
        try:
            output_val.append(int(word))
            continue
        except ValueError:
            pass

        try:
            output_val.append(float(word))
            continue
        except ValueError:
            pass

        output_val.append(word)

    if len(output_val) == 1:
        output_val = output_val[0]
    elif output_val == []:
        output_val = None

    return output_val


class Pykiba(serial.Serial):
    """Main class to communicate with an Arduino running a serial command interpreter.

    Inherits from serial.Serial and provides methods to write and parse commands.
    """
    def __init__(self, **kargs):
        """Initializes the serial connection with given arguments.

        Parameters
        ----------
        port : str
            Serial device name (e.g., '/dev/ttyUSB0' or 'COM3')
        baudrate : int
            Serial baud rate (e.g., 9600)
        """
        super().__init__(**kargs)
        self.string_rep = f"Connected on {kargs} \n\n"
        self.timeout = 5
        _ = self.read_all()  # Clear initial buffer

    def write_line(self, *args):
        """Formats and sends a line to the Arduino.

        Uses prepare_line_to_send to format the data.
        Waits if the serial output buffer is not empty.
        """
        line_for_sending = prepare_line_to_send(*args)
        while self.out_waiting:
            pass
        self.echo_of_the_command = line_for_sending
        self.write(line_for_sending)
        self.flush()

    def raw_lines(self, *args, timeout=5):
        """Sends a command and returns raw response lines (unparsed).

        Parameters
        ----------
        *args : arguments passed to write_line
        timeout : float
            Time to wait for response.

        Returns
        -------
        List[bytes]
            List of lines received from Arduino.
        """
        tmp_timeout = self.timeout
        self.timeout = timeout
        _ = self.read_all()
        self.write_line(*args)
        ninput = self.readlines()
        self.timeout = tmp_timeout
        return ninput

    def command(self, *args, timeout=2.5):
        """Sends a command and returns parsed response from Arduino.

        This is the main method to communicate with Arduino and interpret
        numerical/string results returned.

        Returns float, int, list, or None depending on content.

        Parameters
        ----------
        *args : str/int/float
            The command and arguments.
        timeout : float
            Timeout for reading reply.

        Returns
        -------
        Parsed response.
        """
        tmp_timeout = self.timeout
        self.timeout = timeout
        self.flush()
        while self.out_waiting:
            pass
        time.sleep(0.25)
        _ = self.read_all()
        self.write_line(*args)
        return_value = []
        while True:
            line = self.readline()
            if not line:
                break
            if self.echo_of_the_command in line or b'>>' in line:
                continue
            line = parse_line(line)
            return_value.append(line)
            if '' in return_value:
                return_value.remove('')
                break
        if len(return_value) == 1:
            return_value = return_value[0]
        elif return_value == []:
            return_value = None
        self.echo_of_the_command = None
        self.timeout = tmp_timeout
        return return_value

    def __repr__(self):
        return self.string_rep

    def __str__(self):
        return self.string_rep

    def __del__(self):
        self.close()


class PykiDev(Pykiba):
    """Extended version of Pykiba with auto-installation of Arduino commands.

    If the Arduino supports a 'help' command, this class dynamically binds all available
    commands as methods on the object.
    """
    def __init__(self, **kargs):
        """Constructor. Inherits Pykiba and installs commands.

        Parameters:
        ----------
        **kargs : dict
            Serial connection parameters (port, baudrate, etc.)
        """
        super().__init__(**kargs)
        time.sleep(1)  # Wait for Arduino to initialize
        self.install_arduino_commands()

    def install_arduino_commands(self):
        """Detects Arduino commands via 'help' and binds them as methods.

        Automatically creates Python methods matching the Arduino's serial command list.
        Very useful for dynamic, readable command execution.
        """
        command_list = self.command("help")
        for cmd in command_list:
            def function_template(*args, captured_name=cmd):
                return self.command(captured_name, *args)
            setattr(self, cmd, function_template)

        for cmd in self.command('help'):
            self.string_rep += cmd + '\n'


if __name__ == '__main__':
    serving = False
    usb_manifacturer_name = 'Arduino'
    baudrate = 9600

    if not serving:
        lstedPorts = serial_ports_list()
        prt = search_by_manufacturer(lstedPorts, usb_manifacturer_name)
        ard = PykiDev(port=prt, baudrate=baudrate)
        print(ard)
    else:
        import zerorpc
        lstedPorts = serial_ports_list()
        prt = search_by_manufacturer(lstedPorts, usb_manifacturer_name)
        print(f"Board with name {usb_manifacturer_name} connected dev {prt}")
        print("Starting zerorpc server ...")
        print("To IP address")
        print_my_ip()
        print(":4242")
        s = zerorpc.Server(Pykiba(port=prt, baudrate=baudrate, install_cmd=True))
        s.bind("tcp://0.0.0.0:4242")
        s.run()
