#!/bin/sh

git config --global user.name $GIT_CONFIG_NAME && git config --global user.email $GIT_CONFIG_EMAIL && cd $HEXO_BLOG
if [ "`ls -A $HEXO_BLOG`" = "" ]; then
    hexo init $HEXO_BLOG && cd $HEXO_BLOG && hexo g &&  hexo server -s >> /dev/null & cd $SHOMT && python3 hexo.py
else
    cd $HEXO_BLOG && hexo server -s >> /dev/null & cd $SHOMT && python3 hexo.py
fi