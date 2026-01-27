#!/usr/bin/env python
# coding: utf-8
# Use pykiba after V3.1 – originally named pykibaNew
#     - Added timeout before sending a command
#     - Replaced .split(',') with re.split
#     - Appended '\n' when sending
#     - No use of the Walrus operator!
#     - Compatible with old functions, but modernized
# V3.1 – Added def install_arduino_commands(self)
#=================================================
# Serves Arduino running DipoleMagnet firmware
#--------------------------------------------
# hello
# megaatmega2560

from tools import serial_ports_list, print_my_ip, search_by_manufacturer
from pykiba import PykiDev

import time


class DipoleMagnet(PykiDev):
    """Class for interacting with Arduino running DipoleMagnet firmware.

    Extends PykiDev and automatically installs Arduino commands using the 'help' command.
    Also provides calibrated analog readings via polynomial correction.
    """
    def __init__(self, **kargs):
        """Constructor for DipoleMagnet.

        Parameters
        ----------
        port : str
            Serial port name (e.g. '/dev/ttyACM0')
        baudrate : int, optional
            Baudrate for serial communication (default is 9600).
        install_cmd : bool, optional
            Whether to auto-install commands using 'help' (default is False).
        """
        super().__init__(**kargs)
        time.sleep(1)
        self.command("mode 3")
        self.channels_number = len(self.uv())
        self.poly_dict = {
            "equ": [1, 0],                   # Identity function y = x
            "volts": [1.0 / 1000.0, 0],       # Convert mV to V
            "ampers": [-0.009505813877335156, 23.874869386080572],
            "amperso": [-0.009788782891869855, 24.159543475504957]
        }
        self.string_rep += "\n" + str(self.hello()[0])
        
    def all_references(self,*args):
        """Sets all references 
        Parameters
        ----------
            reference number: 0,1,2
            or None
        Returns
        -------
        [channels ref]   
        """ 
        if args:
            ref_to_be_set = int(args[0])
            if  ref_to_be_set < 0  or   ref_to_be_set > 2:
                ref_to_be_set = 2
        
            for i in range(self.channels_number):
                self.aref(i,ref_to_be_set )
            
        return self.aref()


    def aread(self, pin=None, calib=None, raw=False):
        """Reads one or more analog inputs, optionally applying calibration.

        Parameters
        ----------
        pin : int, optional
            Specific channel to read. If None, all channels are read.
        calib : str, optional
            Name of a polynomial defined in self.poly_dict to apply as calibration.
        raw : bool, optional
            If True, reads using ur() (raw); otherwise uses uv() (filtered).

        Returns
        -------
        list or float
            Raw or calibrated readings.
        """
        if pin is not None and pin < self.channels_number:
            tmp_val = self.ur(pin)[1] if raw else self.uv(pin)
            if calib:
                tmp_val = self.polynom(tmp_val, calib)
        else:
            tmp_val = [inp[1] for inp in self.ur()] if raw else self.uv()
            if calib:
                tmp_val = [self.polynom(inp, calib) for inp in tmp_val]

        return tmp_val

    def all_references(self, *args):
        """Sets or gets reference voltage settings for all analog channels.

        Parameters
        ----------
        *args : int, optional
            Reference type: 0, 1, or 2. If omitted, returns current settings.

        Returns
        -------
        list
            Current reference settings.
        """
        if args:
            ref_to_be_set = int(args[0])
            if ref_to_be_set < 0 or ref_to_be_set > 2:
                ref_to_be_set = 2
            for i in range(self.channels_number):
                self.aref(i, ref_to_be_set)

        return self.aref()

    def polynom(self, arg, name_of_coef):
        """Applies a named polynomial function to a value.

        Parameters
        ----------
        arg : float
            Input value.
        name_of_coef : str
            Name of the polynomial in self.poly_dict.

        Returns
        -------
        float
            Result after applying the polynomial.
        """
        coef = self.poly_dict.get(name_of_coef, None)
        if not coef:
            raise Exception("Polynomial not found.")

        result = 0
        for i, c in enumerate(reversed(coef)):
            result += pow(arg, i) * c

        return result

    def add_polynom(self, coef, polynom_name):
        """Adds or updates a polynomial in poly_dict.

        Parameters
        ----------
        coef : list of float
            Coefficients in form [aN, ..., a1, a0]
        polynom_name : str
            Name of the polynomial.
        """
        self.poly_dict[polynom_name] = coef

    def polynoms_list(self):
        """Returns a string listing all defined polynomials.

        Returns
        -------
        str
            Human-readable representation of self.poly_dict.
        """
        return ", ".join(f"{k}: {v}" for k, v in self.poly_dict.items())

    def polynoms_to_file(self, file_name):
        """Saves polynomial dictionary to a file in JSON format.

        Parameters
        ----------
        file_name : str
            File path to write to.
        """
        # with open(file_name, 'w', newline='') as f:
        #     print(f"File is opened as {f}")
        #     f.write(jsonpickle.encode(self.poly_dict, indent=4))
        #     f.flush()

    def polynoms_from_file(self, file_name):
        """Loads polynomial dictionary from a file.

        Parameters
        ----------
        file_name : str
            File path to read from.
        """
        # with open(file_name, 'r') as f:
        #     string = f.read()
        #     self.poly_dict = jsonpickle.decode(string)

    def defines(self):
        """Returns internal identity string.

        Returns
        -------
        str
            Informational string from self.string_rep.
        """
        return self.string_rep

    def __repr__(self):
        return self.string_rep

    def __str__(self):
        return self.string_rep

    def __del__(self):
        self.close()


if __name__ == '__main__':
    serving = False
    mname = 'Arduino'
    baudrate = 9600

    if not serving:
        lstedPorts = serial_ports_list()
        prt = search_by_manufacturer(lstedPorts, mname)
        ard = DipoleMagnet(port='/dev/ttyACM0', baudrate=baudrate)
        print(ard)
    else:
        import zerorpc
        lstedPorts = serial_ports_list()
        prt = search_by_manufacturer(lstedPorts, mname)
        print(f"Board with a name {mname} connected dev {prt}")
        print("Starting zerorpc server ...")
        print("To IP address")
        print_my_ip()
        print(":4242")
        s = zerorpc.Server(DipoleMagnet(port=prt, baudrate=baudrate))
        s.bind("tcp://0.0.0.0:4242")
        s.run()
