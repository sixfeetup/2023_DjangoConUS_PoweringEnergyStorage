---
title-prefix: Six Feet Up
pagetitle: Powering Energy Storage Beyond Excel
author: Calvin Hendryx-Parker, CTO, Six Feet Up
author-meta:
    - Calvin Hendryx-Parker
date: DjangoCon US 2023
date-meta: 2023
keywords:
    - Python
    - Programming
    - Code
---

# Powering Energy Storage Beyond Excel {.semi-filtered data-background-image="images/abstract.jpg"}
#### Calvin Hendryx-Parker, CTO
#### Six Feet Up

::::::::::::::{.credits}
<a style="background-color:black;color:white;text-decoration:none;padding:4px 6px;font-family:-apple-system, BlinkMacSystemFont, &quot;San Francisco&quot;, &quot;Helvetica Neue&quot;, Helvetica, Ubuntu, Roboto, Noto, &quot;Segoe UI&quot;, Arial, sans-serif;font-size:12px;font-weight:bold;line-height:1.2;display:inline-block;border-radius:3px" href="https://unsplash.com/@davidclode?utm_medium=referral&amp;utm_campaign=photographer-credit&amp;utm_content=creditBadge" target="_blank" rel="noopener noreferrer" title="Download free do whatever you want high-resolution photos from David Clode"><span style="display:inline-block;padding:2px 3px"><svg xmlns="http://www.w3.org/2000/svg" style="height:12px;width:auto;position:relative;vertical-align:middle;top:-2px;fill:white" viewBox="0 0 32 32"><title>unsplash-logo</title><path d="M10 9V0h12v9H10zm12 5h10v18H0V14h10v9h12v-9z"></path></svg></span><span style="display:inline-block;padding:2px 3px">David Clode</span></a>
::::::::::::::


# Energy Storage Projects

## Stages

- Project/System Requirements
- Sizing
- Configuration
- Build
- Maintain


::: notes
- Every project is a multi step process
- Usually calculation for 20 to 25 years lifecycle
- Calculate required hardware components to fulfill contract
- Predict system degradation over defined period of time
- Calculate tranches; new hardware that needs to be added at a particular point in time to keep system above minimum requirements
- Don’t add too much hardware upfront; too expensive
:::

# Why Excel in First Place

- Widely known
- Easy to start with
- Easy to adjust to business case
- Easy collaboration and sharing
- Handling of massive tabular data
- Handle complex formulas and business logic
- High precission calculations

::: notes
- Brief background on why Excel is used so much in first place
- Many companies build their business on Excel
- Explain the features that can be used for businesses:

  - Easy sharing and collaboration
  - Rich set of formulas
  - Fast calculations
  - Use references across multiple sheets
  - Include external data
  - Macros (now also with Python)
:::

# Tables...

![](images/Excel01.png)

::: notes
- Lots of tables everywhere
:::

# Why <ins>NOT</ins> Use Excel

- No scaling
- No reliable versioning
- No protection of business know-how and internals
- No fault tolerance
- No field permissions
- No tests

::: notes
- The “Which version are you working on?” problem
- “Versioning” by filename pattern or written as documentation in a sheet
- Securing business logic (sharing file accidentically with externals)
- Everyone can change the content of a cell and formula; no permission checks
- Everyone can see everything
- No tests for business logic
:::

# Why Django?

- Batteries Included
- Mature
- Secure
- Reliable
- Extendable
- Scalable
- Testable

::: notes
- Django includes everything to get started fast; also admin UI
- You can care about data and business logic first
- It is more than 10 years old
- Python, high security score
- Easily extendable with add-ons
- Horizontal scaling; use Celery for long running tasks, ...
- Easy to write unit tests
:::

# Our Stack

- Django backend
- PostgreSQL database
- `djangorestframework` — DRF, Django REST-Framework
- `drf_spectacular` — OpenAPI
- `django-rest-framework-simplejwt` — JWT
- `django-filter` — Filter classes for DRF
- NextJS UI
  
::: notes
- django: easy to start (admin), Python, we know and use it for so long
- postgres: robust, reliable, scalable
- djangorestframework: THE default rest framework
- drf_spectacular: OpenAPI 3 schema generation for Django REST framework
- django-rest-framework-simplejwt: A JSON Web Token authentication plugin for DRF
- django-filter: filter down a queryset based on a model’s fields
:::


# Transition

1. Evaluate
1. Prototype
1. Review
1. Build
1. Switch

::: notes
- The optimal stages for transition from Excel to custom app with Django

1. **Evaluate:** Inspect and document every formula, every dependency
1. **Prototype:** Re-build business logic (formulas) with Python. Use Jupiter notebooks for this
1. **Review:** Let customer review protoype with real world data
1. **Build:** Implement the prototype in Django
1. **Switch**: Replace Excel files with new Django App
:::

# Transition

## Evaluate

- Collect <ins>ALL</ins> formulas
- Document them
- Add examples
- Add spreadsheet version information

::: notes
- Top priority: every formula in the spreadsheets needs to be documented
- Every formula needs valid and invalid examples (to know when to fail)
- Add information about the spreadsheed version (file version), the cell location, all precedents and dependents
- When possible link to Jupiter notebook example
:::

# Transition

## Prototype

- Using Jupiter Notebooks
- Rapid development
- No full stack required
- Let customer test with real data
- Early feedback

<!-- TODO: Link notebook example -->

::: notes
- Can be easily shared and run locally
- No need to set up full stack to write and test business logic
- Let customers test with their real data (CSV import) and give early feedback
:::

# Transition

## Build

- Custom cookiecutter template
- [https://github.com/sixfeetup/cookiecutter-sixiedjango](https://github.com/sixfeetup/cookiecutter-sixiedjango)
- Terraform and AWS
- Local K8S development
- Fast developement, easy deployment

::: notes
:::

<!-- # Build

## Backend

::: notes
::: -->


<!-- # Build

## Front-end

::: notes
::: -->


# Challenges

- New spreadsheet versions
- Changes in the formulas
- Parallel usage of Excel and Django
- Requirement changes

::: notes
- People are constantly updating and optimizing Excel sheets; every new version results in re-evaluation
- Sometimes (small) changes in formulas without notice
- People are still working with Excel while app is built
- Contant change of business requirements is easier doable in Excel than updating code
:::


# Conclusion

- Use Django from beginning if you can
- Use Excel if you have to
- Transition to Django early

::: notes
:::

# Wrap up and Questions {.semi-filtered data-background-image="images/justin-casey-7B0D1zO3PoQ-unsplash.jpg"}

## Resources

* Six Feet Up Blog Post -- [How to Break Free from Excel](https://www.sixfeetup.com/blog/how-to-break-free-from-excel)

## Find Me 😍

#### <calvin@sixfeetup.com>

🐘 [`@calvinhp@fosstodon.org`](https://fosstodon.org/@calvinhp)  
🐦 [`@calvinhp`](https://twitter.com/calvinhp)
