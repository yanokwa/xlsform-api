import logging
from tempfile import TemporaryDirectory
import os.path

from flask import Blueprint, jsonify, request, send_file
from pyxform import xls2xform

api = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

BAD_REQUEST_STATUS_CODE = 400
GENERIC_ERROR_MESSAGE = "Error converting XLSForm"
XLSFORM_FILE_NAME = "tmp.xlsx"
XFORM_FILE_NAME = "tmp.xml"
XML_MIME_TYPE = "application/xml"

# To test: curl --request POST --data-binary @<FILE_NAME>.xlsx http://127.0.0.1:5000/api/v1/convert
@api.route("/convert", methods=['POST'])
def post():
    with TemporaryDirectory() as temp_dir_name:
        try:
            xform_fp = open(os.path.join(temp_dir_name, XFORM_FILE_NAME), "w")
            xlsform_fp = open(os.path.join(temp_dir_name, XLSFORM_FILE_NAME), "wb")
            xlsform_fp.write(request.get_data())
            form_errors = xls2xform.xls2xform_convert(
                xlsform_path=str(xlsform_fp.name),
                xform_path=str(xform_fp.name),
                validate=True,
                pretty_print=True
            )

            if form_errors:
                logger.warning(form_errors)

            if os.path.isfile(xform_fp.name):
                return send_file(xform_fp.name, mimetype=XML_MIME_TYPE)
            else:
                return format_error(form_errors)

        except Exception as e:
            logger.error(e)
            return format_error(e)
            
        finally:
            xform_fp.close()
            xlsform_fp.close()

def format_error(e=GENERIC_ERROR_MESSAGE):
    return jsonify(
        status=BAD_REQUEST_STATUS_CODE,
        message=str(e)
    ), BAD_REQUEST_STATUS_CODE
