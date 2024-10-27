import requests
import subprocess
from bs4 import BeautifulSoup
import os


def get_package_meta_url(pack_url):
    response = requests.get(pack_url)
    if response.status_code == 200:
        # Парсим HTML-страницу
        soup = BeautifulSoup(response.text, 'html.parser')
        # Находим все ссылки
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and not href.startswith('?') and '.dsc' in href:  # Исключаем ссылки на навигацию
                return pack_url + href
    return None;


def get_dependency_text(description):
    dependencyFlag = 'Build-Depends:'
    alt = 'Build-Depends-Indep:'

    for line in description.splitlines():
        if dependencyFlag in line:
            return line[len(dependencyFlag):].replace(' ', '')
        if alt in line:
            return line[len(alt):].replace(' ', '')
    return None


def trim_package(package):
    for i in range(len(package)):
        if package[i] in '(){}[]>=<.':
            return package[:i]
    return package


def extract_dependencies(dependency_text):
    return dependency_text.split(',')


def get_dependencies(repo, package, dict):
    if package in dict:
        return dict[package]

    url = f'{repo}{package[:4] if 'lib' in package else package[0]}/{package}/'
    # requset exml http://archive.ubuntu.com/ubuntu/ubuntu/pool/universe/n/nanoblogger/
    desc_url = get_package_meta_url(url)
    if desc_url == None:
        return

    print(f'Analyzing {package}')
    response = requests.get(desc_url)
    dependencies = extract_dependencies(get_dependency_text(response.text))
    dict[package] = dependencies
    for dep in dependencies:
        dict[dep] = get_dependencies(repo, trim_package(dep), dict)
    return dependencies


def generate_graph_code(dict):
    arr = '-->'
    res = 'flowchart TD;\n'
    cnt = 0
    ids = {}

    for key in dict.keys():
        if dict[key] is None:
            continue
        if key in ids:
            cur_id = ids[key]
        else:
            cur_id = f'id{cnt}'
            ids[key] = cur_id
            cnt += 1
        for dep in dict[key]:
            if dep in ids:
                dep_id = ids[dep]
            else:
                dep_id = f'id{cnt}'
                ids[dep] = dep_id
                cnt += 1
            res += f'\t{cur_id}["{key}"] --> {dep_id}["{dep}"];\n'
    return res


def main():
    # repo expml http://archive.ubuntu.com/ubuntu/ubuntu/pool/universe/
    # parser = argparse.ArgumentParser(description="Visualize package dependencies.")
    # parser.add_argument('--path', type=str, required=True, help='Path to the mermaid CLI')
    # parser.add_argument('--package', type=str, required=True, help='Package name')
    # parser.add_argument('--repo', type=str, required=True, help='Repository URL')
    # args = parser.parse_args()

    path = r"C:\Users\Policarp\AppData\Roaming\npm\mmdc"
    package = "jabber-muc"
    package = "obsession"
    package = "i2p"
    package = "qatengine"
    package = "ubelt"
    repo = "http://archive.ubuntu.com/ubuntu/ubuntu/pool/universe/"

    print(f'Visualization started with params:\npath: {path}\npackage: {package}\nrepo: {repo}\n')

    dict = {}
    print('Dependencies will only be displayed for packages that have .dcs file in their repo!')
    dependencies = get_dependencies(repo, package, dict)

    print('Dependency tree created. Starting generating graph code')
    graph = generate_graph_code(dict)
    graph_file = open(f'{package}_graph_code.mmd', 'w')
    graph_file.write(graph)
    graph_file.close()
    print(f'Graph code saved in {os.path.abspath(graph_file.name)}')

    output_file = f'{package}_output.svg'
    args = [path, "-i", graph_file.name, "-o", output_file]
    subprocess.run(args, shell=True)

    print(f'Visualization saved in {os.path.abspath(output_file)}')
    subprocess.run([os.path.abspath(output_file)], shell=True)


if __name__ == "__main__":
    main()
