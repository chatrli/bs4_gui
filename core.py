from bs4 import BeautifulSoup as bs
import requests


def scrap_with_filter(url, selected_filter, selected_option):
    req = requests.get(url)
    match selected_filter:
        case 'find_all':
            soup = bs(req.content, 'html.parser').find_all(f'{selected_option}')
        case 'find':
            soup = bs(req.content, 'html.parser').find(f'{selected_option}')
        case 'find_parents':
            soup = bs(req.content, 'html.parser').find_parents(f'{selected_option}')
        case 'find_parent':
            soup = bs(req.content, 'html.parser').find_parent(f'{selected_option}')
        case 'find_previous_siblings':
            soup = bs(req.content, 'html.parser').find_previous_siblings(f'{selected_option}')
        case 'find_next_siblings':
            soup = bs(req.content, 'html.parser').find_next_siblings(f'{selected_option}')
        case 'find_previous_sibling':
            soup = bs(req.content, 'html.parser').find_previous_sibling(f'{selected_option}')
        case 'find_next_sibling':
            soup = bs(req.content, 'html.parser').find_next_sibling(f'{selected_option}')
        case 'find_all_next':
            soup = bs(req.content, 'html.parser').find_all_next(f'{selected_option}')
        case 'find_all_previous':
            soup = bs(req.content, 'html.parser').find_all_previous(f'{selected_option}')
        case 'find_all_next':
            soup = bs(req.content, 'html.parser').find_all_next(f'{selected_option}')
    return str(soup)


def scrap_with_css(url, selected_option, css_selector):
    req = requests.get(url)
    match selected_option:
        case 'id':
            soup = bs(req.content, 'html.parser').select(f'#{css_selector}')
        case 'class':
            soup = bs(req.content, 'html.parser').select(f'.{css_selector}')
    return str(soup)

