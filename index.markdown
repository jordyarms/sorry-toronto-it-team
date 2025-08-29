---
layout: base
title: Home
---

<p>This is a lightweight directory. Add or edit entries in <code>_data/communities.yml</code>.</p>

<div class="grid grid-upgrade">
  {% assign sorted = site.data.communities | sort: "name" %}
  {% for c in sorted %}
    {% include card.html name=c.name url=c.url description=c.description %}
  {% endfor %}
</div>
