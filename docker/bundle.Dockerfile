FROM ruby:2.7.1
RUN mkdir /app
COPY . /app/

WORKDIR /app

RUN gem install bundler:2.3.17
RUN bundle install

ENTRYPOINT [ "bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--force_polling"]
EXPOSE 4000