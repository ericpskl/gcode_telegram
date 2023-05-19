# gcode_telegram
A host module for Klipper that allows the sending of Telegram messages via gcode commands

# Installation

1. Copy gcode_telegram.py to your Klipper "extras" folder.  Under Mainsail OS:

```
cp gcode_telegram.py /home/pi/klipper/klippy/extras
```

2. Install the Python Requests module

``` 
cd klippy-env/
source klippy-env/bin/activate
python -m pip install requests
```

3. Create a Telegram Bot to use with Klipper

See https://core.telegram.org/bots/tutorial for instructions.  Make note of your bot's Token and Chat ID.

4. Enable gcode_telegram in your printer.cfg.  

```
[gcode_telegram bot]
token:  <<token>>
chatid: <<chatid>
printer_name: Elaine
verbose: true
timeout: 5
```

4.  Test


