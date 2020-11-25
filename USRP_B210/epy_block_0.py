from gnuradio import gr
import re
import numpy as np
import time
import re

def sensing_algorithm(sensing_input):
    #print(sensing_input)
    return 1

class mac(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="MAC",
            in_sig=[np.float32],
            out_sig=None
            )
        # Message portsw
        self.message_port_register_out(gr.pmt.intern("transmit_packet"))
        self.message_port_register_in(gr.pmt.intern("transmit_init"))
        self.message_port_register_in(gr.pmt.intern("ack"))
        self.set_msg_handler(gr.pmt.intern('transmit_init'), self.send_pckt)
        self.set_msg_handler(gr.pmt.intern('ack'), self.ack_handler)
        self.i = 0
        self.n = 1
        self.sensing_input = 0
        
    def ack_handler(self, msg):
        
        
        msg_vec = gr.pmt.car(msg)
        msg_data = gr.pmt.write_string(msg_vec)
        pattern = "\(packet_num \. (.*?)\)\)"
        packet_num = int(re.search(pattern, msg_data).group(1))
        
        
        if (packet_num == self.i):
            print("ACK of " + str(packet_num) + "Received")
            self.message_port_pub(gr.pmt.intern('transmit_packet'), gr.pmt.intern('message received!'))
            self.i += 1

        else:
            print("NACK of " + str(packet_num) + "Received")
            self.message_port_pub(gr.pmt.intern('transmit_packet'), gr.pmt.intern('message received!'))
            self.i += 1
        
    def send_pckt(self, msg):

        if self.i < self.n:
            self.message_port_pub(gr.pmt.intern('transmit_packet'), gr.pmt.intern('message!'))
            self.i += 1


    def work(self, input_items, output_items):
        self.sensing_input = input_items[0]
        sensing_algorithm(self.sensing_input)
        return (len(input_items[0]))
       
  
