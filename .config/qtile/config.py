### BUILT-IN LIBRARIES ###

import os
import subprocess

from typing import List  # noqa: F401
from time import time

### LIBQTILE ###

from libqtile import bar, layout, widget, hook, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import volume

### SPECIFIC VARIABLES ##

mod = 'mod4'
TERMINAL = 'alacritty'
BROWSER = 'firefox'


### USEFUL FUNCTIONS ###

def change_audio_volume(qtile, change: str, delta: str='5'):
    subprocess.run(['pamixer', change, delta])
    volume = int(subprocess.run(['pamixer', '--get-volume'], capture_output=True).stdout)
    subprocess.run(['volnoti-show', str(volume)])

def change_monitor_brightness(qtile, change: str, delta: str='5'):
    subprocess.run(['xbacklight', change, delta])
    brightness = float(subprocess.run(['xbacklight', '-get'], capture_output=True).stdout)
    subprocess.run(['volnoti-show',
                    '-s',
                    '/usr/share/pixmaps/volnoti/display-brightness-symbolic.svg',
                    str(brightness)])

def screenshot(save=True, copy=True):
    def f(qtile):
        path = os.path.expanduser('~/Pictures/screenshots/')
        path += f'screenshot_{str(int(time() * 100))}.png'
        shot = subprocess.run(['maim'], stdout=subprocess.PIPE)

        if save:
            with open(path, 'wb') as sc:
                sc.write(shot.stdout)

        if copy:
            subprocess.run(['xclip', '-selection', 'clipboard', '-t',
                            'image/png'], input=shot.stdout)
    return f

### KEY BINDINGS ###

keys = [
    # Switch between windows
    Key(
        [mod], 'h',
        lazy.layout.left(),
        desc='Move focus to left'
    ),
    Key(
        [mod], 'l',
        lazy.layout.right(),
        desc='Move focus to right'
    ),
    Key(
        [mod], 'j',
        lazy.layout.down(),
        desc='Move focus down'
    ),
    Key(
        [mod], 'k',
        lazy.layout.up(),
        desc='Move focus up'
    ),
    Key(
        [mod], 'space',
        lazy.layout.next(),
        desc='Move window focus to other window'
    ),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, 'shift'], 'h',
        lazy.layout.shuffle_left(),
        desc='Move window to the left'
    ),
    Key(
        [mod, 'shift'], 'l',
        lazy.layout.shuffle_right(),
        desc='Move window to the right'
    ),
    Key(
        [mod, 'shift'], 'j',
        lazy.layout.shuffle_down(),
        desc='Move window down'
    ),
    Key(
        [mod, 'shift'], 'k',
        lazy.layout.shuffle_up(),
        desc='Move window up'
    ),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod, 'control'], 'h',
        lazy.layout.grow_left(),
        desc='Grow window to the left'
    ),
    Key(
        [mod, 'control'], 'l',
        lazy.layout.grow_right(),
        desc='Grow window to the right'
    ),
    Key(
        [mod, 'control'], 'j',
        lazy.layout.grow_down(),
        desc='Grow window down'
    ),
    Key(
        [mod, 'control'], 'k',
        lazy.layout.grow_up(),
        desc='Grow window up'
    ),
    Key(
        [mod], 'n',
        lazy.layout.normalize(),
        desc='Reset all window sizes'
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, 'shift'], 'Return',
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'
    ),
    Key(
        [mod], 'Return',
        lazy.spawn(TERMINAL),
        desc='Launch terminal'
    ),

    # Toggle between different layouts as defined below
    Key(
        [mod], 'Tab',
        lazy.next_layout(),
        desc='Toggle between layouts'
    ),
    Key(
        [mod], 'w',
        lazy.window.kill(),
        desc='Kill focused window'
    ),

    # Qtile stuff
    Key(
        [mod, 'control'], 'r',
        lazy.restart(),
        desc='Restart Qtile'
    ),
    Key(
        [mod, 'control'], 'q',
        lazy.shutdown(),
        desc='Shutdown Qtile'
    ),
    Key(
        [mod], 'r',
        lazy.spawncmd(),
        desc='Spawn a command using a prompt widget'
    ),
    Key(
        [mod], 'p',
        lazy.spawn('dmenu_run -b'),
        desc='Run dmenu'
    ),

    # Sound control
    Key(
        [], 'XF86AudioRaiseVolume',
        lazy.function(change_audio_volume, change='-i'),
        desc='Increase volume'
    ),
    Key(
        [], 'XF86AudioLowerVolume',
        lazy.function(change_audio_volume, change='-d'),
        desc='Decrease volume'
    ),

    # Monitor brightness control
    Key(
        [], 'XF86MonBrightnessUp',
        lazy.function(change_monitor_brightness, change='-inc'),
        desc='Increase brightness'
    ),
    Key(
        [], 'XF86MonBrightnessDown',
        lazy.function(change_monitor_brightness, change='-dec'),
        desc='Decrease brightness'
    ),

    # Keyboard layout control
    Key(
        ['shift'], 'Alt_L',
        lazy.widget['keyboardlayout'].next_keyboard(),
        desc='Next keyboard layout'
    ),

    # Running applications
    Key(
        [mod], 'b',
        lazy.spawn(BROWSER),
        desc='Run browser of choice'
    ),
    Key(
        [], 'Print',
        lazy.function(screenshot()),
        desc='Take a screenshot of the whole screen'
    ),
    Key(
        ['control'], 'Print',
        lazy.spawn('flameshot'),
        desc='Run flameshot'
    ),
]


