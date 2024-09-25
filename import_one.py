# configuration for pywikibot
import sys

import pywikibot

# connect to the wikibase
wikibase = pywikibot.Site("en", "sparqulb")
wikibase_repo = wikibase.data_repository()
wikibase_repo.login()

# connect to wikidata
wikidata = pywikibot.Site("wikidata", "wikidata")
wikidata_repo = wikidata.data_repository()

from util.util import WikibaseImporter

wikibase_importer = WikibaseImporter(wikibase_repo, wikidata_repo)

# import a single item or property
arg = sys.argv[1]
print(f"Importing {arg} from Wikidata...")
if arg.startswith("Q"):
    wikidata_item = pywikibot.ItemPage(wikidata_repo, arg)
    wikidata_item.get()
    wikibase_importer.change_item(wikidata_item, wikibase_repo, True)
elif arg.startswith("P"):
    wikidata_property = pywikibot.PropertyPage(wikidata_repo, arg)
    wikidata_property.get()
    wikibase_importer.change_property(wikidata_property, wikibase_repo, True)
