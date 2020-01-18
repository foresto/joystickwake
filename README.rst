joystickwake
============

-----------------------------
A joystick-aware screen waker
-----------------------------

:Manual section: 1
:Date:           2017-02-09


Synopsis
--------

    joystickwake -h|--help

    joystickwake [--command cmd] [--interval seconds] [--loglevel level]


Description
-----------

Linux gamers often find themselves unexpectedly staring at a blank screen,
because their display server fails to recognize game controllers as input
devices and allows the screen blanker to activate during gameplay. This
program attempts to work around the problem by periodically delaying screen
blankers when it detects joystick activity.

Once installed, joystickwake launches automatically when a user logs in to
any modern linux desktop environment.  It can also be run manually, either
from a command prompt or from a user-created menu entry.  It then monitors
udev to find joystick devices (including those that are plugged in later)
and reacts to activity from any of them.

Configuration
-------------

In many desktop environments, no configuration is required.  Joystickwake
comes pre-configured with commands that are known to wake the screen from
DPMS power-off and several common screen savers.  Those commands are::

    xset dpms force on s reset
    xscreensaver-command -deactivate
    gnome-screensaver-command --deactivate
    mate-screensaver-command --poke
    xfce4-screensaver-command --poke

If one of those commands fails, it will be skipped when the screen is next due
to be awakened.

When the built-in commands are not sufficient, a custom command can be defined
in either of the following configuration files::

    $XDG_CONFIG_HOME/joystickwake/joystickwake.conf
    $HOME/.config/joystickwake/joystickwake.conf

This example illustrates the file format and available settings::

    command = xdg-screensaver reset # This might work on some desktops.
    interval = 30                   # Number of seconds between wakes.
    loglevel = warning              # Also: debug, info, error, critical.


Options
-------

Command line options ``--command``, ``--interval``, and ``--loglevel`` are
available, and will override their corresponding config file settings.


Notes
-----

If all the screen-waking commands fail, joystickwake will quit.

If the python3 Xlib package is installed, joystickwake will quit when the
desktop session ends.  Otherwise, it will quit when its parent process exits.
This avoids leaving old instances running after the user logs out.

Log messages go to standard error, which is normally captured by the desktop
environment in a file such as ``$HOME/.xsession-errors`` or
``$HOME/.cache/upstart/startxfce4.log``.  At the default loglevel setting, very
few messages will be produced, if any.

If none of the built-in commands work with a particular desktop environment,
finding one that does can require some experimentation.  Running joystickwake
from a terminal window makes this relatively easy.  For example::

    joystickwake --loglevel debug --interval 5 --command "test command"

Once a working command is discovered, it can be saved in the configuration file
for use in future login sessions.


See Also
--------

- Project page:
  https://github.com/foresto/joystickwake
- Ubuntu package:
  https://launchpad.net/~foresto/+archive/ubuntu/toys
- xdg-screensaver (from xdg-utils, aka Portland) attempts to be a unified
  screen saver control interface:
  https://www.freedesktop.org/wiki/Software/xdg-utils/
- Caffeine inhibits the screen saver when it finds a fullscreen window:
  https://code.launchpad.net/caffeine
- Faux GNOME Screensaver is a GNOME compatibility layer for XScreenSaver:
  https://github.com/jefferyto/faux-gnome-screensaver
