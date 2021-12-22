# Developer guide

## Create and update a book using Jupyter Book

The following sources will be useful:
* [Starter tutorial](https://ubc-dsci.github.io/jupyterdays/sessions/beuzen/jupyter_book_tutorial.html).
* [Jupyter Book docs](https://jupyterbook.org/intro.html).

Once you have created a Jupyter Book, everytime you make some changes on it you have to compile the whole book using:
```
jb build ./
```
This is the basic command you should always remember. After this, the HTML files of your book will be updated and you will be able to check the book locally.

## Upload the book to a repository

Some Jupyter Book features, such as Binder or Thebe, are available only if your book is hosted in a GitHub repository. By now, it can't be done with a GitLab repository, but that may change in the future.

GitHub allows you to upload files up to 100 MB to a repository. If there are larger files in your book (believe me, there will be), you must upload them using Git LFS. You should follow these steps:

1- Download Git LFS from https://git-lfs.github.com/ and install it on your Jupyter Book directory using
```
git lfs install
```
This only needs to be done the first time you use Git LFS.

2- Add and commit changes the way you usually do:
```
git add .
```
```
git commit -m "add large files"
```
3- Import large files. This will create a `.gitattributes` file with all the references to archives above 100 MB.
```
git lfs migrate import --above="100 MB"
```
4- You can check the status of the large files with
```
git lfs migrate info
```
5- Push LFS files to your repository (for example, the one you have called `origin` with branch `main`):
```
git lfs push --all origin main
```
6- Push changes the way you usually do:
```
git push -u origin main
```

**Warning**: Git LFS doesn't support SSH keys. I recommend you to add your remote repository using:
```
git remote add origin https://github.com/MartaVillalba/Wavesbook
```
If you use `git@github.com:MartaVillalba/Wavesbook.git` instead of your repository URL, Git LFS won't work.

## Create a web page for the book

After the previous steps, the book will be available in your GitHub repository. However, in order to make it visible as a web page with an URL, you have to use `ghp-import`. You only need to follow three steps:

1- To use `ghp-import` for the first time, you have to install it in your conda environment using
```
pip install ghp-import
```
2- Everytime you push your book to your remote repository, run this command too:
```
ghp-import -n -p -f ./_build/html
```
3- In your GitHub repository, go to Settings > Pages and, if everything went right, the URL of your book should be available there. For example, mine is https://martavillalba.github.io/Wavesbook/.

**Warning**: `ghp-import` will automatically push the HTML files of your book to your `origin` repository. You should add it to your remote repositories like `origin https://github.com/MartaVillalba/Wavesbook`.

**Note 1**: this process can be automated following the instructions [here](https://jupyterbook.org/publish/gh-pages.html#automatically-host-your-book-with-github-actions).

**Note 2**: it is also possible to create the book web page in GitLab. However, it is more complex and the book will always need to be hosted in GitHub, so I find it more simple if the pages are also created in GitHub.

## Upload the book to GitLab

If you want to have the book hosted in GitLab aside from GitHub, you can easily achieve that with the "mirror" option.

1- Create an empty repository in GitLab: New project/repository > Create blank project. Make it public and do not initialize it with a README.

2- Once you have created your GitLab repository, go to Settings > Repository > Mirroring repositories. There, put your GitHub repository URL (for example, mine is https://github.com/MartaVillalba/Wavesbook) and select the option Pull. After you enter your Password, your GitLab repository will start to import all branches and files from your GitHub repository, and will be updated everytime you push changes to the GitHub repository.

**Warning**: remember that upload the book to GitLab is necessary only if you want to have it there along with the rest of your projects. The important repository is the GitHub one, because it is the one that hosts the book web page and is connected to Binder.

# About Waves Book

Waves Book directory is divided into several folders and files:

* **waves-main**: this folder contains all the code notebooks (_ipynb_), data used in them (_data_) and custom libraries (_lib_).

* **contents**: here are located the notebooks with PDFs, videos and other materials for the course. There is one notebook for each subsection of the book, though some of them are still empty.

* **_build**: this is where all HTML files of the book are builded. It is automatically updated each time you build the book with the command `jb build ./`, but in some cases you will need to add some files to this folder manually as I explain in the following sections.

* **_config.yml**: this file contains the main configuration of the book (for example, title, logo, repository URL, Binder and Thebe options...).

* **_toc.yml**: this is the index of contents of the book. It is structured in chapters, sections and files. New contents for the book (notebooks or markdown) need to be added here with their complete path.

* **.binder** and **requirements.txt**: this is necessary for Binder to build the environment of the book correctly. New libraries have to be added to `requirements.txt` file.

* **.gitattributes**: it is created automatically by Git LFS when you import large files, as it is described in *Upload the book to a repository* section.

* **gitlab-ci.yml**: this file is meant for building the book web page via GitLab. However, it is not necessary unless you want to host the web page in GitLab instead of GitHub.

In the following descriptions, some procedures to add new content to the book and their peculiarities are described.

## Add a new PDF to the book

PDFs need to be added to Waves Book in a notebook. In order to achieve that, follow these steps:

1- Go to *contents* folder and search the notebook of the section where the PDF will go. For example, `A1_observations.ipynb`.

2- Open the notebook and add a markdown cell and a code cell at the end of it. In the markdown one, write the title of the subsection where the PDF will go. For example,
```
## New PDF
```
In the code one, write the following
```Python
from IPython.display import IFrame
IFrame("../contents/PDF_NAME.pdf", width=700, height=700)
```
where `PDF_NAME` is the name of the PDF you want to add. Note that the PDF must be inside folder *contents*.

3- (Optional) Hide the code input in order to keep the book clean and simple. This can be done in JupyterLab by clicking *Property Inspector* (in the upper right corner) when you are in a code cell and adding a new Cell-Tag called `hide-input`.

4- Now the PDF is correctly added to one of the notebooks of Waves Book. However, the PDF also needs to be in the folder where HTML contents of the book are located (i.e. *_build* folder). This step is so important, and if you don't do it the PDF will not be available in the book interface. You only have to go to *_build* > *html* > *contents* and paste the PDF there.

**Warning**: if you have the PDF located inside other folder and not in the *contents* one, you have to copy the PDF to the corresponding folder in *_build* path.

5- Compile the whole book using
```
jb build ./
```
in the command line.

6- Follow the steps in *Upload the book to a repository* and *Create a web page for the book* to update your repository and the book web page with the new PDF.

## Add a new YouTube video to the book

The steps to add new videos to Waves Book are quite similar to those described in *Add a new PDF to the book*, but more simple:

1-  Go to *contents* folder and search the notebook of the section where the PDF will go. For example, `A1_observations.ipynb`.

2- Open the notebook and add a markdown cell and a code cell at the end of it. In the markdown one, write the title of the subsection where the video will go. For example,
```
## New YouTube video
```
In the code one, write the following
```Python
from IPython.display import YouTubeVideo
YouTubeVideo('VIDEO_CODE', width=700, height=400)
```
where `VIDEO_CODE` is the link of the video you want to add. For example, if you want to add the video with URL https://www.youtube.com/watch?v=LW-mWSW9kkg, then `VIDEO_CODE = LW-mWSW9kkg`.

3- (Optional) Hide the code input in order to keep the book clean and simple. This can be done in JupyterLab by clicking *Property Inspector* (in the upper right corner) when you are in a code cell and adding a new Cell-Tag called `hide-input`.

4- Compile the whole book using
```
jb build ./
```
in the command line.

5- Follow the steps in *Upload the book to a repository* and *Create a web page for the book* to update your repository and the book web page with the new YouTube video.

## Add a new section to the book

The index of contents of the book is located in `_toc.yml` file. Open it with a text editor or in Jupyter Lab to modify the sections and files that are included in the book. You can add markdown files (`.md`) or Jupyter Notebooks (`.ipynb`). When adding new sections, be careful with the structure of the `_toc.yml` file. If its structure is incorrect, the book won't compile. You can find all the information about the book structure and index of contents [here](https://jupyterbook.org/customize/toc.html).

# Advanced topics

By now, you have learned how to do the main actions in a Jupyter Book. However, there are many other features that can be added to a book and will make it more interactive and useful. In the following sections you can find the way to do so.

## Configure the book features

The file `_config.yml` is where you can choose all the features you want your book to have. [Here](https://jupyterbook.org/customize/config.html) you can find all the information about the available book settings, but these are the more important ones:

* **Disable execution of notebooks**. With the following code, you prevent your book from re-execute all the notebooks each time it is compiled:
```
execute:
  execute_notebooks: 'off'
```
This is specially important if your book has code that would take so much time to run.

* **Specify your GitHub repository where the book is hosted**. For example, in my configuration it is:
```
repository:
  url: https://github.com/MartaVillalba/Wavesbook # Online location of your book
  branch: main  # Which branch of the repository should be used when creating links (optional)
```
This is completely necessary if you want to add Binder to your book as I explain in the following section. Despite the book may be uploaded to GitHub and mirrored to GitLab at the same time, always use the GitHub URL in the book configuration.

* **Configure the book buttons**. These buttons are located in the upper part of the book pages, and they allow you to go to the source repository of the book, Binder, Google Colab, JupyterHub or Thebe. Some of these features will be explained in more detail in the next section, but here is how the configuration of the buttons should look like:
```
html:
  use_repository_button: true
  use_binder_button: true

launch_buttons:
  notebook_interface: "classic"
  binderhub_url: "https://mybinder.org"
  thebe: true
```

## Make the book executable with Binder and Thebe

When the book is hosted in a GitHub repository, you can connect it to a Binder environment that allows you to execute and modify all the notebooks of the book. [Here](https://jupyterbook.org/interactive/launchbuttons.html) you can find how Binder and other interfaces can be added to the book, but these are the main requirements:

* The book must be hosted in a GitHub repository. By now, it can't be done with a GitLab repository. Remember that you have to specify the repository URL in `_config.yml` file as it is described in the previous section:
```
repository:
  url: https://github.com/MartaVillalba/Wavesbook # Online location of your book
  branch: main  # Which branch of the repository should be used when creating links (optional)
```

* Activate Binder button and URL in `_config.yml` with
```
html:
  use_binder_button: true
```
and
```
launch_buttons:
  binderhub_url: "https://mybinder.org"
```

* Add a `.binder` folder in the book with a `requirements.txt` file with the following content:
```
-r ../requirements.txt
```
and then another `requirements.txt` file in the root directory of the book with all the necessary libraries to build the Binder environment. For example:
```
jupyter-book
ghp-import
sphinx-thebe
pandas
plotly
scipy
matplotlib
netCDF4
notebook
numpy
panel
progressbar
plotly
xarray
gsw
sympy
```

Once Binder is correctly added to the book, you can make it executable without leaving the book pages with Thebe. Note that Thebe is an experimental feature and may not work completely. [Here](https://jupyterbook.org/interactive/thebe.html) and [here](https://thebe.readthedocs.io/en/latest/#) are the tutorial and documentation of Thebe. Once you have Binder in your book, you can activate Thebe by adding this to the `_config.yml` file:
```
launch_buttons:
  thebe: true
```
```
sphinx:
  extra_extensions:
    - sphinx_thebe
    - jupyter_sphinx
```

One important issue with Thebe that you have to take into account is that its directory is not the same as your computer. This means that, when you import some data in a notebook, the path you specify when working locally is not the same as the path that Thebe will need. For example, if you are working on a notebook located in `waves-main/ipynb/A_WaveAnalysis/A1_Observations` and data files are located in `waves-main/data/Bilbao`, in the notebook you would import the data using the path
```Python
p_data = op.abspath(op.join(os.getcwd(),'..', '..', '..', 'data', 'Bilbao'))
```
That is, you start in the notebook folder and go back to enter the corresponding data folder. However, when executing the book with Thebe, the starting directory is not the notebook one, but the home one. If you start in home's directory, the path to the data should be
```Python
p_data = op.abspath(op.join(os.getcwd(), 'waves-main', 'data', 'Bilbao'))
```
In other words, the variable `p_data` should contain different paths when working on the notebook locally (or in Binder) and when  executing the book with Thebe. This can be fixed by adding a conditional each time you import some data or a custom library in the notebook:
```Python
if(os.path.isdir('waves-main')): #thebe
    os.chdir('waves-main')
from lib.eta_spec import *

# path to buoy data
if(os.path.isdir('data')):
    p_data = op.abspath(op.join(os.getcwd(), 'data', 'Bilbao')) # thebe
else:
    p_data = op.abspath(op.join(os.getcwd(),'..', '..', '..', 'data', 'Bilbao')) # notebook
```

## Interactive plots and contents

One of the main cons of Jupyter Book (and Jupyter environment in general) is that interactive plots may not work sometimes. In Waves Book, the interactivity is mainly achieved with Plotly and Panel. In this section, you can find a lot of information and useful links about the issues with interactive plots in Jupyter Book. [Here](https://jupyterbook.org/interactive/interactive.html) it is the general Jupyter Book documentation about interactive plots.

**Interactive plots with [Plotly](https://plotly.com/python/).**

When you make a plot with Plotly in a Jupyter Notebook, you generally show it with `fig.show()` or directly with `fig`. However, the resulting plot may not be rendered correctly in Jupyter Book and won't be visible in the final pages of the book. In order to solve this, you have to use another Plotly renderer instead of the default one. [Here](https://plotly.com/python/renderers/) you can find the documentation about Plotly renderers.

There are several solutions you can try to show Plotly figures in the book:

1- Use `sphinx_gallery` renderer each time you show a plot:
```Python
fig.show('sphinx_gallery')
```

2- Save the plot to a HTML file and then show it in the book:
```Python
fig.write_html("figure.html")
HTML("figure.html") 
```

3- Change the default renderer to `iframe_connected` and then show the plots the way you usually do:
```Python
import plotly.io as pio
pio.renderers.default = 'iframe_connected'
...
fig.show()
```
This will also save the plot into a HTML file.

Remember that if you use methods 2 or 3, you will need to copy-paste the resulting HTML plot into the corresponding *_build* folder as it is explained in *Add a new PDF to the book* section.

**Interactive plots and widgets with [Panel](https://panel.holoviz.org/user_guide/index.html).**

In Waves Book, Panel is used to make plots that can be modified with interactive widgets. This is an interaction between Python and JavaScript and needs a Python kernel running to upgrade the plot each time you change the value of a parameter with the widgets. This is the reason why it is so problematic to achieve this interaction in the final pages of the book, that are only HTML files with no Python kernel at all.

An easy way to fix this is to go to Binder. If you click the Binder button when you are on a book page with a Panel interactive plot, you will go directly to the notebook and will be able to execute it and play with the Panel plot. However, this requires the user to leave the book interface and it is not what we are looking for. Also, if you try to re-run the Panel plots making the book content executable with Thebe, the interactivity will not work. This occurs because the interaction between the widgets and the plot requires recursive callbacks to the Python kernel, and Thebe's kernel only runs when you execute one cell and stops immediately after that.

If you want the user to interact with Panel plots without leaving the book, a temporary solution for this problem is to embed the Panel figures. [Here](https://panel.holoviz.org/user_guide/Deploy_and_Export.html#embedding) you can read the documentation about Panel embedding. This action saves in memory or into a HTML file several figures with different configurations of the interactive parameters. However, this needs a lot of space and can't be done in complex Panel plots. Also, the number of available values for the parameters of the widgets is reduced. This can be achieved in two ways:

1- If the Panel plot is simple, you can plot and embed it directly with
```Python
panel.embed()
```

2- If the Panel plot has more complexity, it is better to save it in a HTML file and then show that file with Python:
```Python
panel.save("panel.html", embed=True)
HTML("panel.html")
```

In some cases, the plot is so complex that the resulting HTML file would be huge, and it would give trouble when uploading the book to a GitHub repository. Because of this, it is necessary to find another solution to this issue. Here are the possible ways to fix this in the future:

* [Plotly sliders](https://plotly.com/python/sliders/). Plotly library allows you to create interactive plots with widgets, and they can be easily shown in the book. However, this method may not be able to reproduce complex plots like the ones we have in Waves Book.

* [Matplotlib + Ipywidgets with Thebe](https://thebe.readthedocs.io/en/latest/examples/matplotlib_interact_example.html). Once Thebe is activated in the book, this feature may allow the user to play with figures and widgets without leaving the book. This method would require to change the code and use Ipywidgets instead of Panel to create the interaction between the plot and the widgets.

* [The Executable Book Project](https://executablebooks.org/en/latest/index.html). In this project, you may find more information about this issues with interactive plots in the future. Note that Jupyter Book is a recent tool that is under development, and it will continue growing up and having new features in the near future.


## Custom Binder computing interface

Instead of using Binder to run the notebooks of Waves Book, it is possible to connect the book to a GeoOcean cluster. This feature still has a long way to go, but these are the steps to try it:

1- Connect your computer to the cluster following these instructions (from GeoOcean Teams group > NODOS channel):
* Login: `ssh username@tejo.unican.es`
* Connect to a port: `ssh -L 8XXX:localhost:8XXX username@tejo.unican.es` where `8XXX` is the number of the ports that are being connected.
* Activate environment: `source /software/geocean/conda/bin/activate`
* Launch Jupyter: `jupyter notebook --no-browser --port=8XXX`

It is so important that, after these steps, Jupyter launches in the same `8XXX` port you have specified. If the port `8XXX` is in use, Jupyter will lauch in the next available port and the number will change. You will see this message in the terminal: `The port 8XXX is already in use, trying another port.`
If this happens, end the session using Ctrl+C two times and then write `logout`, and try using another `8XXX` port until you find one that is available at the moment.

2- In `_config.yml` file, change the Binder URL to `http://127.0.0.1:8XXX/tree` so that `launch_buttons` section looks like this:
```
launch_buttons:
  notebook_interface: "classic"
  binderhub_url: "http://127.0.0.1:8XXX/tree"
  thebe: true
```
Note that `8XXX` has to be the number of the port you have achieved to connect to. Once you are done, compile the book using `jb build ./`.

With the previous step, all the Binder buttons of the book will be automatically changed. This way, when you click "Binder" in the book's interface, you will be redirected to a Jupyter session running in the cluster instead of Binder. However, Jupyter Book by default will create the Binder URL from your repository. That is, if in your `_config.yml` file the Binder URL is `https://mybinder.org` and the GitHub URL is `https://github.com/MartaVillalba/Wavesbook`, when you click the Binder button Jupyter Book will redirect you to `https://mybinder.org/v2/gh/MartaVillalba/Wavesbook/main?urlpath=tree/waves-main/ipynb/A_WaveAnalysis/A1_Observations/MajuroAtoll.ipynb`. This means that it adds the fragment `/v2/gh/MartaVillalba/Wavesbook/main` corresponding to your repository before specifying the route of the notebook you want to run (`tree/waves-main/ipynb/A_WaveAnalysis/A1_Observations/MajuroAtoll.ipynb`). Because of this, you need to do an extra step to make it work when using the cluster URL `http://127.0.0.1:8XXX/tree`:

3- In Tejo's directory, create the path `/v2/gh/MartaVillalba/Wavesbook/main` and copy there all the notebooks of Waves Book, that is:
* Create folder `v2` and move into it:
```
[username@tejo ~]$ mkdir v2
[username@tejo ~]$ cd v2
```
* Repeat with folder `gh`:
```
[username@tejo v2]$ mkdir gh
[username@tejo v2]$ cd gh
```
* Repeat with folder `MartaVillalba`, which will be your username in GitHub:
```
[username@tejo gh]$ mkdir MartaVillalba
[username@tejo gh]$ cd MartaVillalba
```
* Repeat with folder `Wavesbook`, which will be the repository where the book is hosted in GitHub:
```
[username@tejo MartaVillalba]$ mkdir Wavesbook
[username@tejo MartaVillalba]$ cd Wavesbook
```
* Finally, repeat with folder `main`, which will be the branch name of your repository:
```
[username@tejo Wavesbook]$ mkdir main
[username@tejo Wavesbook]$ cd main
```
* Once you are in `/v2/gh/MartaVillalba/Wavesbook/main` directory, copy-paste all the notebooks from the book that you want to run in the cluster. For example, with `BilbaoExt.ipynb`:
```
scp *YOUR ROUTE TO THE NOTEBOOK* username@tejo.unican.es:v2/gh/MartaVillalba/Wavesbook/main
```
In my case, the route to the notebook in my laptop is `c:\Users/Marta/Desktop/Beca/waves_book/waves-main/ipynb/A_WaveAnalysis/A1_Observations/BilbaoExt.ipynb`.

After all these steps, you should be able to run the Waves Book notebooks in the cluster. You should note the following:

* You have to connect to the cluster each time you want to run the book on it. If the number of port `8XXX` changes between sessions, you have to change it in `_config.yml` file too.
* This feature has been tested when working with the book locally, but it may not work when you are seeing the book on its web page.