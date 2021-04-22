#!/usr/bin/python3
#
# Change initial boot config for Diet-Pi + Amiberry 3.3
#
# " Alternate version: works on /mnt/dietpi_userdata/agplus/amiberry.sh "
# "   which is launched by the amiberry service in the ExecStart line.  "
#
# By default, Amiberry boots into the GUI.
#
# This script reads the existing configuration files (*.uae) in
# /mnt/dietpi_userdata/amiberry/ and allows to boot Amiberry into
# an specific configuration bypassing the GUI.
#
# It does it by altering the start parameters for the binary in
# the systemd's Amiberry service file.
#

import os
import sys
import re
import glob

script = "/mnt/dietpi_userdata/agplus/amiberry.sh"
confpath = "/mnt/dietpi_userdata/amiberry/conf"
lang = "en"

confparam = "--config \"./conf/{}\" -G"

#--- Basic i18n support --------------------------------------------------------
i18n_strings = {
    "title"  : { "es": "\n-- Establecer configuración por defecto para Amiberry --\n",
                 "en": "\n-- Set default configuration for Amiberry --\n" },
    "current": { "es": "Configuración actual:",
                 "en": "Current default config:" },
    "select" : { "es": "Selecciona en qué configuración arrancar:\n",
                 "en": "Please select a configuration to boot into:\n" },
    "none"   : { "es": "Ninguna (arrancar en el GUI de Amiberry)",
                 "en": "None (boot in Amiberry's GUI)" },
    "invalid": { "es": "\nValor no válido. Finalizando el programa...\n",
                 "en": "\nInvalid value. Aborting program...\n" },
    "quit":    { "es": "Salir sin realizar cambios.",
                 "en": "Exit with no changes." },
    "choice":  { "es": "Seleccione una opción",
                 "en": "Select an option" },
    "exit":    { "es": "\nSaliendo del programa sin realizar cambios.\n",
                 "en": "\nEnding program with no changes.\n" },
    "done":    { "es": "\nCambio realizado. Reinicia con 'reboot' para aplicar los cambios.\n",
                 "en": "\nChange finished. Please restart with 'reboot' to apply changes.\n" },

}

def i18n( key ):
    if key in i18n_strings and lang in i18n_strings[key]:
        return i18n_strings[key][lang]
    return "{}".format(lang.key)


#--------------------------------------------------------------------------------
def getExecStartLine(script):
    line = ''

    # Get current config line
    with open(script) as fp:
        for line in fp:
            if re.match('.*amiberry/amiberry[$ ]', line):
                break
    return line


#--------------------------------------------------------------------------------
def replaceConfig(script, option):
    if not os.path.exists(script) and os.path.isfile(script):
        print("ERROR: File '{}' does not exist".format(script))
        sys.exit(3)

    try:
        fp = open(script, "r")
        lines = fp.readlines()
        fp.close()
    except:
        print("ERROR: File '{}' cannot be read".format(script))
        sys.exit(4)

    for i in range(0, len(lines)):
        line = lines[i]
        match = re.search("^(.*amiberry/amiberry)($|.*$)", line)
        if match:
            command = match.group(1)
            if option == '':
                line = "{}\n".format(command)
            else:
                param = confparam.format(option)
                line = "{} {}\n".format(command, param)
            lines[i] = line

    try:
        fp = open(script, "w")
        fp.write("".join(lines))
        fp.close()
    except:
        print("ERROR: File '{}' cannot be written".format(script))
        sys.exit(5)


#--------------------------------------------------------------------------------
def main():

    line = getExecStartLine(script)
    if line == '':
        print("ERROR: ExecStart line not found in '{}'".format(script))
        sys.exit(2);

    none = i18n("none")
    current_config = none

    # Get current configuration
    config_found = re.search("./conf/(.*).uae", line)
    if config_found:
        current_config = "{}.uae".format(config_found.group(1))

    # Print main menu with title, current config, and list of configs
    print(i18n("title"))
    print("{}\n".format(i18n("current")))
    print("    {}\n".format(current_config))

    print(i18n("select"))

    selected = " (*)" if current_config == none else ""
    print("    0.- {}{}".format(none, selected))

    # Print list of existing UAE files in the confpath
    files=glob.glob( os.path.join(confpath, "*.uae") )
    files_conf = [""]
    for i, file in enumerate(files, start=1):
        filename = os.path.basename(file)
        files_conf.append(filename)
        selected = " (*)" if filename == current_config else ""
        print("    {}.- {}{}".format(i, filename, selected))

    print("    q.- {}".format(i18n("quit")))

    # Read user input
    option = input("\n{}: ".format(i18n("choice")))
    if option == "q" or option == "Q":
        print(i18n("exit"))
        sys.exit(0)

    try:
        option = int(option)
        option = files_conf[option]
    except:
        print(i18n("invalid"))
        sys.exit(1)

    replaceConfig(script, option)
    print(i18n("done"))

if __name__ == "__main__":
    main()
