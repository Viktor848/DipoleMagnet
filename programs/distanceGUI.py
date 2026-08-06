#!/usr/bin/env python3
"""Simple Tkinter GUI for the distanceTest program.

Features:
- List available serial ports and select one
- Connect / Disconnect to device (DipoleMagnet)
- Start / Stop live polling of sensors (1s interval)
- Display left/right sensor values and computed gaps
- Simple log output
"""
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import serial.tools.list_ports

# Ensure pythonTools parent directory is importable (DipoleMagnet.py lives in ..)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import DipoleMagnet
except Exception as exc:
    DipoleMagnet = None


class DistanceGUI:
    def __init__(self, root):
        self.root = root
        root.title('Distance Monitor')
        # allow main frame to expand
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        self.ard = None
        self.poll_thread = None
        self.running = False
        self.connect_thread = None
        self.connecting = False
        self.connect_timeout_job = None
        self.connect_start_time = None

        main = ttk.Frame(root, padding=10)
        main.grid(sticky='nsew')

        # Port selection
        port_frame = ttk.Labelframe(main, text='Serial Port')
        port_frame.grid(row=0, column=0, sticky='ew')
        port_frame.columnconfigure(1, weight=1)

        self.port_cb = ttk.Combobox(port_frame, values=[], state='readonly', width=30)
        self.port_cb.grid(row=0, column=0, padx=(6,4), pady=6)
        self.refresh_btn = ttk.Button(port_frame, text='Refresh', command=self.refresh_ports)
        self.refresh_btn.grid(row=0, column=1, padx=4)
        self.connect_btn = ttk.Button(port_frame, text='Connect', command=self.toggle_connect)
        self.connect_btn.grid(row=0, column=2, padx=4)
        self.connect_status = ttk.Label(port_frame, text='')
        self.connect_status.grid(row=1, column=0, columnspan=3, sticky='w', padx=6)

        # Sensor readouts
        read_frame = ttk.Labelframe(main, text='Sensors')
        read_frame.grid(row=1, column=0, sticky='ew', pady=(8,0))

        ttk.Label(read_frame, text='Left Distance:').grid(row=0, column=0, sticky='w', padx=6, pady=2)
        self.left_var = tk.StringVar(value='—')
        ttk.Label(read_frame, textvariable=self.left_var).grid(row=0, column=1, sticky='w')

        ttk.Label(read_frame, text='Right Distance:').grid(row=1, column=0, sticky='w', padx=6, pady=2)
        self.right_var = tk.StringVar(value='—')
        ttk.Label(read_frame, textvariable=self.right_var).grid(row=1, column=1, sticky='w')

        ttk.Label(read_frame, text='Left Pole:').grid(row=2, column=0, sticky='w', padx=6, pady=2)
        self.gap1_var = tk.StringVar(value='—')
        ttk.Label(read_frame, textvariable=self.gap1_var).grid(row=2, column=1, sticky='w')

        ttk.Label(read_frame, text='Right Pole:').grid(row=3, column=0, sticky='w', padx=6, pady=2)
        self.gap2_var = tk.StringVar(value='—')
        ttk.Label(read_frame, textvariable=self.gap2_var).grid(row=3, column=1, sticky='w')

        ttk.Label(read_frame, text='Left Gap:').grid(row=4, column=0, sticky='w', padx=6, pady=2)
        self.leftgap_var = tk.StringVar(value='—')
        ttk.Label(read_frame, textvariable=self.leftgap_var).grid(row=4, column=1, sticky='w')

        ttk.Label(read_frame, text='Right Gap:').grid(row=5, column=0, sticky='w', padx=6, pady=2)
        self.rightgap_var = tk.StringVar(value='—')
        ttk.Label(read_frame, textvariable=self.rightgap_var).grid(row=5, column=1, sticky='w')

        ttk.Label(read_frame, text='Gap Diff:').grid(row=6, column=0, sticky='w', padx=6, pady=2)
        self.gapdiff_var = tk.StringVar(value='—')
        ttk.Label(read_frame, textvariable=self.gapdiff_var).grid(row=6, column=1, sticky='w')

        # Controls
        ctrl_frame = ttk.Frame(main)
        ctrl_frame.grid(row=2, column=0, sticky='ew', pady=(8,0))
        self.start_btn = ttk.Button(ctrl_frame, text='Start', command=self.start_polling, state='disabled')
        self.start_btn.grid(row=0, column=0, padx=4)
        self.stop_btn = ttk.Button(ctrl_frame, text='Stop', command=self.stop_polling, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=4)
        self.save_btn = ttk.Button(ctrl_frame, text='Save Log', command=self.save_log)
        self.save_btn.grid(row=0, column=2, padx=4)

        # Log
        log_frame = ttk.Labelframe(main, text='Log')
        log_frame.grid(row=3, column=0, sticky='nsew', pady=(8,0))
        main.rowconfigure(3, weight=1)
        main.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state='disabled')
        self.log_text.grid(row=0, column=0, sticky='nsew')

        self.refresh_ports()

        # ensure window is large enough for contents
        root.update_idletasks()
        try:
            w = main.winfo_reqwidth()
            h = main.winfo_reqheight()
            root.minsize(w + 40, h + 40)
        except Exception:
            pass

        root.protocol('WM_DELETE_WINDOW', self.on_close)

    def refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_cb['values'] = ports
        if ports and not self.port_cb.get():
            self.port_cb.set(ports[-1])
        self.log('Ports: {}'.format(', '.join(ports) or 'none'))

    def toggle_connect(self):
        if self.ard:
            self.disconnect()
        else:
            self.start_connect()

    def start_connect(self):
        port = self.port_cb.get()
        if not port:
            messagebox.showwarning('No port', 'Please select a serial port first.')
            return
        if DipoleMagnet is None:
            messagebox.showerror('Import error', 'DipoleMagnet module not available.')
            return
        if self.connecting:
            return
        self.connecting = True
        self.connect_start_time = time.time()
        self.connect_btn.config(state='disabled')
        self.connect_status.config(text='Connecting...')
        self.connect_thread = threading.Thread(target=self.connect_thread_fn, args=(port,), daemon=True)
        self.connect_thread.start()
        self.connect_timeout_job = self.root.after(1000, self.connect_timeout_check)

    def connect_thread_fn(self, port):
        try:
            ard = DipoleMagnet.DipoleMagnet(port=port)
        except Exception as e:
            self.root.after(0, self.connect_failed, e)
            return
        self.root.after(0, self.connect_success, ard, port)

    def connect_timeout_check(self):
        if not self.connecting:
            return
        elapsed = time.time() - self.connect_start_time
        if elapsed > 15:
            self.connect_failed(Exception('Connection timed out.'))
        else:
            self.connect_timeout_job = self.root.after(1000, self.connect_timeout_check)

    def connect_success(self, ard, port):
        if self.connect_timeout_job:
            self.root.after_cancel(self.connect_timeout_job)
            self.connect_timeout_job = None
        self.ard = ard
        self.connecting = False
        self.connect_btn.config(text='Disconnect', state='normal')
        self.connect_status.config(text='Connected to {}'.format(port))
        self.start_btn.config(state='normal')
        self.log('Connected to {}'.format(port))
        self.ard = ard
        self.connecting = False
        self.connect_btn.config(text='Disconnect', state='normal')
        self.connect_status.config(text='Connected to {}'.format(port))
        self.start_btn.config(state='normal')
        self.log('Connected to {}'.format(port))

    def connect_failed(self, exc):
        if self.connect_timeout_job:
            self.root.after_cancel(self.connect_timeout_job)
            self.connect_timeout_job = None
        self.connecting = False
        self.connect_btn.config(state='normal')
        self.connect_status.config(text='Connect failed')
        self.log('Connect failed: {}'.format(exc))
        messagebox.showerror('Connect failed', str(exc))

    def disconnect(self):
        self.stop_polling()
        # close if DipoleMagnet provides a close method
        try:
            if self.ard and hasattr(self.ard, 'close'):
                self.ard.close()
        except Exception:
            pass
        self.ard = None
        self.connect_btn.config(text='Connect')
        self.start_btn.config(state='disabled')
        self.log('Disconnected')

    def start_polling(self):
        if not self.ard:
            messagebox.showwarning('Not connected', 'Connect to a device first.')
            return
        if self.running:
            return
        self.running = True
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.log('Started polling')

    def stop_polling(self):
        if not self.running:
            return
        self.running = False
        if self.poll_thread:
            self.poll_thread.join(timeout=1.0)
        self.poll_thread = None
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.log('Stopped polling')

    def _poll_loop(self):
        while self.running:
            try:
                # Mirror logic from distanceTest.py
                distanceLeft = self.ard.dmm(0)
                distanceRight = self.ard.dmm(1)
                # try to coerce to float
                try:
                    dl = float(distanceLeft)
                except Exception:
                    dl = None
                try:
                    dr = float(distanceRight)
                except Exception:
                    dr = None

                # calculations (same as original)
                gap1 = dl * 0.64 if dl is not None else None
                gap2 = dr * 0.48 if dr is not None else None
                leftGap = 51.5 - (dl - 32) if dl is not None else None
                rightGap = 51.5 - (dr - 24) if dr is not None else None
                gapDiff = abs(leftGap - rightGap) if (leftGap is not None and rightGap is not None) else None

                # schedule UI update on main thread
                self.root.after(0, self._update_ui, dl, dr, gap1, gap2, leftGap, rightGap, gapDiff)
            except Exception as e:
                self.log('Read error: {}'.format(e))
            # follow original sleep cadence
            time.sleep(1)

    def _update_ui(self, dl, dr, gap1, gap2, leftGap, rightGap, gapDiff):
        self.left_var.set(str(dl) if dl is not None else 'err')
        self.right_var.set(str(dr) if dr is not None else 'err')
        self.gap1_var.set('{:.2f}'.format(gap1) if gap1 is not None else '—')
        self.gap2_var.set('{:.2f}'.format(gap2) if gap2 is not None else '—')
        self.leftgap_var.set('{:.2f}'.format(leftGap) if leftGap is not None else '—')
        self.rightgap_var.set('{:.2f}'.format(rightGap) if rightGap is not None else '—')
        self.gapdiff_var.set('{:.2f}'.format(gapDiff) if gapDiff is not None else '—')
        # also log the quick summary
        self.log('LD:{} RD:{} LP:{} RP:{} LG:{} RG:{} GD:{}'.format(
            dl, dr,
            '{:.2f}'.format(gap1) if gap1 is not None else '—',
            '{:.2f}'.format(gap2) if gap2 is not None else '—',
            '{:.2f}'.format(leftGap) if leftGap is not None else '—',
            '{:.2f}'.format(rightGap) if rightGap is not None else '—',
            '{:.2f}'.format(gapDiff) if gapDiff is not None else '—'))

    def log(self, msg):
        ts = time.strftime('%H:%M:%S')
        try:
            self.log_text.configure(state='normal')
            self.log_text.insert('end', f'[{ts}] {msg}\n')
            self.log_text.yview_moveto(1.0)
            self.log_text.configure(state='disabled')
        except Exception:
            pass

    def save_log(self):
        try:
            file_path = tk.filedialog.asksaveasfilename(
                defaultextension='.txt',
                filetypes=[('Text files', '*.txt'), ('All files', '*.*')],
                title='Save log as')
            if not file_path:
                return
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get('1.0', 'end').rstrip() + '\n')
            messagebox.showinfo('Saved', f'Log saved to {file_path}')
        except Exception as e:
            messagebox.showerror('Save failed', str(e))

    def on_close(self):
        try:
            self.running = False
            if self.poll_thread:
                self.poll_thread.join(timeout=1.0)
        except Exception:
            pass
        if self.connect_timeout_job:
            try:
                self.root.after_cancel(self.connect_timeout_job)
            except Exception:
                pass
        try:
            if self.ard and hasattr(self.ard, 'close'):
                self.ard.close()
        except Exception:
            pass
        self.root.destroy()


def main():
    root = tk.Tk()
    root.geometry('600x420')
    DistanceGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
