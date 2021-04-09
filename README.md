# dietpi-amiberry-bootconf
Change DietPi Amiberry initial configuration profile (skipping GUI).

By default, Amiberry boots into the GUI.

This simple script reads the existing configuration files (*.uae) in `/mnt/dietpi_userdata/amiberry/` and allows to boot Amiberry into
an specific configuration bypassing the GUI.

It does it by altering the start parameters for the binary in the systemd's Amiberry service file.

It changes the ExecStart line in `/etc/systemd/system/amiberry.service` between:

`ExecStart=/mnt/dietpi_userdata/amiberry/amiberry`

and:

`ExecStart=/mnt/dietpi_userdata/amiberry/amiberry --config "./conf/CONFIG_FILE_NAME.uae" -G`

Please note that the current parameter format (`--config "filename.uae"`) will work with Amiberry 3.3. Other versiones use the `-config=filename.uae` format.


# Sample usage output

Just run the script and select the desired configuration file, or "0" to boot into the GUI.

```
# change_default_amiberry_config.py

-- Set default configuration for Amiberry --

Current default config:

    AGPLUS.uae

Please select a configuration to boot into:

    0.- None (boot in Amiberry's GUI)
    1.- AGPLUS.uae (*)
    2.- A1200 WHDLOAD OS31.uae
    3.- MegaAGS.uae
    q.- Exit with no changes.

Select an option: 3

Change finished. Please restart with 'reboot' to apply changes.

```

# TODO

- Read confpath from DietPi's configuration (do not assume /mnt/dietpi_userdata).
- Detect Amiberry's version as the --config/-config parameter format changed in 3.x.
- The script has builin support for i18n into the `lang="XX"` variable. Allow the user to set the language via command line parameter, or get it from $LANG.

