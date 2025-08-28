def edit(text, max_words=1200):
    w = text.split()
    return (" ".join(w[:max_words])+"...") if len(w)>max_words else text
