languages = {
    'English': 'EN',
    'French': 'FR',
    'German': 'DE',
    'Polish': 'PL',
    'Ukrainian': 'UA',
    'Italian': 'IT',
    'Turkish': 'TR',
    'Spanish': 'ES',
    'LatinSpanish': 'LAS',
    'Portuguese': 'PT',
    'BrazilianPortuguese': 'PT-BR',
    'Chinese': 'ZH-HANS',
    'ChineseTraditional': 'ZH-HANT',
    'Russian': 'RU'
}


sorted_languages = dict(sorted(languages.items(), key=lambda x: (x[0] != 'English', x[1])))
languages = sorted_languages


# Future localization support
UI_TRANSLATIONS = {
    'EN': {
        'title': "Dice Mod Helper - Support me on Ko-Fi | SeanConnerX0 - {}",
        'section_handles': "Handles and Folder Name(s)",
        'folder_name': "Folder Name:",
        'generate': "Generate",
        'in_game_info': "In-Game Information",
        'name': "Name:",
        'description': "Description:",
        'mod_uuid': "Mod UUID:",
        'meta_info': "Meta Information",
        'author': "Author:",
        'mod_name': "Mod Name:",
        'mod_description': "Mod Description:",
        'output': "Output",
        'output_directory': "Output Directory:",
        'browse': "Browse",
        'build': "Build",
        'open_output_dir': "Open Output Directory",
        'open_localization_dir': "Open Localization Directory",
        'convert_xml_loca': "Convert XML to .loca",
        'open_dds_dir': "Open .DDS Directory",
    },
    'FR': {

    },
    'DE': {

    },
    'PL': {

    },
    'UK': {

    },
    'IT': {

    },
    'TR': {

    },
    'PT': {

    },
    'ZH': {

    },
    'RU': {

    }
}