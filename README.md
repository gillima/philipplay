# PhilipPlay

This project is used to play OGG sound files on a *Raspberry Pi*.
The player loads OGG files from a base directory. Each folder gets a keyboard key from '1' to '9' assigned.
Pressing one of the assigned keys will start playing the first song of the selected folder.
As long as the same key is pressed, the player will play the files from this folder.

# Build the Debian Package

The *Debian* package for *philipplay* can be build by running the following command:
`debuild -us -uc`

The *Debian* package will be located in the parent folder of the project.

## Contributors:
* [Markus Gilli](https://github.com/gillima)
