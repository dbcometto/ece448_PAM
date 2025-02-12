#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: PAM Main File
# Author: Ben Cometto
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from ascii2float import ascii2float  # grc-generated hier_block
from float2ascii import float2ascii  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from pamRx import pamRx  # grc-generated hier_block
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
        self.samp_rate = samp_rate = 256000
        self.baud_rate = baud_rate = 25600
        self.tail_length = tail_length = 3
        self.symbol_delay = symbol_delay = 4
        self.samples_per_symbol = samples_per_symbol = round(samp_rate/baud_rate)
        self.sample_delay = sample_delay = 6
        self.pulse_type = pulse_type = "rcf"
        self.noise_amplitude = noise_amplitude = 0
        self.msg_start = msg_start = gr.tag_utils.python_to_tag((0, pmt.intern("Start"), pmt.intern("Start"), pmt.intern("src")))
        self.is_polar = is_polar = 1
        self.is_LSB = is_LSB = 0
        self.is_7_bit_ascii = is_7_bit_ascii = 0
        self.invert_bits = invert_bits = 0
        self.channel_delay = channel_delay = 0
        self.bits_per_sym = bits_per_sym = 1
        self.alpha = alpha = 0.5

        ##################################################
        # Blocks
        ##################################################

        self._tail_length_range = qtgui.Range(1, 10, 0.1, 3, 200)
        self._tail_length_win = qtgui.RangeWidget(self._tail_length_range, self.set_tail_length, "'tail_length'", "eng", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tail_length_win)
        self._symbol_delay_range = qtgui.Range(0, 100, 1, 4, 200)
        self._symbol_delay_win = qtgui.RangeWidget(self._symbol_delay_range, self.set_symbol_delay, "'symbol_delay'", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._symbol_delay_win)
        self._sample_delay_range = qtgui.Range(0, 100, 1, 6, 200)
        self._sample_delay_win = qtgui.RangeWidget(self._sample_delay_range, self.set_sample_delay, "'sample_delay'", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sample_delay_win)
        # Create the options list
        self._pulse_type_options = ['rect', 'rcf', 'sinc', 'ramp']
        # Create the labels list
        self._pulse_type_labels = ['rect', 'rcf', 'sinc', 'ramp']
        # Create the combo box
        # Create the radio buttons
        self._pulse_type_group_box = Qt.QGroupBox("'pulse_type'" + ": ")
        self._pulse_type_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._pulse_type_button_group = variable_chooser_button_group()
        self._pulse_type_group_box.setLayout(self._pulse_type_box)
        for i, _label in enumerate(self._pulse_type_labels):
            radio_button = Qt.QRadioButton(_label)
            self._pulse_type_box.addWidget(radio_button)
            self._pulse_type_button_group.addButton(radio_button, i)
        self._pulse_type_callback = lambda i: Qt.QMetaObject.invokeMethod(self._pulse_type_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._pulse_type_options.index(i)))
        self._pulse_type_callback(self.pulse_type)
        self._pulse_type_button_group.buttonClicked[int].connect(
            lambda i: self.set_pulse_type(self._pulse_type_options[i]))
        self.top_layout.addWidget(self._pulse_type_group_box)
        self._noise_amplitude_range = qtgui.Range(0, 5, 0.01, 0, 200)
        self._noise_amplitude_win = qtgui.RangeWidget(self._noise_amplitude_range, self.set_noise_amplitude, "'noise_amplitude'", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_amplitude_win)
        _is_polar_check_box = Qt.QCheckBox("'is_polar'")
        self._is_polar_choices = {True: 1, False: 0}
        self._is_polar_choices_inv = dict((v,k) for k,v in self._is_polar_choices.items())
        self._is_polar_callback = lambda i: Qt.QMetaObject.invokeMethod(_is_polar_check_box, "setChecked", Qt.Q_ARG("bool", self._is_polar_choices_inv[i]))
        self._is_polar_callback(self.is_polar)
        _is_polar_check_box.stateChanged.connect(lambda i: self.set_is_polar(self._is_polar_choices[bool(i)]))
        self.top_layout.addWidget(_is_polar_check_box)
        _is_LSB_check_box = Qt.QCheckBox("'is_LSB'")
        self._is_LSB_choices = {True: 1, False: 0}
        self._is_LSB_choices_inv = dict((v,k) for k,v in self._is_LSB_choices.items())
        self._is_LSB_callback = lambda i: Qt.QMetaObject.invokeMethod(_is_LSB_check_box, "setChecked", Qt.Q_ARG("bool", self._is_LSB_choices_inv[i]))
        self._is_LSB_callback(self.is_LSB)
        _is_LSB_check_box.stateChanged.connect(lambda i: self.set_is_LSB(self._is_LSB_choices[bool(i)]))
        self.top_layout.addWidget(_is_LSB_check_box)
        _is_7_bit_ascii_check_box = Qt.QCheckBox("'is_7_bit_ascii'")
        self._is_7_bit_ascii_choices = {True: 1, False: 0}
        self._is_7_bit_ascii_choices_inv = dict((v,k) for k,v in self._is_7_bit_ascii_choices.items())
        self._is_7_bit_ascii_callback = lambda i: Qt.QMetaObject.invokeMethod(_is_7_bit_ascii_check_box, "setChecked", Qt.Q_ARG("bool", self._is_7_bit_ascii_choices_inv[i]))
        self._is_7_bit_ascii_callback(self.is_7_bit_ascii)
        _is_7_bit_ascii_check_box.stateChanged.connect(lambda i: self.set_is_7_bit_ascii(self._is_7_bit_ascii_choices[bool(i)]))
        self.top_layout.addWidget(_is_7_bit_ascii_check_box)
        _invert_bits_check_box = Qt.QCheckBox("'invert_bits'")
        self._invert_bits_choices = {True: 1, False: 0}
        self._invert_bits_choices_inv = dict((v,k) for k,v in self._invert_bits_choices.items())
        self._invert_bits_callback = lambda i: Qt.QMetaObject.invokeMethod(_invert_bits_check_box, "setChecked", Qt.Q_ARG("bool", self._invert_bits_choices_inv[i]))
        self._invert_bits_callback(self.invert_bits)
        _invert_bits_check_box.stateChanged.connect(lambda i: self.set_invert_bits(self._invert_bits_choices[bool(i)]))
        self.top_layout.addWidget(_invert_bits_check_box)
        self._channel_delay_range = qtgui.Range(0, 100, 1, 0, 200)
        self._channel_delay_win = qtgui.RangeWidget(self._channel_delay_range, self.set_channel_delay, "'channel_delay'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._channel_delay_win)
        self._bits_per_sym_range = qtgui.Range(1, 100, 1, 1, 200)
        self._bits_per_sym_win = qtgui.RangeWidget(self._bits_per_sym_range, self.set_bits_per_sym, "'bits_per_sym'", "eng", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bits_per_sym_win)
        self._alpha_range = qtgui.Range(0, 5, 0.01, 0.5, 200)
        self._alpha_win = qtgui.RangeWidget(self._alpha_range, self.set_alpha, "'alpha'", "eng", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._alpha_win)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
            200, #size
            samp_rate, #samp_rate
            "Rx Output", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "Start")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)


        labels = ['Sampler', 'MF', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_0_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            200, #size
            samp_rate, #samp_rate
            "Tx/Rx", #name
            2, #number of inputs
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


        labels = ['Tx Data', 'Rx Data', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(2):
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
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "Start")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Tx Float Sym', 'Rx Float Sym', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(2):
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
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            16384, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Tx in Freq", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.pamTx_0 = pamTx(
            alpha=alpha,
            pulse_type=pulse_type,
            samp_rate=samp_rate,
            samples_per_symbol=samples_per_symbol,
            tail_length=tail_length,
        )

        self.top_layout.addWidget(self.pamTx_0)
        self.pamRx_0 = pamRx(
            alpha=0.2,
            pulse_type='rect',
            samp_rate=samp_rate,
            sample_delay=sample_delay,
            samples_per_symbol=samples_per_symbol,
            tail_length=tail_length,
        )

        self.top_layout.addWidget(self.pamRx_0)
        self.float2ascii_0 = float2ascii(
            bits_per_sym=bits_per_sym,
            gain=1,
            invert_bits=invert_bits,
            is_7_bit_ascii=is_7_bit_ascii,
            is_LSB=is_LSB,
            is_polar=is_polar,
            samp_rate=samp_rate,
            symbol_delay=symbol_delay,
        )

        self.top_layout.addWidget(self.float2ascii_0)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((69,67,69,52,52,56,32), True, 1, [msg_start])
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'C:\\workspace\\ece448_PAM\\test_output.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, channel_delay)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self._baud_rate_range = qtgui.Range(1, 50000, 1, 25600, 200)
        self._baud_rate_win = qtgui.RangeWidget(self._baud_rate_range, self.set_baud_rate, "'baud_rate'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._baud_rate_win)
        self.ascii2float_0 = ascii2float(
            bits_per_sym=bits_per_sym,
            invert_bits=invert_bits,
            is_7_bit_ascii=is_7_bit_ascii,
            is_LSB=is_LSB,
            is_polar=is_polar,
            samp_rate=samp_rate,
        )

        self.top_layout.addWidget(self.ascii2float_0)
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_f(analog.GR_GAUSSIAN, noise_amplitude, 42, 8192)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.ascii2float_0, 0), (self.pamTx_0, 0))
        self.connect((self.ascii2float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.pamRx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.ascii2float_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.float2ascii_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.pamRx_0, 2), (self.float2ascii_0, 0))
        self.connect((self.pamRx_0, 2), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.pamRx_0, 1), (self.qtgui_time_sink_x_0_0_0, 1))
        self.connect((self.pamRx_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.pamTx_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.pamTx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.pamTx_0, 0), (self.qtgui_time_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "PAM_main")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samples_per_symbol(round(self.samp_rate/self.baud_rate))
        self.ascii2float_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.float2ascii_0.set_samp_rate(self.samp_rate)
        self.pamRx_0.set_samp_rate(self.samp_rate)
        self.pamTx_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.samp_rate)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samples_per_symbol(round(self.samp_rate/self.baud_rate))

    def get_tail_length(self):
        return self.tail_length

    def set_tail_length(self, tail_length):
        self.tail_length = tail_length
        self.pamRx_0.set_tail_length(self.tail_length)
        self.pamTx_0.set_tail_length(self.tail_length)

    def get_symbol_delay(self):
        return self.symbol_delay

    def set_symbol_delay(self, symbol_delay):
        self.symbol_delay = symbol_delay
        self.float2ascii_0.set_symbol_delay(self.symbol_delay)

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.pamRx_0.set_samples_per_symbol(self.samples_per_symbol)
        self.pamTx_0.set_samples_per_symbol(self.samples_per_symbol)

    def get_sample_delay(self):
        return self.sample_delay

    def set_sample_delay(self, sample_delay):
        self.sample_delay = sample_delay
        self.pamRx_0.set_sample_delay(self.sample_delay)

    def get_pulse_type(self):
        return self.pulse_type

    def set_pulse_type(self, pulse_type):
        self.pulse_type = pulse_type
        self._pulse_type_callback(self.pulse_type)
        self.pamTx_0.set_pulse_type(self.pulse_type)

    def get_noise_amplitude(self):
        return self.noise_amplitude

    def set_noise_amplitude(self, noise_amplitude):
        self.noise_amplitude = noise_amplitude
        self.analog_fastnoise_source_x_0.set_amplitude(self.noise_amplitude)

    def get_msg_start(self):
        return self.msg_start

    def set_msg_start(self, msg_start):
        self.msg_start = msg_start
        self.blocks_vector_source_x_0.set_data((69,67,69,52,52,56,32), [self.msg_start])

    def get_is_polar(self):
        return self.is_polar

    def set_is_polar(self, is_polar):
        self.is_polar = is_polar
        self._is_polar_callback(self.is_polar)
        self.ascii2float_0.set_is_polar(self.is_polar)
        self.float2ascii_0.set_is_polar(self.is_polar)

    def get_is_LSB(self):
        return self.is_LSB

    def set_is_LSB(self, is_LSB):
        self.is_LSB = is_LSB
        self._is_LSB_callback(self.is_LSB)
        self.ascii2float_0.set_is_LSB(self.is_LSB)
        self.float2ascii_0.set_is_LSB(self.is_LSB)

    def get_is_7_bit_ascii(self):
        return self.is_7_bit_ascii

    def set_is_7_bit_ascii(self, is_7_bit_ascii):
        self.is_7_bit_ascii = is_7_bit_ascii
        self._is_7_bit_ascii_callback(self.is_7_bit_ascii)
        self.ascii2float_0.set_is_7_bit_ascii(self.is_7_bit_ascii)
        self.float2ascii_0.set_is_7_bit_ascii(self.is_7_bit_ascii)

    def get_invert_bits(self):
        return self.invert_bits

    def set_invert_bits(self, invert_bits):
        self.invert_bits = invert_bits
        self._invert_bits_callback(self.invert_bits)
        self.ascii2float_0.set_invert_bits(self.invert_bits)
        self.float2ascii_0.set_invert_bits(self.invert_bits)

    def get_channel_delay(self):
        return self.channel_delay

    def set_channel_delay(self, channel_delay):
        self.channel_delay = channel_delay
        self.blocks_delay_0.set_dly(int(self.channel_delay))

    def get_bits_per_sym(self):
        return self.bits_per_sym

    def set_bits_per_sym(self, bits_per_sym):
        self.bits_per_sym = bits_per_sym
        self.ascii2float_0.set_bits_per_sym(self.bits_per_sym)
        self.float2ascii_0.set_bits_per_sym(self.bits_per_sym)

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
