---
layout: homepage
title: Blog
permalink: /blog/
---

<h2 style="margin: 2px 0px -15px;"><u>Blog</u></h2>

<br>

Notes and informal essays. Mostly about AI for physicists, scientific machine learning, and things I'm trying to understand more deeply by writing them down.

<ul class="blog-list">
{% for post in site.posts %}
  <li>
    <span class="post-date">{{ post.date | date: "%b %d, %Y" }}</span>
    <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    {% if post.description %}<div style="font-size:0.9rem;color:#666;margin-top:4px;">{{ post.description }}</div>{% endif %}
  </li>
{% endfor %}
</ul>
