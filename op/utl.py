# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0612,W0613


"utility"


import getpass
import os
import pathlib
import pwd
import stat
import time


from stat import ST_UID, ST_MODE, S_IMODE


def __dir__():
    return (
            "cdir",
            "debian",
            "elapsed",
            "fns",
            "fntime",
            "fnclass",
            "spl",
            "user",
            "wait"
           )



def cdir(path):
    if os.path.exists(path):
        return
    if not path.endswith(os.sep):
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    

def debian():
    return os.path.isfile("/etc/debian_version")


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def filesize(path):
    return os.stat(path)[6]


def fns(path, timed=None):
    if not path:
        return []
    if not os.path.exists(path):
        return []
    res = []
    for rootdir, dirs, _files in os.walk(path, topdown=False):
        for dname in  dirs:
            ddd = os.path.join(rootdir, dname)
            fls = sorted(os.listdir(ddd))
            if fls:
                opath = os.path.join(ddd, fls[-1])
                if (
                    timed
                    and "from" in timed
                    and timed["from"]
                    and fntime(opath) < timed["from"]
                   ):
                    continue
                if timed and timed.to and fntime(opath) > timed.to:
                    continue
                try:
                    fntime(opath)
                except ValueError:
                    continue
                opath = opath.split("store")[-1][1:]
                res.append(opath)
    return sorted(res, key=fntime)


def fntime(path):
    after = 0
    path = " ".join(path.split(os.sep)[-2:])
    if "." in path:
        path, after = path.rsplit(".")
    tme = time.mktime(time.strptime(path, "%Y-%m-%d %H:%M:%S"))
    if after:
        try:
            tme = tme + float(".%s"% after)
        except ValueError:
            pass
    return tme


def fnclass(path):
    pth = []
    try:
        _rest, *pth = path.split("store")
    except ValueError:
        pass
    if not pth:
        pth = path.split(os.sep)
    return pth[0]


def locked(lock):

    noargs = False

    def lockeddec(func, *args, **kwargs):

        def lockedfunc(*args, **kwargs):
            lock.acquire()
            if args or kwargs:
                locked.noargs = True
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        lockeddec.__wrapped__ = func
        lockeddec.__doc__ = func.__doc__
        return lockedfunc

    return lockeddec


def permission(ddir, user="operbot", group="operbot", umode=0o700):
    pwdline = pwd.getpwnam(user)
    uid = pwdline.pw_uid
    gid = pwdline.pw_gid
    stats = os.stat(ddir)
    if stats[ST_UID] != uid:
        os.chown(ddir, uid, gid)
    if S_IMODE(stats[ST_MODE]) != umode:
        os.chmod(ddir, umode)


def savepid():
    k = open(os.pah.join(Wd.workdir, 'operbot.pid'),'w')
    k.write(str(os.getpid()))
    k.close()


def spl(txt):
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def touch(fname):
    fd = os.open(fname, os.O_WRONLY | os.O_CREAT)
    os.close(fd)  


def user():
    try:
        import getpass
        return getpass.getuser() 
    except ImportError: return ""


def wait():
    while 1:
        time.sleep(1.0)
