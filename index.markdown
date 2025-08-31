---
layout: base
title: Home
---

<p>This is a lightweight directory. Last Update: <code>{{ site.time | date: "%B %d, %Y %H:%M %Z" }}</code></p>

<p>Add or edit entries:</p>
<ol>
<li>by using the <a href="https://github.com/CivicTechTO/toronto-community-directory/issues/new?template=add_community.yml
">add acommunity issue form</a></li>
<li>by modifying <code>_data/communities.yml</code> on <a href="https://github.com/CivicTechTO/toronto-community-directory">CivicTechTO/toronto-community-directory</a>.</li>
</ol>

<hr/>

<div class="grid-upgrade">
  {% assign sorted = site.data.communities | sort: "name" %}
  {% for c in sorted %}
    {% include card.html name=c.name url=c.url description=c.description source=c.source %}
  {% endfor %}
</div>

<hr/>
