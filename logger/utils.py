
def get_explorer_shortname(explorer_url):
    if "test" in explorer_url:
        return "test"
    elif "dev" in explorer_url:
        return "dev"
    else:
        return "main"
