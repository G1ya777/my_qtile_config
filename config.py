# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from qtile_extras import widget as widget_extras
from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
from libqtile import hook

from libqtile.log_utils import logger


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])


@lazy.function
def float_to_front(qtile):
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.cmd_bring_to_front()


focus_on_window_activation = "focus"
bring_front_click = True
follow_mouse_focus = False

mod = "mod4"
terminal = guess_terminal()


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod, "control"], "f", float_to_front),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows in stack.
    Key([mod], "c", lazy.layout.client_to_next()),
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncd(), desc="Spawn a command using a prompt widget"),
    # My keybindings
    # browser
    Key(
        [mod], "b", lazy.spawn("brave --silent-debugger-extension-api --disable-webgl")
    ),
    Key([mod], "m", lazy.spawn("thunar")),
    # control volume
    Key([mod], "r", lazy.spawn('rofi -font "Fira Sans 16" -show drun')),
    # Increase volume with XF86AudioRaiseVolume key
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pulsemixer --change-volume +10 --max-volume 100"),
    ),
    # Decrease volume with XF86AudioLowerVolume key
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pulsemixer --change-volume -10 --max-volume 100"),
    ),
    # Mute/unmute with XF86AudioMute key
    Key([], "XF86AudioMute", lazy.spawn("pulsemixer --toggle-mute")),
    # launch screenshot program
    Key([mod], "Home", lazy.spawn("flameshot gui")),
]

groups = [
    Group("a", matches=[Match(wm_class=["firefox", "Brave-browser"])]),
    Group("s", matches=[Match(wm_class=["Chat-gpt"])]),
    Group("d", matches=[Match(wm_class=["code-oss"])]),
    Group("f", matches=[Match(wm_class=["Eom", "thunar"])]),
    Group("g", matches=[Match(wm_class=["TelegramDesktop"])]),
    Group("u", matches=[Match(wm_class=["smplayer"])]),
    Group("i", matches=[Match(wm_class=["Uget-gtk", "qBittorrent"])]),
    Group("o"),
    Group(
        "p",
        matches=[
            Match(
                wm_class=[
                    "steam",
                    "Lutris",
                    "Steam",
                    "heroic",
                    "Apex Legends",
                ]
            )
        ],
    ),
]


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


layouts = [
    layout.Max(
        margin=[3, 5, 5, 3],
        border_normal="#808080",
        border_focus="#ac4f06",
        border_width=2,
        rounded=True,
    ),
    layout.Columns(
        border_normal="#808080",
        border_focus="#ac4f06",
        border_width=2,
        rounded=True,
        margin=[3, 5, 5, 3],
    ),
    layout.Floating(
        border_normal="#808080",
        border_focus="#ac4f06",
        border_width=2,
        rounded=True,
        margin=[5, 0, 0, 5],
    ),
    # layout.Stack(num_stacks=5,border_width=2,margin=15),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Fira Mono",
    fontsize=14,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(font="Fira Mono", max_chars=3),
                widget.CurrentLayoutIcon(),
                widget.Sep(padding=10, foreground="ffffe4"),
                widget.GroupBox(
                    font="Fira Mono",
                    disable_drag=True,
                    rounded=True,
                    use_mouse_wheel=False,
                    highlight_method="line",
                    inactive="#808080",
                    highlight_color=["#ac4f06", "#ac4f06"],
                ),
                widget.Sep(padding=10, foreground="ffffe4"),
                widget.WindowName(
                    empty_group_string="                                            Arch Linux",
                    fontsize=12,
                    font="Fira Sans",
                    scroll=True,
                    scroll_fixed_width=True,
                    width=275,
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Sep(padding=10, linewidth=0),
                widget.Sep(padding=10, foreground="ffffe4"),
                widget.Net(
                    interface="enp10s0",
                    format="net {down:6.2f}{down_suffix:<2} ↓↑{up:6.2f}{up_suffix:<2}",
                    prefix="M",
                ),
                widget.Sep(padding=30, foreground="ffffe4"),
                widget.NvidiaSensors(format="GPU {temp}"),
                widget.Sep(padding=30, foreground="ffffe4"),
                widget.Clock(format="%d-%m-%Y %a %H:%M", font="Fira Sans", fontsize=15),
                widget.Sep(padding=20, foreground="ffffe4"),
                widget.CPU(),
                widget.ThermalSensor(tag_sensor="Tctl"),
                widget.Sep(padding=10, foreground="ffffe4"),
                widget.Memory(
                    format="RAM {MemUsed: .0f}{mm} / 32G",
                ),
                widget.Sep(padding=10, foreground="ffffe4"),
                widget.DF(
                    visible_on_warn=False,
                    warn_space=20,
                    format="dir:{p} ({uf}{m} / {s}{m} free)",
                    fontsize=12,
                ),
                widget.DF(
                    visible_on_warn=False,
                    partition="/mnt/Downloads",
                    fmt="dir:  dow {}",
                    warn_space=100,
                    format="({uf}{m} / {s}{m} free)",
                    fontsize=12,
                ),
                widget.Sep(padding=7, foreground="ffffe4"),
                widget.Systray(icon_size=22),
                widget.TextBox(
                    text="RW",
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            "nitrogen --random --set-zoom-fill --save /usr/share/backgrounds"
                        )
                    },
                ),
                # widget.Sep(padding=10),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background="#3d3d3d",
            opacity=0.925,
            rounded=True,
            margin=[2, 2, 2, 2],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
cursor_warp = False
floating_layout = layout.Floating(
    border_normal="#808080",
    border_focus="#ac4f06",
    border_width=2,
    rounded=True,
    margin=[2, 0, 0, 5],
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)
auto_fullscreen = True

reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
