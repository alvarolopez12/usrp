#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SECUNDARY
# Author: alvaro
# GNU Radio version: 3.8.3.1

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
from gnuradio.digital.utils import tagged_streams
import epy_block_0
import epy_block_0_0

from gnuradio import qtgui

class secundary(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SECUNDARY")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SECUNDARY")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "secundary")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
        self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
        self.payload_mod = payload_mod = digital.constellation_bpsk()
        self.packet_length_tag_key = packet_length_tag_key = "packet_len"
        self.occupied_carriers = occupied_carriers = (list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) + list(range(22, 27)),)
        self.length_tag_key = length_tag_key = "packet_len"
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.fft_len = fft_len = 64
        self.tx_gain = tx_gain = 50
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.samp_rate = samp_rate = 1000000
        self.rx_gain = rx_gain = 50
        self.rolloff = rolloff = 0
        self.payload_equalizer = payload_equalizer = digital.ofdm_equalizer_simpledfe(fft_len, payload_mod.base(), occupied_carriers, pilot_carriers, pilot_symbols, 1)
        self.header_formatter = header_formatter = digital.packet_header_ofdm(occupied_carriers, n_syms=1, len_tag_key=packet_length_tag_key, frame_len_tag_key=length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False)
        self.header_equalizer = header_equalizer = digital.ofdm_equalizer_simpledfe(fft_len, header_mod.base(), occupied_carriers, pilot_carriers, pilot_symbols)
        self.hdr_format = hdr_format = digital.header_format_ofdm(occupied_carriers, 1, length_tag_key,)

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_tool_bar = Qt.QToolBar(self)
        self._tx_gain_tool_bar.addWidget(Qt.QLabel('tx_gain' + ": "))
        self._tx_gain_line_edit = Qt.QLineEdit(str(self.tx_gain))
        self._tx_gain_tool_bar.addWidget(self._tx_gain_line_edit)
        self._tx_gain_line_edit.returnPressed.connect(
            lambda: self.set_tx_gain(eng_notation.str_to_num(str(self._tx_gain_line_edit.text()))))
        self.top_layout.addWidget(self._tx_gain_tool_bar)
        self._rx_gain_tool_bar = Qt.QToolBar(self)
        self._rx_gain_tool_bar.addWidget(Qt.QLabel('rx_gain' + ": "))
        self._rx_gain_line_edit = Qt.QLineEdit(str(self.rx_gain))
        self._rx_gain_tool_bar.addWidget(self._rx_gain_line_edit)
        self._rx_gain_line_edit.returnPressed.connect(
            lambda: self.set_rx_gain(eng_notation.str_to_num(str(self._rx_gain_line_edit.text()))))
        self.top_layout.addWidget(self._rx_gain_tool_bar)
        self.uhd_usrp_source_0_0_1 = uhd.usrp_source(
            ",".join(('serial=F5C243', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0_1.set_center_freq(2400000000, 0)
        self.uhd_usrp_source_0_0_1.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0_0_1.set_antenna('RX2', 0)
        self.uhd_usrp_source_0_0_1.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0_1.set_time_unknown_pps(uhd.time_spec())
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(('serial=F5C234', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_center_freq(2450000000, 0)
        self.uhd_usrp_source_0_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_time_unknown_pps(uhd.time_spec())
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(('serial=F5C234', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            length_tag_key,
        )
        self.uhd_usrp_sink_0_0.set_center_freq(2400000000, 0)
        self.uhd_usrp_sink_0_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_time_unknown_pps(uhd.time_spec())
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(('serial=F5C243', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            length_tag_key,
        )
        self.uhd_usrp_sink_0.set_center_freq(2450000000, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            64, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            4000000000, #fc
            50000, #bw
            'SECUNDARY RX', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        self.fft_vxx_1_0_0_0_0_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.fft_vxx_1_0_0_0_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.fft_vxx_0_0_0_0_0_0_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.fft_vxx_0_0_0_0_0_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(fft_len, False, (), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (), True, 1)
        self.epy_block_0_0 = epy_block_0_0.mac()
        self.epy_block_0 = epy_block_0.mac()
        self.digital_protocol_formatter_bb_0_0 = digital.protocol_formatter_bb(hdr_format, length_tag_key)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr_format, length_tag_key)
        self.digital_packet_headerparser_b_0_0_0_0_0_0 = digital.packet_headerparser_b(header_formatter.base())
        self.digital_packet_headerparser_b_0_0_0_0_0 = digital.packet_headerparser_b(header_formatter.base())
        self.digital_ofdm_sync_sc_cfb_0_0_0_0_0_0 = digital.ofdm_sync_sc_cfb(fft_len, fft_len//4, False, 0.9)
        self.digital_ofdm_sync_sc_cfb_0_0_0_0_0 = digital.ofdm_sync_sc_cfb(fft_len, fft_len//4, False, 0.9)
        self.digital_ofdm_serializer_vcc_payload_0_0_0_0_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, length_tag_key, packet_length_tag_key, 1, '', True)
        self.digital_ofdm_serializer_vcc_payload_0_0_0_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, length_tag_key, packet_length_tag_key, 1, '', True)
        self.digital_ofdm_serializer_vcc_header_0_0_0_0_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, length_tag_key, '', 0, '', True)
        self.digital_ofdm_serializer_vcc_header_0_0_0_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, length_tag_key, '', 0, '', True)
        self.digital_ofdm_frame_equalizer_vcvc_1_0_0_0_0_0 = digital.ofdm_frame_equalizer_vcvc(payload_equalizer.base(), fft_len//4, length_tag_key, True, 0)
        self.digital_ofdm_frame_equalizer_vcvc_1_0_0_0_0 = digital.ofdm_frame_equalizer_vcvc(payload_equalizer.base(), fft_len//4, length_tag_key, True, 0)
        self.digital_ofdm_frame_equalizer_vcvc_0_0_0_0_0_0 = digital.ofdm_frame_equalizer_vcvc(header_equalizer.base(), fft_len//4, length_tag_key, True, 1)
        self.digital_ofdm_frame_equalizer_vcvc_0_0_0_0_0 = digital.ofdm_frame_equalizer_vcvc(header_equalizer.base(), fft_len//4, length_tag_key, True, 1)
        self.digital_ofdm_cyclic_prefixer_0_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len + fft_len//4, rolloff, length_tag_key)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len + fft_len//4, rolloff, length_tag_key)
        self.digital_ofdm_chanest_vcvc_0_0_0_0_0_0 = digital.ofdm_chanest_vcvc(sync_word1, sync_word2, 1, 0, 3, False)
        self.digital_ofdm_chanest_vcvc_0_0_0_0_0 = digital.ofdm_chanest_vcvc(sync_word1, sync_word2, 1, 0, 3, False)
        self.digital_ofdm_carrier_allocator_cvc_0_0 = digital.ofdm_carrier_allocator_cvc( fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2), length_tag_key, True)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc( fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2), length_tag_key, True)
        self.digital_header_payload_demux_0_0_0_0_0_0 = digital.header_payload_demux(
            3,
            fft_len,
            fft_len//4,
            length_tag_key,
            "",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            samp_rate,
            (),
            0)
        self.digital_header_payload_demux_0_0_0_0_0 = digital.header_payload_demux(
            3,
            fft_len,
            fft_len//4,
            length_tag_key,
            "",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            samp_rate,
            (),
            0)
        self.digital_constellation_decoder_cb_1_0_0_0_0_0 = digital.constellation_decoder_cb(payload_mod.base())
        self.digital_constellation_decoder_cb_1_0_0_0_0 = digital.constellation_decoder_cb(payload_mod.base())
        self.digital_constellation_decoder_cb_0_0_0_0_0_0 = digital.constellation_decoder_cb(header_mod.base())
        self.digital_constellation_decoder_cb_0_0_0_0_0 = digital.constellation_decoder_cb(header_mod.base())
        self.digital_chunks_to_symbols_xx_0_1 = digital.chunks_to_symbols_bc(header_mod.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_0 = digital.chunks_to_symbols_bc(payload_mod.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(payload_mod.points(), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(header_mod.points(), 1)
        self.blocks_tagged_stream_to_pdu_0_0_0_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, length_tag_key)
        self.blocks_tagged_stream_to_pdu_0_0_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, length_tag_key)
        self.blocks_tagged_stream_mux_0_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, length_tag_key, 0)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, length_tag_key, 0)
        self.blocks_tag_gate_0_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, True)
        self.blocks_tag_gate_0_0.set_single_key("")
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, True)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_repack_bits_bb_0_2_0 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_2 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_1_0_0_0_0_0 = blocks.repack_bits_bb(payload_mod.bits_per_symbol(), 8, packet_length_tag_key, True, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_1_0_0_0_0 = blocks.repack_bits_bb(payload_mod.bits_per_symbol(), 8, packet_length_tag_key, True, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_0_1_0 = blocks.repack_bits_bb(8, 1, length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_0_1 = blocks.repack_bits_bb(8, 1, length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_pdu_to_tagged_stream_0_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, length_tag_key)
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, length_tag_key)
        self.blocks_multiply_xx_0_0_0_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(50e-3)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(50e-3)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_delay_0_0_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, fft_len+fft_len//4)
        self.blocks_delay_0_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, fft_len+fft_len//4)
        self.analog_frequency_modulator_fc_0_0_0_0_0_0 = analog.frequency_modulator_fc(-2.0/fft_len)
        self.analog_frequency_modulator_fc_0_0_0_0_0 = analog.frequency_modulator_fc(-2.0/fft_len)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.epy_block_0_0, 'time_unit'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0_0, 'pdus'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0_0, 'pdus'), (self.epy_block_0_0, 'ack'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0_0_0, 'pdus'), (self.epy_block_0, 'packet'))
        self.msg_connect((self.digital_packet_headerparser_b_0_0_0_0_0, 'header_data'), (self.digital_header_payload_demux_0_0_0_0_0, 'header_data'))
        self.msg_connect((self.digital_packet_headerparser_b_0_0_0_0_0_0, 'header_data'), (self.digital_header_payload_demux_0_0_0_0_0_0, 'header_data'))
        self.msg_connect((self.epy_block_0, 'ack'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.epy_block_0_0, 'transmit_packet'), (self.blocks_pdu_to_tagged_stream_0_0_0, 'pdus'))
        self.msg_connect((self.epy_block_0_0, 'channel_up'), (self.uhd_usrp_sink_0_0, 'command'))
        self.msg_connect((self.epy_block_0_0, 'channel_down'), (self.uhd_usrp_source_0_0, 'command'))
        self.connect((self.analog_frequency_modulator_fc_0_0_0_0_0, 0), (self.blocks_multiply_xx_0_0_0_0_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0_0_0_0_0_0, 0), (self.blocks_multiply_xx_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_multiply_xx_0_0_0_0_0, 1))
        self.connect((self.blocks_delay_0_0_0_0_0_0, 0), (self.blocks_multiply_xx_0_0_0_0_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_tag_gate_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0_0_0, 0), (self.digital_header_payload_demux_0_0_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0_0_0_0, 0), (self.digital_header_payload_demux_0_0_0_0_0_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.blocks_repack_bits_bb_0_2, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0_0, 0), (self.blocks_repack_bits_bb_0_2_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0_0, 0), (self.digital_protocol_formatter_bb_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_1, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_1_0, 0), (self.digital_chunks_to_symbols_xx_0_1, 0))
        self.connect((self.blocks_repack_bits_bb_0_1_0_0_0_0, 0), (self.blocks_tagged_stream_to_pdu_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_1_0_0_0_0_0, 0), (self.blocks_tagged_stream_to_pdu_0_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_2, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_2_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_tag_gate_0_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_1, 0), (self.blocks_tagged_stream_mux_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0_0, 0), (self.digital_packet_headerparser_b_0_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0_0_0, 0), (self.digital_packet_headerparser_b_0_0_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_1_0_0_0_0, 0), (self.blocks_repack_bits_bb_0_1_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_1_0_0_0_0_0, 0), (self.blocks_repack_bits_bb_0_1_0_0_0_0_0, 0))
        self.connect((self.digital_header_payload_demux_0_0_0_0_0, 0), (self.fft_vxx_0_0_0_0_0_0, 0))
        self.connect((self.digital_header_payload_demux_0_0_0_0_0, 1), (self.fft_vxx_1_0_0_0_0, 0))
        self.connect((self.digital_header_payload_demux_0_0_0_0_0_0, 0), (self.fft_vxx_0_0_0_0_0_0_0, 0))
        self.connect((self.digital_header_payload_demux_0_0_0_0_0_0, 1), (self.fft_vxx_1_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.digital_ofdm_chanest_vcvc_0_0_0_0_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_chanest_vcvc_0_0_0_0_0_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_0_0_0_0_0, 0), (self.digital_ofdm_serializer_vcc_header_0_0_0_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_0_0_0_0_0_0, 0), (self.digital_ofdm_serializer_vcc_header_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_1_0_0_0_0, 0), (self.digital_ofdm_serializer_vcc_payload_0_0_0_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_1_0_0_0_0_0, 0), (self.digital_ofdm_serializer_vcc_payload_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_header_0_0_0_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_header_0_0_0_0_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_payload_0_0_0_0, 0), (self.digital_constellation_decoder_cb_1_0_0_0_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_payload_0_0_0_0_0, 0), (self.digital_constellation_decoder_cb_1_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0_0_0_0_0, 0), (self.analog_frequency_modulator_fc_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0_0_0_0_0, 1), (self.digital_header_payload_demux_0_0_0_0_0, 1))
        self.connect((self.digital_ofdm_sync_sc_cfb_0_0_0_0_0_0, 0), (self.analog_frequency_modulator_fc_0_0_0_0_0_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0_0_0_0_0_0, 1), (self.digital_header_payload_demux_0_0_0_0_0_0, 1))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_repack_bits_bb_0_0_1, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0, 0), (self.blocks_repack_bits_bb_0_0_1_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.digital_ofdm_cyclic_prefixer_0_0, 0))
        self.connect((self.fft_vxx_0_0_0_0_0_0, 0), (self.digital_ofdm_chanest_vcvc_0_0_0_0_0, 0))
        self.connect((self.fft_vxx_0_0_0_0_0_0_0, 0), (self.digital_ofdm_chanest_vcvc_0_0_0_0_0_0, 0))
        self.connect((self.fft_vxx_1_0_0_0_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_1_0_0_0_0, 0))
        self.connect((self.fft_vxx_1_0_0_0_0_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_1_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_delay_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.digital_ofdm_sync_sc_cfb_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0_1, 0), (self.blocks_delay_0_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0_1, 0), (self.digital_ofdm_sync_sc_cfb_0_0_0_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "secundary")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_packet_length_tag_key(self):
        return self.packet_length_tag_key

    def set_packet_length_tag_key(self, packet_length_tag_key):
        self.packet_length_tag_key = packet_length_tag_key
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.packet_length_tag_key, frame_len_tag_key=self.length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_hdr_format(digital.header_format_ofdm(self.occupied_carriers, 1, self.length_tag_key,))
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.packet_length_tag_key, frame_len_tag_key=self.length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key
        self.set_hdr_format(digital.header_format_ofdm(self.occupied_carriers, 1, self.length_tag_key,))
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.packet_length_tag_key, frame_len_tag_key=self.length_tag_key, bits_per_header_sym=header_mod.bits_per_symbol(), bits_per_payload_sym=payload_mod.bits_per_symbol(), scramble_header=False))

    def get_header_mod(self):
        return self.header_mod

    def set_header_mod(self, header_mod):
        self.header_mod = header_mod

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_mod.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))
        self.analog_frequency_modulator_fc_0_0_0_0_0.set_sensitivity(-2.0/self.fft_len)
        self.analog_frequency_modulator_fc_0_0_0_0_0_0.set_sensitivity(-2.0/self.fft_len)
        self.blocks_delay_0_0_0_0_0.set_dly(self.fft_len+self.fft_len//4)
        self.blocks_delay_0_0_0_0_0_0.set_dly(self.fft_len+self.fft_len//4)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        Qt.QMetaObject.invokeMethod(self._tx_gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.tx_gain)))
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
        self.uhd_usrp_sink_0_0.set_gain(self.tx_gain, 0)

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0_1.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        Qt.QMetaObject.invokeMethod(self._rx_gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_gain)))
        self.uhd_usrp_source_0_0.set_gain(self.rx_gain, 0)
        self.uhd_usrp_source_0_0_1.set_gain(self.rx_gain, 0)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_payload_equalizer(self):
        return self.payload_equalizer

    def set_payload_equalizer(self, payload_equalizer):
        self.payload_equalizer = payload_equalizer

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_header_equalizer(self):
        return self.header_equalizer

    def set_header_equalizer(self, header_equalizer):
        self.header_equalizer = header_equalizer

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format





def main(top_block_cls=secundary, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
