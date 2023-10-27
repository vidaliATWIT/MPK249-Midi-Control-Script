from __future__ import absolute_import, print_function, unicode_literals
import Live
#from builtins import range
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from .GLOBALS import *

# ==== midi types ====:
# 0 -> momentary controls
# 1 -> toggle
# ==== note types ====:
# 0 -> note_msg
# 1 -> cc_msg

class MPK249(ControlSurface):
    __module__ = __name__
    __doc__ = "A custom script for the MPK249"

    def __init__(self, c_instance): # Import control surface component
        ControlSurface.__init__(self, c_instance)
        self.msg_test()
        with self.component_guard(): # Context Manager. It guards user code. Enables optimizations.
            self._Create_controls()
    
    def msg_test(self):
        log_msg = "#################### LOG FROM MPK249 ########################\nHello from the MPK remote script!\n( . Y . )"
        reg_msg = "MPK249 KontakteV1 Script Loaded."
        self.show_message(reg_msg)
        self.log_message(log_msg)
    
    # creates controls
    
    def _create_controls(self):
        def _make_button(identifier, name, midi_type=1):
            self._log_message("Creating %, identifier %s" % (name, identifier))
            return ButtonElement()
