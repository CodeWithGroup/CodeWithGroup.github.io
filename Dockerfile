FROM ruby:2.7.1
RUN mkdir /app
WORKDIR /app
COPY Gemfile /app/Gemfile
COPY Gemfile.lock /app/Gemfile.lock

RUN bundle config set deployment true
RUN bundle install --jobs=4

COPY . /app

EXPOSE 3000

ENTRYPOINT [ "bundle" ]

CMD [ "exec", "jekyll", "serve", "--drafts", "-H", "0.0.0.0", "-P", "3000" ]
