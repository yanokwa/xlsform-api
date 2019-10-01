import logging
from tempfile import TemporaryDirectory
import os.path

from flask import Blueprint, jsonify, request, send_file
from pyxform import xls2xform

api = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

BAD_REQUEST_CODE = 400
GOOD_REQUEST_CODE = 200

# To test: curl --request POST --data-binary @<FILE_NAME>.xlsx http://127.0.0.1:5000/api/v1/convert
@api.route("/convert", methods=['POST'])
def post():
    with TemporaryDirectory() as temp_dir_name:
        try:
            xform_fp = open(os.path.join(temp_dir_name, "tmp.xlsx"), "w")
            xlsform_fp = open(os.path.join(temp_dir_name, "tmp.xml"), "wb")
            xlsform_fp.write(request.get_data())
            convert_status = xls2xform.xls2xform_convert(
                xlsform_path=str(xlsform_fp.name),
                xform_path=str(xform_fp.name),
                validate=True,
                pretty_print=False
            )

            if convert_status:
                logger.warning(convert_status)

            # if a file exists, there are no errors
            if os.path.isfile(xform_fp.name):
                return send_file(xform_fp.name, mimetype="application/xml")
            else:
                return format_status(convert_status)

        except Exception as e:
            logger.error(e)
            return format_status(e)
            
        finally:
            xform_fp.close()
            xlsform_fp.close()

def format_status(e=None):
    return jsonify(
        status=BAD_REQUEST_CODE,
        message=str(e)
    ), BAD_REQUEST_CODE
