FROM jekyll/jekyll:3.8


WORKDIR /srv/jekyll
COPY --chown=jekyll:jekyll . /srv/jekyll

EXPOSE 3000
CMD ["jekyll", "serve", "--drafts", "-H", "0.0.0.0", "-P", "3000" ]
