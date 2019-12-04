# alchemist: a chemistry solver

## Overview (December 02, 2019)
`alchemist` is a [python](https://www.python.org/) package that can solve chemistry problems. As of now, its scope is limited to:
- balancing chemical equations
- predicting the products of simple inorganic chemical reactions  

`alchemist` aims to remove the user from as much of the programming as possible, utilizing natural language processing and machine learning to trigger appropriate chemistry problem-solving algorithms.

The project can be summarized by the following milestones:

1. natural language processing (NLP)
    - (complete) recognizing the topic of a chemistry word problem
    - (incomplete) parsing chemically relevant information and transforming English syntax into chemical symbols
    - (in progress) translation of chemical names into chemical formulas
2. problem-solving
    - (complete) applying proper algorithms to solve chemistry problems
    - (complete) accessing the processing power of computers to use experimental data to predict the products of a chemical reaction

This project is inspired by current research in machine learning and NLP, and significant portions of code are imported from outside libraries.

- inspiration from [mat2vec](https://github.com/materialsintelligence/mat2vec), an application of [Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html) shown to extract domain-specific knowledge from materials science texts
- [tika-python](https://github.com/chrismattmann/tika-python), a port of the [Apache Tika](http://tika.apache.org/) library that parses text from pdf files
- [chemdataextractor](https://github.com/mcs07/ChemDataExtractor), a chemistry-aware NLP toolkit
- [pubchempy](https://github.com/mcs07/PubChemPy), an API wrapper providing access to [pubchem](https://pubchem.ncbi.nlm.nih.gov/), the world's largest free chemical database, operated by the [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/)
- [chempy](https://github.com/bjodah/chempy), a chemistry package with many useful algorithms for physical, inorganic, and analytical chemistry
- [CHNOSZ](http://chnosz.net/), a package for [R](http://www.r-project.org/) with specific applications for thermodynamic calculations in aqueous geochemistry
- and the usual suspects: [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [TensorFlow/Keras](https://www.tensorflow.org/guide/keras), and python itself.

## Natural Language Processing

### Word Vectors: AI for Language
[*](https://aegis4048.github.io/demystifying_neural_network_in_skip_gram_language_modeling)[*](http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/)In 2013, Thomas Mikolov proposed a prediction-based NLP technique called [Word2Vec](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf), an efficient method of learning vector representations of words from large amounts of text data using an unsupervised neural network with a single hidden layer. 

<img src="http://mccormickml.com/assets/word2vec/skip_gram_net_arch.png">

While continuous bag-of-word models attempt to quantify word importance by calculating overall frequency, word vectors focus on a word's co-occurence with neighboring words. A word's vector representation does not depend on its own frequency but on the *context* of that word within the corpus. 

>Example: the words "beautiful" and "pretty" can be used somewhat interchangably, which would imply that the words they co-occur with are similar. Therefore, their word vectors would occupy similar space and have a high cosine similarity.

<img src="https://s3-ap-south-1.amazonaws.com/av-blog-media/wp-content/uploads/2017/06/06062705/Word-Vectors.png">

Earlier this year, Tshitoyan et. al. [reported](https://www.nature.com/articles/s41586-019-1335-8) how these Word2Vec models were sophisticated enough to extract materials science knowledge without any explicit insertion of chemical knowledge. The model was able to understand the underlying structure of the periodic table, cluster materials based on both chemical composition and application, and (perhaps most notably) recommend materials for functional applications before their discovery. 

<img src="https://miro.medium.com/max/14362/1*_5Q3a91iS3SiG3d15MCQoA.png">

### Training a Model to Learn Undergraduate Chemistry
Inspired by this field of NLP, `alchemist` uses a specific variant of the Word2Vec neural network architecture called skip gram Word2Vec, trained on 15 general chemistry textbooks. The result was a Word2Vec model that accurately ranks text by their similarity to key phrases or topics.

In this project, we chose to limit the scope of our categorization into a binary class:

- asking the reader to produce a balanced chemical equation
- not doing that

MORE STUFF GOES HERE

## Translating English into Chemistry
Interpreting a sentence is actually a complex set of events that many of us probably take for granted. Consider the following *chemical statement*:

> Sodium metal reacts with water to form sodium hydroxide and hydrogen gas.

The chemical statement is a semantic representation of our observations of the [reaction that occurs among different *chemical species*](https://www.youtube.com/watch?v=vCvcg8XQMrM). Even if we aren't familiar with the chemistry, we are able to glean meaning from the statement through part-of-speech (POS) analysis. Let's use the [Stanford Parser](http://nlp.stanford.edu:8080/parser/index.jsp) to decompose the sentence into its [Penn Treebank POS Tags](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html):

sodium metal|reacts with|water|to form|sodium hydroxide|and|hydrogen gas
:---:|:---:|:---:|:---:|:---:|:---:|:---:
JJ NN|VBZ IN|NN|TO VB|JJ NN|CC|JJ NN

We know `metal` is a singular noun (NN) that is modified by an adjective `sodium` (JJ); that noun then performs an action `react` (VBZ) with another noun `water`. Together they perform another action `form` which directly relates to two more nouns modified nouns: `sodium hydroxide` and `hydrogen gas`.

Sodium metal and water are the substances that we start with, which we call our *reactants*. Sodium hydroxide and hydrogen gas are the substances which result from the reaction, which we call our *products*.

Writing *chemical equations* involves another layer of translation, as we transform chemical entity mentions (CEMs) into their corresponding *chemical formulas*, and convert actions into relevant *chemical symbols*:

sodium metal|reacts with|water|to form|sodium hydroxide|and|hydrogen gas
:---:|:---:|:---:|:---:|:---:|:---:|:---:
CEM|VBZ IN|CEM|TO VB|CEM|CC|CEM
Na(*s*)|+|H<sub>2</sub>O(*l*)|&rightarrow;|NaOH(*aq*)|+|H<sub>2</sub>(*g*)

Here, the chemical symbol to each reactant is represented on the left side of the arrow, and the symbol for each product is on the right side.

Those of us who have taken chemistry will have already noticed that the chemical equation is incomplete in its current form. Much like how cooking recipes specify the *quantity* of each ingredient, chemical equations must also specify the quantity of each chemical species. And as each ingredient we use in our cooking ends up in our meal, the number and type of each atom must be equal on both sides of the reaction arrow.

This can be fixed algebraically with the rewritten equation:

>2 Na(*s*) + 2 H<sub>2</sub>O(*l*) &rightarrow; 2 NaOH(*aq*) + H<sub>2</sub>(*g*)

In this *balanced chemical equation*, there are two Na atoms, four H atoms, and two O atoms on each side of the reaction arrow (e.g. counting the hydrogen atoms, there are two in each H<sub>2</sub>O; on the other side, there is one in each NaOH and two in H<sub>2</sub>). Therefore, the chemical equation is a tool that allows us to simultaneously understand the semantic meaning of what is being observed—the identities of each chemical substance and how they interact with each other—as well as the *quantitative* relationship between the chemical species involved.

A python package named `ChemDataExtractor` combines the power of POS tagging and chemistry-specific word embedding, allowing us to programatically classify each CEM and action for direct translation into a chemical equation.

The nomenclature of chemical species follow a consistent pattern; as such, an earlier iteration of this project attempted to hard-code the translation of compound names to chemical formulas. That proved to be too time-consuming to program. Instead, this project uses [pubchem](https://pubchem.ncbi.nlm.nih.gov/) via [pubchempy](https://github.com/mcs07/PubChemPy) to translate the tagged CEMs into their chemical formulas.

## Creating an equation predictor
- quantifying chemical intuition
    - describing free energy?
- CHNOSZ for thermodynamic data
- oxtoby and CRC to fill in some blanks

## 