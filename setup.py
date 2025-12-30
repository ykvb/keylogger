from setuptools import setup

setup(
      name="keylogger",
      version="1.0.0",
      description="Test Python Keylogger Template",
      author="ykvb",
      packages=[],
      install_requires=[
          "pyHook==1.1.1",
          "pywin32",
          "psutil>=5.8.0"
      ],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Operating System :: Microsoft :: Windows",
      ],
  )
