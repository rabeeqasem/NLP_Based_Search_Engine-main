This Project is an NLP-Based search engine with GUI.

The main features: 
1.	Regular Expression Matching
2.	Stem-based Matching: using Porter, Snowball, Lancaster, and manually developed stemmer 
3.	Boolean Matching: such as (A and B, A or B, A and not B).
4.	Exact Matching
5.	Proximity Matching: support queries in the form of A /k B, where k is positive integer between 1-10. Example query: Palm /2 Tree.
6.	Wildcard Matching: Example queries: welc* , *tion, com*s
7.	Zone-based Matching: Example query: (title) Hotel  or (description) Hotel 
8.	Semantics-based Matching: query reformulation (synonymous terms, hypernyms, meronyms, hyponyms). The used semantic resources are: WordNet, Yago3
9.	Cosine-based Matching: tf.idf matching function 

Dataset used: http://www-i6.informatik.rwth-aachen.de/imageclef/resources/iaprtc12.tgz

full report can be found in Report.docx

to run the model:
1.	you need to install Yago_df using https://drive.google.com/file/d/1ACw2k9683N1-c9rdJBlhuSg7gcER2eq2/view?usp=sharing
	extract it where main.py exists)
	Note: if you don't intend to use YAGO, just ignore this step
2.	run data_parser.py
3.	run main.py
Note: you might need to change the main path in data parser before running the code