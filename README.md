# Topics Inference Approaches

## Python ##
### Install Libraries ###
```bash
easy_install --upgrade numpy
pip install -U scikit-learn
pip install openpyxl
pip install nltk
pip install beautifulsoup4
```

### File Parser ###
```python
python email_reader.py splitfile data/email_export.xlsx ./output
```

### LDA Topics ###
```python
from nmf_topics import NMFTopics

processor = NMFTopics(email_file_path)
processor.process()
processor.print_topics()
```

### NMF Topics ###
```python
from nmf_topics import NMFTopics

processor = LDATopics(email_file_path)
processor.process()
processor.print_topics()
```

## Mallet ##
Download
http://mallet.cs.umass.edu/download.php
Put each email in a separate folder

Import data into mallet readable format
```bash
./bin/mallet import-dir --input sample-data/web/email/ --output tutorial.mallet --keep-sequence --remove-stopwords
```

Train Topics
```bash
./bin/mallet train-topics --input tutorial.mallet --num-top-words 5   --num-topics 5 --output-topic-keys topics.txt --output-doc-topics topic-files.txt
```

topics.txt - list of all topics
topic-files.txt - for each file the topic probabilities

e.g.
topics.txt
0       1.25    ipad access subscription viewer version
1       1.25    nytimes service dear password yahoo.com
2       1.25    paper nyt cancel genentech experience
3       1.25    delivery email receive day iphone

topic-files.txt
0       file:/Users/204714/Documents/topics_inference/mallet-2.0.8RC3/sample-data/web/email/email1.txt  0.19117647058823528     0.3088235294117647      0.36764705882352944     0.1323529411764706
1       file:/Users/204714/Documents/topics_inference/mallet-2.0.8RC3/sample-data/web/email/email2.txt  0.5580357142857143      0.18303571428571427     0.20089285714285715     0.05803571428571429
2       file:/Users/204714/Documents/topics_inference/mallet-2.0.8RC3/sample-data/web/email/email3.txt  0.15476190476190477     0.15476190476190477     0.20238095238095238     0.4880952380952381
3       file:/Users/204714/Documents/topics_inference/mallet-2.0.8RC3/sample-data/web/email/email4.txt  0.06428571428571428     0.35    0.2357142857142857      0.35
4       file:/Users/204714/Documents/topics_inference/mallet-2.0.8RC3/sample-data/web/email/email5.txt  0.041666666666666664    0.375   0.175   0.4083333333333333
5       file:/Users/204714/Documents/topics_inference/mallet-2.0.8RC3/sample-data/web/email/email6.txt  0.32954545454545453     0.10227272727272728     0.4659090909090909      0.10227272727272728
6       file:/Users/204714/Documents/topics_inference/mallet-2.0.8RC3/sample-data/web/email/email7.txt  0.07738095238095238     0.22023809523809523     0.3630952380952381      0.3392857142857143

## Sarah Palin Email Parser using Stanford Topic Modeling ##
https://github.com/echen/sarah-palin-lda

- Stanford Topic Modeling Toolbox (http://nlp.stanford.edu/software/tmt/tmt-0.4/)

## Personality ##
https://indico.io/product

```python
import indicoio

indicoio.config.api_key = '68394629d3fabe1c4f08a0ebcabec43a'

print(indicoio.personality('I finally was able to call your help line and all it took was YOUR HELP LINE putting me back on a list, not me doing anything from my end. Since none of the issues appeared in my spam file it is not likely that that was the problem. In any case, I am now receiving the headline news again. In the future, it would have been helpful to have received directions on"'))
```

Result
```python
{u'openness': 0.5113306794768181, u'extraversion': 0.41991408750162285, u'agreeableness': 0.4928200720695027, u'conscientiousness': 0.5703676003834297}
```

## Visualize Results (Word Cloud) ##
https://github.com/jasondavies/d3-cloud
