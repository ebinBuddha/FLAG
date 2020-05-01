# Flag list, advanced generator (FLAG)

## Introduction

Welcome to FLAG, a simple Python utility that generates fillable /extraflags/ list templates.

What is /extraflags/? Omfg, check out the [Extra Flags for 4chan](https://gitlab.com/flagtism/Extra-Flags-for-4chan "Extra Flags for 4chan") project and repository.

![extraflags](/misc/extraflags.png)

If you run into any issues, please make a post on /flag/.

## Requirements

- Python 3+
- Pillow (https://pillow.readthedocs.io/)
- pyuca (https://github.com/jtauber/pyuca)
- A local copy of the previously-mentioned /extraflags/ project repo

## How to install

Download this repository to a safe location (clone or download the zip archive as you prefer)

## How to run

1. Open your terminal in the folder where you downloaded this repository
2. Type `pyhton3 flag.py` or `pyhton flag.py` depending on your installation
3. Follow the prompts

## See this, what do

![Screenshot](/misc/flag_prompt.png "Screenshot of the utility")

To get to run you'll be asked a some things:

1. ***Path to flags/ folder***: this is the path (relative or absolute) to the folder containing the /extraflags/. E.g. if you saved your local copy in `C:\extraflags\`, this path should contain a folder called `flags` where all the nations' folders are in turn contained. Write therefore `C:\extraflags\flags` or the equivalent relative path in the prompt.

```
C:\extraflags\
    |- flags    <------ you need to write the path to here
        |- Afghanistan
        |- Albania
        ...
```

2. ***Relative path to root folder to parse***: this is the path, relative to the one given in the previous point, from which FLAG should start its job. E.g. Do you want to get the U.S. States? Write `United States`. If you want to parse all the nations just write `.` or press `Enter` without writing anything (parsing all the nations may take a while).

3. ***Maximum folder recursion depth from given root***: this value sets the maximum depth FLAG will traverse the folder, depth zero is the depth of the folder given at point *2*. The higher the value, the bigger the list, the longer it takes. E.g., given the input of the previous points, by setting this value to *1*, FLAG will parse down to County level.

4. ***Initial folder recursion depth from given root***: this value sets the starting depth for folder traversing. Given the input of the previous points, by setting this value to *0*, FLAG will output both States and Counties. By setting *1*, FLAG will output all the Counties from each State.

5. ***Insert output file name***: this should be clear enough. Give the output file name. The only valid extension is `.png`, so if you omit that FLAG will add it for you.

6. ***Generate also TAMPA file? y/n***: type `y` if you want to generate also a `listofcoordinates.txt` file for TAMPA to read. See the [TAMPA](#tampa "TAMPA") section for more info.

## Limits

FLAG is currently limited to a canvas of 12k x 3.5k pixels.

## TAMPA

The utility can produce a 'listofcoordinates.txt' file which is TAMPA compatibile, allowing TAMPA to autofill /extraflags/ lists too!

Dk what TAMPA is? Holy fuck you must have been living under a rock!
https://gitlab.com/Tampanon/TAMPA
