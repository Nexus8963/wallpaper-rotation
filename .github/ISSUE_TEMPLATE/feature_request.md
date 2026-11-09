name: Feature Request
description: Suggest a new feature or enhancement
title: "[FEATURE] "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for the suggestion! Tell us about your idea.
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the feature you'd like
      placeholder: I would like...
    validations:
      required: true
  - type: textarea
    id: use-case
    attributes:
      label: Use Case
      description: Why would this feature be useful?
      placeholder: This would help because...
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Other approaches you've considered
      placeholder: "- Alternative 1\n- Alternative 2"
