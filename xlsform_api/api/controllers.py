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
            xform_fp = open(os.path.join(temp_dir_name, "tmp.xml"), "w")
            xlsform_fp = open(os.path.join(temp_dir_name, "tmp.xlsx"), "wb")
            xlsform_fp.write(request.get_data())
            convert_status = xls2xform.xls2xform_convert(
                xlsform_path=str(xlsform_fp.name),
                xform_path=str(xform_fp.name),
                validate=True,
                pretty_print=False
            )

            if convert_status:
                logger.warning(convert_status)

            if os.path.isfile(xform_fp.name):
                return response(status=GOOD_REQUEST_CODE, result=send_file(xform_fp.name, mimetype="application/xml"), warnings=convert_status)
            else:
                return response(status=BAD_REQUEST_CODE, error=convert_status)

        except Exception as e:
            logger.error(e)
            return response(status=BAD_REQUEST_CODE, error=str(e))
            
        finally:
            xform_fp.close()
            xlsform_fp.close()

def response(status=None, result=None, warnings=None, error=None):
    return jsonify(
        status=status,
        result=result,
        warnings=warnings,
        error=error
    ), status