from setuptools import setup, find_packages

# 从requirements.txt读取依赖
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='CrawlerProject',
    version='0.1',
    packages=find_packages(where='src'),  # 指定源代码所在的目录
    package_dir={'': 'src'},  # 指定源代码的根目录
    install_requires=required,  # 使用requirements.txt中的依赖
    # 如果您有脚本或者命令行工具，也可以在这里指定
    entry_points={
        'console_scripts': [
            # 例如: 'script_name = module:function'
        ],
    },
)
