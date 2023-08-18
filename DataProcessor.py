import pandas as pd
import string
import phik
import gensim
from gensim import corpora
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import datetime as dt

df = pd.read_csv('articles_all.csv')


def rough_data_prep(article):
    
        chars_to_remove = string.punctuation + '«»'  
        
        article = article.translate(str.maketrans('', '', chars_to_remove))  #maybe outsource this part as "rought cleaning"
        article = article.lower()   
        words = pd.Series(article.split())
        words = words.str.replace(r'\s', '')  

        return words

def confirmatory_analysis(df): #go through all articles, and code them as 1 and 0 variables for: ua, nato and "ua and nato"

    df = df.assign(ua=0, nato=0, country_nato=0)    #adds three bulean collums to the data frame, one for ua, nato and both, default is False

    ua_set = ("Украин", "Киев", "Донбас", "Донецк", "дончан", "Луганск", "луганчан", "ДНР", "ЛНР", "Харьков", "Мариупол", "Херсон", "Запорож", "Одес", "Крым", "Севастоп", "Керч", "СВО", "спецоперац") 
    nato_set = ("НАТО", "Атлант", "Запад", "ЕС", "Евросоюз", "США", "Америк", "Обам", "Байден" ) 
    ua_set = set(x.lower() for x in ua_set)
    nato_set = set(x.lower() for x in nato_set)
    index = 0

    for article in df["text"]: #break down text and search them for dictionary words
        
        words = rough_data_prep(article)

        if any(element in ua_set for element in list(words)):
            df.ua[index] = 1

        if any(element in nato_set for element in list(words)):
            df.nato[index] = 1

        if df.ua[index] == 1 and df.nato[index] == 1:
            df.country_nato[index] = 1

        index += 1

    #phi correlate the two binary variables to anser H1
    corr_data = pd.DataFrame()
    corr_data =  corr_data.assign(ua= df["ua"],nato= df["nato"])
    phi_corr = corr_data.phik_matrix()
    print(phi_corr) # = 0.339966 - for rought data

    print(df)

    #display frequency of ua & nato per month to asses H2
    
    df['date'] = pd.to_datetime(df["date"])
    df['month'] = df['date'].dt.to_period('M')
    df['week'] = df['date'].dt.week
    

    monthly_data = df.groupby('month')['country_nato'].count()
    monthly_data.index = monthly_data.index.to_timestamp()
    # Plot the monthly data
    plt.plot(monthly_data.index, monthly_data.values)
    plt.xlabel('Month')
    plt.ylabel('Occurrences of country_nato')
    plt.title('Occurrences of country_nato by Month')
    plt.show()

    

    weekly_data = df.groupby('week')['country_nato'].count()
    weekly_data.index = pd.to_datetime(weekly_data.index, unit='W')
    # Plot the weekly data
    plt.plot(weekly_data.index, weekly_data.values)
    plt.xlabel('Week')
    plt.ylabel('Occurrences of country_nato')
    plt.title('Occurrences of country_nato by Week')
    #plt.show() #this seams kinda borken, look at graph

    #x_values = df['month'].astype(str)
    #y_values = df['country_nato'] # need to sort this into occurances per month or week
    #figure(figsize=(20, 20), dpi=300)
    #fig = plt.figure()
    #ax = plt.axes()
    #ax.set_facecolor('#F5F5F5')
    #plt.plot(x_values, df['country_nato'], label = "Ukraine texts ratio", linestyle=":", color='#505050')
    #plt.plot(x_values, df['cleaned_GPW_counts']/y_values, label = "GPW texts ratio", color='#808080', linestyle="solid")
    #plt.plot(x_values, df['all_counts']/y_values, label = "GPW and Ukraine texts ratio", linestyle="--", color='#101010')
    #ticks = list(df['month'].astype(str))
    #plt.xticks([ticks[i] for i in range(len(ticks)) if i % 5 == 0], rotation=45)
    #ax.legend()
    #plt.title('Number of texts per topic to total number of texts \n for each month from 2014-01 to 2022-10')
    #plt.xlabel('Date')
    #plt.ylabel("Number of texts per topic to total number")
    #plt.show()
    # save to png
    fig.savefig('png_new_graph.png', dpi=300)
    return df



def thorough_date_prep(df): #identify all posible expressions before and after the text body and regex them away
    

    return df

def explorative_analysis(df): #factor ananlisi? topic modeling? run of the mill corpus linguisitcs? best to first finish the methods and leave this open for now. also consult allie and flek
    
    for article in df["text"]: #break down text and search them for dictionary words
        
        words = rough_data_prep(article)
        #words = remove_stopwords() #still need to implment for decent results
        dictonary = corpora.Dictionary(words) 
        #corpus = [dictonary.doc2bow(word) for ] ####ok idk how this contiues fuck it, look at this later

    
    
    return df
    '''
    if topic modeling ty this. should work for russian and cirlic :
        import gensim
    from gensim import corpora

    # Create a corpus from a list of texts
    documents = ["This is a document about sports.", "This is another document about politics.", "This is yet another document about science."]
    texts = [[text for text in doc.split()] for doc in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Train the LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=3)

    # Print the topics
    for idx, topic in lda_model.print_topics(-1):
        print('Topic: {} \nWords: {}'.format(idx, topic))'''
    

df = confirmatory_analysis(df)


#print(df.ua.to_string())#, , df.ua_nato.to_string()     df.nato.to_string()
#print(df)