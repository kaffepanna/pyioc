import importlib
import yaml


class UnknownInstanceException(Exception):
    pass


class Kernel():
    def __init__(self, *args, **kwargs):
        self.singletons = {}
        self.mappings = {}
        pass

    def add(self, *args, **kwargs):
        if isinstance(kwargs.get('klass'), str):
            module_name = '.'.join(kwargs.get('klass').split('.')[0:-1])
            module = importlib.import_module(module_name)
            klass_name = kwargs.get('klass').split('.')[-1]
            klass = getattr(module, klass_name)
        else:
            klass = kwargs.get('klass')

        mapping = kwargs.copy()
        mapping['klass'] = klass
        self.mappings[mapping['name']] = mapping

    def get_instance(self, name, *args, **kwargs):
        if name not in self.mappings:
            raise UnknownInstanceException()

        mapping = self.mappings[name]

        if mapping.get('singleton') is True and \
                name in self.singletons:
            return self.singletons[name]

        instance = mapping['klass'](*args, **kwargs)

        if 'attributes' in mapping:
            for attr in mapping['attributes']:
                if 'instance' in attr:
                    val = self.get_instance(attr['instance'])
                else:
                    val = attr['value']
                setattr(instance, attr['name'], val)

        if mapping.get('singleton'):
            self.singletons[name] = instance

        return instance


def load(path):
    with open(path, 'r') as stream:
        kernel = Kernel()
        conf = yaml.load(stream)
        for mapping in conf:
            kernel.add(**mapping)
    return kernel
