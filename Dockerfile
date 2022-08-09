FROM jekyll/jekyll:3.8


WORKDIR /srv/jekyll
COPY --chown=jekyll:jekyll . /srv/jekyll

EXPOSE 3000
RUN bundle config set deployment true
RUN bundle install --jobs=4


CMD ["jekyll", "serve", "--drafts", "-H", "0.0.0.0", "-P", "3000", "--incremental" ]
