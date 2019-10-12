import tables
from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPInternalServerError
from webob.static import FileApp
from webob.dec import wsgify

import os
import json

def dtype2json(dtype):
    if not dtype.fields:
        return str(dtype)
    else:
        fields = {}
        for name in dtype.names:
            subdtype = dtype.fields[name][0]
            fields[name] = dtype2json(subdtype)
        return {"names": dtype.names, "fields": fields}

def dset2json(dset):
    attrs = dset.attrs
    names = attrs._v_attrnames
    ret = {}
    if len(names):
        for name in names:
            ret[name] = str(attrs.__getattr__(name))
    return ret


def response_file(path_local, fmt):
    print 'format', fmt
    if fmt == "raw":
        # return the raw h5 file
        # fname = os.path.basename(path_local).encode('utf-8')
        # res = FileApp(path_local,
        #               content_disposition="attachment; filename=%s" % fname,
        #               content_type="application/x-hdf")
        return "None"
    elif fmt == "json":
        # return json representation of the h5 header
        with tables.open_file(path_local, "r") as fh:
            def dset_to_dict(dset, path, name):
                d = {}
                d["attrs"] = dset2json(dset)
                print d["attrs"]
                d["shape"] = dset.shape
                d["dtype"] = dtype2json(dset.dtype)
                d["name"] = name
                d["path"] = path
                return d

            def visit_group(group_obj, path, gname="/"):
                dsets = []
                groups = []
                nodes = group_obj.get_node(gname)
                for node in nodes:
                    if isinstance(node, tables.Group):
                        groups.append(visit_group(group_obj, node._v_pathname, node._v_pathname))
                    else:
                        dsets.append(dset_to_dict(node, node._v_pathname, node._v_name))

                g = {}
                g["attrs"] = nodes._v_attrs._v_attrnames
                g["groups"] = groups
                g["datasets"] = dsets
                g["path"] = path if path else "/"
                g["name"] = gname
                return g

            header = visit_group(fh, "")
            header["fname"] = os.path.basename(path_local)

        res = Response(content_type="application/json", charset="utf-8")
        res.body = json.dumps(header, indent=4, separators=(',', ': '))
        res.encode_content(encoding='gzip', lazy=True)
        return res
    else:
        return HTTPNotFound("Invalid format requested.")

