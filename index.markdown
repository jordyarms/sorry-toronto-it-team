---
layout: base
title: Home
---

<details name="about">
  <summary>About</summary>
  <p>This is a lightweight directory of Toronto's various communities. It is intended to facilitate the discovery of communities in Toronto and as serve as an example of community centred data.</p> 
  <p>Currently in early development, the data structure and directory content will be evolving as requirements and insights emerge.</p> 
  <p>This initiative is an open collaboration. You are welcome to contribute. To get involved or learn more please come to Civic Tech Toronto's hacknights on Tuesday evenings, or 1RG's monthly Civic Sundays.</p>
  <p>For ease of access you can get the directory in <code>JSON</code> or <code>CSV</code> formats from the following:</p>
  <ul>
  <li><a href="{{"/all.csv" | relative_url }}">all.csv</a></li>
  <li><a href="{{"/all.json" | relative_url }}">all.json</a></li>
  </ul>
  <p>Last Update: <code>{{ site.time | date: "%B %d, %Y %H:%M %Z" }}</code></p>
  <p>Count of listings: <code>{{ site.communities | size }}</code></p>
</details>
<hr/>
<details name="additions">
  <summary>Make an addition</summary>

<p>Add or edit entries:</p>
<ol>
<li>by using the <a href="https://github.com/CivicTechTO/toronto-community-directory/issues/new?template=add_community.yml
">add a community</a> issue form template on github.</li>
<li>by including a record in <code>_communities</code> on <a href="https://github.com/CivicTechTO/toronto-community-directory">CivicTechTO/toronto-community-directory</a>.</li>
</ol>
</details>
<hr/>

{% assign all_tags = site.communities | map: "tags" | compact | join: "," | split: "," | uniq | sort %}

{% assign namespaces = '' | split: '' %}
{% for tag in all_tags %}
{% assign trimmed_tag = tag | strip %}
{% if trimmed_tag contains '/' %}
{% assign namespace = trimmed_tag | split: '/' | first %}
{% unless namespaces contains namespace %}
{% assign namespaces = namespaces | push: namespace %}
{% endunless %}
{% endif %}
{% endfor %}
{% assign namespaces = namespaces | sort %}

<details name="filters">
  <summary>Filter Controls</summary>
  <div id="filter-bar">
    <div>
      <button class="filter-btn active" data-filter="all">Show All</button>
      <button id="filter-mode-toggle" class="filter-toggle" role="button">Mode: ANY (OR)</button>
    </div>
    
    {% for namespace in namespaces %}
      <fieldset>
        <legend>{{ namespace | replace: '-', ' ' | capitalize }}</legend>
        {% for tag in all_tags %}
          {% assign trimmed_tag = tag | strip %}
          {% assign tag_namespace = trimmed_tag | split: '/' | first %}
          {% if tag_namespace == namespace %}
            {% assign tag_value = trimmed_tag | split: '/' | last %}
            <button class="filter-btn" data-filter="{{ trimmed_tag }}">{{ tag_value | replace: '-', ' ' }}</button>
          {% endif %}
        {% endfor %}
      </fieldset>
    {% endfor %}

    {% assign unnamespaced_tags = '' | split: '' %}
    {% for tag in all_tags %}
      {% assign trimmed_tag = tag | strip %}
      {% unless trimmed_tag contains '/' %}
        {% assign unnamespaced_tags = unnamespaced_tags | push: trimmed_tag %}
      {% endunless %}
    {% endfor %}

    {% if unnamespaced_tags.size > 0 %}
      <fieldset>
        <legend>Other</legend>
        {% for tag in unnamespaced_tags %}
          <button class="filter-btn" data-filter="{{ tag }}">{{ tag | replace: '-', ' ' }}</button>
        {% endfor %}
      </fieldset>
    {% endif %}

  </div>
</details>

<div class="grid-upgrade">
  {% assign sorted = site.communities | sort: "name" %}
  {% for c in sorted %}
    {% include card.html name=c.name url=c.link description=c.description source=c.source tags=c.tags %}
  {% endfor %}
</div>

<hr/>
