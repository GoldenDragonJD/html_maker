import dominate
from dominate.tags import *
import os
import re


class Page:
    def __init__(self, number, path):
        self.number = number
        self.path = path


class Chapter:
    def __init__(self, chapter_name, chapter_path):
        self.chapter_name = chapter_name
        self.chapter_path = chapter_path
        self.pages = []

    def add_page(self, number):
        page_path = f"{self.chapter_path}/{number}"
        page = Page(number, page_path)
        self.pages.append(page)


class Manga:
    def __init__(self, manga_name, manga_path):
        self.manga_name = manga_name
        self.manga_path = manga_path
        self.chapters = []

    def add_chapters(self, chapter_name):
        path = f"Manga-Folder/{self.manga_name}/{chapter_name}"
        chapter = Chapter(chapter_name, path)
        self.chapters.append(chapter)

    def sort_chapters(self):
        def extract_numeric_part(chapter_name):
            match = re.search(r'\d+', chapter_name)
            return int(match.group()) if match else 0

        self.chapters = sorted(self.chapters, key=lambda x: extract_numeric_part(x.chapter_name))

    def reverse_chapter(self):
        list_chapters = self.chapters
        list_chapters.reverse()
        return list_chapters


def sort_chapters(name):
    def extract_numeric_part(chapter_name):
        match = re.search(r'\d+', chapter_name)
        return int(match.group()) if match else 0

    return sorted(name, key=lambda x: extract_numeric_part(x))


def reformat_path(directory):
    file_names = os.listdir(directory)
    get_file_directories = [os.path.join(directory, file) for file in file_names]
    fixed_paths = [path.replace("\\", "/") for path in get_file_directories]

    return fixed_paths


def create_class():
    manga_folder = os.listdir(r"Manga-Folder")

    manga_folder_paths = reformat_path("Manga-Folder")

    for manga_name, manga_folder_path in zip(manga_folder, manga_folder_paths):
        manga = Manga(manga_name, manga_folder_path)

        chapters = sort_chapters(os.listdir(manga_folder_path))

        print(manga_name)

        for index, chapter in enumerate(chapters, start=0):
            manga.add_chapters(chapter)
            manga.sort_chapters()
            print(manga.chapters[index].chapter_path)
            pages = sort_chapters(os.listdir(manga.chapters[index].chapter_path))
            print(chapter)

            for page in pages:
                manga.chapters[index].add_page(page)
                print(page)

            create_page(manga, index, chapters)

        create_chapter(manga)


def create_page(manga_class, chapter_index, all_chapters):
    if not os.path.exists("Html-Folder"):
        os.makedirs("Html-Folder")

    manga = manga_class
    current_chapter = manga.chapters[chapter_index]
    doc = dominate.document(title=f"{manga.manga_name}: {current_chapter.chapter_name}")

    manga_name = manga.manga_name

    fixed_name = str(manga_name).replace('\u2019', "")

    if not os.path.exists(f"Html-Folder/{fixed_name}"):
        os.makedirs(f"Html-Folder/{fixed_name}")

    # Add your stylesheet link
    with doc.head:
        link(rel='stylesheet', href='../../Resources/chapter.css')

    with doc:

        script(src="../../Resources/log.js")

        with div(cls="Header"):
            with div(cls="Header-buttons"):
                with div(cls="bound"):
                    with a(href=f"../../Golden Manga Reader.html"):
                        h2("Home")

        with div(cls="Title"):
            h1(f"{manga.manga_name}: {current_chapter.chapter_name}")
            b("All chapters listed in ", a(manga.manga_name, href="Home.html"))

        with div(cls="Controls"):
            with div(cls="Control-buttons"):

                if chapter_index > 0:
                    with a(href=f"{all_chapters[chapter_index - 1]}.html"):
                        h3("< Prev")
                else:
                    with a(href="Home.html"):
                        h3("Info")

                if chapter_index < len(all_chapters) - 1:
                    with a(href=f"{all_chapters[chapter_index + 1]}.html"):
                        h3("Next >")
                else:
                    with a(href="Home.html"):
                        h3("Info")

        with div(cls="Image-list"):
            with div(cls="Image-container"):
                for image in [page.path for page in current_chapter.pages]:
                    img(src=f'../../{image}')

        with div(cls="Controls"):
            with div(cls="Control-buttons"):

                if chapter_index > 0:
                    with a(href=f"{all_chapters[chapter_index - 1]}.html"):
                        h3("< Prev")
                else:
                    with a(href="Home.html"):
                        h3("Info")

                if chapter_index < len(all_chapters) - 1:
                    with a(href=f"{all_chapters[chapter_index + 1]}.html"):
                        h3("Next >")
                else:
                    with a(href="Home.html"):
                        h3("Info")

    with open(f"Html-Folder/{fixed_name}/{manga.chapters[chapter_index].chapter_name}.html",
              "w") as file:
        file.write(str(doc))


