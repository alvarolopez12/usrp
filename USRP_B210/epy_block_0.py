from gnuradio import gr
import re

class tuning_uhd(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Gain Tuning",
            in_sig=[],
            out_sig=[]
            )
        # Message ports
        self.message_port_register_out(gr.pmt.intern("uhd"))
        self.message_port_register_in(gr.pmt.intern("gain"))
        self.set_msg_handler(gr.pmt.intern('gain'), self.handle_msg)
        
    def handle_msg(self, msg):
    	sensing_algorithm(msg)
    	
def sensing_algorithm(msg):
        print(msg)
