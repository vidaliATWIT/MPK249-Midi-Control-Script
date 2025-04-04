from __future__ import absolute_import, print_function, unicode_literals
import Live
#from builtins import range
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.SliderElement import SliderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.DeviceComponent import DeviceComponent
from .GLOBALS import *

# ==== midi types ====:
# 1 -> momentary controls
# 0 -> toggle
# ==== note types ====:
# 0 -> note_msg
# 1 -> cc_msg

# TODO:
# xFix transport playback (check how other people do it) (no self on instantiate)
# xSet up clip launching
# xLook into setting up a create_toggle_pad for clip arming
# xSet up drum pads
# xRe-Map rest of Knobs
#   xKnobs need to bed different functions cuz switching back and forth on the same controls doesn't work
# -Set up capture midi

class MPK249(ControlSurface):
    __module__ = __name__
    __doc__ = "A custom script for the MPK249"

    def __init__(self, c_instance): # Import control surface component
        ControlSurface.__init__(self, c_instance)
        self.msg_test()
        with self.component_guard(): # Context Manager. It guards user code. Enables optimizations.
            self._create_controls()
            self._create_session()
            self._create_transport()
            self._create_mixer()
            self._create_device()
    
    def msg_test(self):
        log_msg = "#################### LOG FROM MPK249 #####################\nHello from the MPK remote script!\n"
        reg_msg = "MPK249 Kontakte V1 Script Loaded."
        self.show_message(reg_msg)
        self.log_message(log_msg)
    
    # creates controls
    def _create_controls(self):
        '''
        def _make_button(identifier, name, midi_type=1, channel=chan, is_momentary=True): ##default midi_type 1 and default channel = chan (1), default momentary flag = true
            self.log_message("Creating %s, identifier %s" % (name, identifier))
            return ButtonElement(is_momentary=True, msg_type=midi_type, channel=channel, identifier=identifier, name=name)
        '''

        def _make_button(identifier, name, midi_type=1):
            self.log_message("CREATING %s, identifier %s" % (name, identifier))
            return ButtonElement(is_momentary=True, msg_type=midi_type, channel=chan, identifier=identifier, name=name)

        def _make_toggle(identifier, name, midi_type=1):
            self.log_message("CREATING %s, identifier %s" % (name, identifier))
            return ButtonElement(is_momentary=False, msg_type=midi_type, channel=chan, identifier=identifier, name=name)

        def _make_pad(identifier, name, midi_type=0):
            self.log_message("CREATING %s, identifier %s" % (name, identifier))
            return ButtonElement(is_momentary=True, msg_type=midi_type, channel=pad_chan, identifier=identifier, name=name)
        
        def _make_pad_toggle(identifier, name, midi_type=0):
            self.log_message("CREATING %s, identifier %s" % (name, identifier))
            return ButtonElement(is_momentary=False, msg_type=midi_type, channel=pad_chan, identifier=identifier, name=name)
        
        #self, is_momentary, msg_type, channel, identifier

        def _make_encoder(identifier, name, channel=chan): ##default midi_type 1 and default channel = chan (1)
            self.log_message("Creating %s, identifier %s" % (name, identifier))
            return EncoderElement(msg_type=1, channel=channel, map_mode = Live.MidiMap.MapMode.absolute, identifier=identifier, name=name)

        def _make_slider(identifier, name, channel=chan): ##default midi_type 1 and default channel = chan (1)
            self.log_message("Creating %s, identifier %s" % (name, identifier))
            return SliderElement(msg_type=1, channel=channel, identifier=identifier, name=name)

        # Creating Sliders. Because AKAI numbered their page 1 controls all wack, we can't automate this
        self._faders = ButtonMatrixElement(rows=[
            [_make_slider(18, 'slider_1'), _make_slider(21, 'slider_2'),
            _make_slider(22, 'slider_3'), _make_slider(23, 'slider_4'),
            _make_slider(24 , 'slider_5'), _make_slider(25, 'slider_6'),
            _make_slider(26, 'slider_7'), _make_slider(27, 'slider_1')]
        ])

        # Creating Encoder Buttons
        self._encoders = ButtonMatrixElement(rows=[
            [_make_encoder(3, 'encoder_1'), _make_encoder(9, 'encoder_2'),
            _make_encoder(14, 'encoder_3'), _make_encoder(15, 'encoder_4'),
            _make_encoder(16 , 'encoder_5'), _make_encoder(17, 'encoder_6'),
            _make_encoder(19, 'encoder_7'), _make_encoder(20, 'encoder_1')]
        ])

        self._pan_encoders = ButtonMatrixElement(rows=[
            [_make_encoder(52, 'pan_1'), _make_encoder(53, 'pan_2'),
            _make_encoder(54, 'pan_3'), _make_encoder(55, 'pan_4'),
            _make_encoder(57, 'pan_5'), _make_encoder(58, 'pan_6'),
            _make_encoder(59, 'pan_7'), _make_encoder(60, 'pan_1')]
        ])

        # Creating Mute Buttons
        self._mute_buttons = ButtonMatrixElement(rows =[
            [ _make_toggle(28, 'mute_1'),  _make_toggle(29, 'mute_2'),
             _make_toggle(30, 'mute_3'),  _make_toggle(31, 'mute_4'),
             _make_toggle(35 , 'mute_5'),  _make_toggle(41, 'mute_6'),
             _make_toggle(46, 'mute_7'),  _make_toggle(47, 'mute_1')]
        ])

        # Creating Solo Buttons
        self._solo_buttons = ButtonMatrixElement(rows =[
            [_make_toggle(75+i, 'solo %d' % (i + 1)) for i in range (8)]
        ])
        
        # Creating Util Buttons
        self._util_buttons = ButtonMatrixElement(rows =[
            [_make_button(106+i, 'util %d' % (i + 1)) for i in range (8)]
        ])

        # Create Scene Buttons
        self._scene_buttons = ButtonMatrixElement(rows=[
            [_make_pad(identifier, 'clip %d' % (identifier)) for identifier in row] 
            for row in SCENE_PADS])

        # Create Clip Launch Pads
        self._clip_launch_buttons = ButtonMatrixElement(rows=[
            [_make_pad(identifier, 'clip %d' % (identifier)) for identifier in row] 
            for row in PAD_ROWS])
        
        # Create Arm Track Buttons
        self._arm_track_buttons = ButtonMatrixElement(rows=[
            [_make_pad_toggle(identifier, 'arm track %d' % (identifier)) for identifier in row] 
            for row in ARM_PAD_ROWS])
        
        # Create Stop Clip Buttons
        self._stop_clip_buttons = ButtonMatrixElement(rows=[
            [_make_pad(identifier, 'stop clip %d' % (identifier)) for identifier in row] 
            for row in STOP_PAD_ROWS])

        # Create Track Select Buttons
        self._track_select_buttons = ButtonMatrixElement(rows=[
            [_make_pad_toggle(identifier, 'track %d' % (identifier)) for identifier in row] 
            for row in TRACK_SELECT_PADS])


        ##[make_encoder(7 + i, 'Volume_%d' % (i+1)) for i in range(1)]])

        # Create Transport Controls'
        
        self._loop_button = _make_button(114, 'loop')
        self._play_button = _make_toggle(118, 'play')
        self._stop_button = _make_button(117, 'stop')
        self._rec_button = _make_button(119, 'record')
        self._arm_button = _make_button(115, 'arm track') ##ffwd
        self._capture_midi_button = _make_pad(84, 'capture midi') ##rev

    # Create Session Component
    def _create_session(self):
        self.log_message("############## Session Created ################")
        self._session = SessionComponent(num_tracks=num_tracks, num_scenes=num_scenes, is_enabled=True, auto_name=True)
        self.set_highlighting_session_component(self._session)
        # Will assign track left-right and up-down for session highlight
        self._session.set_track_bank_buttons(self._util_buttons[5], self._util_buttons[4])
        self._session.set_scene_bank_buttons(self._util_buttons[7], self._util_buttons[6])
        # Set Session Launch Buttons
        self._session.scene(0).set_launch_button(self._scene_buttons[3])
        self._session.scene(1).set_launch_button(self._scene_buttons[2])
        self._session.scene(2).set_launch_button(self._scene_buttons[1]) 
        self._session.scene(3).set_launch_button(self._scene_buttons[0]) 
        # Set stop all clips button
        self._session.set_stop_all_clips_button(self._util_buttons[3])

        # Set up clip launching 4x4 grid and 2x4 clip stopping grid
        if self._clip_launch_buttons:
            self._clip_launch_buttons.reset()
        self._session.set_clip_launch_buttons(self._clip_launch_buttons)
        if self._stop_clip_buttons:
            self._stop_clip_buttons.reset()
        self._session.set_stop_track_clip_buttons(self._stop_clip_buttons)

    # Craete Transport Component NOT WORKING
    def _create_transport(self):
        self.log_message("=======================Transport Created==========================")
        self._transport = TransportComponent()

        self._transport.set_loop_button(self._loop_button)
        self._transport.set_play_button(self._play_button) #not working
        self._transport.set_stop_button(self._stop_button)
        self._transport.set_record_button(self._rec_button)
    
    def _create_mixer(self):
        self.log_message("=======================Mixer Created==========================")
        self._mixer = MixerComponent(num_tracks=8, name='Mixer')
        #Make sure we are focused on the first track upon opening Live Set
        self.song().view.selected_track = self._mixer.channel_strip(0)._track
        self._mixer.set_volume_controls(self._faders)
        self._mixer.set_pan_controls(self._pan_encoders)
        self._mixer.set_mute_buttons(self._mute_buttons)
        self._mixer.set_solo_buttons(self._solo_buttons)
        if (self._arm_track_buttons):
            self._arm_track_buttons.reset()
        self._mixer.set_arm_buttons(self._arm_track_buttons)
        if (self._track_select_buttons):
            self._track_select_buttons.reset()
        self._mixer.set_track_select_buttons(self._track_select_buttons)

    def _create_device(self):
        self.log_message("=======================Device Created==========================")
        self._device = DeviceComponent(name='Device Component', is_enabled=True, device_selection_follows_track_selection=True)
        self._device.set_parameter_controls(self._encoders)
        self.set_device_component(self._device)

    '''
    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        self.show_message("MIDI CAPTURED")
        
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
        '''
    '''
    capture_midi_button = ButtonControl()
    @capture_midi_button.pressed
    def capture_midi_button(self, button):
            self.song.capture_midi()
    '''
