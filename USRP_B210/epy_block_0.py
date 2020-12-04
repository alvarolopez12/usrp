from gnuradio import gr
import re
import numpy as np
import time
import re


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
        self.set_msg_handler(gr.pmt.intern('time_unit'), self.send_packet)
        self.set_msg_handler(gr.pmt.intern('ack'), self.ack_handler)
        self.sensing_input = 0
        self.interation_wait_ack = 10 # interation_wait_ack * 3ms = 30ms waiting
        self.packet_num_send = -1
        self.packet_num_received = 0
        
        
    def ack_handler(self, msg):
        
        msg_vec = gr.pmt.cdr(msg)

        # Convert the PMT vector into a Python list
        msg_data = []
        for i in range(48):
            msg_data.append(gr.pmt.u8vector_ref(msg_vec, i))
            
        a = 0           
        for i in msg_data[1:]:
            a = a + i
        
        self.packet_num_received =  a * 255 + msg_data[0]

        print(self.packet_num_received )
                
        
    def send_packet(self, msg):
    
        
        self.packet_num_send += 1
        #print("The packet number" + str(self.packet_num_send ) + "was sending")
        self.message_port_pub(gr.pmt.intern('transmit_packet'), gr.pmt.intern('message received!'))

        #if (self.packet_num_received == self.packet_num_send):
            #print("ACK of " + str(self.packet_num_received) + "Received")
            #self.message_port_pub(gr.pmt.intern('transmit_packet'), gr.pmt.intern('message received!'))
            #self.packet_num_send += 1
            #self.interation_wait_ack = 10
        
        #elif (self.interation_wait_ack > 0):
            #print("NACK of " + str(self.packet_num_received) + "Received")
            #self.interation_wait_ack -= 1
            
        #elif (self.interation_wait_ack == 0):
            #print("DROPPING" + str(self.packet_num_received))
            #self.message_port_pub(gr.pmt.intern('transmit_packet'), gr.pmt.intern('message received!'))
            #self.packet_num_send += 1
            #self.interation_wait_ack = 10
            
        #else:
            #return 0 

        
    def work(self, input_items, output_items):
        self.sensing_input = input_items[0]
        return (len(input_items[0]))
       
  
