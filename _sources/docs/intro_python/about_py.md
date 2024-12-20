---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(about_py)=

# About Python

> \"Python has gotten sufficiently weapons grade that we don't descend
> into R anymore. Sorry, R people. I used to be one of you but we no
> longer descend into R.\" -- Chris Wiggins


## What\'s Python?

[Python](https://www.python.org) is a general-purpose programming
language conceived in 1989 by Dutch programmer [Guido van
Rossum](https://en.wikipedia.org/wiki/Guido_van_Rossum).

Python is free and open source, with development coordinated through the
[Python Software Foundation](https://www.python.org/psf/).

Python has experienced rapid adoption in the last decade and is now one
of the most commonly used programming languages. It has a large and supportive user community, especially in the scientific and data science domains. Python is beginner-friendly and routinely used to teach computer science and programming in top computer science programs.

### Python for Scientific Programming

Python has become one of the core languages of scientific computing.

It\'s either the dominant player or a major player in [machine learning](https://pytorch.org/), [data science](http://scikit-learn.org/stable/), [astronomy](http://www.astropy.org/), [chemistry](http://chemlab.github.io/chemlab/), [computational biology](http://biopython.org/wiki/Main_Page), and [meteorology](https://pypi.org/project/meteorology/).

### Textbooks and Tutorials

Our favorite Python textbooks/tutorials include:
- [A Whirlwind Tour of Python](https://nbviewer.org/github/jakevdp/WhirlwindTourOfPython/blob/master/Index.ipynb) by Jake VanderPlas: **highly recommended for everyone**. It's worth reading even if you are already familiar with Python. We will cover some of the materials in the course.
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) also by Jake VanderPlas. It covers more advanced packages such as `pandas`.
- [Learn Astropy](https://learn.astropy.org/) tutorials. 

Of course, when you encounter a problem, you can always ask for help on [Stack Overflow](https://stackoverflow.com/), or ask your favorite large language model. 


### Popularity

The following figure (made by Yuan-Sen Ting) shows the evolution of programming languages used in astronomy papers over time. It's clear that Python has become the dominant language in the field (whereas IRAF and IDL were dominant in the past). Python is now the number one choice not only because it is easy to learn, but also because it has a huge number of libraries that fit the needs of astronomers (especially observational astronomers!!).

You will have a chance to use different Python libraries in the course, and some of them will continue to be useful in your future research.


```{figure} /_static/lecture_specific/about_py/astro_language_evolution.jpeg
---
height: 450px
---
Credit: [Yuan-Sen Ting](https://x.com/TingAstro/status/1869723006354022800)
```


### Features

Python is a [high-level language](https://en.wikipedia.org/wiki/High-level_programming_language) suitable for rapid development. It supports multiple programming styles are supported (procedural, object-oriented, functional, etc.). We will (probably) use all these styles in the course.

## Code Style

It is **very important** to write clean and readable code. We highly recommend you to read this [Python Style Guide](https://www.classes.cs.uchicago.edu/archive/2017/fall/12100-1/style-guide/index.html) to get a sense of what good Python code looks like. As you go through the course materials, you will see how we write code and you will be able to develop your own style based on these guidelines.


## What to do if your code doesn't work?
- Ask Google, Stack Overflow, or your favorite search engine. New programmers often make the mistake of thinking that they need to solve every problem from scratch. In reality, most programming problems have been encountered by someone else before. Don't feel embarrassed by the mistakes you make. Everyone makes mistakes when they are learning to program (including the instructors -- they still suffer a lot now).
- Ask your classmates. They are likely to have encountered the same problem.
- Ask large language models (such as GPT or Claude). These models now are really good at debugging code.
- Try the AI assistant on Google Colab. 