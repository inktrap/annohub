# Introduction

I made the observation, that forensic linguists are frequently annotating data.
Unfortunately not all the processing steps are done in the same way, so the
results might not be reproducible. Besides that, a lot of implicit decision may
lead to incomparable results and that should change.


# Annohub

 - our goal is to make the implicit steps explicit and you should do as less work as possible
 - we do the heavy lifting: preprocessing, segmentation and initial annotation
 - we would like to esablish a platform where people can share their process and data

## Design Considerations

 - be flexible and support multiple languages and tagsets
 - be transparent about the annotation process
 - users should always get their data back

## Features

 - tokenization gui
 - annotation gui
 - manage projects and annotators
 - export your data
 - stats for your project

## We Want To Encourage You

 - to learn NLTK and Python
 - to host annohub yourself (batteries are included!)
 - to contribute to annohub's development
 - to adapt annohub to your personal requirements
 - to improve NLTK by providing tagset-mappings or by training taggers

# How-to

Every project has different steps that you have to complete. For some of them
you can find additional details in the sections below. The following list is an
overview of the lifecycle of each project:

 - **creation**: the creator uploads the text. He chooses additional data that helps to process the text: the genre, the language and a tagset.
 - **tokenization**: the creator of a project has to decide what the sentences and
 the token are. Also words sentences and punctuation can be separated or
 completely deleted from the text. It is also possible to join punctuation,
 tokens or sentences so mistakes of the automated segmentation can be
 corrected.
 - **manage annotators**: the creator can invite annotators now. Only annotators can annotate the project and have to be invited, even if the creator and the annotator are the same person. The creator has to finally choose a tagset here but currently only one tagset is available.
 - **annotation**: this is the main step for annotators you will do most of the work.
    - the menu on the top enables annotators to display information related to the tag by hovering over it. A different tag is chosen by clicking on it in the menu.
    - it is also possible to select a tag by typing it into the search bar. This also displays the description of the currently selected tag which can be chosen by pressing enter.
 - **publish** and display **statistics**: After the annotation you can select a license and publish your project. After this step you and your annotators can view basic statistics about your project. Published projects are currently not listed. TODO: implement stats.

It is always possible to **export** the project. This is also useful for annotators
that might be removed from the project and permits them to save their data. TODO: implement export.Projects can also be deleted or transfered. TODO: implement transfer.

# Preprocessing

What are typical preprocessing steps?

 - Somehow the data that should be processed has to be read, so we have to handle different kinds of encodings.
 - After we successfully read the data, we might want to “clean” it. What you do while
preprocessing depends on your needs, but how you do it should be consistent and
in the best case the tools you used should be accessible to everyone.
 - However there are preprocessing steps that might be problematic, because they are irreversibly changing the data. Stripping punctuation and the practice of writing uppercase characters as lowercase are examples for this.

## Punctuation And Lowercase


@manning_foundations_1999 [124, p. 124] write the following about stripping inter-sentence-punctuation:

> While normally people want to keep sentence boundaries (see section 4.2.4
> below), often sentence-internal punctuation has just been stripped out.
> This is probably unwise. Recent work has emphasized the information
> contained in all punctuation. No matter how imperfect a representation,
> punctuation marks like commas and dashes give some clues about the macro
> structure of the text and what is likely to modify what.

