name: Bug Report
description: Report a bug or issue
title: "[BUG] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug! Please fill in the details below.
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear description of the issue
      placeholder: Describe the bug...
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How to reproduce the issue
      placeholder: |
        1. Step one
        2. Step two
        3. ...
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen
      placeholder: Expected behavior...
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Your system details
      placeholder: |
        - OS: Ubuntu 22.04
        - Desktop: Cinnamon 5.4
        - Monitors: 2x 1920x1080
        - Python: 3.10
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs
      description: Relevant log output from ~/.local/share/wallpaper-rotation/rotator.log
      render: bash
