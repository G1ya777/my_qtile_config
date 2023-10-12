#!/bin/bash
xrandr --output DP-0 --mode 1920x1080 --rate 144 &
redshift -x && redshift -O 4000 &
picom --config  ~/.config/picom/picom.conf &
nitrogen --restore &
lxpolkit &
caffeine &
parcellite &
pasystray &
xpad &
muezzin &
uget-gtk &
xfce4-power-manager &
