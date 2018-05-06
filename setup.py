from setuptools import setup

setup(name='bifrost',
      version='0.1',
      description='Code in Quero Hackathon project. SlackBot messaging service with embedded social linking clustering',
      url='https://github.com/CarlosMatheus/HackathonQueroEducacao2018',
      author=['Aloysio Galvao', 'Carlos Matheus', 'Felipe Coimbra', 'Luiz Henrique'],
      author_email=['','','felipecoimbra97@gmail.com',''],
      license='MIT',
      packages=['bifrost'],
      install_requires=[
          'numpy',
          'matplotlib',
          'tensorflow'
      ],
      zip_safe=False)
