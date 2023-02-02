joystickwake
============

-----------------------------
A joystick-aware screen waker
-----------------------------

:Manual section: 1
:Date:           2023-02-01


Synopsis
--------

    joystickwake -h|--help

    joystickwake [--command cmd] [--cooldown seconds] [--loglevel level]


Description
-----------

Linux gamers often find themselves unexpectedly staring at a blank screen,
because their display server fails to recognize game controllers as input
devices, allowing the screen blanker to activate during gameplay.  This
program works around the problem by suppressing screen blankers while
joystick activity is detected.


Overview
--------

When installed from a package, joystickwake launches automatically when a user
logs in to any modern linux desktop environment.  It can also be run manually,
without formal installation, since the executable is self-contained.

While running, it monitors udev to find devices with the ID_INPUT_JOYSTICK
property (including devices that are plugged in later) and reacts to activity
from any of them.

The screen is kept awake by periodically running a heartbeat-like wake command:
an external tool provided by the system.  Most desktop environments and screen
savers include such a command, and joystickwake knows how to use the common
ones, so there is normally no need for a user to install or configure one.
This design keeps joystickwake compatible with just about every screensaver and
power management system there is.


Operation
---------

When joystick activity is detected, all known wake commands are executed.
Any command reporting an error or missing from the system will be skipped
thereafter.  This process repeats in a loop, with a cooldown period between
wakes.  Joystickwake thereby learns which commands are available on the host
system, avoids excessive work that might cause game lag, and minimizes log
clutter.  In practice, it is very lightweight.

If the python3 dbus-next package is installed, joystickwake will also try to
inhibit the desktop environment's screen idle state for a short while after
detecting activity, using the org.freedesktop.ScreenSaver interface.  This
helps with certain environments whose heartbeat-style wake interfaces are
missing or broken.

If all known wakers fail, joystickwake will quit.  This could happen if no
screen blanker is running, or if one that is running requires a custom wake
command (see below).

If the python3 Xlib package is installed, joystickwake will quit when the
desktop session ends.  Otherwise, it will quit when its parent process exits.
(This avoids leaving old instances running after the user logs out.)

Log messages are written to standard error, which is normally captured by the
desktop environment in a file such as ``$HOME/.xsession-errors``.  At the
default log level, few messages will be produced, if any.


Configuration and Options
--------------------------

In many desktop environments, no configuration is needed.  Joystickwake
comes preconfigured with commands that will suppress common screensavers
and DPMS power-off.  Those commands are::

    xset dpms force on
    xset s reset
    xscreensaver-command -deactivate
    gnome-screensaver-command --deactivate
    mate-screensaver-command --poke
    xfce4-screensaver-command --poke
    dbus-send [...] org.freedesktop.ScreenSaver.SimulateUserActivity

If needed, an additional wake command can be configured in either of the
following files::

    $XDG_CONFIG_HOME/joystickwake/joystickwake.conf
    $HOME/.config/joystickwake/joystickwake.conf

This example illustrates the configuration file format and settings::

    command = xdg-screensaver reset # This might work on some desktops
    cooldown = 30                   # Number of seconds between wakes
    loglevel = warning              # Also: debug, info, error, critical

Command line options ``--command``, ``--cooldown``, and ``--loglevel``
will override their corresponding config file settings.


Troubleshooting
---------------

The first step in diagnosing a problem is to set joystickwake's log level
to ``debug``, restart it, and look for unexpected messages when the problem
occurs.  Running it in a terminal window may help with log visibility.

Note:  Joystickwake cannot see your screen, and therefore has no way to be
certain of its state.  A success message in the log means only that a wake
command ran without reporting an error.  That is a good sign, but not always
sufficient to wake the screen, especially if that wake command was designed
for a screen blanker other than the one in use.

Every log message begins with "joystickwake" and a timestamp, so if you see
text in some other format, it comes from another program.  For example, one of
the wake commands might print a message about being unable to find its screen
saver, or your shell's command-not-found script might offer suggestions when
joystickwake probes for a command that is not installed on your system.  Both
of these examples are harmless, and should appear only a few times, since
joystickwake avoids failing commands after a few tries.

