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

# TODO:

- Read confpath from DietPi's configuration (do not assume /mnt/dietpi_userdata).
-
- Detect Amiberry's version as the --config/-config parameter format changed in 3.x.

