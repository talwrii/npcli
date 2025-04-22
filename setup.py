import setuptools

from setuptools.command.test import test as TestCommand


class ToxTest(TestCommand):
    user_options = []

    def initialize_options(self):
        TestCommand.initialize_options(self)

    def run_tests(self):
        import tox
        tox.cmdline()


setuptools.setup(
    name='npcli',
    version="1.0.0",
    author='@readwithai',
    author_email='talwrii@gmail.com',
    description='',
    license='MIT',
    keywords='',
    url='',
    install_requires=['numpy'],
    packages=[],
    entry_points={
        'console_scripts': ['npcli=npcli.npcli:main']
    },
    classifiers=[
    ],
    cmdclass = {'test': ToxTest},
)
