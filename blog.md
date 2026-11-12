---
layout: homepage
title: Blog
permalink: /blog/
---

<h2 style="margin: 2px 0px -15px;"><u>Blog</u></h2>

<br>

Notes and informal essays. Mostly about AI for physicists, scientific machine learning, and things I'm trying to understand more deeply by writing them down.

<div class="pub-filter" id="blog-filter">
  <button class="active" data-cat="all">All</button>
  {% assign live = site.posts | where_exp: "p", "p.placeholder != true" | map: "label" | uniq %}
  {% assign soon = site.posts | where: "placeholder", true | map: "label" | uniq %}
  {% assign cats = live | concat: soon | uniq %}
  {% for c in cats %}{% if c %}<button data-cat="{{ c | slugify }}">{{ c }}</button>{% endif %}{% endfor %}
</div>

<ul class="blog-list">
{% assign real_posts = site.posts | where_exp: "p", "p.placeholder != true" %}
{% assign upcoming = site.posts | where: "placeholder", true %}
{% for post in real_posts %}
  <li class="blog-item" data-cat="{{ post.label | slugify }}">
    <div class="blog-item-meta">
      <span class="post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
      {% if post.label %}<span class="cat-badge cat-{{ post.label | slugify }}">{{ post.label }}</span>{% endif %}
    </div>
    <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    {% if post.description %}<div class="post-desc">{{ post.description }}</div>{% endif %}
  </li>
{% endfor %}
{% for post in upcoming %}
  <li class="blog-item upcoming" data-cat="{{ post.label | slugify }}">
    <div class="blog-item-meta">
      <span class="post-date">Coming soon</span>
      {% if post.label %}<span class="cat-badge cat-{{ post.label | slugify }}">{{ post.label }}</span>{% endif %}
    </div>
    {% if post.description %}<div class="post-desc">{{ post.description }}</div>{% endif %}
  </li>
{% endfor %}
</ul>

<script>
(function () {
  var buttons = document.querySelectorAll('#blog-filter button');
  var items = document.querySelectorAll('.blog-list .blog-item');
  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      buttons.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var cat = btn.getAttribute('data-cat');
      items.forEach(function (it) {
        var show = (cat === 'all') || (it.getAttribute('data-cat') === cat);
        it.style.display = show ? '' : 'none';
      });
    });
  });
})();
</script>
