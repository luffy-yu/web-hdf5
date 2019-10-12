# Web HDF5

## Reference

```html
https://github.com/pwuertz/webhdf.git
```


Webhdf is a web browser based viewer for HDF5 files. It is driven by a Python
WSGI application that is either deployed on a webserver or started locally.

For displaying the content, the browser frontend uses recent HTML+JS features
that are found in Firefox (v19.0), Chrome (v25.0), Opera (v12.1) and Internet
Exlorer (v10.0). The backend requires a Python interpreter including the h5py
and webob modules.

## Usage

-  Install requirements

```shell
pip install -r requirements.txt
```

-  Put hdf5 files to test folder

-  Run command

```shell
python test/testserver.py
```

