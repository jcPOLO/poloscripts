class Template(object):

    def __init__(self, templates: list) -> None:
        self.templates = templates

    def merge_templates(self, platform: str = '') -> str:
        result = []
        for template in self.templates:
            file = str(template)
            path = f'./templates/{platform}/'
            filename = f'{path}{file}'
            with open(filename, 'r') as f:
                lines = f.read()
            result.append(lines)
        template = '\n'.join(result)
        return template

    def create_final_template(self, platform: str = '') -> None:
        file = 'final.j2'
        path = f'./templates/{platform}/'
        filename = f'{path}{file}'

        with open(filename, 'w') as f:
            f.write(self.merge_templates(platform))
