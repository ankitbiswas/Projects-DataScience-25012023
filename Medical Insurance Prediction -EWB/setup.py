from setuptools import find_packages, setup
from typing import List


requirement_file_name = "requirements.txt"
REMOVE_PACKAGE ="-e ."

#get the requirements in list 
def get_requirements()->List[str]:
    with open(requirement_file_name) as requirement_file:
        requirement_list = requirement_file.readline()
    requirement_list_new = [requirement_name.replace("\n","") for requirement_name in requirement_list]

    if REMOVE_PACKAGE in requirement_list_new:
        requirement_list_new.remove(REMOVE_PACKAGE)

    return requirement_list_new


#create the setup constructor
setup(name='Insurance',
      version='0.0.1',
      description='Insurance Industry Project',
      author='Ankit Biswas',
      author_email='ankitbiswas008@gmail.com',
      packages=find_packages(),
      install_reqires=get_requirements()
     )