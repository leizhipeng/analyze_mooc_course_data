import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.stem.porter import *
from stop_words import get_stop_words
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import gensim
from gensim import corpora, models
import codecs


def preprocess_sent(text):
    """
    Get sentence level preprocessed data from raw texts
    :param rw: review to be processed
    :return: sentence level pre-processed review
    """
    # Add missing delimiter: xxxThis is a --> xxx.
    s = re.sub(r'([a-z])([A-Z])', r'\1\. \2', text)  # before lower case
    # Make words all lower case.
    s = s.lower()
    # Remove < and >
    s = re.sub(r'&gt|&lt', ' ', s)
    # Remove letters that repeat more than 2 time.
    s = re.sub(r'([a-z])\1{2,}', r'\1', s)
    # Remove non-word characters that repeat more than 1 time.
    s = re.sub(r'([\W+])\1{1,}', r'\1', s)
    # Use string * as delimiter
    s = re.sub(r'\*|\W\*|\*\W', '. ', s)
    # Remove words in parenthesis, which are assumed less informal
    s = re.sub(r'\(.*?\)', '. ', s)
    # xxx[?!]. -- > xxx.
    s = re.sub(r'\W+?\.', '.', s)
    # [.?!]xxx --> [.?!] xxx
    s = re.sub(r'(\.|\?|!)(\w)', r'\1 \2', s)
    return s.strip()


# define stemmer
p_stemmer = PorterStemmer()
# create stop words list
stop_words = (list(
    set(get_stop_words('en'))
    | set(get_stop_words('es'))
    | set(get_stop_words('de'))
    | set(get_stop_words('it'))
    | set(get_stop_words('ca'))
    | set(get_stop_words('pt'))
    | set(get_stop_words('pl'))
    | set(get_stop_words('da'))
    | set(get_stop_words('ru'))
    | set(get_stop_words('sv'))
    | set(get_stop_words('sk'))
    | set(get_stop_words('nl'))
    | set(["course", "data"])
))


def preprocess_word(s):
    """
    Get word level preprocessed data from preprocessed sentences
    including: remove punctuation, select noun, stem, stop_words
    :param s: sentence to be processed
    :return: word level pre-processed documents
    """
    if not s:
        return []
    w_list = word_tokenize(s)
    w_list = [word for word in w_list if word.isalpha()]
    w_list = [word for (word, pos) in nltk.pos_tag(w_list) if pos[:2] == 'NN']
    w_list = [word for word in w_list if word not in stop_words]
    w_list = [p_stemmer.stem(word) for word in w_list]

    return w_list


def word_cloud(token_lists):
    """
    Plot word cloud
    :param token_lists: Token list.
    """
    unique_string = " ".join([" ".join(tl) for tl in token_lists])
    wordcloud = WordCloud(width=1000, height=500, background_color='white').generate(unique_string)
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("word_cloud" + ".png", bbox_inches='tight')
    plt.show()
    plt.close()


def lda_topic_model(token_lists, ntopic, output):
    """
    Perform LDA topic modeling using Gensim package.
    :param token_lists: A list of word lists for texts, in which a text is represented as a list of processed words.
    :param output: output name for saving model and results.
    :param ntopic: number of topics.
    :return model: trained lda model.
    """
    # create dictionary from token lists.
    dictionary = corpora.Dictionary(token_lists)
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in token_lists]
    model = gensim.models.ldamodel.LdaModel(corpus, num_topics=ntopic, random_state=66, id2word=dictionary, passes=20)
    for topic in model.print_topics(num_topics=10):
        print(topic)
    model.save(output)
    return model, corpus, dictionary


def dominant_topic(ldamodel, corp, texts, saved_file_name):
    """
    Determine the dominant topic and its percentage contribution in each documents.
    :param ldamodel: LDA model.
    :param corp: corpus.
    :param texts: Documents.
    :param saved_file_name: The file name for saving the dataframe.
    :return: A dataframe having the dominant topic, topic percentage contribution, keywords, and Abstract.
    """
    topic_df = pd.DataFrame()
    for i, row_list in enumerate(ldamodel[corp]):
        row = row_list[0] if ldamodel.per_word_topics else row_list
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        if row:
            topic_num, prop_topic = row[0]
            topic_keywords = ", ".join([word for word, prop in ldamodel.show_topic(topic_num)])
            topic_df = topic_df.append(pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]),
                                       ignore_index=True)
        else:
            topic_df = topic_df.append(pd.Series([10000, round(0.0, 4), ""]), ignore_index=True)
    topic_df.index = texts.index
    topic_df = pd.concat([topic_df, texts], axis=1)
    topic_df.columns = ['Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Abstract']
    topic_df.to_csv(saved_file_name)
    return topic_df


def show_topic(topic_df, lda_model, topic_num, first_n_abstract):
    """
    Show a topic using representative abstracts.
    :param text_topic_df: a dateframe with topic percentage contribution of each abstract.
    :param topic_num: the topic number.
    :param first_n_abstract: the number of the abstract to be shown.
    """
    topic_group = topic_df[topic_df["Dominant_Topic"] == topic_num]
    topic_group = topic_group.sort_values(['Topic_Perc_Contrib'], ascending=False)
    print("Show topic, No. ", topic_num)
    cloud = WordCloud(
        background_color='white',
        width=2500,
        height=1500,
        colormap='tab10',
        prefer_horizontal=1.0
    )
    cloud.generate_from_frequencies(dict(lda_model.show_topic(topic_num, topn=30)), max_font_size=300)
    plt.figure(figsize=(8, 5.6), facecolor=None)
    plt.imshow(cloud, interpolation='bilinear')
    plt.title('Topic ' + str(topic_num), fontdict=dict(size=16))
    plt.axis("off")
    plt.show()
    print("Keywords", topic_group["Keywords"].iloc[0])
    for i in range(first_n_abstract):
        print(topic_group["Abstract"].iloc[i])
        print(topic_group['Topic_Perc_Contrib'].iloc[i])


