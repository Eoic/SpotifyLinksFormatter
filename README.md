# Spotify Links Formatter
Formats list of Spotify tracks into human headable markdown list.

## Usage
1. Create input file `tracks.txt` and enter a list of track links.
2. Create `.env` and set required environment variables.
3. Install dependencies and run `python main.py`.
4. Output will be written into `tracks.md`.

### Example input
**tracks.txt**
```
https://open.spotify.com/track/2lmLfGIG14WEDJw8FYdQ7m?si=6029e6956d244991
```

### Example output
**tracks.md**
```
1. [Aglisia - Vento leggero](https://open.spotify.com/track/6ksVNrLijeVZjx4zmWKzQQ?si=5d87dfa947c84e8b)
```
