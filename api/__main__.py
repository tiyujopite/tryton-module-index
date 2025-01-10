#  _____           _
# |_   _| __ _   _| |_ ___  _ __
#   | || '__| | | | __/ _ \| '_ \
#   | || |  | |_| | || (_) | | | |
#   |_||_|   \__, |\__\___/|_| |_|
#            |___/
#  __  __           _       _           ___           _
# |  \/  | ___   __| |_   _| | ___     |_ _|_ __   __| | _____  __
# | |\/| |/ _ \ / _` | | | | |/ _ \     | || '_ \ / _` |/ _ \ \/ /
# | |  | | (_) | (_| | |_| | |  __/     | || | | | (_| |  __/>  <
# |_|  |_|\___/ \__,_|\__,_|_|\___|    |___|_| |_|\__,_|\___/_/\_\
#
import json
import os
import sys
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlparse

import requests

ROOT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'src', 'assets')
MODULES_LOCK_FILE = os.path.join(ROOT_DIR, 'modules-lock.json')
TYPING_ERROR = '%s must be lowercase and without spaces'
TYPING_ERROR_DETAIL = TYPING_ERROR + ': %s'
VCS_TYPES = ['gitlab', 'github']
CURRENT_VERSION = '7.4'
FORBIDDEN_NAMES = [
    'tryton',
    'trytond',
    'sao',
    'proteus',
]


def error(message, start='\n', exit_=True):
    print(f'{start}\033[1;31m{message}\033[0m')
    if exit_:
        exit(1)


def inline_error(message, exit_=True):
    error(message, start='', exit_=exit_)


def success(message):
    print(f'\033[1;32m{message}\033[0m')


def bold(message):
    return f'\033[1m{message}\033[0m'


def get_serie_branch(branch, known_series):
    if branch.startswith('branch/'):
        branch = branch.split('/')[1]
    if branch not in known_series:
        return None
    return branch


def get_ISO_date(date_str):
    return str(datetime.strptime(date_str[:10], '%Y-%m-%d').date())


def read_file(name, key=None):
    with open(os.path.join(ROOT_DIR, f'{name}.json'), 'r') as f:
        return json.load(f)[key or name]


def write_modules(modules, module_key_list=None):
    if os.path.exists(MODULES_LOCK_FILE):
        modules_lock = read_file('modules-lock', key='modules')
    else:
        modules_lock = {}
    key2module = {module.pop('key'): module for module in modules}
    today = str(datetime.now().date())

    for key_, module in key2module.items():
        if module_key_list and key_ not in module_key_list:
            continue
        if key_ in modules_lock:
            modules_lock[key_].update(module)
        else:
            module['added_at'] = today
            modules_lock[key_] = module
        modules_lock[key_]['info_updated_at'] = today

        # Sort the dict by keys
        modules_lock[key_] = OrderedDict(
            sorted(modules_lock[key_].items()),
            key=lambda x: x[0])
        modules_lock[key_].pop('key', None)

    # Sort the dict by keys
    modules_lock = OrderedDict(
        sorted(modules_lock.items()),
        key=lambda x: x[0])
    modules_lock.pop('key', None)

    with open(MODULES_LOCK_FILE, 'w') as file:
        json.dump({'modules': modules_lock}, file, indent=2)


