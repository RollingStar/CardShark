# CardShark

An incomplete suite of tools meant to interface with previous decoders and encoders for the GBA e-Reader. This project is completely unaffiliated with anyone else.

# Requirements

* Python 3
* [Dotcode dev package](https://www.caitsith2.com/ereader/devtools.htm)
* Windows for the trivial **bat** files

# Workflow

Imagine 4 folders:

1. raw
2. bin
3. vpk
4. dec

Summary: Go 1 through 4 to decode. Make your changes. Go from 4 through 1 to encode.

e-Reader dotcodes begin life as **raw** files. They are about 3 KB. Each raw file has some redundancy, and can be decoded to a **bin** (binary) file. Each binary is made up of what I am calling a **header** and 1 or more data **chunk**s. Each **chunk** begins with bytes `76 70 6B 30` (vpk0), which has given them the name **vpk**. The **chunks** can be split into individual **vpk** files through normal, general-purpose file splitting tools. Finally, the **vpk**s can be decompressed into plaintext / plain binaries that are interpreted by GBA and GC games. I call the decompressed / decoded files **dec**s.

The workflow I had involves automatically converting from **raw** files into **dec**. The user manually makes edits to the decoded **dec**s. Then they command the tools to package them back into either a **raw** or a **bin** file. (Some tools prefer **bin**.) The text `-hax` is added to the end of the filename when packaging, to avoid overwriting existing input files with hacked versions.

# Unfinished

As fun as this project is/was at its best, debugging it and reverse-engineering e-Cards has been tiring. I don't know if I'll ever pick up this project again, so at the time being, everything here is provided as-is. Looking through the code, converting `bin_to_vpk.py` should function fine, but the inverse conversion `vpk_to_bin` has caused me some serious trouble.

On top of that, this was created to hack the e-Cards used for Animal Crossing, and documenting the format has been doubly tiring due to having a slower / less-automated workflow for testing the e-Cards in Dolphin + VisualBoyAdvance-M-WX-2.0.0-beta2.