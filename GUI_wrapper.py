''' GUI wrapper for MangaReaderScraper.'''
import search
import download
import jpg2pdf
import easygui
import sys


def enter_box(msg, title):
    ''' Simple enterbox with exit functionality.'''
    user_text = easygui.enterbox(msg, title)
    if not user_text:
        sys.exit()
    return user_text


def search_window():
    ''' Manga search entry window.'''
    msg = "What manga do you want to search for?"
    title = 'Manga Search'
    search_term = enter_box(msg, title)
    return search_term


def search_results_choicebox(search_term):
    ''' Choicebox with search results which returns manga link.'''
    df = search.query2df(search_term)
    choices = df['Title'].tolist()
    choice = easygui.choicebox('Pick a manga.', 'Search Results', choices)
    if not choice:
        sys.exit()
    link = df[df['Title'] == choice]['Link'].to_string(index=False)
    to_continue = easygui.ccbox("You chose: {}".format(choice))
    if to_continue:
        return link
    else:
        return search_results_choicebox(search_term)


def volume_window():
    ''' Manga volume entry window.'''
    msg = "What volume of the series do you want (enter '0' to download all volumes)?"
    title = "Volume Choice"
    volume = enter_box(msg, title)
    if not volume.isdigit():
        easygui.msgbox('Volume entered must be a digit. {} is not a digit'.format(volume))
        return volume_window()
    else:
        return volume


# Main
search_term = search_window()
link = search_results_choicebox(search_term)
volume = volume_window()
volume = None if volume == '0' else volume

download.download_manga(link, volume)
jpg2pdf.create_manga_pdf(link, volume)
