---
layout: default
title: Releases
---

# {{ site.title }}

{% assign sorted = site.data.releases | sort: 'published_at' | reverse %}
{% for release in sorted %}

## {{ release.tag_name }} — {{ release.published_at | date: "%Y-%m-%d" }}

**Overview**  
{{ release.body | markdownify }}

{% if release.assets and release.assets.size > 0 %}
**Assets:**  
{% for asset in release.assets %}
- [{{ asset.name }}]({{ asset.browser_download_url }})
{% endfor %}
{% endif %}

---

{% endfor %}
