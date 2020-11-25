from gnuradio import gr
import re
import numpy as np
import time

def sensing_algorithm(sensing_input):
    print(sensing_input)

class mac(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="MAC",
            in_sig=[np.float32],
            out_sig=None
            )
        # Message portsw
        self.message_port_register_out(gr.pmt.intern("transmit_packet"))
        self.message_port_register_in(gr.pmt.intern("time_unit"))
        self.message_port_register_in(gr.pmt.intern("ack"))
        self.set_msg_handler(gr.pmt.intern('time_unit'), self.send_pckt)
        self.set_msg_handler(gr.pmt.intern('ack'), self.ack_handler)
        
        self.sensing_input = 0
        self.ks = 1000
        self.kt = 1000
        
    def ack_handler(self, msg):
        print("ACK received")
        
    def send_pckt(self, msg):
        self.message_port_pub(gr.pmt.intern('transmit_packet'), gr.pmt.intern('message!'))
        
    def work(self, input_items, output_items):
        self.sensing_input = input_items[0]
        aa(self.sensing_input)
        return (len(input_items[0]))
       
  
