# Welcome
This repository holds the code for CodeWith, a group in the UK that offers free coding help and tuition.

# Our Event
We run the event monthly and manage it all through 
[our Slack group](https://www.slack.com/).
It's all free, so if you're in the area please come along!

# To add yourself to the people page

* Create a branch
* Make a copy of one of the existing bios in *pages-people* 
* Name it using the convention people-*yourname* 
* Modify to be your bio including
    * Photograph
    * Information paragraph
    * Twitter (optional)
    * Things you can help with

If you need any help, contact one of the pople who have already added themselves.

Copy the includes code `<br />
{% include_relative pages-people/people-yourname.html %}` to the bottom of people.html (ensure you update the file name)

# Sitemap
All pages not defined as a default in _config.yml are added to the sitemap

To exclude a specific page use the snippet `sitemap:false` at the top of the page

> :warning: **If you are including the page in another page (using `include_relative`)**: add the page as a default in `_config.yml` otherwise the `sitemap:false` is displayed as HTML on the page.

## Example default to add to `_config.yml`
```yml
-
  scope:
    path: 'pages-people/*'
  values:
    sitemap: false
```

All files in `_include` are excluded from the sitemap automatically
# Adding a page to the typed suffix functionality
* Add a variable to the suffix-lists.js file with the first word of the page title. Assign the array you want to use to the variable. 

e.g. 

For a page named "Home"

```javascript
var Languages = ["Java","HTML"]
var Home = Languages
```