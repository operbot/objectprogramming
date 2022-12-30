# This file is placed in the Public Domain.


"version"


## defines


__txt__ = "functional programming with objects"
__version__ = "106"


def __dir__():
    return (
            "ver",
           ) 


## commands


def ver(event):
    event.reply("%s version %s - %s" % (Cfg.name.upper(), __version__, Cfg.banner or __txt__))
