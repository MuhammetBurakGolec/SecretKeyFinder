def two_words(keywords="keywords.data"):
    tw0_words = []
    with open(keywords,"r") as f:
        keywords = f.read().splitlines()
        for keyword in keywords:
            for kewords in keywords:
                if keyword != kewords:
                    print(keyword + "_" + kewords)
                    tw0_words.append(keyword + "_" + kewords)
    with open("keywords_gen.data","a") as f:
        for keyword in tw0_words:
            f.write(keyword)
            f.write("\n")

def three_words(keywords="keywords.data"):
    three_words = []
    with open(keywords,"r") as f:
        keywords = f.read().splitlines()
        for keyword in keywords:
            for kewords in keywords:
                for kewords2 in keywords:
                    if keyword != kewords and keyword != kewords2 and kewords != kewords2:
                        print(keyword + "_" + kewords + "_" + kewords2)
                        three_words.append(keyword + "_" + kewords + "_" + kewords2)
    with open("keywords_gen.data","a") as f:
        for keyword in three_words:
            f.write(keyword)
            f.write("\n")

# If you want to generate 2 or 3 words keywords, uncomment the following line
# two_words()
# three_words()