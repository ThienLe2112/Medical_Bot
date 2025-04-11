from setuptools import setup

package_name = 'arm_bot'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ThienLC',
    maintainer_email='helu@helu.helu',
    description='TODO: Implement Surgical Robot',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = arm_bot.my_node:main',
            'keyboard = arm_bot.pub_key:main',
            'sensors = arm_bot.pub_sens:main',
            'sens_info = arm_bot.sub_sensinfo:main',
            'servoes = arm_bot.sub_servoes:main',

            # 'talker = arm_bot.pub:main',
            # 'listener = arm_bot.sub:main',
        ],
    },
)
