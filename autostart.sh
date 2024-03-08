#!/bin/bash
numlockx &
# xrandr --output DP-0 --mode 1920x1080 --rate 144 &
redshift -x && redshift -O 3000 &
picom --config  ~/.config/picom/picom.conf &
xfsettingsd &
nitrogen --restore &
lxpolkit &
caffeine &
parcellite &
pasystray &
xpad &
uget-gtk &
dunst &
xfce4-power-manager &
xfce4-volumed-pulse &
qbittorrent &