### DRAG FLOATING LAYOUTS ###

mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]


### GROUPS ###

groups = [Group(i) for i in '123456789']

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc='Switch to group {}'.format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        # Key([mod, 'shift'], i.name, lazy.window.togroup(i.name, switch_group=True),
        #     desc='Switch to & move focused window to group {}'.format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        Key([mod, 'shift'], i.name, lazy.window.togroup(i.name),
            desc='move focused window to group {}'.format(i.name)),
    ])


### COLORS ###

colors = {
    'border_focus':  '#34dccc',
    'border_normal': '#1d2330',
    'bg_odd':        '#464299',
    'bg_even':       '#904299',
    'bg_bar':        '#282a36',
    'bg_third':      '#19b085',
}


### DEFAULT LAYOUT THEME ###

layout_theme = dict(
    border_width=2,
    border_focus=colors['border_focus'],
    border_normal=colors['border_normal'],
    margin=8,
)


### LAYOUTS ###

layouts = [
    layout.Columns(
        **layout_theme,
        border_on_single=True,
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
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

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='flameshot'), # Flameshot
    Match(wm_class='display'), # ImageMagick
])


### DEFAULT WIDGET SETTINGS ###

widget_defaults = dict(
    font='JetBrainsMono',
    fontsize=14,
    padding=8,
)
extension_defaults = widget_defaults.copy()


### SCREENS ###

def icon(icon_text, background):
    return widget.TextBox(
        background=background,
        text=icon_text,
    )


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(),

                widget.GroupBox(
                    highlight_method='block',
                    disable_drag=True,
                ),

                widget.Prompt(),

                widget.WindowName(
                    max_chars=40,
                ),

                widget.Systray(),

                widget.Spacer(
                    length=25,
                ),

                icon('\U0001f321', colors['bg_even']),
                widget.ThermalSensor(
                    background=colors['bg_even'],
                ),

                icon('\U0001f4be', colors['bg_odd']),
                widget.Memory(
                    background=colors['bg_odd'],
                    format='{MemUsed}MiB/{MemTotal}MiB',
                ),

                icon('\U0001f50a', colors['bg_even']),
                volume.Volume(
                    background=colors['bg_even']
                ),

                widget.Battery(
                    background=colors['bg_odd'],
                    charge_char='\U0001f50c',
                    discharge_char='\U0001f50b',
                    format='{char} {percent:2.0%}',
                ),

                widget.KeyboardLayout(
                    background=colors['bg_even'],
                    configured_keyboards=['us', 'ru'],
                ),

                icon('\U0001f553', colors['bg_third']),
                widget.Clock(
                    background=colors['bg_third'],
                    format='%H:%M:%S, %A %d.%m.%Y',
                ),
            ],
            32,
            background=colors['bg_bar'],
            opacity=0.9,
        ),
    ),
]


### AUTOSTART ###

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run(['sh', script])


### VARIABLES ###

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = 'smart'

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'LG3D'
