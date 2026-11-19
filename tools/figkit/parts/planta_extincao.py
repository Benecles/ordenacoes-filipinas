"""Extinction lesson's planta, using the shared planta renderer.
Same params as planta. The older-law shelf is absent; crop its unused space so
three threads determine the plate's height. No marks are edited after casting.
"""
from . import planta

def build(p):
    art,states=planta.build(p)
    return art.replace('viewBox="0 0 1180 472"','viewBox="0 105 1080 355"'),states