If joystickwake keeps the screen awake even when all joysticks are idle, it is
likely due to "stick drift", meaning that a joystick either is not centering
itself properly or is suffering from a faulty sensor.  This is unfortunately
common in modern game controllers.  Other than replacing the hardware, or
disconnecting it when not in use, this can be resolved by calibrating the dead
zones used by the linux evdev and joystick APIs, as described here:

https://wiki.archlinux.org/title/Gamepad#Setting_up_deadzones_and_calibration

If the screen wakes with joystick input, but never blanks again even when all
joysticks are disconnected, it could be due to a mismatch between your screen
blanker and one of the wake commands installed on your system.  For example, a
modern GNOME Shell might misinterpret D-Bus messages sent by an old
gnome-screensaver-command.  Removing that command from your system and
restarting your desktop session should help.

If the log shows at least one waker succeeding but the screen still blanks
while a joystick is in use, your screen blanker's timeout might be too short
for joystickwake.  Increasing that timeout or decreasing joystickwake's
``cooldown`` setting might help.

Alternatively, it is possible that multiple screen blankers are running, such
as a graphical screen saver and a power manager, with joystickwake only knowing
how to wake one of them.  The solution is to find a command that will wake the
problematic one, make sure that command is installed, and if joystickwake
doesn't recognize it by default, configure it as a custom command.

If all wakers fail and the screen still blanks, the solution is the same as
above:  Identify your desktop's screen blanker, install a command that will
wake it, and (if necessary) configure joystickwake to use it.


Custom Wake Commands
--------------------

If none of joystickwake's preconfigured commands wake the screen in a
particular desktop environment, finding one that does can require some effort.
Asking community members who use the same environment might yield a helpful
answer.  Once you know the name of the component that blanks the screen,
consult its documentation to see if it has a command line tool for controlling
it.  It may also be worthwhile to query your linux distribution's package
manger to see if such a tool was installed along with the screen blanker.

After identifying a command that might work, the next step is to test it,
preferably without joystickwake running.  The simplest way is to set your
screen blanker to use a short timeout (e.g. one minute), run the command
preceded by a ``sleep`` delay longer than the blanker's timeout, and let
your system sit idle to see if it works.

For example, this command line does it with a 77 second delay::

    sleep 77; my-cmd --wake

If the screen blanks as expected and then wakes after the sleep delay, the
command will probably work with joystickwake.  You can try it in a terminal
window, like so::

    joystickwake --loglevel debug --cooldown 2 --command "my-cmd --wake"

If joystickwake logs a "custom waker failed" message, it means the custom
command either produced an error or could not be executed.  If pressing a
joystick button wakes the screen and logs a "custom waker succeeded" message,
then the command works, and can be saved in the configuration file for future
login sessions.

When run in a terminal window, Control+C will tell joystickwake to quit.

The xdg-screensaver tool might work as a custom wake command in some
environments::

    xdg-screensaver reset

Users of KDE Plasma with XWayland might find that joystickwake's preconfigured
commands do not suppress the screen energy saving feature.  This appears to be
a bug in KDE's SimulateUserActivity implementation, reported as bug #440882.
A KDE maintainer stated in that report that XWayland is not supported, so the
bug seems unlikely to be fixed, but the following custom wake command might
be an effective workaround::

    qdbus org.kde.Solid.PowerManagement /org/kde/Solid/PowerManagement wakeup


See Also
--------

- Project page:
  https://github.com/foresto/joystickwake
- Ubuntu package:
  https://launchpad.net/~foresto/+archive/ubuntu/toys
- xdg-screensaver (from xdg-utils, aka Portland) attempts to be a unified
  screensaver control interface:
  https://www.freedesktop.org/wiki/Software/xdg-utils/
- Caffeine runs `xdg-screensaver suspend` when it finds a fullscreen window:
  https://code.launchpad.net/caffeine
- Faux GNOME Screensaver is a GNOME compatibility layer for XScreenSaver:
  https://github.com/jefferyto/faux-gnome-screensaver