This is exactly the point why there is a warning sign next to this
preprocessing option: Do you want to lose clues about the macro structure? Have
a look at the first paragraphs of [Alice in
Wonderland](http://www.gutenberg.org/cache/epub/11/pg11.txt), which includes
a lot of embedded speech and thoughts, and also some words are uppercase which gives them a different emphasis:

    CHAPTER I. Down the Rabbit-Hole

    Alice was beginning to get very tired of sitting by her sister on the
    bank, and of having nothing to do: once or twice she had peeped into the
    book her sister was reading, but it had no pictures or conversations in
    it, 'and what is the use of a book,' thought Alice 'without pictures or
    conversations?'

    So she was considering in her own mind (as well as she could, for the
    hot day made her feel very sleepy and stupid), whether the pleasure
    of making a daisy-chain would be worth the trouble of getting up and
    picking the daisies, when suddenly a White Rabbit with pink eyes ran
    close by her.

    There was nothing so VERY remarkable in that; nor did Alice think it so
    VERY much out of the way to hear the Rabbit say to itself, 'Oh dear!
    Oh dear! I shall be late!' (when she thought it over afterwards, it
    occurred to her that she ought to have wondered at this, but at the time
    it all seemed quite natural); but when the Rabbit actually TOOK A WATCH
    OUT OF ITS WAISTCOAT-POCKET, and looked at it, and then hurried on,
    Alice started to her feet, for it flashed across her mind that she had
    never before seen a rabbit with either a waistcoat-pocket, or a watch
    to take out of it, and burning with curiosity, she ran across the field
    after it, and fortunately was just in time to see it pop down a large
    rabbit-hole under the hedge.

Clearly we would not be able to find good sentence boundaries for the last
sentence if we stripped the markers for embedded speech.

# Tokenization

 - all the available tokenizers are based on punctuation
 - because of that, the preprocessing option ``strip punctuation`` has a warning sign: implemented carelessly it would mess up the segmentation of sentences.
 - ``strip punctuation`` excludes punctuation that is used to end a sentence, defined by the ``delimiter_list = ['?', '!', '.', '…']`` in ``preprocessor.py``
 - also it won't strip hyphens that mark a compound like *waistcoat-pocket*
 - tokenizers for the following languages are available:
    - czech
    - danish
    - dutch
    - english
    - estonian
    - finnish
    - french
    - german
    - greek
    - italian
    - norwegian
    - polish
    - portuguese
    - slovene
    - spanish
    - swedish
    - turkish

## Tokenization Background

We have our cleaned data now, time to decide what a sentence is (sentence
segmentation) and what a word is (tokenization). This is sounds very easy at
first: Words are separated by whitespaces. But this is not always the case and
there are cases that are hard to decide but need to be handled consistently.
Again, from @manning_foundations_1999 [124, p. 124]:

> What is a humble computational linguist meant to do? Kucera and Francis
> (1967) suggested the practical notion of a graphic word which they define
> as a string of contiguous alphanumeric characters with space on either
> side; may include hyphens and apostrophes, but no other punctuation marks.
> But, unfortunately, life is not that simple, even if one is just looking
> for a practical, workable definition. Kucera and Francis seem in practice
> to use intuition, since they regard as words numbers and monetary amounts
> like $22.50 which do not strictly seem to obey the definition above.

Also, not all languages separate words by whitespaces and “the question of what
counts as a word is a vexed one in linguistics, and often linguists end up
suggesting that there are words at various levels, such as phonological words
versus syntactic words, which need not all be the same.” [@manning_foundations_1999, p.125, p.125]


## Annotation And Agreement

After these steps we can finally start our annotation. Obviously we want to
minimize the work we have to do, that's why we start with an automated approach
that chooses the correct annotation most of the time. But most of the time
means: There will be errors and we would like to know about the algorithm, the
training the tagger got, better paramaters we could choose and the error-rate.
Finally we have to review the output of the tagger and correct it's mistakes.
That is one of the main jobs of annohub: Provide a nice interface that enables the
annotator to choose the matching tag most efficiently.

