Python developer test task
==========================

Requirements
------------

#) Code style by http://www.python.org/dev/peps/pep-0008/
#) Project deployment using http://pypi.python.org/pypi/zc.buildout and providing installation instructions in INSTALL.txt in code root folder
#) Should be published on https://github.com/
#) Commented code is a plus

The task
--------

Build a web application using latest django/pyramid/gae, which will allow:

- log in using twitter or google auth
- upload a file, which should be stored on amazon s3 service (there should be special settings in config for that)
- view list of your uploaded files
- ability to view and share the file with any other people by sending link to them (have an action and form asking email(s) and optional message to the person). Going by link people should be able to download or view file in google docs using google docs api, of course if file type allows to be viewed though it

Strict requirement: application should not reload browser page at all, so all should be done using ajax technology.
Recommendations: reuse as much existing django apps/tool as possible and you will win :)
Always remember the KISS principle