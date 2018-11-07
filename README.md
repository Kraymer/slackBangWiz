# slackBangWiz
python-rtmbot plugin adding `!bang` shortcuts<sup id="a1">[1](#f1)</sup> wizardry to slack

> Ca fait vlam! Ca fait SLACK!  
> Des clip! Crap! Des BANG! Des vlop! Et des zip!   
> Shebam! Pow! Blop! WIZ!  

-- *Slightly edited* lyrics of [Comic Strip - Serge Gainsbourg ft Brigitte Bardot](https://www.youtube.com/watch?v=22Uf4-khGAk) 

# Glossary

_bang:_ shortcut starting by `!` to execute arbitrary action to a slack channel/message

_memoji:_ custom emoji refering to a meme, eg `:feels_good_man:`, `:fry_not_sure:`, etc 

# Usage

- **B**omb   
  `!b <text>`: destruct the message after 10 seconds elapsed

  <img src=https://raw.githubusercontent.com/Kraymer/bulkdata/master/emobomb.gif width=600>

- **D**efine  
  `!kym <MEMOJI>`: show *MEMOJI* description 

  <img src=https://i.imgur.com/Qs0BY1L.png width=600>
  
- **K**aomoji  
  `!k <EMOJI>`: replace *EMOJI* by its kawai version

  <img src=https://thumbs.gfycat.com/CavernousLikableFrigatebird-size_restricted.gif width=600>

- **M**eme    
  `!m <MEMENAME> <TOP TEXT> <BOTTOM TEXT>`: generate meme image

  <img src=https://raw.githubusercontent.com/Kraymer/bulkdata/master/ezgif-5-3974dd57a36e.gif width=600>

- **P**oll
  `!p <QUESTION> <EMOJIS>`: post an emopoll 

# Install

1. Install python-rtmbot using instructions at https://github.com/slackapi/python-rtmbot#installation
2. `cd python-rtmbot/plugins ; git clone https://github.com/Kraymer/slackBangWiz.git`
3. declare the plugin : 

   ~~~~
   $ more rtmbot.conf
   [...]
   ACTIVE_PLUGINS:
    - plugins.bangwiz.BangPlugin
   ~~~~
 
 4. enter slack users tokens in `bang/auth.py`
 
 
 ---
<i id="f1">1</i> *à la* DuckDuckGo, see https://duckduckgo.com/bang [⤸](#a1) 
