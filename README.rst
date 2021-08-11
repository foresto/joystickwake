joystickwake
============

-----------------------------
A joystick-aware screen waker
-----------------------------

:Manual section: 1
:Date:           2020-07-09


Synopsis
--------

    joystickwake -h|--help

    joystickwake [--command cmd] [--interval seconds] [--loglevel level]


Description
-----------

Linux gamers often find themselves unexpectedly staring at a blank screen,
because their display server fails to recognize game controllers as input
devices, allowing the screen blanker to activate during gameplay.  This
program works around the problem by (temporarily) disabling screen blankers
while joystick activity is detected.


Operation
---------

Once installed, joystickwake launches automatically when a user logs in to
any modern linux desktop environment.  It can also be run manually, either
from a command prompt or from a user-created menu entry, so formal installation
is not required.

While running, it monitors udev to find joystick devices (including any that
are plugged in later) and reacts to activity from any of them.

The screen is kept awake by periodically running simple commands provided by
whatever screen blanker is in use.  This approach keeps joystickwake compatible
with just about every screensaver and power management system there is.

The first time joystick activity is detected, all known wake commands will
be run.  Those that fail will be skipped thereafter.  A minimum time between
wakes is always observed.  Joystickwake thereby learns the needs of the host
system, avoids causing lag with unnecessary work, and minimizes log clutter.
In practice, it is very lightweight.

If all of the wake commands fail, it usually means that the screen blanker
requires a custom command that has not yet been configured, so joystickwake
will quit.

If the python3 Xlib package is installed, joystickwake will quit when the
desktop session ends.  Otherwise, it will quit when its parent process exits.
(This avoids leaving old instances running after the user logs out.)

Log messages are written to standard error, which is normally captured by the
desktop environment in a file such as ``$HOME/.xsession-errors``.  At the
default log level, very few messages will be produced, if any.


Configuration and Options
--------------------------

In many desktop environments, no configuration is needed.  Joystickwake
comes pre-configured with commands that will defer DPMS power-off
and common screensavers.  Those commands are::

    xset dpms force on s reset
    xscreensaver-command -deactivate
    gnome-screensaver-command --deactivate
    mate-screensaver-command --poke
    xfce4-screensaver-command --poke

If needed, an additional wake command can be configured in either of the
following files::

    $XDG_CONFIG_HOME/joystickwake/joystickwake.conf
    $HOME/.config/joystickwake/joystickwake.conf

This example illustrates the configuration file format and settings::

    command = xdg-screensaver reset # This might work on some desktops
    interval = 30                   # Number of seconds between wakes
    loglevel = warning              # Also: debug, info, error, critical

Command line options ``--command``, ``--interval``, and ``--loglevel`` are
available, and will override their corresponding config file settings.


Custom Wake Commands
--------------------

If none of the built-in commands work with a particular desktop environment,
finding one that does can require some experimentation.  For example, to
determine whether ``test command`` will wake the screen, try it with
joystickwake running in a terminal window, using a short wake interval and a
verbose log level, like so::

    joystickwake --loglevel debug --interval 2 --command "test command"

If joystickwake logs a "custom waker failed" message, it means the custom
command either produced an error or could not be executed.  If it logs a
"custom waker succeeded" message, and pressing a joystick button wakes the
screen, then the command works.  It can then be saved in the configuration
file for future login sessions.  (This experiment is best done with the screen
blanker set for a very short timeout, so the screen will blank while being
observed and the command being tested will have a chance to wake it.)

When run in a terminal window, Control+C will tell joystickwake to quit.


See Also
--------

- Project page:
  https://github.com/foresto/joystickwake
- Ubuntu package:
  https://launchpad.net/~foresto/+archive/ubuntu/toys
- xdg-screensaver (from xdg-utils, aka Portland) attempts to be a unified
  screensaver control interface:
  https://www.freedesktop.org/wiki/Software/xdg-utils/
- Caffeine inhibits the screensaver when it finds a fullscreen window:
  https://code.launchpad.net/caffeine
- Faux GNOME Screensaver is a GNOME compatibility layer for XScreenSaver:
  https://github.com/jefferyto/faux-gnome-screensaver