Human annotators make errors too and typicly we are looking at the
[inter-annotator
agreement](https://corpuslinguisticmethods.wordpress.com/2014/01/15/what-is-inter-annotator-agreement/)
to decide if we can actually use an annotation.


## Languages

Unfortunately the available taggers are only trained with
english language data from f.e. :

 - the [Penn Treebank](https://www.cis.upenn.edu/~treebank/),
 - the [Wall Street Journal](https://catalog.ldc.upenn.edu/LDC2000T43) (WSJ)
 - or the [Brown Corpus](http://www.hit.uib.no/icame/brown/bcm.html)

Information about the data that was used to train the tagger is really hard to
find, because only the pickled tagger is available.

That means genres not included there might not work as good and the situation
for languages other than english is a little bit … embarassing?

## Tagsets

Documentation for three tagsets is included in NLTK:

 - Penn Treebank (upenn)
 - Brown-Corpus (brown)
 - Claws-5 (claws5)

The default tagger was trained with the ``upenn`` tagset on the ``WSJ`` corpus
([PerceptronTagger](https://spacy.io/blog/part-of-speech-POS-tagger-in-python>)).
So in order to use a different tagset than the ``upenn`` tagset, two solutions
are possible: mappings and training.


## Mappings


A mapping maps the tags of one tagset to the tags of another tagset (an at
least surjective function). NLTK can load and
[map](http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.mapping) between
two tagsets. Mappings have the following form and currently exist only **to**
the [Universal Tagset](http://arxiv.org/abs/1104.2086).

~~~
ABL	PRT
ABN	PRT
ABN-HL	PRT
ABN-NC	PRT
ABN-TL	PRT
ABX	DET
AP	ADJ
AP$	PRT
AP+AP-NC	ADJ
AP-HL	ADJ
AP-NC	ADJ
AP-TL	ADJ
AT	DET
~~~

As you can see from the example, the Universal Tagset is by intention very
general and maps multiple tags from the Brown Corpus to the same tag That
means detailed linguistic information is lost and as a consequence, you won't be
able to map the universal tagset back (mapping to the Universal Tagset is not
a bijection). If you don't want that to happen, you have to write your own
mapping from the ``upenn`` tagset to whatever tagset you want to use.

Fortunately other people (Nathan Schneider) already put some work into that:

 - <https://gist.github.com/nschneid/4231292>
 - <https://gist.github.com/nschneid/6476715>

but I have not tested these scripts or verfied that they do a good job. It also
would be nice to include the mappings into NLTK, I think they would be happy
about reliable mappings.

As an additional idea: Why shouldn't we create a very detailed tagset that can
represent all the other tagsets? We could use it as a mapping tagset so we
would be able to map from every other tagset to the mapping tagset and from the
mapping tagset to every other tagset. That would greatly simplify all
mapping-worries, right?


## Training

If you really want to have better support for other languages you should start
to train the
[Perceptron-Tagger](http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.perceptron),
see ``train()`` and make your results available to NLTK.

There also is
[nltk-trainer](http://nltk-trainer.readthedocs.org/en/latest/train_tagger.html),
which might be helpful, or can give you ideas (see
[train_tagger.py](https://github.com/japerk/nltk-trainer/blob/master/train_tagger.py>))
on how to train an HMM-Tagger.

Training taggers needs a lot of data, the more the better (the author of the
Perceptron-Tagger talks about 5000 examples, but that is only an example by
itself). If we would go to conventional way, we would use like 95% of the
``WSJ`` Corpus (~47M words) for training, and we would need 44.650.000 words
with the correct part of speech label in our language. Read more about training
in the NLTK book, [about classifying text](http://www.nltk.org/book/ch06.html).

If you have ideas about training taggers or are working on a mapping our would
like to write the Mapping Tagset outlined above, write me.


# Developer Documentation

## Extensibility

 - the app is separated into blueprints
 - the library is separated into componants that are testable
 - the nlp parts are separated in dedicated modules and can also be changed easily

## Open Source

 - join us on GitHub (looking for contributors!)
 - please submit a ticket if you find an issue
 - ideas! fixes! Pull requests are welcome!

## Tests

 - some tasks are covered by seleniumtests
 - library is covered by unittests

## DB

 - saving individual sentences increases the performance of MongoDB
 - other approaches with embedded documents or growing list fields were not performant enough
 - data can be deduplicated more easily
 - MongoDB can scale TODO: limit

# Wishlist

 - let the user add arbitrary annotations
 - more languages, more tagsets, more kinds of annotation
 - implement a plugin system that administrators can use
 - implement imports and a REST API
 - translate the gui to different languages

# References