def create_chapter(manga_class):
    manga = manga_class

    manga_name = manga.manga_name.replace('\u2019', "'")

    doc = dominate.document(title=f"{manga_name}")

    with doc.head:
        link(rel='stylesheet', href='../../Resources/manga.css')

    with doc:
        with div(cls="Header"):
            with div(cls="Header-buttons"):
                with div(cls="bound"):
                    with a(href=f"../../Golden Manga Reader.html"):
                        h2("Home")

        with div(cls="Info"):
            h1(manga_name)
            b("Manga details are not implemented yet...")

        with div(cls="Chapter-list"):
            b(f"Chapter list for {manga_name}")

            input_(type="text", id="searchInput", placeholder="Search for Chapter. ex: 30 or 50")

            with div(cls="Chapter-container"):
                with label('Reverse Chapter Order', for_='myCheckbox'):
                    with div(cls="check"):
                        input_(type="checkbox", id="myCheckbox")

                with ul():
                    for chapter in manga.reverse_chapter():
                        with li(id=f"{chapter.chapter_name.split(' ')[-1]}"):
                            with a(href=f"{chapter.chapter_name}.html", id=f"{chapter.chapter_name.split(' ')[-1]}"):
                                h2(chapter.chapter_name)
        
        script(src="../../Resources/chapterSearch.js")
        script(src="../../Resources/checkChapter.js")

    manga_name = manga.manga_name

    fixed_name = str(manga_name).replace('\u2019', "")

    with open(f"Html-Folder/{fixed_name}/Home.html", "w") as file:
        file.write(str(doc))

    
def create_manga():
    doc = dominate.document(title="Golden Manga Reader")

    with doc.head:
        link(rel='stylesheet', href='Resources/lib.css')

    with doc:
        with div(cls="Header"):
            h1("Golden Manga Reader")

        with div(cls="Controls"):
            with div(cls="Sorters"):
                with div(cls="SortersName"):
                    h2("SORTING SETTINGS")
                button("RECENT", onclick="resetOrder()")
                button("ALPHABETICAL", onclick="sortManga()")
                input_(id="searchInput", placeholder="Search Manga...")

        manga_folders = os.listdir("Manga-Folder")
        html_files = sorted(manga_folders, key=lambda manga_folder: os.path.getmtime(os.path.join("Manga-Folder",
                                                                                                  manga_folder)))
        html_files.reverse()

        with div(cls="Manga-container"):
            for order, html_file in enumerate(html_files, start=1):
                    html_file_encoded = str(html_file).replace('\u2019', "")
                    a_text = html_file.replace('\u2019', "'")
                    with a(cls="Manga-display", id=html_file, data_order=str(order), href=f"Html-Folder/{html_file_encoded}/Home.html"):
                        h2(a_text)
                        h3("", id="CurrentChapter")


        script(src="Resources/mangaSearch.js")

    with open(f"Golden Manga Reader.html", "w") as file:
        file.write(str(doc))


input("[Press Enter to Start Program]")
create_class()
create_manga()
