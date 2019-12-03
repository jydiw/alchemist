# alchemist: a chemistry solver

## Overview (December 02, 2019)
`alchemist` is a chemistry word problem solver utilizing natural language processing (NLP) and neural networks (NNs) to allow for plain-English input. Currently, the scope of the project is limited to balancing chemical equations and predicting the products of a chemical reaction. Development of the project will persist into the next year with hopes of evolving into a robust machine-learning-assisted word-problem solver covering all general chemistry topics.

The project can be summarized by the following milestones:

1. topic classification
2. parts-of-speech (POS) and chemically-relevant entity (CRE) extraction
    - symbolic transformation of grammar structures
    - translation of chemical names into chemical formulas
3. codifying the problem-solving process
4. codifying the intuition of chemical phenomena

The work in this project would not be possible without the following `python` packages, chemical databases, and texts:

- [chempy](https://github.com/bjodah/chempy), an extremely robust chemistry package offering powerful modeling tools for inorganic and physical chemistry
- [chemdataextractor](https://github.com/mcs07/ChemDataExtractor), a chemistry-aware NLP toolkit
- [pubchempy](https://github.com/mcs07/PubChemPy), an API wrapper providing access to [pubchem](https://pubchem.ncbi.nlm.nih.gov/), the world's largest free chemical database, operated by the [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/).
- ideas from [mat2vec](https://github.com/materialsintelligence/mat2vec), an application utilizing `gensim.models.word2vec` which has been shown to extract domain-specific information on materials science texts

## Training a Word Vector Model
Tshitoyan et al recently published a paper in Nature magazine, titled: [*Unsupervised word embeddings capture latent knowledge from materials science literature*](https://www.nature.com/articles/s41586-019-1335-8). In short, word vector models were able to extract domain-specific information as well as predict the existence of never-discovered material properties after processing materials science abstracts published within the last 80 years.

We trained a `word2vec` model on fifteen general chemistry textbooks

### Word2Vec

<img src="http://mccormickml.com/assets/word2vec/skip_gram_net_arch.png">

## Further NLP to Extract CREs
- using chemdataextractor and pubchempy

## Creating an equation predictor
- quantifying chemical intuition
    - describing free energy?
- CHNOSZ for thermodynamic data
- oxtoby and CRC to fill in some blanks

## 