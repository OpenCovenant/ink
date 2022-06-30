## Roadmap

Outlines several current limitations and some planned future work. Many items are prefixed by a label, indicating
relevant information. The following lists are not comprehensive by any mean, if you come across some issue or topic that
needs to be addressed, feel free to bring it up.

### Short-Term

- [**good first issue**] Add proper code for the height of the footer (the footer should be shown at the bottom of every
  display, open to other suggestions).
- [**good first issue**] When writing a text, selecting it all and pressing space, repositions the cursor to be
  displayed in the middle of the line, instead of the beginning.
- [**enhancement**] In some displays, the suggestions on the right/bottom panel overflows the borders on the sides.
  Either address by only showing enough suggestions, or add ... (perhaps via the `.text-truncate` Bootstrap class)
  towards the end of that line, or through some other subtle way.
- [**good first issue**] When deleting a word in the editor, call the `generateMarkings` POST request so that markings
  on the right reflect the new text.
- [**enhancement**] Rewrite the central algorithm to now include the context, maybe trigrams for now (and later on some
  Deep Learning technique).
- [**help wanted**] Improve quality of the datasets (currently [loanwords](https://github.com/OpenCovenant/loanwords)),
  ideally including references if there's considerable ambiguity.
- [**good first issue**] _onscroll_, remove the shown popover.
- [**help wanted**] Compile a brief set of grammatical rules that the text can be matched against. This in turn,
  provides more details on the mistakes found on the text.
- [**good first issue**] Write decent code for the popovers, specifically the positioning.
- When returning from the POST request for the text parsing, try to make the text replacement seem more organic.
- [**enhancement**] Drop running calls if new ones are created (previous calls are now obsolete, given that the text
  changed).
- Redesign how text markings are described and/or displayed on the right.
- [**help wanted**] ARIA, address the quality of the current accessibility (A11Y) and outline and/or implement
  improvements. More information on this can be
  found [here](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA).
- [**enhancement**] CI/CD (linters)
- [**enhancement**] tests
- [**good first issue**] Add an Angular component for displaying a global information label, scenarios include server
  issues, outages, etc.
- [**good first issue**] Keep text in the editor even after toggling out of that div, this should be relatively
  straightforward (might be obsolete soon as the design of the toggles might change).
- [**question**] For text with emojis, the algorithm currently raises an error. Maybe simply skip emojis?
- [**question**] For text with links, the algorithm currently attempts to parse them. Maybe simply skip links?
- [**good first issue**] Create a PoC algorithm for plagiarism detection.
- [**good first issue**] Add the capability to process .odt files (LibreOffice Writer documents).

### Long-Term

- Design of the markings, complex topic.
    - Currently using a very pale red for errors, #FFC8C8, very light orange, #FFD182, and a very soft blue, #A1B6DC,
      for stylistics, which we don't yet recognize. The colors should be strong enough to be distinct, but also not seem
      too aggressive. In this regard, the two latter colors seem fine, but the calm red might have a better
      substitution. Perhaps a relaxing purple or green? While deciding also consider the distribution of each marking,
      therefore how often the user will encounter each color, which in turn will paint in his subconscious the feeling
      of this entire interaction with the markings.
    - An additional topic here is the way they are displayed. Should they surround a word in its entirety, what about
      underlines?
    - Finally, consider that a word/sentence might qualify for multiple markings, what then? Do we display the most
      relevant/important/urgent one, or somehow attach all that information there?
- Evaluate how a Dark Mode would be implemented, perhaps along with a demo?
- [**question**] Consider adding plain text onpaste, can this be easily done without the `execCommand`? is there a valid
  scenario in which we need the not-plain text?
- Consider adding text to the editor via voice, probably at best it requires a trained (pretrained?) NLP model that
  simply does this.
- [**good first issue**] Consider how to process numbers written through words. They seem to adhere to a certain group
  of rules, check if a straightforward script can be written for this purpose.
- Redesign UI of the editor, as several new features should be considered to be added.
- Consider adding a "copy raw text" button on the top right of the editor.
- Consider adding a "clear all written text" button, perhaps as an "x" button in the top-right of the editor.
- Consider adding a history of the texts processed.
- Consider on how to technically handle the conjugations of loanwords?
- [**enhancement**] After deciding on the algorithms, if their implementation on C++ provides sufficiently increased
  performance, add Python bindings and utilize them through this Django
  application.
- [**question**] Would word autocomplete/autosuggest be a useful tool here (perhaps during the writing of relatively
  long words e.g. **përpjestueshmërisht**?)
- [**question**] Would optical character recognition be a useful tool here, (perhaps during the reading of images, or
  scans of text?)

### Linguistic Challenges

- Should the text inside the quotes be taken into account for typos and loanwords?
- How to tackle dialectics?
- Ignore words with a starting capital letter? Probably only attempt to consider when it is the first word in a
  sentence, as it might be a **common noun** written wrong?
- Always ignore words with only capitalized letters?
- Address words with a line between them.