def build_module(module):
    print(f"Building {bold(module['key'])}... ", end='')

    url = module['url']
    vcs_types = read_file('vcs_types')
    known_series = read_file('series')
    url_parsed = urlparse(url)
    netloc = url_parsed.netloc
    scheme = url_parsed.scheme
    path = url_parsed.path[1:]
    vcs_type = vcs_types.get(netloc)

    # Ensure required fields.
    module['series'] = []
    module['stars'] = 0
    module['forks'] = 0
    module.setdefault('tags', [])
    module['pypi_available'] = False
    module['license'] = 'N/A'
    module.setdefault('doc_url', '')

    if vcs_type == 'gitlab':
        # Main data
        safe_path = path.replace('/', '%2F')
        api_url = f'{scheme}://{netloc}/api/v4/projects/{safe_path}'
        response = requests.get(f'{api_url}?license=true')
        response.raise_for_status()
        data = response.json()
        module['stars'] = data['star_count']
        module['forks'] = data['forks_count']
        module['created_at'] = get_ISO_date(data['created_at'])
        module['updated_at'] = get_ISO_date(data['last_activity_at'])
        if data['license']:
            module['license'] = data['license']['key']

        # Check if is tryton module.
        default_branch = data['default_branch']
        response = requests.get(
            f'{api_url}/repository/files/tryton.cfg?ref={default_branch}')
        response.raise_for_status()

        # Branches data
        branches_url = f'{api_url}/repository/branches'
        response = requests.get(branches_url)
        response.raise_for_status()
        branches = response.json()
        for branch in branches:
            serie = get_serie_branch(branch['name'], known_series)
            if serie is not None:
                module['series'].append(serie)

    elif vcs_type == 'github':
        headers = {}
        if os.environ.get('GH_TOKEN'):
            headers = {
                'Authorization': f'Bearer {os.environ.get('GH_TOKEN')}',
                }
        # Main data
        api_url = f'{scheme}://api.{netloc}/repos/{path}'
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        module['stars'] = data['stargazers_count']
        module['forks'] = data['forks_count']
        module['created_at'] = get_ISO_date(data['created_at'])
        module['updated_at'] = get_ISO_date(data['updated_at'])
        if data['license']:
            module['license'] = data['license']['key']

        # Check if is tryton module.
        default_branch = data['default_branch']
        response = requests.get(
            f'{api_url}/contents/tryton.cfg?ref={default_branch}',
            headers=headers)
        response.raise_for_status()

        # Branches data
        branches_url = f'{api_url}/branches'
        response = requests.get(branches_url, headers=headers)
        response.raise_for_status()
        branches = response.json()
        for branch in branches:
            serie = get_serie_branch(branch['name'], known_series)
            if serie is not None:
                module['series'].append(serie)

    # Check pypi
    package_name = module['package_name']
    try:
        response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
        response.raise_for_status()
        module['pypi_available'] = True
    except requests.HTTPError:
        pass

    if not module['series']:
        module['series'].append('N/A')

    success("OK")


