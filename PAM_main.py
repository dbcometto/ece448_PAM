#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: PAM Main File
# Author: Ben Cometto
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from ascii2float import ascii2float  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from pamTx import pamTx  # grc-generated hier_block
import pmt
import sip



class PAM_main(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "PAM Main File", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("PAM Main File")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "PAM_main")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.tail_length = tail_length = 3
        self.samples_per_symbol = samples_per_symbol = 10
        self.samp_rate = samp_rate = 32000
        self.pulse_type = pulse_type = "rcf"
        self.msg_start = msg_start = gr.tag_utils.python_to_tag((0, pmt.intern("Start"), pmt.intern("Start"), pmt.intern("src")))
        self.is_polar = is_polar = 1
        self.is_LSB = is_LSB = 0
        self.is_7_bit_ascii = is_7_bit_ascii = 0
        self.invert_bits = invert_bits = 0
        self.bits_per_sym = bits_per_sym = 1
        self.alpha = alpha = 0.5

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            200, #size
            samp_rate, #samp_rate
            "Tx", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "Start")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            20, #size
            samp_rate, #samp_rate
            "Float Symbols", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "Start")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.pamTx_0 = pamTx(
            alpha=alpha,
            pulse_type=pulse_type,
            samp_rate=samp_rate,
            samples_per_symbol=samples_per_symbol,
            tail_length=tail_length,
        )

        self.top_layout.addWidget(self.pamTx_0)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((90,111), True, 1, [msg_start])
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.ascii2float_0 = ascii2float(
            bits_per_sym=bits_per_sym,
            invert_bits=invert_bits,
            is_7_bit_ascii=is_7_bit_ascii,
            is_LSB=is_LSB,
            is_polar=is_polar,
            samp_rate=samp_rate,
        )

        self.top_layout.addWidget(self.ascii2float_0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.ascii2float_0, 0), (self.pamTx_0, 0))
        self.connect((self.ascii2float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.ascii2float_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.pamTx_0, 0), (self.qtgui_time_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "PAM_main")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tail_length(self):
        return self.tail_length

    def set_tail_length(self, tail_length):
        self.tail_length = tail_length
        self.pamTx_0.set_tail_length(self.tail_length)

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.pamTx_0.set_samples_per_symbol(self.samples_per_symbol)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.ascii2float_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.pamTx_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_pulse_type(self):
        return self.pulse_type

    def set_pulse_type(self, pulse_type):
        self.pulse_type = pulse_type
        self.pamTx_0.set_pulse_type(self.pulse_type)

    def get_msg_start(self):
        return self.msg_start

    def set_msg_start(self, msg_start):
        self.msg_start = msg_start
        self.blocks_vector_source_x_0.set_data((90,111), [self.msg_start])

    def get_is_polar(self):
        return self.is_polar

    def set_is_polar(self, is_polar):
        self.is_polar = is_polar
        self.ascii2float_0.set_is_polar(self.is_polar)

    def get_is_LSB(self):
        return self.is_LSB

    def set_is_LSB(self, is_LSB):
        self.is_LSB = is_LSB
        self.ascii2float_0.set_is_LSB(self.is_LSB)

    def get_is_7_bit_ascii(self):
        return self.is_7_bit_ascii

    def set_is_7_bit_ascii(self, is_7_bit_ascii):
        self.is_7_bit_ascii = is_7_bit_ascii
        self.ascii2float_0.set_is_7_bit_ascii(self.is_7_bit_ascii)

    def get_invert_bits(self):
        return self.invert_bits

    def set_invert_bits(self, invert_bits):
        self.invert_bits = invert_bits
        self.ascii2float_0.set_invert_bits(self.invert_bits)

    def get_bits_per_sym(self):
        return self.bits_per_sym

    def set_bits_per_sym(self, bits_per_sym):
        self.bits_per_sym = bits_per_sym
        self.ascii2float_0.set_bits_per_sym(self.bits_per_sym)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.pamTx_0.set_alpha(self.alpha)




def main(top_block_cls=PAM_main, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
