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
The site's sitemap is generated automatically on deployment 

To avoid a page being indexed, e.g people pages that are included use the below snippet at the top of the page. 

`sitemap: false`
