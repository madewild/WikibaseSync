"""
This family file was auto-generated by generate_family_file.py script.

Configuration parameters:
  url = https://wikidata.org
  name = wikidata

Please do not commit this to the Git repository!
"""
from pywikibot import family


class Family(family.DefaultWikibaseFamily):  # noqa: D101

    name = 'wikidata'
    langs = {
        'wikidata': 'www.wikidata.org',
    }

    def scriptpath(self, code):
        return {
            'wikidata': '/w',
        }[code]

    def protocol(self, code):
        return {
            'wikidata': 'https',
        }[code]
