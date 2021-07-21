### BUILT-IN LIBRARIES ###

import os
import subprocess

from typing import List  # noqa: F401
from time import time

### LIBQTILE ###

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# My version of widget.Volume using `pamixer`
import volume


### AUTOSTART ###

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run(['sh', script])


### SPECIFIC VARIABLES ##

mod = 'mod4'
TERMINAL = 'alacritty'
BROWSER = 'brave'
FILEMANAGER = 'pcmanfm'
# TERMFILEMANAGER = 'vifm'


### COLORS ###

colors = {
    'border_focus':  '#34dccc',
    'border_normal': '#1d2330',
    'bg_odd':        '#464299',
    'bg_even':       '#904299',
    'bg_bar':        '#282a36',
    'bg_third':      '#19b085',
}


### GROUPS ###

# Needed for groups, the rest is at the end of the config
keys = []

groups = [Group(i) for i in '123456789']

for i in groups:
    keys.extend([
        Key(
            [mod], i.name,
            lazy.group[i.name].toscreen(),
            desc='Switch to group {}'.format(i.name)
        ),
        Key(
            [mod, 'shift'], i.name,
            lazy.window.togroup(i.name),
            desc='Move focused window to group {}'.format(i.name)
        ),
    ])


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
    Match(role='pop-up'),
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
        padding=0,
    )

def arrow(foreground, background):
    return widget.TextBox(
        text='\uf0d9',
        foreground=foreground,
        background=background,
        fontsize=64,
        padding=-1,
    )

def lower_right_triangle(foreground, background):
    return widget.TextBox(
        text='\u25e2',
        foreground=foreground,
        background=background,
        fontsize=64,
        padding=0,
    )


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                    scale=0.6
                ),

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

                arrow(
                    foreground=colors['bg_even'],
                    background=colors['bg_bar']
                ),

                icon('\U0001f321', colors['bg_even']),
                widget.ThermalSensor(
                    background=colors['bg_even'],
                    threshold=80,
                ),

                arrow(
                    foreground=colors['bg_odd'],
                    background=colors['bg_even']
                ),

                icon('\uf2db', colors['bg_odd']),
                widget.Memory(
                    background=colors['bg_odd'],
                    format='{MemUsed: .0f}MiB/{MemTotal: .0f}MiB',
                ),

                arrow(
                    foreground=colors['bg_even'],
                    background=colors['bg_odd']
                ),

                icon('\uf028', colors['bg_even']),
                volume.Volume(
                    background=colors['bg_even']
                ),

                arrow(
                    foreground=colors['bg_odd'],
                    background=colors['bg_even']
                ),

                widget.Battery(
                    background=colors['bg_odd'],
                    charge_char='\ufaf0',
                    discharge_char='\uf578',
                    format='{char} {percent:2.0%}',
                    low_percentage=0.15,
                    notify_below=15,
                ),

                arrow(
                    foreground=colors['bg_even'],
                    background=colors['bg_odd']
                ),

                icon('\uf11c', colors['bg_even']),
                widget.KeyboardLayout(
                    background=colors['bg_even'],
                    configured_keyboards=['us', 'ru'],
                ),

                lower_right_triangle(
                    foreground=colors['bg_third'],
                    background=colors['bg_even']
                ),

                icon('\uf5ef', colors['bg_third']),
                widget.Clock(
                    background=colors['bg_third'],
                    format='%I:%M:%S %p, %A %d.%m.%Y',
                ),
            ],
            32,
            background=colors['bg_bar'],
            margin=3,
            opacity=0.9,
        ),
    ),
]


### QTILE'S VARIABLES ###

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = 'smart'
wmname = 'LG3D'


### USEFUL FUNCTIONS ###

def change_audio_volume(qtile, change: str, delta: str='5'):
    subprocess.run(['pamixer', change, delta])

def toggle_mute_audio(qtile):
    subprocess.run(['pamixer', '-t'])

def change_monitor_brightness(qtile, change: str, delta: str='5'):
    subprocess.run(['xbacklight', change, delta])


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

keys.extend([
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
    # Key(
        # [mod, 'shift'], 'Return',
        # lazy.layout.toggle_split(),
        # desc='Toggle between split and unsplit sides of stack'
    # ),

    # Toggle between different layouts as defined below
    Key(
        [mod], 'Tab',
        lazy.next_layout(),
        desc='Toggle between layouts'
    ),
    Key(
        [mod], 'q',
        lazy.window.kill(),
        desc='Kill focused window'
    ),
    Key(
        [mod], 't',
        lazy.window.toggle_floating(),
        desc='Put the focused window to/from floating mode'
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
    Key(
        [], 'XF86AudioMute',
        lazy.function(toggle_mute_audio),
        desc='Toggle mute audio'
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

    # Screenshots
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

    # Running applications
    Key(
        [mod], 'Return',
        lazy.spawn(TERMINAL),
        desc='Launch terminal'
    ),
    Key(
        [mod, 'shift'], 'Return',
        lazy.spawn('dmenu_run -b'),
        desc='Run dmenu'
    ),
    Key(
        [mod], 'b',
        lazy.spawn(BROWSER),
        desc='Run browser of choice'
    ),
    Key(
        [mod], 'g',
        lazy.spawn(FILEMANAGER),
        desc='Run GUI-based file manager of choice'
    ),
    # Key(
        # [mod], 'f',
        # lazy.spawn(TERMINAL + ' -e ' + TERMFILEMANAGER),
        # desc='Run terminal-based file manager of choice'
    # ),
])


### DRAG FLOATING LAYOUTS ###

mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

