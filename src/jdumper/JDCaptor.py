import threading
import queue
import os
from typing import List, Tuple
from jpcap import JpcapCaptor, JpcapWriter, PacketReceiver, IPPacket, Packet
from jdumper.ui import (
    JDCaptureDialog,
    JDContinuousStatFrame,
    JDCumlativeStatFrame,
    JDFrame,
    JDStatFrame,
)
from jdumper.stat import JDStatisticsTaker

MAX_PACKETS_HOLD = 10000
hostname_cache = {}


class JDCaptor:
    def __init__(self):
        self.packets = []
        self.jpcap = None
        self.is_live_capture = False
        self.is_saved = False
        self.frame = None
        self.capture_thread = None
        self.sframes = []

    def set_jd_frame(self, frame):
        self.frame = frame

    def get_packets(self):
        return self.packets

    def capture_packets_from_device(self):
        if self.jpcap:
            self.jpcap.close()
        self.jpcap = JDCaptureDialog.get_jpcap(self.frame)
        self.clear()

        if self.jpcap:
            self.is_live_capture = True
            self.frame.disable_capture()

            self.start_capture_thread()

    def load_packets_from_file(self):
        self.is_live_capture = False
        self.clear()

        path = self.choose_file()
        if path:
            try:
                if self.jpcap:
                    self.jpcap.close()
                self.jpcap = JpcapCaptor.openFile(path)
            except IOError as e:
                print(f"Can't open file: {path}")
                print(e)
                return

            self.frame.disable_capture()
            self.start_capture_thread()

    def clear(self):
        self.packets.clear()
        self.frame.clear()

        for sframe in self.sframes:
            sframe.clear()

    def save_to_file(self):
        if not self.packets:
            return

        file_path = self.choose_file(save=True)
        if file_path:
            if os.path.exists(file_path):
                response = self.frame.show_confirm_dialog(
                    f"Overwrite {os.path.basename(file_path)}?", "Overwrite?"
                )
                if response == "no":
                    return

            try:
                writer = JpcapWriter.open_dump_file(self.jpcap, file_path)

                for packet in self.packets:
                    writer.write_packet(packet)

                writer.close()
                self.is_saved = True
            except IOError as e:
                print(f"Can't save file: {file_path}")
                print(e)

    def stop_capture(self):
        self.stop_capture_thread()

    def save_if_not(self):
        if self.is_live_capture and not self.is_saved:
            response = self.frame.show_confirm_dialog("Save this data?", "Save this data?")
            if response == "yes":
                self.save_to_file()

    def add_cumulative_stat_frame(self, taker: JDStatisticsTaker):
        self.sframes.append(JDCumlativeStatFrame.open_window(self.packets, taker.newInstance()))

    def add_continuous_stat_frame(self, taker: JDStatisticsTaker):
        self.sframes.append(JDContinuousStatFrame.open_window(self.packets, taker.newInstance()))

    def close_all_windows(self):
        for sframe in self.sframes:
            sframe.dispose()

    def start_capture_thread(self):
        if self.capture_thread:
            return

        self.capture_thread = threading.Thread(target=self._capture_thread)
        self.capture_thread.setPriority(threading.Thread.MIN_PRIORITY)

        self.frame.start_updating()
        for sframe in self.sframes:
            sframe.start_updating()

        self.capture_thread.start()

    def stop_capture_thread(self):
        self.capture_thread = None
        self.frame.stop_updating()
        for sframe in self.sframes:
            sframe.stop_updating()

    def _capture_thread(self):
        while self.capture_thread:
            if self.jpcap.process_packet(1, self.handler) == 0 and not self.is_live_capture:
                self.stop_capture_thread()
            threading.Thread.yield()

        self.jpcap.break_loop()
        self.frame.enable_capture()

    def handler(self, packet):
        self.packets.append(packet)
        while len(self.packets) > MAX_PACKETS_HOLD:
            self.packets.pop(0)

        if self.sframes:
            for sframe in self.sframes:
                sframe.add_packet(packet)

        self.is_saved = False

        if isinstance(packet, IPPacket):
            self._update_hostname_cache(packet)

    def _update_hostname_cache(self, packet):
        def update_cache():
            src_ip = packet.src_ip
            dst_ip = packet.dst_ip

            if src_ip not in hostname_cache:
                hostname_cache[src_ip] = src_ip.gethostbyname()
            if dst_ip not in hostname_cache:
                hostname_cache[dst_ip] = dst_ip.gethostbyname()

            print(len(hostname_cache))

        thread = threading.Thread(target=update_cache)
        thread.start()

    @staticmethod
    def choose_file(save=False):
        dialog = JDCaptureDialog()
        if save:
            return dialog.show_save_dialog()
        else:
            return dialog.show_open_dialog()


# Example usage
if __name__ == "__main__":
    captor = JDCaptor()
    frame = JDFrame(captor)
    captor.set_jd_frame(frame)
    frame.show_frame()