def load_modules(module_key_list=None, chunk=None, chunk_size=None,
                 build=False):
    authors = read_file('authors')
    tags = read_file('tags')
    vcs_types = read_file('vcs_types')
    modules = read_file('modules')

    # Load forbidden names
    request = requests.get(
        f'https://downloads.tryton.org/{CURRENT_VERSION}/modules.txt')
    request.raise_for_status()
    forbidden_names = set(request.text.splitlines())
    forbidden_names |= set(FORBIDDEN_NAMES)

    # Check authors
    print(f"Checking {bold('authors')}... ", end='')
    for author in authors:
        if author.lower().replace(' ', '') != author:
            error(TYPING_ERROR_DETAIL % ('Author', author))
    if len(set(authors)) != len(authors):
        error(f"Duplicate author: {author}")
    if authors != sorted(authors):
        error("Authors must be sorted")
    success("OK")

    # Check tags
    print(f"Checking {bold('tags')}... ", end='')
    for tag in tags:
        if tag.lower().replace(' ', '') != tag:
            error(TYPING_ERROR_DETAIL % ('Tag', tag))
    if len(set(tags)) != len(tags):
        error(f"Duplicate tag: {tag}")
    if tags != sorted(tags):
        error("Tags must be sorted")
    success("OK")

    # Check vcs_types
    print(f"Checking {bold('vcs_types')}... ", end='')
    for netloc, vcs_type in vcs_types.items():
        if netloc.lower().replace(' ', '') != netloc:
            error(TYPING_ERROR_DETAIL % ('VCS type', netloc))
        if vcs_type.lower().replace(' ', '') != vcs_type:
            error(TYPING_ERROR % ('VCS type', vcs_type))
        if len(set(vcs_types)) != len(vcs_types):
            error(f"Duplicate VCS type: {netloc}")
        if vcs_type not in VCS_TYPES:
            error(f"Invalid VCS type: {vcs_type}")
    success("OK")

    print(bold('-' * 40))
    # Check modules consistency
    module_keys = []
    res_modules = []
    for module in modules:
        print(f"Checking {bold(module['key'])}... ", end='')

        # Required fields
        if 'key' not in module:
            inline_error("'key' not found")
        if 'url' not in module:
            inline_error("'url' not found")
        if 'package_name' not in module:
            inline_error("'package_name' not found")

        # Check order
        required = ['key', 'package_name', 'url']
        if 'doc_url' in module:
            required.append('doc_url')
        if 'tags' in module:
            required.append('tags')
        if list(module.keys()) != required:
            inline_error("Invalid module keys order")

        key = module['key']
        author, name = key.split('/')
        module_tags = module.get('tags', [])
        url = module['url']

        # Forbidden names
        if name in forbidden_names:
            inline_error(
                "You can not use a name already used by Tryton project")

        # Author
        if author.lower().replace(' ', '') != author:
            inline_error(TYPING_ERROR % 'Author')
        if author not in authors:
            inline_error("Author not found")
        module['author'] = author

        # Name
        if name.lower().replace(' ', '') != name:
            inline_error(TYPING_ERROR % 'Name')
        module['name'] = name

        # Key
        if key in module_keys:
            inline_error("Duplicate module key")
        module_keys.append(key)

        # Tag
        for tag in module_tags:
            if tag.lower().replace(' ', '') != tag:
                inline_error(TYPING_ERROR_DETAIL % ('Tag', tag))
            if tag not in tags:
                inline_error(f"Tag not found: {tag}")
        if len(set(module_tags)) != len(module_tags):
            inline_error("Duplicate tag")
        if module_tags != sorted(module_tags):
            inline_error("Tags must be sorted")

        # Url
        if not url:
            inline_error(f"URL not found: {key}")
        if not url.lower().startswith('https://'):
            inline_error(f"URL must start with 'https://': {key}")
        if url.lower().startswith('https://www.'):
            inline_error(f"URL can not contain 'www.': {key}")
        if url.lower().endswith('.git'):
            inline_error(f"URL can not end with '.git': {key}")
        url_parsed = urlparse(url)
        netloc = url_parsed.netloc
        if netloc not in vcs_types.keys():
            inline_error(f"Missing {netloc} in vcs_types.json: {key}")

        res_modules.append(module)
        success("OK")

    print(bold('-' * 40))
    # Check module list
    for key in module_key_list or []:
        if key not in module_keys:
            error(f"Module not found {bold(key)}")

    # Check chunk and chunk size
    if chunk is not None and type(chunk) is not int:
        chunk = int(chunk)
    if chunk_size is None:
        chunk_size = 50
    if chunk and (len(module_keys) + chunk_size < chunk_size * chunk):
        error("Invalid chunk")
    if chunk is not None:
        from_ = chunk_size * chunk
        to_ = chunk_size * (chunk + 1)
        module_key_list = module_keys[from_:to_]

    for module in res_modules.copy():
        if module_key_list and module['key'] not in module_key_list:
            continue
        try:
            build_module(module)
        except requests.HTTPError:
            if build:
                res_modules.remove(module)
                inline_error("Could not fetch module data", exit_=False)
            else:
                inline_error("Could not fetch module data")

    return res_modules


def build(module_key_list=None, chunk=None, chunk_size=None):
    modules = load_modules(
        module_key_list=module_key_list,
        chunk=chunk,
        chunk_size=chunk_size,
        build=True,
        )
    write_modules(modules, module_key_list=module_key_list)
    print(bold('-' * 40))
    success("-- Build completed --")


def check(module_key_list=None):
    load_modules(module_key_list=module_key_list)
    print(bold('-' * 40))
    success("-- Check completed --")


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command == 'build':
        build(module_key_list=sys.argv[2:])
    elif command == 'check':
        check(module_key_list=sys.argv[2:])
    elif command == 'build_chunk':
        build(
            chunk=sys.argv[2],
            chunk_size=len(sys.argv) > 3 and int(sys.argv[3]) or None
            )
    else:
        error("Invalid command")
