import logging
from tempfile import NamedTemporaryFile

from flask import Blueprint, jsonify, request, send_file
from pyxform import xls2xform

api = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

XLSX_FILE_SUFFIX = ".xlsx"
XML_FILE_SUFFIX = ".xml"
XML_MIME_TYPE = "application/xml"


@api.route("/convert", methods=['POST'])
def post():
    xform_fp = NamedTemporaryFile(suffix=XML_FILE_SUFFIX)
    xls_fp = NamedTemporaryFile(suffix=XLSX_FILE_SUFFIX)
    try:
        xls_fp.write(request)
        form_errors = xls2xform.xls2xform_convert(
            xlsform_path=str(xls_fp.name),
            xform_path=str(xform_fp.name),
            validate=True,
            pretty_print=True
        )
        logger.warning(form_errors)
        return send_file(xform_fp.name, mimetype=XML_MIME_TYPE)
    except Exception as e:
        return format_error(e)
    finally:
        xls_fp.close()
        xform_fp.close()


def format_error(e):
    return jsonify(
        status=400,
        message=str(e)
    )
