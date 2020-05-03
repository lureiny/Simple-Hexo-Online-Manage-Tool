FROM amd64/alpine:3.11
RUN mkdir /root/.ssh && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache nodejs git python3 py3-apipkg openssh npm && \
    pip3 install -i "https://pypi.tuna.tsinghua.edu.cn/simple" flask && \
    npm config set registry https://registry.npm.taobao.org && \
    npm install -g hexo-cli && \
    npm install hexo-server --save 
WORKDIR /home
CMD ["/bin/sh"]
