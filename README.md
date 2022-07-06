## penda

An open-source text assistant designed for the Albanian language.

![a penda example](docs/penda_example.png)

### Getting Started

Simply add the text in the designated area and interact with the generated markings. Some current and planned
capabilities of **penda** include:

- spelling corrector
- loanword substitutor
- plagiarism detector
- stylistic changes to address tautologies, nominalizations, overly long and/or complex sentences, and other general bad
  writing practices, given the context
- providing various details on etymology, synonyms, antonyms, and so on, on each word
- translator

The **penda** project is compound of two repositories, [**quill**](https://github.com/OpenCovenant/quill) and
[**ink**](https://github.com/OpenCovenant/ink). The former is tasked with much of the logic and behaviour,
while the latter with its visual aspect. A more formal evaluation of the current behaviour is provided in
the [INITIAL EVALUATION](docs/INITIAL_EVALUATION.md) page. Additionally, you can also check out what we look forward to
in the future for **penda** at [ROADMAP](docs/ROADMAP.md).

#### How to Run

To have **ink** running locally, start by cloning the repository and installing the dependencies. Afterwards, simply
running `python manage.py runserver` will start the server. Keep in mind that a new secret key is generated on each run
if one is not found in the environment (managing the security aspect is entirely your responsibility and should be
handled with the appropriate care).

### Contributors

Throughout the development of this project we've received significant help from various contributors related to a wide
range of aspects. We'd like to express our gratitude in the following alphabetical list. Note to contributors, before
finalizing your first MR, **add yourself**! The format is _username [(firstname lastname)] - role/contribution_, in
which the actual name is obviously optional.

- AndersonCeci (Anderson Ceci) - developer
- AndiBraimllari (Andi Braimllari) - core developer
- KostaTB - linguistic advisor

To get started with contributing, simply create an [issue](https://github.com/OpenCovenant/ink/issues) if there's a
concern to be addressed, or a [pull request](https://github.com/OpenCovenant/ink/pulls) if there are changes you'd
like to make.

### Contact

Feel free to reach us via opencovenant@outlook.com
