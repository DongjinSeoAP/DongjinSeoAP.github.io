---
# Leave the homepage title empty to use the site title
title: ""
date: 2022-10-24
type: landing

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ""
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Download CV
        url: uploads/resume.pdf
    design:
      css_class: dark
      background:
        color: black
        image:
          filename: stacked-peaks.svg
          filters:
            brightness: 1.0
          size: cover
          position: center
          parallax: false

  - block: collection
    content:
      title: Journal Publication
      text: ""
      filters:
        folders:
          - journal publication
        exclude_featured: false
    design:
      view: citation


  - block: collection
    content:
      title: Conference Publication
      text: ""
      filters:
        folders:
          - journal publication
        exclude_featured: false
    design:
      view: citation


  - block: collection
    id: news
    content:
      title: Recent News
      text: ""
      page_type: post
      count: 5
      filters:
        exclude_featured: false
        exclude_future: false
        exclude_past: false
      order: desc
    design:
      view: date-title-summary
      spacing:
        padding: [0, 0, 0, 0]
---
