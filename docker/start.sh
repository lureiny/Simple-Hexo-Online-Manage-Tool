#!/bin/sh

git config --global user.name $GIT_CONFING_NAME && git config --global user.email $GIT_CONFING_EMAIL && cd $HEXO_BLOG && hexo server -s >> /dev/null & cd $SHOMT && python3 hexo.py
