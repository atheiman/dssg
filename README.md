# dssg - Django Static Site Generator

Here we go. Second attempt at the static site generator.



## Quick Reference:

### Post Metadata Attributes

Metadata stored at the top of each Post markdown source file. Defaults are generated from the filename. Here are all the possible values for an example post markdown source file named `Python JSON Basics.md`:

```
author: Austin Heiman
date: Jan 24 2015
title: Python JSON Basics
tags: python, json, javascript
preview: An introduction to the json builtin Python module.
published: True
```

Defaults are set for most of these. I will document them eventually. The post body should be entered below this metadata. Here is more information about [Python Markdown's Meta-Data extension](https://pythonhosted.org/Markdown/extensions/meta_data.html).

The above values are all `Post` attributes as well. Here are the additional `Post` attributes and callables:

```
html
url
```

### Category Config Keys

JSON keys stored in each category's `category-config.json`:

```
verbose_name
description
posts_dir
post_template
index_template
```



## Basic dssg App Flow / Ideas / Features / Info

The idea of this app is that it will read in templates and blog post markdown source files, and output a static site in the `output/` directory which could be easily uploaded to any static hosting service. I'd recommend [GitHub pages](https://pages.github.com/), but that's just me.

Here is a quick summary of how to get your static site going:



### Pages

Create one-off pages in the `pages/` directory. Templates there are run through the template engine with the context and dropped into the top level of the output. You will probably at least want an `index.html` file in `pages/`, so your static site will have an index located at `output/index.html`.

Pages are rendered with the context variables `categories` and `posts`.



### Categories and Posts

A `categories/` directory contains category dirs. Each category directory should have the following files and directories:

- `category-config.json` JSON configuration file, with the keys described in the quick reference above.

- `posts/` directory containing post markdown source files. The markdown source files should include metadata at the top as described in the quick reference above.

- `post.html` template that is run through the template engine for each post with the context variables `post` and `category` and can extend / include any templates in the `TEMPLATE_DIRS`.

- Other templates for rendering category pages. Similar to the `pages/` directory, you might want an `index.html`. These templates are rendered with the context variables `category` and `posts`, and can extend / include any templates in the `TEMPLATE_DIRS`.

> **Note**<br>
> Posts *must* be categorized. If you don't like this, you could make an `uncategorized` Category.

The `output/` directory will contain directories for each category. Each of these category dirs will have your processed `index.html` and a post html file for each of the posts in the `posts/` directory.

The category directory name comes from the `category-config.json` `slug` key. The post html file names come from the post markdown metadata `slug` attribute + ".html". So if a post markdown source file with the slug `python-json-basics` exists in the category directory with the `category-config.json` `slug` value `code`, the output post html file will be `output/code/python-json-basics.html`.



### Template Inheritance

`TEMPLATES_DIR` should contain `includes/` and `pages/` `TEMPLATE_DIRS` should be set to `(CATEGORIES_DIR, TEMPLATES_DIR)`. All templates in the `pages/` directory are rendered and dropped in the `output/` directory.

Create templates that are for including or extending in the `includes/` directory, so that they are not put into the `output/` directory. Include them in a namespaced fashion. For example, place `base.html` in `includes/` and extend it in `pages/index.html` with `{% extends 'includes/base.html' %}`.

A global post template could exist in `includes/` also, and be extended in each categories `post.html` with the same strategy.



### Static Files

Create your static files in the `static/` directory. This directory is simply copied to `output/static`.
