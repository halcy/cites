import argparse
import os

from biblib import bib
from biblib import algo

from jinja2 import Environment, FileSystemLoader

URL_BASE = "https://halcy.de/cites"
MY_NAME = "Lorenz Diener"
TEMPLATE_DIR = "templates"
BIB_FILE = "bibliography.bib"

def main():
    arg_parser = argparse.ArgumentParser(description='Parse .bib database(s) and generate a nice HTML page from them.')
    arg_parser.add_argument('--myname', help='Your name as it appears in the .bib file', default=MY_NAME)
    arg_parser.add_argument('--urlbase', help='Base URL for the generated HTML pages', default=URL_BASE)
    arg_parser.add_argument('--template', help='Directory containing the Jinja2 templates', default=TEMPLATE_DIR)
    arg_parser.add_argument('--bibfile', nargs='+', help='.bib file(s) to process', default=[BIB_FILE])
    args = arg_parser.parse_args()

    # Ensure URL base ends with a /
    if not args.urlbase.endswith("/"):
        args.urlbase += "/"

    # Go through bib files, open them all
    bibfiles = []
    for bibfile in args.bibfile:
        bibfiles.append(open(bibfile, 'r'))

    # Parse out domain from URL base, for same origin policy
    domain = args.urlbase.split("//")[1].split("/")[0]

    environment = Environment(loader=FileSystemLoader(args.template + "/"))
    list_template = environment.get_template("list.htm")
    entry_template = environment.get_template("entry.htm")

    # Load bibtex
    db = bib.Parser().parse(bibfiles).get_entries()

    # Prettyprint some fields so that the jinja template is simpler
    bibitems = []
    for ent_key in db:
        ent = db[ent_key]
        
        # Prettyprint fields
        title = algo.tex_to_unicode(ent["title"])
        abstract = algo.tex_to_unicode(ent["abstract"])
        date = ent["month"] + " " + ent["year"]
        key = ent.key
        authors = [algo.tex_to_unicode(author.pretty(), pos=ent.field_pos['author']) for author in ent.authors()]
        entry_type = ent.typ
        doi = ent.get("doi")
        isbn = ent.get("isbn")
        video = ent.get("video")
        supplementary = ent.get("supplementary")
        code = ent.get("code")
        note = ent.get("note")

        # Add URL and poster URL
        if os.path.exists(f"pdf/{key}.pdf"):
            ent["url"] = f"{args.urlbase}/pdf/{key}.pdf"
        if os.path.exists(f"pdf/{key}_poster.pdf"):
            ent["poster"] = f"{args.urlbase}/pdf/{key}_poster.pdf"

        # Generate source
        bib_source = ent.to_bib(wrap_width=100)

        # Generate how-published field
        how_published = None
        if entry_type == "bachelorsthesis":
            how_published = "Bachelors Thesis"
        elif entry_type == "mastersthesis":
            how_published = "Masters Thesis"
        elif entry_type == "phdthesis":
            how_published = "PhD Thesis"
        elif entry_type == "article":
            how_published = "in <span class=\"bibbooktitle\">" + algo.tex_to_unicode(ent["journal"]) + "</span>, volume " + ent["volume"]
            if "number" in ent:
                how_published += ", number " + ent["number"]
            how_published += ", pages " + algo.tex_to_unicode(ent["pages"])
        elif entry_type == "inproceedings":
            how_published = "at " + algo.tex_to_unicode(ent["booktitle"])
        elif entry_type == "incollection":
            how_published = "chapter of <span class=\"bibbooktitle\">\"" + ent["booktitle"] + "\"</span>, pages " + ent["pages"]

        # Check if first author
        primary = False
        if authors[0] == args.myname:
            primary = True
        
        # Add hilite
        authors_raw = authors[:]
        for idx, author in enumerate(authors):
            if author == args.myname:
                authors[idx] = "<span class=\"authorme\">" + author + "</span>"
        if not note is None:
            note = note.replace(args.myname, "<span class=\"authorme\">" + args.myname + "</span>")

        # Param dict
        params = {
            "primary": primary,
            "entry_type": entry_type,
            "key": key,
            "title": title,
            "abstract": abstract,
            "date": date,
            "authors": authors,
            "bib_source": bib_source,
            "doi": doi,
            "isbn": isbn,
            "video": video,
            "supplementary": supplementary,
            "code": code,
            "url": ent.get("url"),
            "poster": ent.get("poster"),
            "how_published": how_published,
            "authors_raw": authors_raw,
            "note": note,
            "urlbase": args.urlbase,
            "domain": domain
        }
        bibitems.append(params)
        
        with open("papers/{}.htm".format(key), 'w') as f:
            f.write(entry_template.render(**params))

    with open("index.htm", 'w') as f:
        f.write(list_template.render(bibitems = bibitems))

    # Close all bib files
    for bibfile in bibfiles:
        bibfile.close()

if __name__ == '__main__':
    main()
