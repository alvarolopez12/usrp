from gnuradio import gr
import re
import numpy as np
import time
import re


class mac(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="MAC",
            in_sig=None,
            out_sig=None
            )
        # Message portsw
        self.message_port_register_in(gr.pmt.intern("packet"))
        self.message_port_register_out(gr.pmt.intern("ack"))
        self.set_msg_handler(gr.pmt.intern('packet'), self.ack_sender)
        self.packet_num_received = 0
        self.shift = 0
        
    def ack_sender(self, msg):
        
        msg_vec = gr.pmt.car(msg)
        msg_data = gr.pmt.write_string(msg_vec)
        pattern = "\(packet_num \. (.*?)\)\)"
        self.packet_num_received = int(re.search(pattern, msg_data).group(1))
        
        send_str = self.packet_num_received.to_bytes(119, 'little', signed=True) 
        
        send_pmt = gr.pmt.make_u8vector(len(send_str), 0xFF)
        
        for i in range(len(send_str)):
            gr.pmt.u8vector_set(send_pmt, i, send_str[i])
        
        msg = gr.pmt.cons(gr.pmt.PMT_NIL, send_pmt)

        print(self.packet_num_received)

        self.message_port_pub(gr.pmt.intern('ack'), msg)

