# This file is placed in the Public Domain.


"config"


from op import Cfg, edit, keys, last, write


def cfg(event):
    last(Cfg)
    if not event.sets:
        event.reply(printable(
                              Cfg,
                              keys(Cfg),
                              skip="name,password,prs",
                             )
                   )
    else:
        edit(Cfg, event.sets)
        write(Cfg)
        event.done()
