import xxhash

from kgai_basic_nlp.model.NLPArticle import NLPArticle


def hash_article(article: NLPArticle) -> str:
    """
    creates a unique ID for an article by hashing
    Args:
        article:

    Returns:

    """
    hash_content = article.articleText + article.title + article.url
    return xxhash.xxh64(hash_content).hexdigest()
