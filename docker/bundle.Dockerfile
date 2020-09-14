FROM ruby:2.7.1
RUN mkdir /app
WORKDIR /app
COPY Gemfile /app/Gemfile

ENTRYPOINT [ "bundle" ]
