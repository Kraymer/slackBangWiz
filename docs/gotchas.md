---
layout: default
title: Gotchas
nav_order: 2
---

# Glossary

_bang:_ shortcut starting by `!` to execute arbitrary action to a slack channel/message

_memoji:_ custom emoji refering to a meme, eg `:feels_good_man:`, `:fry_not_sure:`, etc 

# Configuration files

All the configuration files that you may have to edit are located in `slackBangWiz/bang/rsrc/`.
Amongst them, `auth.py` is the more important as it contains oauth tokens that allows the app to 
post to your workspace.
Others files are named after the different commands and contain resources accessed by these 
commands. You can edit these files to declare data specific to your workspace, like [custom emojis for
_`!k`aomoji_ command](https://github.com/Kraymer/slackBangWiz/blob/master/bang/rsrc/kaomoji.py).

# Private vs public

Some commands generate answers, by default they post it as private message to the command author.  
Use uppercase command (eg `!R`) to post answer publicly on the same channel than the original command.  
