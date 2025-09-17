---
layout: none
title: Kata_web Releases
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{{ page.title }}</title>

  <!-- Bootstrap CSS CDN -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />

  <style>
    body {
      padding-top: 4.5rem;
      background-color: #f8f9fa;
    }
    header, footer {
      background-color: #343a40;
      color: white;
      padding: 1rem 0;
    }
    footer {
      font-size: 0.9rem;
    }
    .release-card {
      margin-bottom: 1.5rem;
    }
    .release-date {
      color: #6c757d;
      font-size: 0.9rem;
    }
  </style>
</head>
<body>

<header class="fixed-top">
  <div class="container d-flex justify-content-between align-items-center">
    <h1 class="h3 mb-0">Kata_web</h1>
    <nav>
      <small>by changcheng967</small>
    </nav>
  </div>
</header>

<main class="container mt-4">

  <h2 class="mb-4">Releases</h2>

  {% assign sorted = site.data.releases | sort: 'published_at' | reverse %}
  {% for release in sorted %}
  <div class="card release-card shadow-sm">
    <div class="card-body">
      <h3 class="card-title">{{ release.tag_name }}</h3>
      <p class="release-date">{{ release.published_at | date: "%B %d, %Y" }}</p>

      {% if release.body %}
      <div class="card-text mb-3">{{ release.body | markdownify }}</div>
      {% endif %}

      {% if release.assets and release.assets.size > 0 %}
      <h5>Assets:</h5>
      <ul class="list-unstyled">
        {% for asset in release.assets %}
        <li><a href="{{ asset.browser_download_url }}" class="link-primary" target="_blank" rel="noopener">{{ asset.name }}</a></li>
        {% endfor %}
      </ul>
      {% endif %}
    </div>
  </div>
  {% endfor %}

</main>

<footer class="text-center mt-5">
  <div class="container">
    <p>Sponsored by <a href="https://douletmedia.com" class="text-white text-decoration-underline" target="_blank" rel="noopener">Doulet Media</a></p>
  </div>
</footer>

<!-- Bootstrap JS Bundle CDN -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>

