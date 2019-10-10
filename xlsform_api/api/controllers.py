import logging
from tempfile import TemporaryDirectory
import os.path

from flask import Blueprint, jsonify, request, send_file
from pyxform import xls2xform

api = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

# To test: curl --request POST --data-binary @<FILE_NAME>.xlsx http://127.0.0.1:5000/api/v1/convert
@api.route("/convert", methods=["POST"])
def post():
    with TemporaryDirectory() as temp_dir_name:
        try:
            with open(os.path.join(temp_dir_name, "tmp.xml"), "w+") as xform, open(
                os.path.join(temp_dir_name, "tmp.xlsx"), "wb"
            ) as xlsform:
                xlsform.write(request.get_data())
                convert_status = xls2xform.xls2xform_convert(
                    xlsform_path=str(xlsform.name),
                    xform_path=str(xform.name),
                    validate=True,
                    pretty_print=False,
                )

                if convert_status:
                    logger.warning(convert_status)

                if os.path.isfile(xform.name):
                    return response(
                        status=200, result=xform.read(), warnings=convert_status
                    )
                else:
                    return response(error=convert_status)

        except Exception as e:
            logger.error(e)
            return response(error=str(e))


def response(status=400, result=None, warnings=None, error=None):
    return jsonify(status=status, result=result, warnings=warnings, error=error), status
