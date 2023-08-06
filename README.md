# Bing Image of the Day
A small library for accessing Bing's Image of the Day feed.

There are known quirks with the feed. Since little is documented, this was developed based on the observed behaviors. The feed will not generate errors when provided bad inputs. It will attempt to either generate a feed based on the parameters it is provided, or return a `NULL` reponse. It is a good idea to verify that the library has returned content, before acting on it.

## Dependencies
The following libraries are needed by this project
* requests

## Running as a script
There is a `__main__.py` script included for running the library directly. It's intended to demonstrate the library's functions.

|Argument | Description
|-|-
|--help | Prints a help message to the terminal. |
|--num-entries | Specifies the number of images to download. |
|--index | Specifies the offset of the first image in the source image feed.
|--metadata | Enables writing the images metadata to a JSON file.
|--list | Prints the available images date and title to the terminal. (Images are not downloaded)
|--path | Specifies a directory path to save images to. Defaults to the current working directory.
