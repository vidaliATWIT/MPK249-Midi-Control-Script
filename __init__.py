from __future__ import absolute_import, print_function, unicode_literals
from .MPK249 import MPK249

def create_instance(c_instance):
    return MPK249(c_instance)