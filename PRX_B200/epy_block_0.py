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
        
        msg_vec = gr.pmt.cdr(msg)
        # Convert the PMT vector into a Python list to extract the number
        msg_data = []
        for i in range(48):
            msg_data.append(gr.pmt.u8vector_ref(msg_vec, i))
        a = 0           
        for i in msg_data[1:]:
            a = a + i
        
        self.packet_num_received =  a * 255 + msg_data[0]

                
        # Introduce the same received number into the pdu to send the ACK
        send_str = self.packet_num_received.to_bytes(48, 'little', signed=True) 
        send_pmt = gr.pmt.make_u8vector(len(send_str), 0)
   
        for i in range(len(send_str)):
            gr.pmt.u8vector_set(send_pmt, i, send_str[i])
        
        msg = gr.pmt.cons(gr.pmt.PMT_NIL, send_pmt)
        print("ACK from packet number " + str(self.packet_num_received) + " sended")
        self.message_port_pub(gr.pmt.intern('ack'), msg)


