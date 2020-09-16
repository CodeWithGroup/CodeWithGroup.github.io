# Welcome
This repository holds the code for CodeWith, a group in the UK that offers free coding help and tuition.

# Our Event
We run events online and manage it all through 
[our Slack group](https://www.codewith.org.uk/contact.html).
It's all free, so if you're in the area please come along!

You can see our current events at https://www.codewith.org.uk/events.html

# Contributing to this repository
## Repository branches

Branch | Purpose | Who can commit
------------ | ------------- | ---------------
Master | The **Live** branch, commits here will appear in the live website | Maintainers, only from the release branch
Release | Tested code that is ready for the live website | Maintainers, via pull requests
Feature/* | New code being developed | Contributors 

## Pull requests

Please submit pull requests with useful descriptions, if you don't know how to use pull requests ask in [our Slack group](https://www.codewith.org.uk/contact.html).


## Testing 

Testing is important for maintainers and contributors alike. Ensure all aspects of the site work as the did previously before submitting a pull request. 

Things to look out for when testing

* Responsive design - how does the page display on different devices, and different orientations.
* Browser support - Test your changes in a few major browsers, are there any errors?

Before pull requests are merged maintainers should test all aspects of the site. 

# Getting started with this site and Jekyll

## What is Jekyll?

Jekyll is a static site generator. It takes text written in your favorite markup language and uses layouts to create a static website. You can tweak the site’s look and feel, URLs, the data displayed on the page, and more.

Quoted from https://jekyllrb.com/docs/

## Jekyll setup

If you're familiar with Ruby gems, run the following:

`gem install bundle`

`gem install jekyll`

If this is your first time using Ruby or gems, use [this guide](https://jekyllrb.com/docs/installation/) to setup Jekyll for your operating system.

## Building the site

Open a command line in the root directory of the repository.

If this is the first time you have built the site, make sure you have run `bundle pack` before attempting to build the site using jekyll.

>:Warning: The website uses extensionless links, meaning we don't need to include the '.html' extension on web pages and in anchor (&lt;a&gt;) links. In order that these links work while you view the site locally, open a new command-line window, navigate to the folder containing the website's source code, and run `bundle exec jekyll serve`. Leave that window running while you make your changes. This will start a local server and the address is shown in the command-line.

The site rebuilds after every change, so just refresh the page in your browser to see the changes. 

>:Warning: do not edit anything in the site folder as it will not be comitted and is overwritten everytime you build the site.



## Includes

Jeykll has functionality to include files, which this site makes extensive use of. You can find the documentation for includes here: https://jekyllrb.com/docs/includes/

# Useful guides

## To add yourself to the people page

* Create a branch
* Make a copy of one of the existing bios in *_data/people/*
* Name it using the convention *yourname* 
* Modify to be your bio including
    * Photograph
    * Information paragraph
    * Twitter (optional)
    * Things you can help with

If you need any help, contact one of the pople who have already added themselves.

## Sitemap
All pages not defined as a default in _config.yml are added to the sitemap

To exclude a specific page use the snippet `sitemap: false` at the top of the page

:warning: **If you are including the page in another page (using `include_relative`)**: add the page as a default in `_config.yml` otherwise the `sitemap:false` is displayed as HTML on the page.

### Example default to add to `_config.yml`
```yml
-
  scope:
    path: 'pages-people/*'
  values:
    sitemap: false
```

All files in `_include` are excluded from the sitemap automatically
## Adding a page to the typed suffix functionality

* Add a key to the Jekyll build options at the top of the page

e.g. 

```
suffixes:
    - Databases,
    - Docker,
    - Git,
    - SQL,
    - Kubernetes,
    - Us
```



