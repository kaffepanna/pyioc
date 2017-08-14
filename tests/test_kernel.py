import os
import unittest
import pyioc as ioc


current_dir = os.path.dirname(os.path.realpath(__file__))


class Service(object):
    pass


class Entity(object):
    service = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class TestKernel(unittest.TestCase):
    def test_kernel_undefined(self):
        kernel = ioc.Kernel()
        with self.assertRaises(ioc.UnknownInstanceException):
            kernel.get_instance('dummy')

    def test_kernel_add_simple(self):
        kernel = ioc.Kernel()
        kernel.add(name='entity', klass='tests.test_kernel.Entity')

        e = kernel.get_instance('entity')
        self.assertIsInstance(e, Entity)

    def test_kernel_direct_reference(self):
        kernel = ioc.Kernel()

        kernel.add(name='entity', klass=Entity)

        i = kernel.get_instance('entity')
        self.assertIsInstance(i, Entity)

    def test_kernel_add_instance_attributes(self):
        kernel = ioc.Kernel()

        kernel.add(name='service', klass='tests.test_kernel.Service')
        kernel.add(name='entity', klass='tests.test_kernel.Entity',
                   attributes=[{'name': 'service', 'instance': 'service'}])

        i = kernel.get_instance('entity')
        self.assertIsInstance(i.service, Service)

    def test_kernel_add_instance_value(self):
        kernel = ioc.Kernel()

        kernel.add(name='entity', klass=Entity,
                   attributes=[{'name': 'service', 'value': kernel}])

        i = kernel.get_instance('entity')

        self.assertEqual(i.service, kernel)

    def test_kernel_get_with_args(self):
        args = (1, 2, 3)
        kwargs = {'one': 1, 'two': 2}

        kernel = ioc.Kernel()
        kernel.add(name='entity', klass='tests.test_kernel.Entity')

        i = kernel.get_instance('entity', *args, **kwargs)

        self.assertEqual(i.args, args)
        self.assertEqual(i.kwargs, kwargs)

    def test_kernel_add_singleton(self):
        kernel = ioc.Kernel()
        kernel.add(name='entity', klass='tests.test_kernel.Entity',
                   singleton=True)

        i1 = kernel.get_instance('entity')
        i2 = kernel.get_instance('entity')

        self.assertEqual(i1, i2)

    def test_load(self):
        kernel = ioc.load(os.path.join(current_dir, 'fixtures',
                                       'simple.yaml'))

        i = kernel.get_instance('entity')
        self.assertIsInstance(kernel, ioc.Kernel)
        self.assertIsInstance(i, Entity)
