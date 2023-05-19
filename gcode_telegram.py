#
# gcode_telegram.py -- Send a Telegram (https://telegram.org/) message via gcode
# https://github.com/ericpskl/gcode_telegram
# 5/19/2023 -- Initial Public Release
#
# Copyright (C) 2023 Eric Smith <eric@apisresearch.org>
# This file may be distributed under the terms of the GNU GPLv3 license.
#
# Installation Note: This host module requires the 'requests' module.  To install requests into the klippy-env virtual environment:
#
# $ cd klippy-env/
# $ source klippy-env/bin/activate
# $ python -m pip install requests
# $ service klipper restart

import requests
import logging
import re
import pprint

class Telegram:
    def __init__(self, config):

        self.name = config.get_name().split()[-1]
        
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
       
        self.verbose = config.getboolean('verbose', True)
        self.timeout= config.getint('timeout', 5.)

        self.token  = config.get('token')
        self.chatid = config.get('chatid')

        self.printer_name = config.get('printer_name', '')

        self.gcode.register_mux_command( "SEND_TELEGRAM", "BOT", self.name, self.cmd_SEND_TELEGRAM, desc=self.cmd_SEND_TELEGRAM_help)

    cmd_SEND_TELEGRAM_help = "Syntax:  SEND_TELEGRAM BOT=<bot name> MESSAGE='<message text>'"

    def cmd_SEND_TELEGRAM(self, params):

	# Send the telegram message through the Telegram Bot API: https://core.telegram.org/bots

        if self.printer_name != '':
            message = requests.utils.quote(f'[{self.printer_name}] ' + params.get('MESSAGE',''))
        else:
            message = requests.utils.quote(                            params.get('MESSAGE',''))

        if len(message) == 0:
            self.gcode.respond_info("[gcode_telegram] MESSAGE cannot be empty.")

        else:

            try:
                 url=f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chatid}&text={message}"
                 r=requests.get(url, timeout=self.timeout)
    
                 if r.status_code == 200 and r.json()['ok']:
                     if self.verbose: self.gcode.respond_info(f"[gcode_telegram] Message '{message}' sent OK by {r.json()['result']['from']['username']}")
                     r.close()
                 else:
                     if self.verbose: self.gcode.respond_info("Unable to send Telegram message. See log.")
                     logging.exception(f"[gcode_telegram] Unable to send Telegram Message: {r.content}")
                     r.close()
    
            except Exception as e:
                 if self.verbose: self.gcode.respond_info("Unable to send Telegram message: %s" % str(e))

def load_config_prefix(config):
    return Telegram(config)
