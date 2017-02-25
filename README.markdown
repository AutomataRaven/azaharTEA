# AzaharTEA

AzaharTEA is a text editor with highlighting. The name is just a play with Azahar Text Editor (T.E, tea pronounced faster).

## Prerequisites

To run the text editor you will need.

* [Python](https://www.python.org/) - Version 3.5
* [Kivy](https://kivy.org/#home) - Version 1.9.1
* [Pygments](http://pygments.org/) - Version 2.2.0

## Features

Because the text editor is not a very complete one, here is a list of the features:

- Text highlighting
- Loading and saving files
- Change the style of the text
- Line numbers display

## Suported languages for highlighting

All the [lexers](http://pygments.org/docs/lexers/) included in Pygments are supported.
The files with *.kv* extension are highlighted with the [kivy lexer](https://github.com/kivy/kivy/blob/master/kivy/extras/highlight.py).

## Running the program

Execute **azaharTEA.py** in the *root* directory.

```
./azaharTEA.py
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
