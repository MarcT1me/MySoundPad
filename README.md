# Mys SoundPad

![icon](ico.png)

### Descriprion
Hello. This My sound pad. That use this application you need set VirtualCable. In App dir Im copy my VB Cable.

Im recommend copy this guid in txt file. You can delete config, to see this guid
First steps:
1) set VB;
2) restart App;
3) find him in `Devise/VB-list` on bar
4) copy id, or name in field.
5) click \"detect devise\"
Congratulation, you set up app configs

How Use:
1) find your sound in `File/File`
2) set configs
3) select your Virtual Cable in Discord/Game/other app
4) click play
5) to stop click stop

Tips: (REQUIREMENT TO READING)
* use standard `sound` dir in main app patch
* `volume` change ONLY headphone volume, not microphone
* you can find new file, before ending current playing fil
    Them name on `selected` and `played` file field be not equal
* read tracback text, him can help fix this error in future
* ids in `VB-list` not fuller, you can click on `debug - all devises` to see all
GOOD USING. Thanks.

### Command on compilation
* pyinstaller:\
`pip install --upgrade pyinstaller`\
don't forget to transfer the icon and the mp3 file
```shell
pyinstaller --name "Test Bild" --icon="ico.png" main.pyw
```