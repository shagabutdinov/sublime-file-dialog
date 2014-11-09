# Sublime FileDialog plugin

Replacement for default "save as...", "open" sublime functionality. Also
provides "rename file..." feature.


### Reason

I don't like OS's default "save as..." and "open" dialog because there is no way
to navigate through files and directories in fuzzy way and there is no way to
put default file name into the "save as..." file name field even if I can detect
it pretty precisely (for most mvc framework filename will be name of class in
file text). So it is attempt to replace this default dialogs and I found it
quite usable after a bit training.

### Demo

![Demo](https://github.com/shagabutdinov/sublime-enhanced-demos/raw/master/file_dialog.gif "Demo")


### WARNING

This plugin replaces default sublime "save as...", "open" functionality in
unobvious way. When saving new file you should enter then name of file into the
dialog and hit "tab" (not "enter") to save file. "Enter" will open directory or
file.

By default it tries to detect your file name and put this file name into the
file name field. It will hide other files or directories that not match this
file name so if you want to save file under different directory you should
delete (or cut) file name and navigate to directory you need. Current directory
is listed in status bar.


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Usage

To open file: hit keyboard shortcut than select file you need and hit enter. You
can use fuzzy search to quickly find file or directory you need.

To save file: hit keyboard shortcut than navigate to directory you need than
than enter file name and hit "tab".

To rename file: hit keyboard shortcut than navigate to directory you need than
than enter new file name and hit "tab".

There is keyboard shortcuts to go up and down in directory stack. Please refer
sublime-file-folder plugin to find out keyboard shortcuts.

FileDialog works over [sublime-folder-files](http://github.com/shagabutdinov/sublime-folder-files)
so its shortcuts will work here.

### Commands

| Title                          | Keyboard shortcut | Command palette        |
|--------------------------------|-------------------|------------------------|
| Save                           | ctrl+s            | FileDialog: Save       |
| Save as                        | ctrl+shift+s      | FileDialog: Save as... |
| Open                           | ctrl+u, ctrl+o    | FileDialog: Open       |
| Rename                         | ctrl+u, ctrl+r    | FileDialog: Rename     |
| Complete operation             | tab               |                        |


### Dependencies

* [QuickSearchEnhanced](https://github.com/shagabutdinov/sublime-quick-search-enhanced)
* [FolderFiles](https://github.com/shagabutdinov/sublime-folder-files)