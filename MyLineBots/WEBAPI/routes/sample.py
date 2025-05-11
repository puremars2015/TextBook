from flask import Blueprint, jsonify

# 定義一個 Blueprint
sample_bp = Blueprint('sample', __name__)

@sample_bp.route('/sample', methods=['GET'])
def get_sample():
    """一個簡單的範例 API，回傳 JSON 資料"""
    return jsonify({"message": "This is a sample API response!"})
