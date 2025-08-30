# Decisions for modelling & code writing

This file goes into detail about some of the most important modelling decisions made throughout this project and
clarifies why they are implemented in the way they are.

<details>
<summary>Table of contents</summary>

- [Software architecture](#software-architecture)
    - [Services](#services)
    - [Components](#components)
- [Programming style](#programming-style)
    - [Comments](#comments)
    - [Naming](#naming)

</details>

## Software architecture

This section of the documentation goes into detail about the high-level architectural questions and how I went about
them.

### Services

Many Django projects are written using a fat-model approach. This means that there is no dedicated package/class which
deals with basic CRUD tasks. These tasks are rather implemented directly in the views themselves.

For this project I actively chose not to follow this approach. The main reason for that is, that using the fat-model
approach is prone to code-duplication and high coupling. This makes it hard if business-logic requirements change, as
many different parts of the system then have to be changed as well.

Instead for this project I chose to introduce a **service layer**. The task for the services is to perform all CRUD
tasks one would typically do, but through a clear interface which decouples code responsible for visualization from the
actual data-manipulation code. Then my components (ref. below) will simply access those interfaces (methods) and don't
have to worry about the implementation details.

### Components

In frontend development terms, a component is a re-usable piece of visualization code. Out of the box, django does not
support components. Even though this is not natively supported I actively chose to use a "third-party" library to add
this support. Components originally were made popular by Javascript frameworks (like Angular or React) and help to
massively reduce code duplication and maintain a single-responsibility software design.
To get exactly these benefits for this project, I opted to use the library `django-components`.

## Programming style

The style of writing programming is often very opinionated. No one style of code is of course always correct.
This section of the documentation purely goes into detail why I chose to write my code in the way I did.

### Comments

It often feels like either one loves or hates comments. I don't really belong to any of these extremes, but I do think
overusing comments ruins code bases quite drastically, as they are rarely updated whenever the code they are written for
changes.

Therefore I opted to only add comments wherever extra context is really needed.

The same applies to docstrings. The reason for mostly omitting docstrings is that often docstrings just repeat the
method name. For instance:

```python
def get_currently_active_student():
    """Loads and returns the currently logged in student."""
    pass
```

I don't see any value added in these sorts of scenarios - so I omit them entirely and only add docstrings which
actually convey additional context about the method: What errors do methods raise, what does the user have to take
care of, are there prerequisites before calling a method, and so on..

### Naming

For both variables and method/function names I try to encode as much of context in the name itself - instead of relying
on comments. While this approach sometimes results in very bulky method names, it is a great way to make code easier to
understand, as the context is in the code itself - not in any accommodating comments next to it.

