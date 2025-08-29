---
layout: base
title: Home
---

<p>This is a lightweight directory.</p>

<p>Add or edit entries in <code>_data/communities.yml</code> on <a href="https://github.com/CivicTechTO/toronto-community-directory">github.com/CivicTechTO/toronto-community-directory</a>.</p>

<p>Last Update: <code>{{ site.time | date: "%B %d, %Y %H:%M %Z" }}</code></p>

<hr/>

<div class="grid grid-upgrade">
  {% assign sorted = site.data.communities | sort: "name" %}
  {% for c in sorted %}
    {% include card.html name=c.name url=c.url description=c.description source=c.source %}
  {% endfor %}
</div>

<hr/>
