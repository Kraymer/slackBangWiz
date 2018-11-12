---
layout: default
title: Getting started
nav_order: 1
permalink: /
---

# slack plugin for [python-rtmbot](https://github.com/slackapi/python-rtmbot) adding !bang wizardry (_à la_ [DuckDuckGo](ttps://duckduckgo.com/bang))
{: .fs-6 .fw-300 }

> Ca fait vlam! Ca fait SLACK!  
> Des clip! Crap! Des BANG! Des vlop! Et des zip!   
> Shebam! Pow! Blop! WIZ!  

-- *Slightly edited* lyrics of [Comic Strip - Serge Gainsbourg ft Brigitte Bardot](https://www.youtube.com/watch?v=22Uf4-khGAk) 

<br>

[Get started now](#getting-started){: .btn .btn-purple .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/Kraymer/slackBangWiz){: .btn .fs-5 }


---

## Getting started

### Install 

1. Install python-rtmbot using instructions at [https://github.com/slackapi/python-rtmbot#installation](https://github.com/slackapi/python-rtmbot#installation)
2. `cd python-rtmbot/plugins ; git clone https://github.com/Kraymer/slackBangWiz.git`
3. declare the plugin : 

   ~~~~
   $ more rtmbot.conf
   [...]
   ACTIVE_PLUGINS:
    - plugins.bangwiz.BangPlugin
   ~~~~
 
4. enter slack users tokens in `bang/auth.py`.  
 These legacy tokens are available at 
 [https://api.slack.com/custom-integrations/legacy-tokens](https://api.slack.com/custom-integrations/legacy-tokens)

### Bot app permissions

Following permissions are needed :

- Confirm user’s identity
- Access user’s public channels
- Access the workspace’s emoji
- Send messages as user
- Send messages as slack-cli

And additional permissions for these bang commands :

- _`!r`andom user_ : Access information about user’s public channels 


