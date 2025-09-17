---
layout: none
title: Kata_web Releases
---

<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{{ page.title }}</title>

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono&family=Poppins:wght@400;600&display=swap" rel="stylesheet" />

  <!-- Bootstrap 5 CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />

  <!-- AOS Animation CSS -->
  <link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet" />

  <style>
    /* Root and fonts */
    :root {
      --color-primary: #007bff;
      --color-bg-light: #f5f8fa;
      --color-bg-dark: #121212;
      --color-text-light: #212529;
      --color-text-dark: #e4e6eb;
    }

    body {
      font-family: 'Poppins', sans-serif;
      background-color: var(--color-bg-light);
      color: var(--color-text-light);
      transition: background-color 0.3s ease, color 0.3s ease;
      padding-top: 70px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Dark mode styles */
    body.dark-mode {
      background-color: var(--color-bg-dark);
      color: var(--color-text-dark);
    }

    header {
      background: rgba(255 255 255 / 0.8);
      backdrop-filter: saturate(180%) blur(10px);
      position: fixed;
      top: 0; left: 0; right: 0;
      height: 70px;
      display: flex;
      align-items: center;
      box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
      z-index: 1000;
      padding: 0 1.5rem;
      transition: background 0.3s ease;
    }

    body.dark-mode header {
      background: rgba(18 18 18 / 0.9);
      box-shadow: 0 2px 12px rgb(0 0 0 / 0.6);
    }

    header h1 {
      font-family: 'Poppins', sans-serif;
      font-weight: 600;
      font-size: 1.5rem;
      margin: 0;
      color: var(--color-primary);
      user-select: none;
    }

    header nav {
      margin-left: auto;
      font-size: 1rem;
      color: #666;
      font-weight: 500;
      user-select: none;
    }

    body.dark-mode header nav {
      color: #ccc;
    }

    main.container {
      flex-grow: 1;
      max-width: 900px;
      margin: 0 auto 3rem auto;
      padding: 1rem 1rem 3rem 1rem;
    }

    main h2 {
      font-weight: 600;
      font-size: 2rem;
      margin-bottom: 2rem;
      text-align: center;
      letter-spacing: 1.2px;
    }

    /* Release Cards */
    .release-card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 8px 20px rgb(0 0 0 / 0.08);
      margin-bottom: 2rem;
      padding: 1.5rem 2rem;
      transition: box-shadow 0.3s ease, transform 0.3s ease;
      cursor: default;
      user-select: text;
    }

    body.dark-mode .release-card {
      background: #1e1e1e;
      box-shadow: 0 8px 20px rgb(0 0 0 / 0.6);
      color: var(--color-text-dark);
    }

    .release-card:hover {
      box-shadow: 0 15px 40px rgb(0 123 255 / 0.4);
      transform: translateY(-6px);
    }

    .release-card h3 {
      font-family: 'Poppins', sans-serif;
      font-weight: 700;
      font-size: 1.75rem;
      margin-bottom: 0.25rem;
      color: var(--color-primary);
    }

    .release-date {
      font-size: 0.9rem;
      color: #999;
      margin-bottom: 1rem;
      font-family: 'JetBrains Mono', monospace;
    }

    body.dark-mode .release-date {
      color: #aaa;
    }

    /* Release body with monospace code style */
    .release-body {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1rem;
      line-height: 1.6;
      margin-bottom: 1rem;
      white-space: pre-wrap;
    }

    /* Assets list */
    .assets-list {
      list-style: none;
      padding-left: 0;
    }

    .assets-list li {
      margin-bottom: 0.5rem;
    }

    .assets-list a {
      color: var(--color-primary);
      font-weight: 600;
      text-decoration: none;
      transition: color 0.2s ease;
    }

    .assets-list a:hover,
    .assets-list a:focus {
      color: #0056b3;
      text-decoration: underline;
    }

    /* Footer */
    footer {
      background-color: var(--color-primary);
      color: white;
      padding: 1rem 0;
      text-align: center;
      font-weight: 500;
      user-select: none;
      margin-top: auto;
    }

    footer a {
      color: white;
      font-weight: 700;
      text-decoration: underline;
    }

    footer a:hover,
    footer a:focus {
      color: #cce5ff;
    }

    /* Dark mode toggle button */
    #darkModeToggle {
      background: none;
      border: 2px solid var(--color-primary);
      color: var(--color-primary);
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s ease;
      user-select: none;
    }

    #darkModeToggle:hover,
    #darkModeToggle:focus {
      background-color: var(--color-primary);
      color: white;
      outline: none;
    }
  </style>
</head>
<body>

<header>
  <h1>Kata_web</h1>
  <nav>
    by changcheng967 &nbsp;|&nbsp;
    <button id="darkModeToggle" aria-label="Toggle dark mode">🌙 Dark Mode</button>
  </nav>
</header>

<main class="container" data-aos="fade-up">
  <h2>Latest Releases</h2>

  {% assign sorted = site.data.releases | sort: 'published_at' | reverse %}
  {% for release in sorted %}
  <article class="release-card" data-aos="fade-up" data-aos-delay="{{ forloop.index0 | times: 100 }}">
    <h3>{{ release.tag_name }}</h3>
    <p class="release-date">{{ release.published_at | date: "%B %d, %Y" }}</p>

    {% if release.body %}
    <div class="release-body">{{ release.body | markdownify }}</div>
    {% endif %}

    {% if release.assets and release.assets.size > 0 %}
    <h5>Assets:</h5>
    <ul class="assets-list">
      {% for asset in release.assets %}
      <li>
        <a href="{{ asset.browser_download_url }}" target="_blank" rel="noopener">{{ asset.name }}</a>
      </li>
      {% endfor %}
    </ul>
    {% endif %}
  </article>
  {% endfor %}
</main>

<footer>
  Sponsored by <a href="https://douletmedia.com" target="_blank" rel="noopener">Doulet Media</a>
</footer>

<!-- Bootstrap JS Bundle -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- AOS Animation JS -->
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
<script>
  AOS.init({
    duration: 800,
    once: true,
    easing: 'ease-in-out'
  });

  // Dark mode toggle
  const toggleBtn = document.getElementById('darkModeToggle');
  toggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    if(document.body.classList.contains('dark-mode')){
      toggleBtn.textContent = '☀️ Light Mode';
    } else {
      toggleBtn.textContent = '🌙 Dark Mode';
    }
  });
</script>

</body>
</html>
