---
title: >
  Inverse design of organic light-emitting diode structure based on deep neural networks
authors:
  - "[J1] Sanmun Kim"
  - "Jeong Min Shin"
  - "Jaeho Lee"
  - "Chanhyung Park"
  - "Songju Lee"
  - "Juho Park"
  - "Dongjin Seo"
  - "Sehong Park"
  - "Chan Y Park"
  - "Min Seok Jang"

date: "2021-08-01T00:00:00Z"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2017-01-01T00:00:00Z"

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ["article-journal"]

# Publication name and optional abbreviated publication name.
publication: "*Nanophotonics, 10*(18)"
publication_short: ""

abstract: >
  The optical properties of thin-film light emitting diodes (LEDs) are strongly dependent on their structures due to light interference inside the devices. However, the complexity of the design space grows exponentially with the number of design parameters, making it challenging to optimize the optical properties of multilayer LEDs with rigorous electromagnetic simulations. In this work, we demonstrate an artificial neural network that can predict the light extraction efficiency of an organic LED structure in 30 ms, which is ∼103 times faster than the rigorous simulation in a single-treaded execution with root-mean-squared error of 1.86 × 10−3. The effective inference time per structure is brought down to ∼0.6 μs with unaltered error rate with parallelization. We also show that our neural networks can efficiently solve the inverse problem – finding a device design that exhibits the desired light extraction spectrum – within the similar time scale. We investigate the one-to-many mapping issue of the inverse problem and find that the degeneracy can be lifted by incorporating additional emission spectra at different observing angles. Furthermore, the forward neural network is combined with a conventional genetic algorithm to address additional large-scale optimization problems including maximization of light extraction efficiency and minimization of angle dependent color shift. Our approach establishes a platform for tackling computation-heavy optimization tasks with one-time computational cost.

tags:
  - Source Themes
featured: false

# Links
url_paper: 'https://pubs.acs.org/doi/full/10.1021/acsphotonics.1c00839'
url_code: 'https://github.com/dongjin-seo2020/1DFreeFormDQN'
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''

# Featured image
image:
  caption: 'Image credit: [**Unsplash**](https://unsplash.com/photos/jdD8gXaTZsc)'
  focal_point: ""
  preview_only: false

# Associated Projects (optional).
projects: []

# Slides (optional).
slides: example
---
