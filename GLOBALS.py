# Setup and Globals for MPK249 Kontakte V1 Script
#
# ============= Common ===============
# PLAY          = Start Playback
# STOP          = Stop Playback
# REC           = Global Record
# LOOP          = Loop
# FFW           = Capture Midi
# REV           = Arm Track

# ============= Buttons ==============

# ============== A Bank ==============
# Encoders      = Parameters
# Buttons       = Mute
# Faders        = Volume

# ============== B Bank ==============
# Encoders      = Pans
# Buttons       = Solo
# Faders        = Volume

# ============== C Bank ==============
# Encoders      = Custom Mapping 1
# Faders        = Custom Mapping 1
# Button 1      = Metronome
# Button 2      = Switch View
# Button 3      = Device Off
# Button 4      = Unmute All
# Button 5      = Session Box Up
# Button 6      = Session Box Down
# Button 7      = Session Box Left
# Button 8      = Session Box Right 

# =============== Pads ===============

# ============== A Bank ==============
# Pads          = Trigger Clips

# ============== B Bank ==============
# Pads          = Stop Clips

# ============== C Bank ==============
# Pads          = Drum Pads

# ============== D Bank ==============
# Pads          = Scene Trigger

chan = 0
pad_chan = 9
num_tracks = 4
num_scenes = 4
PAD_ROWS = [[48, 49, 50, 51],
            [44, 45, 46, 47],
            [40, 41, 42, 43],
            [36, 37, 38, 39]]
ARM_PAD_ROWS = [[56, 57, 58, 59],
                [52, 53, 54, 55]]
STOP_PAD_ROWS = [[64, 65, 66, 67],
                [60, 61, 62, 63]]

SCENE_PADS = [[99, 98, 97, 96]]

TRACK_SELECT_PADS = [[92, 93, 94, 95],
                    [88, 89, 90, 91]]
UTIL_PADS = [[84, 85, 86, 87]]