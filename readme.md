# mcdata-to-json

Python script to generate json files from a minecraft server.

Currently when provided a minecraft server directory that contains a minecraft server jar named `server.jar`, it will run and save the following information:

- server-advancements.json
  - possible advancements and which player has what critera complete
- `<player-uuid>`.json
  - advancements progress
  - stats
  - playerdata (includes inventory and ender chest)
  - in-game name
  - url to skin texture
- uuids.json
  - dictionary of `<player-uuid>`: 'in-game name'

## Usage

Clone this repository (or download a release and unzip). Inside the `py-mcdata-to-json` folder:

(Optionally create a venv to run the following from.)

```bash
pip install -r requirements.txt
python ./mcdata_to_json/ -i /path-like/string/to/minecraft-server-directory
```

If you unzip this in the folder next to your server, you could run it:

```bash
python ./mcdata_to_json/ -i ../minecraft-server/
```

## Argument Help

```bash
Python tool to create JSON files from minecraft server data.

optional arguments:
  -h, --help            show this help message and exit
  -i MINECRAFTDIR, --minecraft-dir MINECRAFTDIR
                        Directory of the minecraft server.
  -j SERVERJAR, --jar-name SERVERJAR
                        Name of the miencraft server jar.
  -o OUTPUTDIR, --outdir OUTPUTDIR
                        Destination directory for JSON files.
  -t CACHEDIR, --cachedir CACHEDIR
                        Destination directory for JSON files.
```
