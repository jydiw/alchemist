# alchemist: a chemistry solver

## Overview (December 02, 2019)
`alchemist` is a [python](https://www.python.org/) package that solves chemistry problems. As of now, its scope is limited to:
- balancing chemical equations
- predicting the products of simple inorganic chemical reactions  

`alchemist` aims to remove the user from as much of the programming as possible, utilizing natural language processing and machine learning to trigger appropriate chemistry problem-solving algorithms.

The package can be summarized by the following milestones:

1. natural language processing (NLP)
    - recognizing the topic of a chemistry word problem
    - parsing chemically relevant information and transforming English syntax into chemical symbols
    - translation of chemical names into chemical formulas
2. problem-solving
    - applying proper algorithms to solve chemistry problems
    - accessing the processing power of computers to use experimental data to predict the products of a chemical reaction

This project is inspired by current research in machine learning and NLP, and significant portions of code are imported from outside libraries.

- [chempy](https://github.com/bjodah/chempy), a robust chemistry package offering powerful modeling tools for inorganic and physical chemistry
- [chemdataextractor](https://github.com/mcs07/ChemDataExtractor), a chemistry-aware NLP toolkit
- [pubchempy](https://github.com/mcs07/PubChemPy), an API wrapper providing access to [pubchem](https://pubchem.ncbi.nlm.nih.gov/), the world's largest free chemical database, operated by the [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/)
- [tika-python](https://github.com/chrismattmann/tika-python), a python port of the [Apache Tika](http://tika.apache.org/) library that parses text from `pdf` files
- inspiration from [mat2vec](https://github.com/materialsintelligence/mat2vec), an application which has been shown to extract chemical knowledge from text (based on [Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html))
- and the usual suspects: [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [TensorFlow/Keras](https://www.tensorflow.org/guide/keras), and python itself.

## Natural Language Processing

### Training a Neural Network to Learn Chemistry
[*](https://aegis4048.github.io/demystifying_neural_network_in_skip_gram_language_modeling)[*](http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/)In 2013, Thomas Mikolov proposed a prediction-based NLP technique called Word2Vec, a neural network trained on count-vectorized text with a single hidden layer. The weights of the hidden layer, called "word vectors",  mathematically represent the co-occurence of words in a corpus. By scanning through a document and calculating the statistics that other words occur with the target word, the model is able to mathmatically quantify word context; it would make sense that a pair of synonyms would likely occur around similar words since they carry similar meaning and have identical parts of speech.

<img src="https://s3-ap-south-1.amazonaws.com/av-blog-media/wp-content/uploads/2017/06/06062705/Word-Vectors.png">

Earlier this year, Tshitoyan et al demonstrated that these Word2Vec techniques could be used to extract domain-specific information, in a paper in Nature magazine titled: [*Unsupervised word embeddings capture latent knowledge from materials science literature*](https://www.nature.com/articles/s41586-019-1335-8). Not only were the models capable of clustering related materials-science concepts together, but they have correctly predicted as-of-then undiscovered chemical properties.

<img src="https://scx2.b-cdn.net/gfx/news/hires/2019/1-withlittletr.jpg">

Inspired by their discoveries, `alchemist` uses a related neural network architecture called skip gram Word2Vec, which focuses 

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