# p3-fastqc
### Practicum 3 &amp; BIN toolbox opdracht with FastQC al tool.

*version 2.0 7-4-2025*


This is web app created using the Flask web framework in python for the backend and HTML/CSS & 
  Javaschript for the frontend. The website contains more info about the project and the 
  FastQC tool. You can also use the tool via the web app, just upload a fastq-file and select your 
  preferred settings. The size of the file determines the speed of the tool, but as soon as the 
  file is uploaded and processed the app will take you to the results page with your report. The 
  FastQC tool is mostly used to check the quality of unprocessed genetic data. If there are 
  problems which are helped with, for example, trimming the data, than the test is usually run 
  again to check if the desired outcome is achieved. The tool gives per test it has run either a 
  pass (tick), warning (exclamation mark) or fail (cross/x) determined by the standard limits or 
  custom limits given by the user. While entering the setting for the tool, the help-pages for 
  each selected test is show for a description, example and common errors. The picture below 
  shows an example of a finished report. 

![img.png](website/static/images/Example_report.png)


#### System requirements
This project is a python project, so having python installed is necessary. For the necessary 
packages please reference the requirements.txt file.

FastQC is a java application. In order to run it needs your system to have a suitable
Java Runtime Environment (JRE) installed.

Actually installing FastQC is not necessary as it comes included in the project. 

#### Installation and running the project
To install the project locally, please fork this repository. After that you can clone it to run 
the project locally.

To run you can use your preferred IDE or via the commandline using *python 
PathToProject/website/app.py* This should give the following output:
> * Serving Flask app 'app' (lazy loading)
> * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
> * Debug mode: on
> * Restarting with stat
> * Debugger is active!
> * Debugger PIN: 122-348-451
> * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Click on the link, which should open a browser hosting the web app.

#### Author
Maartje van der Hulst

#### References
Reference to the FastQC tool: 
https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

Background reseach references can be found in the project proposal or on the references page of 
the web app.
#### License
The FastQC licence is available in this repository under 
[licence] (website/tools/fastqc_v0.12.1/FastQC/LICENSE.txt)

"website/tools/fastqc_v0.12.1/FastQC/LICENSE.txt"













