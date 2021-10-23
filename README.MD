# Listify

Listify is a Spotify playlist generator that creates playlists from artists' top songs. It uses OAuth for secure user connection and the Spotipy Library for interacting with Spotify.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Setup

Create a `.env` file in the root directory of the project with your spotify app cridentials.

```bash
# .env

CLIENT_ID= ""
CLIENT_SECRET = ""
COOKIE_NAME = ""
SECRET_KEY = ""
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
